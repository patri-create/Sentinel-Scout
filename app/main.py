"""FastAPI application."""

from dotenv import load_dotenv

load_dotenv()

import logging
import csv

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks

from app import __version__
from app.schemas import Transaction
from app.scout import get_fraud_explanation
from app.schemas import Feedback
from app.model_manager import ModelManagerSingleton

import json
import os
import redis
from pathlib import Path
from datetime import datetime

import xgboost as xgb
import numpy as np
from contextlib import asynccontextmanager

import time

from app.tracker_manager import tracker, TrackEvent
from app.metrics_logger import MetricsLogger

import uuid

start_time = time.time()
model = xgb.Booster()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
security_audit_log = []

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), 
    port=6379, 
    db=0, 
    decode_responses=True
)

def _model_path() -> Path:
    return Path(__file__).resolve().parent / "model_sentinel.json"

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    path = _model_path()
    try:
        if path.exists():
            model.load_model(str(path))
            print("🧠 Sentinel Brain Loaded and Ready")
        else:
            print(f"⚠️ Model not found at {path}; /predict and /investigate will fail until the file exists.")
    except Exception as e:
        print(f"❌ Critical Failure: Could not load model: {e}")
    yield
    del model

app = FastAPI(title="Sentinel & Scout API", lifespan=lifespan)

@app.post("/predict")
async def predict(transaction: Transaction):
    tx_id = str(uuid.uuid4())
    user_key = f"tx_count:{transaction.user_id}"
    current_count = redis_client.incr(user_key)
    if current_count == 1: redis_client.expire(user_key, 60)

    features = np.array([[
        transaction.amount, 
        transaction.timestamp.hour, 
        1.0,
        float(current_count)
    ]])

    prediction_prob = float(ModelManagerSingleton.model.predict_proba(features)[0][1])

    tx_data = transaction.model_dump(mode="json")
    tx_data["tx_id"] = tx_id
    redis_client.setex(f"tx_features:{tx_id}", 86400, json.dumps(tx_data))

    tracker.increment(TrackEvent.PREDICTION)
    
    is_fraud = prediction_prob > 0.5 or current_count > 3

    if is_fraud:
        tracker.increment(TrackEvent.FRAUD_DETECTED)

    MetricsLogger.log_audit(transaction.user_id, prediction_prob, current_count, is_fraud)

    return {
        "tx_id": tx_id,
        "is_fraud": bool(is_fraud),
        "probability": float(prediction_prob),
        "tx_per_minute": current_count,
        "model_type": "XGBoost_Sentinel_v1"
    }

async def run_scout_investigation(transaction_dict, prob, count):
    print(f"🕵️‍♂️ Scout is investigating the transaction for user: {transaction_dict['user_id']}")
    try:
        report = await get_fraud_explanation(transaction_dict, prob, count)
        entry = {"user": transaction_dict['user_id'], "report": report}
        security_audit_log.append(entry)
        print(f"✅ Investigation report for user {transaction_dict['user_id']}: {report}")
    except Exception as e:
        print(f"❌ Error in background investigation: {e}")

@app.post("/investigate")
async def investigate(transaction: Transaction, background_tasks: BackgroundTasks):
    tx_id = str(uuid.uuid4())
    user_key = f"tx_count:{transaction.user_id}"
    current_count = redis_client.incr(user_key)
    if current_count == 1:
        redis_client.expire(user_key, 60)

    features = np.array([[transaction.amount, transaction.timestamp.hour, 1.0, float(current_count)]])
    prediction_prob = float(ModelManagerSingleton.model.predict_proba(features)[0][1])
    tx_data = transaction.model_dump(mode="json")
    tx_data["tx_id"] = tx_id
    redis_client.setex(f"tx_features:{tx_id}", 86400, json.dumps(tx_data))
    tracker.increment(TrackEvent.PREDICTION)

    is_fraud = prediction_prob > 0.5 or current_count > 3

    if is_fraud:
        tracker.increment(TrackEvent.FRAUD_DETECTED)
        background_tasks.add_task(
            run_scout_investigation, 
            transaction.model_dump(mode="json"), 
            prediction_prob, 
            current_count
        )

    MetricsLogger.log_audit(transaction.user_id, prediction_prob, current_count, is_fraud)
    
    return {
        "tx_id": tx_id,
        "is_fraud": is_fraud,
        "probability": prediction_prob,
        "status": "Action Taken" if is_fraud else "Clear",
        "message": "Detailed report is being generated in the background." if is_fraud else None
    }

@app.get("/health")
async def health_check():
    try:
        redis_ready = redis_client.ping()
    except:
        redis_ready = False
    
    model_ready = model is not None

    tracker_stats = tracker.get_stats()

    return {
        "status": "healthy" if redis_ready and model_ready else "unhealthy",
        "uptime_seconds": int(time.time() - start_time),
        "checks": {
            "redis:": "up" if redis_ready else "down",
            "model_sentinel": "loaded" if model_ready else "missing"    
        },
        "performance": tracker_stats
    }

@app.post("/feedback")
async def feedback(data: Feedback):
    tx_key = f"tx_features:{data.transaction_id}"
    raw_data = redis_client.get(tx_key)
    
    if not raw_data:
        return {"status": "error", "message": "Transaction ID not found or expired (24h limit)"}

    raw_str = raw_data if isinstance(raw_data, str) else raw_data.decode("utf-8")
    tx_features = json.loads(raw_str)

    new_row = [
        tx_features['amount'],
        tx_features['timestamp'],
        data.is_fraud_actual
    ]

    csv_file = Path(__file__).resolve().parent / "retraining_data.csv"
    file_exists = csv_file.is_file()

    with open(csv_file, mode="a", newline="") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["amount", "timestamp", "is_fraud_actual"])
        writer.writerow(new_row)

    redis_client.delete(tx_key)

    return {
        "status": "success", 
        "message": f"Feedback processed for {data.transaction_id}. Data added to retraining set."
    }

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unexpected error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error in ML Sentinel."},
    )


@app.post("/admin/reload-model")
async def reload_model(filename: str = "model_sentinel_new.json"):
    full_path = f"app/{filename}"
    success = ModelManagerSingleton.reload(full_path)

    if success:
        return {
            "status": "success", 
            "message": f"Sentinel has updated its brain with {filename}",
            "model_path": full_path
        }
    else:
        return {
            "status": "error", 
            "message": "Error to reload the model. The previous model is still active."
        }

