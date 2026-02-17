"""FastAPI application."""

import logging

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

from app import __version__
from app.schemas import Transaction

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Sentinel & Scout ML API", version=__version__)


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
async def predict_fraud(transaction: Transaction):
    try:
        is_fraud = transaction.amount > 10000

        return {
            "transaction_id": transaction.transaction_id,
            "is_fraud": is_fraud,
            "probability": 0.99 if is_fraud else 0.01,
            "model_version": "v0_baseline",
        }
    except Exception as e:
        logger.error("Error in prediction: %s", e)
        raise HTTPException(status_code=500, detail="Error in prediction")
