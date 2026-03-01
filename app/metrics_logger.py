import logging
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s | %(levelname)s | %(message)s'
)
logger = logging.getLogger("SentinelAudit")

class MetricsLogger:
    @staticmethod
    def log_audit(user_id: str, prob: float, count: int, is_fraud: bool, custom_msg: str = None):
        if custom_msg:
            result = custom_msg
        else:
            result = "BLOCK" if is_fraud else "CLEAR"

        audit_msg = (
            f"AUDIT | USER: {user_id} | "
            f"PROB: {prob:.4f} | "
            f"COUNT: {count} | "
            f"RESULT: {result}"
        )
        logger.info(audit_msg)