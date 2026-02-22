# ADR-0006: Use XGBoost for Real-Time Fraud Detection (Hot Path)

**Date:** 2026-02-22
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The Sentinel component of the *Sentinel & Scout* system performs real-time fraud detection under strict latency requirements (< 50ms target).

The model must:

- Deliver fast inference.
- Handle structured/tabular data.
- Provide strong performance with limited feature engineering.
- Be lightweight enough for containerized deployment.

Given the real-time nature of the Hot Path, deep neural networks were considered but may introduce unnecessary latency and operational complexity.

---

## Decision

Adopt **XGBoost** as the model for fraud detection in the Hot Path.

The model will be:

- Trained offline.
- Versioned using MLflow.
- Serialized and loaded at service startup.
- Used for synchronous inference within the FastAPI service.

---

## Rationale

XGBoost provides:

- High performance on structured/tabular datasets.
- Fast inference suitable for real-time APIs.
- Strong regularization and robustness.
- Mature ecosystem and production stability.
- Efficient CPU-based serving (no GPU dependency).

Compared to neural networks, XGBoost:

- Requires fewer computational resources.
- Is easier to deploy.
- Has more predictable latency.
- Is simpler to debug and monitor.

Given that fraud detection is primarily structured-data-driven, XGBoost is an appropriate balance between performance and operational simplicity.

---

## Consequences

### Positive

- Low-latency inference.
- Stable and mature production-ready model.
- Reduced infrastructure complexity.
- No GPU requirement.

### Negative

- Limited capacity for complex unstructured data.
- Requires careful feature engineering.
- No native support for online learning.

---

## Alternatives Considered

### 1. Neural Networks (MLP)

- Potentially flexible.
- Higher operational complexity.
- Increased latency variability.

### 2. Logistic Regression

- Simpler and interpretable.
- Lower predictive power for nonlinear relationships.

### 3. LightGBM

- Similar performance to XGBoost.
- Slight differences in training dynamics.
- Chosen XGBoost due to ecosystem familiarity and stability.

---

## Future Considerations

If model complexity increases or latency constraints change, model architecture may be revisited and documented via a new ADR.