from enum import Enum
from dataclasses import dataclass
import threading
from app.metrics_logger import MetricsLogger

class TrackEvent(Enum):
    PREDICTION = "total_predictions"
    FRAUD_DETECTED = "total_fraud_detected"

class TrackerManager:
    def __init__(self):
        self._stats = { TrackEvent.PREDICTION: 0, TrackEvent.FRAUD_DETECTED: 0 }
        self._lock = threading.RLock()
        self._alert_sent = False
    

    def increment(self, event: TrackEvent):
        with self._lock:
            self._stats[event] += 1

            p, f, ratio = self._calculate_stats()

            if p > 10 and ratio > 50 and not self._alert_sent:
                MetricsLogger.log_audit("SYSTEM", 0.0, 0, True, custom_msg="🚨 CRITICAL_FRAUD_RATE")
                self._alert_sent = True

            if ratio < 20:
                self._alert_sent = False


    def _calculate_stats(self):
        predictions = self._stats[TrackEvent.PREDICTION]
        frauds = self._stats[TrackEvent.FRAUD_DETECTED]
        ratio = (frauds / predictions * 100) if predictions > 0 else 0.0
        return predictions, frauds, ratio

    def get_stats(self):
        with self._lock:
            predictions = self._stats[TrackEvent.PREDICTION]
            frauds = self._stats[TrackEvent.FRAUD_DETECTED]
            
            ratio = (frauds / predictions * 100) if predictions > 0 else 0.0

            return {
                "total_predictions": predictions,
                "total_fraud_detected": frauds,
                "fraud_ratio": ratio
            }

tracker = TrackerManager()