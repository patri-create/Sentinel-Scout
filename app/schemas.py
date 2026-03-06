"""Data definitions with Pydantic."""

from pydantic import BaseModel, Field, field_validator
from datetime import datetime

class Transaction(BaseModel):
    user_id: str
    amount: float = Field(gt=0, description="The amount must be greater than zero")
    timestamp: datetime
    merchant_category: str
    
    @field_validator('merchant_category')
    @classmethod
    def validate_category(cls, v):
        allowed = ['retail', 'online', 'transfer', 'atm']
        if v not in allowed:
            raise ValueError(f"Invalid category. Use: {allowed}")
        return v

class Feedback(BaseModel):
    transaction_id: str
    is_fraud_actual: bool
    analyst_id: str