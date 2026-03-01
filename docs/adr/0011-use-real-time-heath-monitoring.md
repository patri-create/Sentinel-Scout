# ADR-0011: Implement Real-Time Health Monitoring and Business Metrics

**Date:** 2026-03-01  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The Sentinel & Scout system operated as a black box.

There was no immediate way to determine:

- Whether the ML model was properly loaded.
- Whether Redis was accessible.
- The current fraud rate.
- The operational health of the system.

Operational visibility required manually inspecting server logs, which is not aligned with MLOps best practices.

The system required immediate observability to:

- Detect runtime failures.
- Expose readiness/liveness signals.
- Monitor business-level KPIs (fraud ratio).

---

## Decision

Implement:

1. A `/health` endpoint exposing:
   - Model loaded status.
   - Redis connectivity status.
   - Basic system readiness checks.

2. A `TrackerManager` class responsible for:
   - Tracking total predictions.
   - Tracking detected fraud cases.
   - Computing fraud rate dynamically.
   - Exposing real-time business metrics.

---

## Consequences

### Positive

- Improved system observability.
- Clear integration path with container orchestration health checks (Docker/Kubernetes).
- Immediate detection of service misconfiguration.
- Centralized business metric tracking.
- Better MLOps alignment.

### Negative

- Slight CPU overhead when computing fraud ratios.
- Additional complexity in request lifecycle.
- Increased need for concurrency safety mechanisms.

---

## Alternatives Considered

### 1. Log-Only Monitoring
- Minimal implementation effort.
- No structured operational insight.
- Requires manual inspection.

### 2. External Monitoring Only
- Offloads logic to external tools.
- No internal business-level metric aggregation.

---

## Future Considerations

Integration with Prometheus exporters or OpenTelemetry may replace or extend internal metric aggregation.