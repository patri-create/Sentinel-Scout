# ADR-0015: Transaction Identification for Data Lineage (UUID Usage)

**Date:** 2026-03-06  
**Status:** Accepted  

---

## Context

The `/predict` endpoint processes fraud detection requests in real time.

However, once a prediction is returned, there is no reliable way to:

- Trace the exact input features used during inference.
- Link future analyst feedback to the original prediction.
- Reconstruct the transaction context for retraining.

Without unique identification, the system lacks prediction traceability and data lineage.

---

## Decision

Assign a **UUIDv4** identifier to every request processed by the `/predict` endpoint.

The UUID:

- Is generated using the `uuid` library.
- Is returned in the API response.
- Is used as the primary reference key in downstream systems.

---

## Rationale

- Enables full prediction traceability.
- Allows linking analyst feedback to exact model inputs.
- Supports construction of a retraining dataset.
- Improves auditability and forensic analysis.

This decision establishes a foundation for reliable data lineage.

---

## Consequences

### Positive

- Enables feedback-driven retraining.
- Improves system transparency.
- Facilitates debugging and auditing.

### Negative

- Slight additional payload in API responses.
- Requires careful propagation across systems.

## Future Considerations

- Propagate `transaction_id` across logging and tracing layers (e.g., OpenTelemetry) to enable full end-to-end request reconstruction.
- Persist prediction metadata (features + model version) in a lightweight store if audit requirements increase.
- Standardize UUID exposure across services to support cross-system lineage.