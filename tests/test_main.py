"""Tests for the main API."""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health() -> None:
    """The health endpoint returns status healthy."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_invalid_category():
    payload = {
        "transaction_id": "1",
        "user_id": "1",
        "amount": 100,
        "timestamp": "2026-02-17T08:00:00",
        "merchant_category": "invalid_cat"
    }
    response = client.post("/predict", json=payload)
    assert response.status_code == 422
    
