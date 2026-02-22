import xgboost as xgb
import numpy as np

n_samples = 2000
np.random.seed(42)

# Features: [Amount, Hour, Category, Tx_per_minute]
amounts = np.random.uniform(1, 2000, n_samples)
hours = np.random.randint(0, 24, n_samples)
categories = np.random.choice([0, 1, 2, 3], n_samples)
counts = np.random.randint(1, 10, n_samples)

# Fraud if: (High amount and night) or (many transactions per minute)
y = ((amounts > 1500) & (hours < 6)) | (counts > 7)
y = y.astype(int)

# Add noise to make it imperfect (simulates reality)
noise = np.random.choice([0, 1], size=n_samples, p=[0.95, 0.05])
y = np.logical_xor(y, noise).astype(int)

X = np.column_stack((amounts, hours, categories, counts))

# Train with control parameters
model = xgb.XGBClassifier(
    n_estimators=50, 
    max_depth=3, 
    learning_rate=0.1,
    objective='binary:logistic'
)
model.fit(X, y)

model.save_model("app/model_sentinel.json")
print("✅ Sentinel model trained and saved")