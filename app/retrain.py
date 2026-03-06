"""Retrain Sentinel model with new feedback data. Run from project root: uv run python app/retrain.py"""
import csv
import xgboost as xgb
import numpy as np
from pathlib import Path
from datetime import datetime

_APP_DIR = Path(__file__).resolve().parent
CSV_PATH = _APP_DIR / "retraining_data.csv"
MODEL_PATH = _APP_DIR / "model_sentinel.json"
MODEL_NEW_PATH = _APP_DIR / "model_sentinel_new.json"


def _parse_timestamp(val: str) -> float:
    """Parse timestamp column: either hour (0-23) or ISO datetime string."""
    val = val.strip()
    try:
        return float(val)
    except ValueError:
        pass
    try:
        dt = datetime.fromisoformat(val.replace("Z", "+00:00"))
        return float(dt.hour)
    except (ValueError, TypeError):
        return 0.0


def retrain_model():
    if not CSV_PATH.exists():
        print("❌ No new data to retrain (retraining_data.csv not found).")
        return

    rows = []
    with open(CSV_PATH, newline="") as f:
        reader = csv.DictReader(f)
        for row in reader:
            amount = float(row["amount"])
            ts = _parse_timestamp(row["timestamp"])
            is_fraud_val = row["is_fraud_actual"].strip().lower()
            is_fraud = 1.0 if is_fraud_val in ("true", "1", "yes") else 0.0
            rows.append([amount, ts, is_fraud])

    if not rows:
        print("❌ No data rows in retraining_data.csv.")
        return

    X_new = np.array([r[:2] for r in rows], dtype=np.float64)
    y_new = np.array([r[2] for r in rows], dtype=np.int32)

    n_unique = len(np.unique(y_new))
    if n_unique < 2:
        print("⚠️ New data has only one class (need both fraud and non-fraud). Add more feedback and run again.")
        return

    # Match main.py features: amount, hour, category=1.0, tx_per_minute (use 1 if not in CSV)
    n = len(rows)
    X_full = np.column_stack((X_new[:, 0], X_new[:, 1], np.ones(n), np.ones(n))).astype(np.float64)

    if not MODEL_PATH.exists():
        print("❌ Base model not found at", MODEL_PATH)
        return

    model = xgb.XGBClassifier(
        n_estimators=50,
        max_depth=3,
        learning_rate=0.1,
        objective="binary:logistic",
    )
    model.load_model(str(MODEL_PATH))

    print(f"🔄 Retraining with {n} new samples...")
    model.fit(X_full, y_new, xgb_model=model.get_booster())

    model.save_model(str(MODEL_NEW_PATH))
    print("✅ New model saved to", MODEL_NEW_PATH.name, "— replace model_sentinel.json to deploy.")


if __name__ == "__main__":
    retrain_model()