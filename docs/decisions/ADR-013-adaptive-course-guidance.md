# ADR-013: Adaptive, student-first course guidance

Status: Accepted; implementation and evidence tracked in Task 61.

## Context

The existing discovery loop returns course buttons, then sorted eligibility questions.
It does not learn why a student wants a course or introduce unfamiliar relevant options.
The user requested an English adaptive conversation for institution applicants, with
optional deeper exploration and honest acknowledgment of absent offerings.

## Decision

Use the existing OpenAI decision boundary to interpret the current message first,
validate corrections and refresh catalog eligibility, then choose a contextual next question,
provisional support stage, evidence-backed interest notes and a small course shortlist.
The [research record](../engineering/ADAPTIVE_GUIDANCE_RESEARCH.md) distinguishes
interest exploration, experience, values, constraints and formal academic eligibility.
No model training, new AI provider, framework or psychometric-scoring dependency.

1. Open text is the default for interests/background. Use signed choices for concrete
   catalog decisions and deeper exploration. Decided applicants may skip exploration.
2. Persist literal, correctable profile evidence encrypted with conversation memory.
   Themes/stages are tentative guidance notes, not diagnoses or aptitude scores.
3. Code filters tenant courses, intakes and known failed academic prerequisites.
   Missing information remains unverified. Only explicit choices change selection.
4. Explain matches using student and course evidence. Offer relevant unfamiliar options
   without overriding an informed preference or pressuring enrollment.
5. If no fit is verified, acknowledge it. Clearly label general fields to research
   elsewhere; invent no external institutions, availability or outcomes.
6. Optional deeper conversation uses original contextual prompts. Link the official
   O*NET® resource on request; do not redistribute items, shorten tests, import results
   or claim the conversation inherits an instrument's validity.
7. Preserve FAQ grounding, human/safety escalation, consent and application/payment
   controls. Outages preserve state and offer retry or explicit catalog browsing.

## Consequences

The model makes question order flexible, so unit rules alone cannot prove conversation
quality. Add bounded realistic OpenAI evaluations alongside database and adversarial
checks. Catalog descriptions and academic rules determine the quality of local matches;
missing descriptions must not be filled with invented curriculum. No claim of
validated counseling or real-student outcome improvement is made by this release.

ADR-006 code-owned outcomes, ADR-009 privacy and ADR-012 provider/channel decisions
remain in force. English-only onboarding supersedes the language-choice step for this
slice; historical translations and transcripts are preserved.
