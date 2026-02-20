# ADR-0005: Use Redis for Low-Latency Feature Caching in the Hot Path

**Date:** 2026-02-16  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The *Sentinel & Scout* system includes a real-time fraud detection component (Sentinel) operating under strict latency constraints (< 50ms target).

Fraud prediction requires enriched contextual features such as:

- Recent transaction counts.
- Short-term behavioral patterns.
- Aggregated user activity metrics.

Querying a primary database (e.g., relational or document-based) during real-time inference would introduce:

- Increased latency.
- I/O bottlenecks.
- Reduced throughput under high concurrency.

To maintain low-latency inference performance, frequently accessed and time-sensitive features must be stored in a fast, in-memory system.

---

## Decision

Adopt **Redis** as an in-memory data store for feature caching in the Hot Path.

Redis will be used to:

- Store short-lived behavioral features.
- Retrieve user-related aggregates during inference.
- Support fast read/write operations.
- Enable TTL-based expiration for time-bound features.

---

## Rationale

Redis provides:

- Sub-millisecond read/write latency.
- In-memory storage optimized for high-throughput workloads.
- Built-in expiration (TTL) support.
- Simple key-value and structured data models (hashes, sets, sorted sets).
- Strong ecosystem support in distributed systems.

Given the real-time nature of fraud detection, Redis ensures that feature enrichment does not become the system bottleneck.

This aligns with production-grade ML system design, where feature retrieval latency must remain predictable and minimal.

---

## Consequences

### Positive

- Reduced inference latency.
- Improved system throughput.
- Decoupling of feature computation from primary database queries.
- Support for time-windowed behavioral modeling via TTL.
- Better scalability under concurrent load.

### Negative

- Additional infrastructure component to maintain.
- Risk of stale features if not properly invalidated.
- Requires careful memory management.
- Potential consistency trade-offs compared to primary data source.

---

## Alternatives Considered

### 1. Direct Database Queries

- Simpler architecture.
- Higher latency.
- Reduced scalability under load.
- Increased coupling between inference and persistence layer.

### 2. In-Memory Application Cache (e.g., Python dict)

- No external dependency.
- Not distributed.
- Not scalable across instances.
- Data loss on service restart.

### 3. Feature Store (e.g., Feast)

- More structured feature management.
- Overkill for the current project scope.
- Higher setup and operational complexity.

---

## Future Considerations

If the system evolves toward more complex feature engineering or distributed training/inference pipelines, integration with a dedicated feature store may be considered.

Any architectural shift replacing Redis must be documented via a new ADR superseding this one.
