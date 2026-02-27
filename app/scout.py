import os
from groq import Groq
import json

client = Groq(api_key=os.environ.get("GROQ_API_KEY"))

SYSTEM_PROMPT = """
You are a Senior Fraud Investigator. You must ALWAYS respond in valid JSON format.
The JSON must contain exactly these keys:
- "risk_level": (High, Medium, or Low)
- "reason": (A concise 1-sentence explanation)
- "suggested_action": (Allow, Review, or Block)

SCALES:
- Prob < 0.2: Low Risk
- Prob 0.2 - 0.7: Medium Risk
- Prob > 0.7: High Risk
- 'tx_per_minute' > 3: CRITICAL VELOCITY.
"""

async def get_fraud_explanation(tx_data: dict, probability: float, count: int):
    prompt = f"""
    Analyze this transaction:
    - Amount: ${tx_data['amount']}
    - User History: {count} transactions in the last minute.
    - Model Probability: {probability:.2f}
    - Category: {tx_data['merchant_category']}
    
    Provide a 2-sentence summary for the security team.
    """
    
    chat_completion = client.chat.completions.create(
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        model="llama-3.1-8b-instant",
    )
    response_text = chat_completion.choices[0].message.content
    structured_data = json.loads(response_text)
    return structured_data