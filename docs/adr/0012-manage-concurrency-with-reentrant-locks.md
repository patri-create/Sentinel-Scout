# ADR-0012: Manage Concurrency Using Reentrant Locks (RLock)

**Date:** 2026-03-01  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The introduction of global counters in an asynchronous FastAPI environment introduced the risk of race conditions.

Counters such as:

- total_predictions
- fraud_detected

must remain accurate under concurrent access.

Initial implementation using `threading.Lock` resulted in deadlock scenarios when a thread attempted to re-acquire a lock it already held.

This compromised system stability.

---

## Decision

Replace `threading.Lock` with `threading.RLock`.

---

## Justification

`RLock` (Reentrant Lock):

- Allows the same thread to acquire the lock multiple times.
- Prevents self-deadlocking.
- Preserves data integrity in nested or re-entrant function calls.
- Ensures thread-safe counter updates.

This solution balances simplicity and correctness without introducing external concurrency primitives.

---

## Consequences

### Positive

- Eliminates race conditions in shared counters.
- Prevents deadlocks caused by re-entrant calls.
- Maintains accurate fraud statistics.
- Minimal refactor required.

### Negative

- Slight performance overhead compared to a basic Lock.
- Increased responsibility to manage proper lock acquisition patterns.

---

## Alternatives Considered

### 1. threading.Lock
- Simpler.
- Unsafe in nested acquisition scenarios.

### 2. Async-native primitives (e.g., asyncio.Lock)
- More aligned with async context.
- Requires deeper architectural refactor.

### 3. External metrics store (Redis counters)
- Offloads concurrency.
- Adds network overhead.