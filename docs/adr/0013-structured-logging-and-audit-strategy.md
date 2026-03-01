# ADR-0013: Structured Logging and Audit Strategy

**Date:** 2026-03-01  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

Default application logs were unstructured and textual.

For:

- Forensic analysis
- Fraud investigations
- Data Drift detection
- External monitoring ingestion

Each fraud decision needed to be:

- Traceable
- Structured
- Machine-parseable

Free-form logs are difficult to aggregate and process reliably.

---

## Decision

Implement a `MetricsLogger` class with structured output format:

TIMESTAMP | LEVEL | AUDIT | USER | PROB | RESULT

Each prediction event is logged in this consistent format.

---

## Consequences

### Positive

- Logs are machine-parseable.
- Compatible with ELK Stack and Grafana Loki.
- Enables forensic auditing.
- Simplifies drift analysis.
- Avoids in-memory storage accumulation (.append()).

### Negative

- Less human-friendly raw output.
- Requires discipline in maintaining format consistency.

---

## Alternatives Considered

### 1. Default logging module (textual)
- Easy.
- Poor for structured ingestion.

### 2. JSON logging
- Highly structured.
- Slightly heavier payload size.
- More verbose output.

---

## Future Considerations

Migration to structured JSON logging with OpenTelemetry integration may be considered if system scale increases.