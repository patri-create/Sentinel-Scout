# ADR-0008: Conditional LLM Invocation for High-Risk Transactions

**Date:** 2026-02-27  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The *Sentinel & Scout* architecture separates fraud detection into two layers:

- **Sentinel**: Fast, structured-data-based model (XGBoost).
- **Scout**: LLM-powered reasoning layer (Llama 3 via Groq).

LLMs introduce:

- Higher latency compared to traditional models.
- Increased operational cost.
- External API dependency.
- Non-deterministic outputs.

Calling the LLM for every transaction would significantly impact latency and cost efficiency.

---

## Decision

Invoke the LLM (Scout) **only when Sentinel detects:**

- High fraud probability above a defined threshold.
- Anomalous or borderline behavior.
- Explicit uncertainty in model output.

For the majority (~95%) of low-risk transactions, only Sentinel is executed.

---

## Rationale

- LLM inference is slower and more expensive.
- Real-time payment flows require minimal latency.
- High-risk gating reduces cost and improves scalability.
- Preserves user experience for legitimate transactions.
- Aligns with production-grade hybrid ML system design.

This approach balances performance, cost, and reasoning depth.

---

## Consequences

### Positive

- Reduced operational cost.
- Lower average response time.
- Controlled LLM usage.
- Improved scalability.

### Negative

- Requires careful threshold tuning.
- Risk of missing nuanced fraud cases below threshold.
- Adds branching complexity to inference logic.

---

## Alternatives Considered

### 1. Always Call the LLM

- Maximum reasoning depth.
- High latency and cost.
- Poor scalability.

### 2. Never Call the LLM

- Lowest latency.
- No explainability layer.
- Reduced fraud detection sophistication.

---

## Future Considerations

Threshold calibration may evolve using offline evaluation and monitoring metrics.

Any change to gating logic must be documented in a new ADR.