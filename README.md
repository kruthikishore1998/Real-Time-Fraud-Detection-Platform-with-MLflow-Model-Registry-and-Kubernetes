# 🚀 Real-Time Fraud Detection Platform  
**MLflow Model Registry • Kubernetes • Prometheus • Grafana**

---

## 📌 Overview

This project implements a production-style, real-time fraud detection system with dynamic model versioning, observability, and alerting.

Unlike traditional ML deployments where models are baked into containers, this platform loads the active model directly from the MLflow Model Registry at runtime. Model upgrades do not require rebuilding Docker images.

---
## 🏗 System Architecture

```text
                           ┌─────────────────────────┐
                           │     MLflow Registry     │
                           │  (Model Versioning)     │
                           └─────────────┬───────────┘
                                         │
                         models:/FraudDetectionModel/Production
                                         │
                                         ▼
┌──────────────────────────────────────────────────────────────────┐
│                         Kubernetes Cluster                       │
│                                                                  │
│   ┌──────────────────────────────────────────────────────────┐   │
│   │                  Fraud Inference Service                 │   │
│   │                  (FastAPI + Uvicorn)                     │   │
│   │                                                          │   │
│   │  • Loads model dynamically from MLflow                  │   │
│   │  • Exposes /predict endpoint                            │   │
│   │  • Emits Prometheus metrics                             │   │
│   └───────────────┬──────────────────────────────┬──────────┘   │
│                   │                              │              │
│                   ▼                              ▼              │
│        Fraud Probability Output         Custom Metrics          │
│                                          (Counters, Histogram,  │
│                                           Drift Gauge)          │
└───────────────────┬───────────────────────────────┬──────────────┘
                    │                               │
                    ▼                               ▼
        ┌──────────────────────┐        ┌────────────────────────┐
        │     Prometheus       │        │        Grafana         │
        │  (Metrics Scraping)  │        │  (Dashboards & Alerts) │
        └──────────┬───────────┘        └───────────┬────────────┘
                   │                                │
                   ▼                                ▼
            Alertmanager                 Fraud Monitoring Dashboard
```


## 🏗 Architecture

### 🔹 Model Layer
- RandomForest fraud classifier
- ROC-AUC evaluation
- MLflow experiment tracking
- Model Registry with version control
- Production alias–based serving

### 🔹 Serving Layer
- FastAPI inference API
- `/predict` REST endpoint
- Dynamic model loading:

### 🔹 Infrastructure
- Dockerized inference service
- Kubernetes Deployment (replicas + resource limits)
- Versioned image tags
- Environment-based MLflow configuration

### 🔹 Observability
- Prometheus metrics instrumentation
- Custom business metrics:
- `total_transactions_total`
- `high_risk_transactions_total`
- `fraud_score_distribution`
- `avg_transaction_amount`
- Grafana dashboard for fraud monitoring
- Prometheus alert rules for fraud spikes

---

## 🔁 Model Lifecycle

1. Train model locally
2. Log experiment and metrics to MLflow
3. Register model as `FraudDetectionModel`
4. Promote version to `Production`
5. Kubernetes service loads latest Production model dynamically

No Docker rebuild required for model updates.

---

## 📊 Monitoring & Drift Detection

### Business Metrics
- Transactions per minute
- High-risk transaction rate
- Fraud score distribution (P95)
- Average transaction amount (drift proxy)

### Alerting
PrometheusRule triggers alert if fraud rate exceeds threshold:


---

## 🧠 Tech Stack

- Python
- FastAPI
- Scikit-learn
- MLflow (Model Registry)
- Docker
- Kubernetes
- Prometheus
- Grafana

