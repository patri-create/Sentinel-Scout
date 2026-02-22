# ADR-0007: Enable Redis AOF Persistence and Docker Volume Storage

**Date:** 2026-02-22  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

Redis is used in the Sentinel Hot Path as an in-memory feature cache for real-time enrichment.

By default, Redis operates fully in-memory, meaning:

- Data is lost if the container restarts.
- Feature state may be inconsistent after crashes.
- Development environments may lose debugging context.

While Redis is primarily used as a cache, certain short-term behavioral features benefit from persistence across container restarts during development.

To improve durability and debugging reliability, persistence must be enabled.

---

## Decision

Enable:

- **Append Only File (AOF)** persistence in Redis.
- A **Docker volume** to persist Redis data across container restarts.

Redis configuration includes:

- `appendonly yes`
- Mounted volume for `/data` directory in Docker Compose.

---

## Rationale

### AOF Persistence

- Logs every write operation.
- Provides better durability guarantees compared to snapshot-only persistence.
- Suitable for systems where recent writes must not be lost.

### Docker Volume

- Ensures Redis data survives container recreation.
- Improves development stability.
- Allows inspection of persisted state.

Although Redis is used primarily as a cache, enabling AOF improves realism and resilience of the system design.

---

## Consequences

### Positive

- Improved durability during development.
- Reduced data loss on container restart.
- More realistic production-like behavior.
- Easier debugging and state inspection.

### Negative

- Slight performance overhead due to write logging.
- Increased disk usage.
- Additional configuration complexity.

---

## Alternatives Considered

### 1. No Persistence (Default)

- Simpler setup.
- Data loss on restart.
- Less realistic system behavior.

### 2. RDB Snapshots Only

- Lower overhead.
- Risk of losing recent writes between snapshots.

### 3. External Persistent Store

- Higher durability.
- Unnecessary complexity for this project scope.

---

## Future Considerations

In production environments, Redis persistence strategy may be adjusted depending on durability requirements and scalability needs.

Any change in persistence configuration must be documented via a new ADR superseding this one.