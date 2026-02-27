# ADR-0009: Enforce Structured JSON Output from LLM

**Date:** 2026-02-27 
**Author:** Patricia Tarazaga  
**Status:** Accepted  

---

## Context

The Scout layer generates contextual reasoning about suspicious transactions.

LLMs naturally return free-form text, which:

- Is difficult to parse reliably.
- Cannot be programmatically consumed safely.
- Introduces automation risks.

To integrate Scout into a production-grade system, outputs must be machine-readable.

---

## Decision

Require the LLM to return responses strictly in structured JSON format, including predefined fields such as:

- risk_summary
- reasoning
- confidence_score
- suggested_action

The system validates the JSON before taking any action.

---

## Rationale

- Enables deterministic downstream automation.
- Allows programmatic decision-making.
- Improves safety and guardrail enforcement.
- Simplifies logging and observability.
- Reduces hallucination impact.

Structured output transforms LLM responses from narrative text into actionable system components.

---

## Consequences

### Positive

- Automation-friendly responses.
- Easier monitoring and auditing.
- Reduced parsing errors.
- Safer system integration.

### Negative

- Requires stricter prompt engineering.
- Potential failure if LLM returns malformed JSON.
- Slight increase in validation logic complexity.

---

## Alternatives Considered

### 1. Free-Form Text

- Simpler prompting.
- Not production-safe.
- Manual interpretation required.

### 2. Regex Parsing

- Fragile and error-prone.
- Not reliable for structured systems.

---

## Future Considerations

Future integration with tool-calling or function-calling APIs may replace manual JSON enforcement.