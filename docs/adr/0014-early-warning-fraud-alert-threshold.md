# ADR-007: Early Warning Fraud Alert Threshold

**Date:** 2026-03-01  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

A large-scale fraud attack could go unnoticed if no one actively monitors dashboards.

The system required internal anomaly detection capable of triggering proactive alerts.

Passive monitoring was insufficient.

---

## Decision

Establish an Early Warning threshold:

- Trigger alert if fraud rate > 50%
- Minimum of 10 transactions processed
- Introduce internal state flag `_alert_sent` to prevent duplicate alert spam

---

## Consequences

### Positive

- Automated anomaly detection.
- Reduced reliance on manual monitoring.
- Prevents alert flooding via state flag.
- Improves incident responsiveness.

### Negative

- Threshold-based detection may produce false positives.
- Static threshold may not adapt to evolving fraud patterns.

---

## Alternatives Considered

### 1. Manual Dashboard Monitoring
- No engineering effort.
- High operational risk.

### 2. Statistical anomaly detection (e.g., Z-score)
- More robust.
- Higher implementation complexity.

---

## Future Considerations

Threshold may evolve toward adaptive anomaly detection using rolling windows or statistical modeling.