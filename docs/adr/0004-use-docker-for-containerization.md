# ADR-0004: Use Dockerfile and Docker Compose for Containerization and Local Orchestration

**Date:** 2026-02-20  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The *Sentinel & Scout* system is designed as a distributed ML architecture composed of multiple services, including:

- FastAPI services (Sentinel - fraud detection, Scout - recommendation engine).
- Redis for feature caching.
- Vector database (Qdrant) for semantic search.
- MLflow for experiment tracking and model registry.
- Monitoring components (Evidently, Grafana).

To ensure:

- Environment consistency across development and CI.
- Reproducibility of service configurations.
- Isolation of dependencies.
- Production-aligned infrastructure design.

The system must be containerized.

Running services directly on the host machine would introduce dependency conflicts, environment drift, and non-reproducible builds.

---

## Decision

Adopt:

- **Dockerfile** for building service images.
- **Docker Compose** for local multi-service orchestration.

Each service (API, MLflow, Redis, etc.) will be containerized using a dedicated Dockerfile where applicable.

Docker Compose will define:

- Service dependencies.
- Network configuration.
- Environment variables.
- Volume mounts.
- Port mappings.

---

## Rationale

### Dockerfile

Using Dockerfile allows:

- Explicit definition of runtime environment.
- Dependency isolation.
- Reproducible builds.
- Alignment with production container workflows.
- Easy CI/CD integration.

Container images represent deployable artifacts, reducing "it works on my machine" issues.

### Docker Compose

Docker Compose enables:

- Local orchestration of multiple services.
- Simplified service startup with a single command.
- Network isolation between services.
- Explicit infrastructure definition as code.
- Faster development feedback loop.

Since this project simulates a distributed ML system, Compose provides a lightweight alternative to Kubernetes for local development.

---

## Consequences

### Positive

- Reproducible environments.
- Production-aligned development workflow.
- Clear infrastructure-as-code structure.
- Easier onboarding for contributors.
- Reduced dependency conflicts.
- Simplified local orchestration.

### Negative

- Additional configuration complexity.
- Slight performance overhead compared to native execution.
- Learning curve for container networking and volumes.

---

## Alternatives Considered

### 1. Running Services Directly on Host

- Simpler initial setup.
- High risk of dependency conflicts.
- Non-reproducible environment.
- Poor alignment with production practices.

### 2. Kubernetes (Local)

- Closer to production-grade orchestration.
- Overly complex for a development environment.
- Increased operational overhead.

### 3. Single-Container Architecture

- Simplified setup.
- Breaks separation of concerns.
- Unrealistic representation of distributed ML systems.

---

## Future Considerations

If the system evolves toward a production deployment, orchestration may migrate to:

- AWS ECS/Fargate
- Kubernetes
- Managed container platforms

Any change in orchestration strategy must be documented via a new ADR superseding this one.
