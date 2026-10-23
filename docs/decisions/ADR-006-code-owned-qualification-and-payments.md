# ADR-006: Code-Owned Qualification and Payments

## Status
Accepted


## Context
The core value proposition of AdmitFlow is qualifying leads based on institution-defined rules (e.g., "Age >= 16", "Passed 10th grade") and collecting application fees. We need to decide how much authority the AI has over these critical business outcomes.

## Decision
**Code Owns the State and the Money.**
- **Qualification**: The LLM's only job is to extract field values from the chat (e.g., `extracted_age = 17`). A deterministic Python rule engine evaluates these values against the database rules. The LLM cannot transition a lead to `admission_ready`.
- **Payments**: The LLM never decides the fee amount. When generating a Razorpay link, the amount is pulled directly from `course.application_fee` in the database.

## Alternatives Considered

### Prompt-Based Qualification
- Pros: Easy to implement (just give the LLM the rules in text and ask it to decide).
- Cons: LLMs are non-deterministic. They might incorrectly qualify a 15-year-old for a course requiring age 16 because "they are close enough".
- Rejected: Institutions require 100% deterministic rule enforcement.

## Consequences
- The database schema must rigidly support structured rule definitions (`field`, `operator`, `value`).
- The dashboard frontend must provide a structured rule builder UI, rather than a free-text prompt box for staff.
