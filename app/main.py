"""FastAPI application."""

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app import __version__
from app.schemas import Transaction

import os
import redis

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentinel & Scout ML API", version=__version__)

redis_client = redis.Redis(
    host=os.getenv("REDIS_HOST", "localhost"), 
    port=6379, 
    db=0, 
    decode_responses=True
)

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

@app.post("/predict")
async def predict(transaction: Transaction):
    user_key = f"tx_count:{transaction.user_id}"
    current_count = redis_client.incr(user_key)
    
    if current_count == 1:
        redis_client.expire(user_key, 60)

    is_fraud = transaction.amount > 10000 or current_count > 3
    
    return {
        "is_fraud": is_fraud,
        "tx_per_minute": current_count,
        "msg": "Transaction blocked" if current_count > 3 else "Transaction allowed"
    }
