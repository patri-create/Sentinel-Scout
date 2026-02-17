# ADR-0003: Use Pydantic for Data Validation and Schema Enforcement

**Date:** 2026-02-16  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The *Sentinel & Scout* system processes external user inputs in real time, including:

- Transaction data for fraud detection (Hot Path - Sentinel).
- User context and product interaction signals (Cold Path - Scout).

Since these inputs originate from external clients or upstream systems, they must be:

- Strictly validated.
- Type-safe.
- Schema-controlled.
- Explicitly defined to avoid silent failures.

Given that the Hot Path must operate under low-latency constraints, input validation must be efficient and reliable.

Improper validation could lead to:
- Incorrect predictions.
- Model crashes.
- Data drift amplification.
- Silent logical errors in downstream components.

---

## Decision

Adopt **Pydantic** for request and response schema validation within the FastAPI services.

Pydantic will be used to:

- Define structured request/response models.
- Enforce type validation.
- Perform automatic data parsing and coercion.
- Ensure consistent API contracts.
- Reduce runtime errors caused by malformed input data.

---

## Rationale

Pydantic provides:

- Runtime data validation based on Python type hints.
- Automatic request parsing in FastAPI.
- Clear and explicit schema definitions.
- Strong integration with OpenAPI documentation.
- Minimal performance overhead.

Given that this project emphasizes production-grade ML engineering, strict input validation is necessary to ensure model reliability and system robustness.

Using Pydantic reduces the risk of passing malformed or incomplete data to the model, which is especially critical in real-time fraud detection scenarios.

---

## Consequences

### Positive

- Strongly typed request/response models.
- Reduced risk of malformed input reaching the model layer.
- Automatic and clear API documentation.
- Cleaner separation between transport layer and model logic.
- Easier debugging and observability of input errors.

### Negative

- Slight runtime overhead for validation.
- Additional learning curve for complex schema definitions.
- Potential performance impact if overused in high-frequency internal calls.

---

## Alternatives Considered

### 1. Manual Validation

- Full control over validation logic.
- Higher risk of inconsistency and human error.
- Increased boilerplate.
- Lower maintainability.

### 2. Dataclasses + Custom Validation

- Cleaner structure than raw dicts.
- No built-in validation.
- Requires additional custom logic.

### 3. Marshmallow

- Mature schema validation library.
- More verbose configuration.
- Less tightly integrated with FastAPI.

---

## Future Considerations

If performance profiling reveals validation overhead as a bottleneck in the Hot Path, validation boundaries may be optimized or partially moved upstream.

Any architectural change affecting schema enforcement must be documented via a new ADR superseding this one.
