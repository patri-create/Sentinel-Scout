# ADR-0018: Incremental Offline Retraining Strategy

**Date:** 2026-03-06  
**Status:** Accepted  

---

## Context

Model retraining is CPU-intensive and unsuitable for execution inside the live API process.

Blocking inference for retraining would:

- Increase latency.
- Risk service instability.
- Reduce availability.

A safe retraining mechanism must operate independently of the prediction service.

---

## Decision

Create a standalone script `retrain.py` that:

- Loads the current XGBoost model.
- Loads `retraining_data.csv`.
- Performs incremental training using the `xgb_model` parameter.
- Saves the updated model artifact.

Retraining runs offline and does not execute inside the API process.

---

## Rationale

- Protects real-time inference performance.
- Enables scheduled or manual retraining.
- Keeps operational boundaries clear.
- Aligns with MLOps best practices.

---

## Consequences

### Positive

- No service disruption during retraining.
- Modular training pipeline.
- Clear separation of concerns.

### Negative

- Requires orchestration (manual or scheduled).
- Model version management becomes necessary.

## Future Considerations

- Automate retraining through scheduled CI pipelines with performance comparison against baseline metrics.
- Introduce model version tracking (e.g., via MLflow) to manage artifacts.
- Implement automated rollback if new model performance degrades.