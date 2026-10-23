# System-1 Decision Models — Laya & Jev (Research Notes)

> Personal reference, captured 2026-09-27. What these models are, the numbers, how they fit AdmitFlow, and the caveats. The decision record is in [ADR-008](decisions/ADR-008-system-1-decision-layer.md); how it changes the build is in [SPEC.md](../SPEC.md) and [DEMO_SPEC.md](../DEMO_SPEC.md).

## TL;DR
"System 1" decision models **don't generate text**. You give them a *state* + *typed questions*; they return *typed answers with calibrated probabilities* in one non-autoregressive forward pass. For bounded decisions (routing, classification, scoring, yes/no) they are ~100–400x cheaper and faster than an LLM. In AdmitFlow they become a **decision layer** in front of the frontier-LLM **generation layer**.

## The three primitives
- **choice** — pick one label from a caller-defined list, with a probability for each option.
- **score** — place input on an ordered scale (probability-weighted average).
- **noul** — probability (0.0–1.0) that a yes/no question is true.

## Jev (TypeSafe AI)
- Released 15 Sep 2026; founded by Diogo Almeida (co-invented RLHF/InstructGPT at OpenAI); $40M led by DCVC.
- **Closed weights, early access. Text-only.**
- Cost **$0.042 / 1M input tokens, output free**; latency **70–500 ms**.
- LangChain's independent test: **$0.00035/call vs $0.028 for Claude Sonnet 4.6**; 30 days @ 10k/day = **$104 vs $8,434**. Matched a human oracle 100% over 500 repeats; score variance 92–913x lower than LLM judges.
- Trained with RLCD (Reinforcement Learning for Calibrated Decisions). The restricted-softmax trick is reproducible with open tools (SGLang `/v1/score`): ~463 ms vs 848 ms generation on one H100 w/ Qwen2.5-0.5B.

## Laya (Convai Innovations) — our pick
- **Apache 2.0, open-source, self-hostable, local-first.** Released Sep 2026.
- Checkpoints (a Router picks per request by script/language):
  - `laya` — ModernBERT-large, 421M, 512 ctx — English
  - `laya-multilingual` — mmBERT-base, 322M, 1024 ctx (→8192) — **100+ languages, 2x faster**
  - `laya-typed-decisions` — ModernBERT-large, 421M, 1024 ctx
- Latency **33 ms/question, 7.2 ms batched (cheap T4 GPU)**. Languages: 100+ advertised, benchmarked on 51 ("45 of 51 usable").

- Runs: `pip install laya` (Py 3.10+), CLI, **FastAPI server with a Jev-compatible `POST /v1/systemone`**, MCP server, LangChain/LangGraph integration, Docker. Downloads checkpoints from HF.
- Output: per-question answer (label+probs / score / noul prob) + routing metadata + token usage.

## Why Laya first, Jev as the escape hatch
- Free + self-hosted → no per-call cost, **PII stays local (DPDPA-friendly)**, no lock-in.
- Multilingual with a script/language router → the better bet for Malayalam/Hindi.
- **Jev-compatible endpoint** → start on Laya, swap individual decisions to Jev later with no rewrite.
- Jev is stronger on hard/high-cardinality decisions (Banking77 **0.870 vs Laya 0.425**) and better-calibrated out of the box → keep it as an upgrade for specific decisions.

## Where they fit in AdmitFlow
**Decision layer (System-1):** input guardrail (noul), triage/intent routing (choice), "is this a knowledge question?" (noul), **enrollment readiness (score)**, escalation triggers (noul/score), language detect (choice).
**Stays on the frontier LLM:** field extraction (both are weak at extracting unknown values) + all text generation (discovery replies, RAG answers, co-pilot, re-engagement).

## Caveats (do not skip)
1. **Malayalam unverified** — not named; the English checkpoint collapses on non-Latin scripts (Khmer 0.000 acc @ 0.95 conf). Run our own Malayalam/Hinglish eval before trusting each decision.
2. **Not zero-shot** — base ≈ chance (0.36 vs 0.318 random); fine-tune to ~0.77. "A fast base to specialise." Needs labeled data.
3. **Calibration ships over-confident** — fit temperature on our data (ECE 0.466 → 0.081 after fitting).
4. **Weak at** extraction / arithmetic / date-compare / negation / high-cardinality choice. Avoid boolean-word labels; always add an OTHER/ESCALATE option (restricted softmax forces every input into a declared label).
5. **Jev:** closed weights, early access, thin independent calibration data — don't hard-depend.

## Recommended sequencing
- **Demo (M0–M3):** decisions on Gemini Flash (current `gemini-3.7-flash`) via structured outputs, behind one `decide()` interface. No fine-tuning; fastest path to demo.
- **Post-demo:** distill high-frequency decisions (triage, guardrail-triage, readiness, escalation) into self-hosted Laya using demo-collected labels; keep the Jev endpoint as the upgrade valve; measure Malayalam per decision before flipping.

## Sources
- Jev — TypeSafe AI (Hyperstack): https://www.hyperstack.cloud/technical-resources/tutorials/jev-inside-typesafe-ais-first-system-one-decision-model
- Jev — built for decisions, not conversation (Eden AI): https://www.edenai.co/post/jev-a-new-kind-of-ai-model-built-for-decisions-not-conversation
- Jev (AI model) — Wikipedia: https://en.wikipedia.org/wiki/Jev_(AI_model)
- Laya — GitHub (NandhaKishorM/laya): https://github.com/NandhaKishorM/laya
- Laya AI: the open 33ms decision model (eesel): https://www.eesel.ai/blog/laya-ai
- Best Frontier LLMs 2026 (CometAPI): https://www.cometapi.com/best-frontier-llms-2026-comparison/
