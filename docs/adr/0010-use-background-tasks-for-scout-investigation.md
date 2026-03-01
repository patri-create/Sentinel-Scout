# ADR-0010: Execute Scout Investigation as Background Task

**Date:** 2026-02-27
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The system processes payment transactions under strict latency requirements.

The Sentinel layer must respond immediately.

Scout (LLM-based reasoning) introduces:

- Higher latency (hundreds of milliseconds to seconds).
- External API dependency.
- Non-deterministic completion time.

Blocking the main request while waiting for LLM reasoning would degrade user experience.

---

## Decision

Respond to the client immediately after Sentinel evaluation.

If Scout is triggered, execute the LLM investigation asynchronously using background tasks.

The result may:

- Update logs.
- Trigger alerts.
- Modify user status post-transaction.

---

## Rationale

- Protect user experience.
- Avoid blocking payment flow.
- Decouple reasoning from transaction confirmation.
- Align with event-driven system design.

Security enhancements must not degrade core transaction flow.

---

## Consequences

### Positive

- Improved perceived latency.
- Better UX.
- Clear separation between decision layer and reasoning layer.
- Increased system resilience.

### Negative

- Increased architectural complexity.
- Requires async task handling.
- Potential race conditions if not carefully managed.

---

## Alternatives Considered

### 1. Synchronous LLM Call

- Simpler flow.
- High latency.
- Poor UX.

### 2. External Queue System (e.g., Kafka)

- Highly scalable.
- Overkill for current scope.

---

## Future Considerations

If system scale increases, background processing may migrate to a queue-based architecture.