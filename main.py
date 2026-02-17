from fastapi import FastAPI
from pydantic import BaseModel
import numpy as np
import os
import mlflow.pyfunc
from prometheus_fastapi_instrumentator import Instrumentator
from prometheus_client import Counter, Histogram, Gauge

app = FastAPI()

# Set MLflow tracking URI (for Docker Desktop)
MLFLOW_TRACKING_URI = os.getenv("MLFLOW_TRACKING_URI", "http://host.docker.internal:5000")
mlflow.set_tracking_uri(MLFLOW_TRACKING_URI)

# Load model from MLflow Registry
model = mlflow.pyfunc.load_model(
    model_uri="models:/FraudDetectionModel/Production"
)

# Prometheus metrics
transaction_counter = Counter(
    "total_transactions",
    "Total transactions scored"
)

high_risk_counter = Counter(
    "high_risk_transactions",
    "Transactions with fraud probability > 0.8"
)

fraud_score_histogram = Histogram(
    "fraud_score_distribution",
    "Distribution of fraud scores"
)

avg_transaction_amount = Gauge(
    "avg_transaction_amount",
    "Average transaction amount observed"
)

transaction_amounts = []

class Transaction(BaseModel):
    transaction_amount: float
    account_age_days: int
    transactions_last_24h: int
    merchant_risk_score: float
    device_risk_score: float

@app.get("/")
def health():
    return {"status": "running"}

@app.post("/predict")
async def predict(tx: Transaction):
    features = np.array([[
        tx.transaction_amount,
        tx.account_age_days,
        tx.transactions_last_24h,
        tx.merchant_risk_score,
        tx.device_risk_score
    ]])

    fraud_prob = model.predict(features)[0]

    transaction_counter.inc()
    fraud_score_histogram.observe(fraud_prob)

    if fraud_prob > 0.8:
        high_risk_counter.inc()

    # Drift tracking
    transaction_amounts.append(tx.transaction_amount)
    if len(transaction_amounts) > 100:
        transaction_amounts.pop(0)
    avg_transaction_amount.set(np.mean(transaction_amounts))

    return {"fraud_probability": float(fraud_prob)}

Instrumentator().instrument(app).expose(app)

