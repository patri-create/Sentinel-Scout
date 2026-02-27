"""FastAPI application."""

from dotenv import load_dotenv

load_dotenv()

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi import BackgroundTasks

from app import __version__
from app.schemas import Transaction
from app.scout import get_fraud_explanation

import json
import os
import redis

import xgboost as xgb
import numpy as np
from contextlib import asynccontextmanager

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

@asynccontextmanager
async def lifespan(app: FastAPI):
    global model
    try:
        model.load_model("app/model_sentinel.json")
        print("🧠 Sentinel Brain Loaded and Ready")
    except Exception as e:
        print(f"❌ Critical Failure: Could not load model: {e}")
    yield
    del model

app = FastAPI(title="Sentinel & Scout API", lifespan=lifespan)

@app.post("/predict")
async def predict(transaction: Transaction):
    user_key = f"tx_count:{transaction.user_id}"
    current_count = redis_client.incr(user_key)
    if current_count == 1: redis_client.expire(user_key, 60)

    features = np.array([[
        transaction.amount, 
        transaction.timestamp.hour, 
        1.0,
        float(current_count)
    ]])

    dmatrix = xgb.DMatrix(features)
    prediction_prob = model.predict(dmatrix)[0]

    # DEBUG LOG
    print(f"DEBUG: Amount={transaction.amount}, Count={current_count}, Prob={prediction_prob}")
    
    is_fraud = prediction_prob > 0.5 or current_count > 3

    return {
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
    user_key = f"tx_count:{transaction.user_id}"
    current_count = redis_client.incr(user_key)
    if current_count == 1:
        redis_client.expire(user_key, 60)

    features = np.array([[transaction.amount, transaction.timestamp.hour, 1.0, float(current_count)]])
    prediction_prob = float(model.predict(xgb.DMatrix(features))[0])

    is_fraud = prediction_prob > 0.5 or current_count > 3

    if is_fraud:
        background_tasks.add_task(
            run_scout_investigation, 
            transaction.model_dump(mode="json"), 
            prediction_prob, 
            current_count
        )

    return {
        "is_fraud": is_fraud,
        "probability": prediction_prob,
        "status": "Action Taken" if is_fraud else "Clear",
        "message": "Detailed report is being generated in the background." if is_fraud else None
    }

@app.get("/health")
def health_check():
    return {"status": "healthy", "timestamp": "2026-02-16T...Z"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error("Unexpected error: %s", exc)
    return JSONResponse(
        status_code=500,
        content={"message": "Internal server error in ML Sentinel."},
    )
