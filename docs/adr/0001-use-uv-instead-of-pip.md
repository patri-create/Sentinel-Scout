# ADR-0001: Use `uv` Instead of `pip` for Dependency Management

**Date:** 2026-02-16  
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The *Sentinel & Scout* project requires:

- Fast and reproducible dependency resolution.
- Deterministic builds across local development and CI environments.
- A lockfile mechanism to ensure consistent installations.
- A modern dependency workflow compatible with containerized environments.

The traditional `pip + requirements.txt` approach does not provide strict dependency resolution guarantees or built-in lockfile management. Additionally, dependency resolution speed can become a bottleneck in CI pipelines.

Given the architectural focus of this project (ML system with multiple services, reproducibility, and CI/CD integration), dependency management must be reliable and performant.

---

## Decision

Adopt **`uv`** as the dependency manager for this project.

`uv` will be used to:

- Manage dependencies.
- Generate and maintain a lockfile.
- Install dependencies deterministically in both local and CI environments.
- Improve dependency resolution speed.

---

## Rationale

`uv` provides:

- Significantly faster dependency resolution compared to `pip`.
- Deterministic lockfile support, ensuring reproducible builds.
- Improved performance in CI pipelines.
- A modern dependency management workflow aligned with production-grade Python systems.

Given that this project emphasizes engineering quality (MLOps, CI/CD, containerization), reproducibility and performance are prioritized over ecosystem familiarity.

---

## Consequences

### Positive

- Faster dependency resolution and installation.
- Deterministic builds via lockfile.
- Better CI/CD performance.
- Cleaner dependency management structure.

### Negative

- Lower ecosystem adoption compared to `pip`.
- Potential onboarding friction for contributors unfamiliar with `uv`.
- Less historical documentation and community support.

---

## Alternatives Considered

### 1. `pip` + `requirements.txt`

- Simple and widely adopted.
- No deterministic lockfile by default.
- Slower dependency resolution.
- Higher risk of environment inconsistencies.

### 2. `pip-tools`

- Provides lockfile support.
- Additional tooling complexity.
- Slower resolution compared to `uv`.

### 3. `poetry`

- Mature ecosystem and lockfile support.
- Heavier workflow.
- Additional abstraction layer not strictly required for this project.

---

## Future Considerations

If `uv` adoption decreases or compatibility issues arise, migration to `poetry` or `pip-tools` may be considered. Any such migration must be
