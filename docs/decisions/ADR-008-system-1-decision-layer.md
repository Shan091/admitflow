# ADR-008: Typed OpenAI decision layer

Status: Accepted; revised by user decision. Replaces the earlier self-hosted-model proposal.

## Decision

Use OpenAI through the existing provider factory and a shared `decide()` interface.
Pydantic schemas describe intent, safety classifications and explicitly supported
eligibility facts. Refusal, empty output and invalid schemas are failures, never
permission to approve a student or invent facts. Model IDs remain in configuration.

No fine-tuning, distillation, training-label collection or separate model server is
planned. There is no provider selection layer beyond the existing OpenAI roles.
Do not present model confidence as calibrated probability.

The active Telegram router uses typed intent for questions, discovery, qualification
and staff requests. Explicit commands, deterministic safety checks and escalation
shortcuts run first. Eligibility extraction retains exact evidence validation.
Eligibility rules, lifecycle/readiness state, authorization, prices, discounts,
seat allocation and payments remain deterministic code decisions.

## Consequences and verification

Reuse configured OpenAI credentials and existing bounded provider retries/timeouts.
Generation still uses the same factory; a schema does not establish factual accuracy.
The journey preserves memory and gives its existing unavailable response on failure.
Safety classifiers fail closed; compatibility triage defaults to discovery.

Decision, guardrail and triage unit tests plus PostgreSQL Telegram journey checks
cover these boundaries. See Task 40 and ADR-012 for the active acceptance criteria.
