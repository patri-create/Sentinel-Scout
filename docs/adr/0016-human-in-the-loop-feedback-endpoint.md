# ADR-0016: Implementation of Human-in-the-Loop (HITL) Feedback Endpoint

**Date:** 2026-03-06  
**Status:** Accepted  

---

## Context

Fraud detection models degrade over time because fraud patterns evolve.

Without human validation, the model:

- Cannot learn from false positives.
- Cannot adapt to new fraud strategies.
- Lacks reliable ground truth labels.

A feedback mechanism is required to capture validated outcomes.

---

## Decision

Implement a REST endpoint `/feedback` that:

- Accepts a `transaction_id` (UUID).
- Accepts a validated label from a human analyst.
- Appends validated examples incrementally to `retraining_data.csv`.

The CSV file acts as the accumulating dataset for offline retraining.

---

## Rationale

- Human feedback provides true ground truth.
- Enables supervised retraining with real-world data.
- Closes the feedback loop between prediction and validation.
- Keeps implementation simple and transparent.

---

## Consequences

### Positive

- Enables model adaptation.
- Improves fraud detection accuracy over time.
- Introduces structured human oversight.

### Negative

- Requires governance of analyst input.
- CSV storage may not scale indefinitely.

## Future Considerations

- Replace CSV storage with a relational database if feedback volume or concurrency increases.
- Introduce schema validation and analyst approval workflows before incorporating labels into retraining.
- Add authentication and role-based access control to protect the `/feedback` endpoint.