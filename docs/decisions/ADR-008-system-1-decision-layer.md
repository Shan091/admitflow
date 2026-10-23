# ADR-008: System-1 Decision Layer (Laya / Jev)

## Status
Accepted


## Context
AdmitFlow is readiness-aware and adaptive ([PRODUCT.md](../../PRODUCT.md)): most per-message work is *decisions* — route intent, detect abuse/injection, judge enrollment readiness, decide escalation — not text generation. Doing each as a full frontier-LLM call is slow and expensive, and these run on **every inbound message**. A new model category — "System 1" decision models (Jev by TypeSafe AI; Laya by Convai Innovations, Apache-2.0) — returns typed answers with calibrated probabilities in one non-autoregressive forward pass, roughly 100–400x cheaper/faster than an LLM for bounded decisions. Full research notes: [docs/research/system-1-decision-models-laya-jev.md](../research/system-1-decision-models-laya-jev.md).

## Decision
Adopt a **two-tier conversation engine**:

- **Decision layer (System-1):** intent/triage routing (choice), input guardrail (noul), "is knowledge question?" (noul), **enrollment readiness (score)**, escalation triggers (noul/score), language detect (choice) — all behind a single `decide()` abstraction in `src/decision/`.
- **Generation layer (frontier LLM):** all user-facing text — discovery replies, RAG answers, co-pilot suggestions, re-engagement hooks — via the existing Gemini → OpenAI → Anthropic factory.
- **Unchanged:** field extraction stays on the LLM + code (System-1 models are weak at extracting unknown values); money and hard eligibility remain code-owned (SPEC §2).

Implementation choice:
- **Laya (self-hosted, Apache-2.0) is the default decision engine** — free, local (PII stays in-house), multilingual, and exposes a **Jev-compatible `/v1/systemone`** endpoint.
- **Jev is the escape hatch** — swap specific high-cardinality / high-stakes decisions to it later without a rewrite.

Sequencing:
- **Demo (M0–M3):** implement `decide()` on **Gemini Flash** (current `gemini-3.7-flash`) with structured outputs. No fine-tuning; fastest path to a demo. The interface, not the backend, is what matters now.
- **Post-demo:** distill high-frequency decisions into self-hosted Laya using labels collected during the demo; per-decision, **measure Malayalam/Hinglish accuracy and fit calibration** before switching.

Readiness representation: enrollment readiness is a **`score` primitive** (ordinal + calibrated probability) → drives a numeric readiness signal plus the soft lifecycle stages in SPEC §7.3.

## Consequences
- Large cost/latency cut on the hottest path (decisions run on every message). Aligns with the cost-aware model-routing pattern the team has built before.
- New dependency surface (a self-hosted model service) — deferred to post-demo to keep the demo simple.
- Requires labeled data + calibration before Laya is trusted; **Malayalam quality is unverified** and gated behind our own eval.
- Reinforces (does not settle) the hand-rolled leaning for the engine: "decide → route → generate" is a natural explicit dispatcher. Engine choice stays open — see SPEC §17 and [ADR-007](ADR-007-finalized-stack.md).
- LLM model IDs stay config-driven, not pinned in docs — versions churn monthly.
