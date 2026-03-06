# ADR-0017: Temporary Feature Persistence for Retraining (Redis Buffer)

**Date:** 2026-03-06  
**Status:** Accepted  

---

## Context

The `/feedback` endpoint requires access to the original transaction features.

However, requiring analysts to resubmit all technical details:

- Increases complexity.
- Introduces risk of data mismatch.
- Reduces usability.

The system must temporarily preserve transaction features.

---

## Decision

Store transaction features in Redis for 24 hours using:

- `SETEX`
- `transaction_id` as key
- JSON-serialized feature payload as value

This allows `/feedback` to retrieve the original feature set using only the UUID.

---

## Rationale

- Simplifies feedback interface.
- Preserves full feature context.
- Avoids unnecessary data duplication.
- Maintains ephemeral storage model.

Redis acts as a temporary buffer for contextual reconstruction.

---

## Consequences

### Positive

- Clean separation between prediction and feedback.
- Reduced analyst burden.
- Consistent retraining dataset integrity.

### Negative

- Data expires after TTL.
- Requires Redis availability.

## Future Considerations

- Monitor Redis memory usage and eviction patterns under higher traffic.
- Migrate from Redis TTL buffering to a dedicated feature store if retention requirements expand.
- Encrypt or redact sensitive feature fields if compliance constraints arise.