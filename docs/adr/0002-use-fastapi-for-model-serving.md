# ADR-0002: Use FastAPI for Model Serving

**Date:** 2026-02-16  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The *Sentinel & Scout* system requires a lightweight, high-performance API layer to serve:

- Real-time fraud predictions (Hot Path - Sentinel).
- Context-aware recommendations (Cold Path - Scout).
- Health checks and observability endpoints.

The API must:

- Support low-latency inference.
- Provide automatic request validation.
- Integrate cleanly with async workflows.
- Be easy to containerize and deploy in cloud environments.
- Scale horizontally if required.

Given that the Hot Path must respond in milliseconds, the serving framework must introduce minimal overhead.

---

## Decision

Adopt **FastAPI** as the API framework for model serving.

FastAPI will be used to:

- Expose inference endpoints (`/predict`, `/recommend`).
- Validate request/response schemas using Pydantic.
- Provide automatic OpenAPI documentation.
- Support asynchronous request handling where appropriate.

---

## Rationale

FastAPI provides:

- High performance based on ASGI and Starlette.
- Automatic data validation via Pydantic, reducing input-related errors.
- Native async support, enabling non-blocking operations.
- Built-in OpenAPI/Swagger documentation for easier debugging and integration.
- Strong ecosystem adoption in ML and microservices architectures.

Compared to traditional frameworks, FastAPI offers a better balance between performance, developer experience, and production readiness.

Given the architectural focus of this project (real-time inference + distributed ML components), FastAPI aligns well with scalability and maintainability goals.

---

## Consequences

### Positive

- Low-latency API layer suitable for real-time inference.
- Automatic schema validation reduces runtime errors.
- Clear API documentation without additional tooling.
- Clean integration with Docker and cloud deployments.
- Async capabilities support I/O-heavy operations (e.g., Redis, vector DB queries).

### Negative

- Slightly more complex async model compared to Flask.
- Requires understanding of ASGI servers (e.g., Uvicorn, Gunicorn with workers).
- Potential misuse of async patterns if not carefully designed.

---

## Alternatives Considered

### 1. Flask

- Simpler and widely adopted.
- Limited async support.
- Lower performance under high concurrency.
- Requires additional tooling for schema validation and documentation.

### 2. Django

- Full-featured framework.
- Heavyweight for a model-serving use case.
- Introduces unnecessary complexity for a microservice architecture.

### 3. Raw ASGI (Starlette)

- Maximum control.
- More boilerplate and lower developer ergonomics.
- Less structured validation out of the box.

---

## Future Considerations

If traffic scales significantly or stricter performance guarantees are required, the deployment configuration (e.g., worker strategy, autoscaling, load balancing) may be revisited without changing the framework itself.

Any future migration to a different serving framework must be documented via a new ADR superseding this one.
