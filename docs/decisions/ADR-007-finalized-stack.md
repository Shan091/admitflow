# ADR-007: Finalized Production Stack (Hosting, Data Stores, LLM, Tooling)

## Status
Accepted


## Context
Earlier ADRs and SPEC v1 left several infrastructure choices provisional or inconsistent: Railway (ADR-001) vs Render/Koyeb (SPEC) for hosting, Supabase for the database, Upstash for Redis, self-hosted Langfuse (ADR-005), and an OpenAI-first LLM chain. We needed one settled stack that (a) stays always-on for WhatsApp webhooks and the re-engagement scheduler, (b) protects customer data, and (c) suits a solo team launching a real product. The demo and production share this stack — the demo (see DEMO_SPEC.md) is the first production-grade slice of it.

## Decision

### Hosting
- **Backend API + TaskIQ worker + scheduler: Fly.io**, always-on machines (no sleep). Supersedes ADR-001's "Railway" and SPEC v1's "Render/Koyeb". Free-tier hosts that sleep drop the first webhook of a conversation and break the scheduled re-engagement worker.
- **Frontend: Vercel.**

### Data stores
- **Database: Neon** (managed PostgreSQL + pgvector). Supersedes Supabase. Managed backups/PITR and DB branching with far less ops than self-managing Fly Postgres; the small cross-provider latency is absorbed by async workers. App uses the pooled endpoint; long-running jobs (migrations, RAG ingestion) use the direct (session-mode) endpoint. HNSW index on the embedding column.
- **Redis: Redis on Fly** (persistence on), co-located and flat-cost. Supersedes Upstash. A constantly-polling TaskIQ broker + mutex keepalive is a poor fit for per-command pricing; most Redis data here is ephemeral, so self-hosting is low-risk and persistence protects the job queue.
- **Object storage: Cloudflare R2** for uploaded RAG documents.

### AI
- **LLM chain: Gemini → OpenAI → Anthropic.** Supersedes OpenAI-first. Gemini Flash has the best Malayalam/Indic coverage and lowest cost for high-frequency nodes; OpenAI is the reliable fallback and strongest for structured extraction; Anthropic for co-pilot nuance.
- **Embeddings: pluggable** — `bge-m3` (self-hosted) in dev, OpenAI `text-embedding-3-small` in prod. Chunks tagged with model + dimension; switching triggers a per-tenant re-index (1024 vs 1536 dims are not interchangeable).

### LLM efficiency
- **Model IDs live in settings, never in docs or code.** The provider layer references *roles* (`FAST_MODEL`, `FALLBACK_MODEL`, `NUANCE_MODEL`); the concrete version strings (e.g. Gemini Flash, GPT, Claude Opus/Fable generations) sit only in `.env`/settings. Model generations churn monthly — pinning them here would rot the ADR. Docs describe the *role*, settings carry the *ID*.
- **Prompt caching on the static prefix** — system prompt + per-institution context are cached so the cold-reload-per-turn engine doesn't pay full input cost every WhatsApp turn. Caveat: provider cache TTLs are short (Anthropic ~5 min; Gemini implicit/explicit), and WhatsApp turns are bursty with long gaps, so the real win is *within a burst* and on the static institution block, not across a whole conversation.
- **Structured outputs are the default for all extraction** — field extraction (qualification), the `decide()` layer, and any place we pull typed data from an LLM use native JSON-schema / function calling, not free-text parsing. Extracted fields feed deterministic code (rule eval, Code Owns Eligibility), so the LLM boundary must be typed.

### Observability
- **Langfuse Cloud (free tier)**, scrubbing PII before logging. Supersedes ADR-005's self-hosted Langfuse; self-hosting is a post-MVP option if data-residency requires it.

### Dashboard real-time
- **SSE** (server→client only), authenticated via an httpOnly cookie.

### Secrets, auth, tooling
- Secrets in **Fly secrets**; a master data-encryption key (Fly secrets) envelope-encrypts PII columns and per-tenant WhatsApp/Razorpay credentials.
- Auth via **fastapi-users** (hashing, reset, verification), token in an httpOnly cookie.
- **Transactional email: Resend.**
- Tooling: **uv, ruff, mypy --strict, pytest**, run in **GitHub Actions** on every push.
- Guardrails are **deterministic-first**: code/regex checks run before any LLM classifier.

## Consequences
- One settled stack; DEMO_SPEC.md's "same stack as production" resolves to this ADR.
- A small always-on cost replaces SPEC v1's "$0 MVP" goal, in exchange for reliability (no dropped webhooks, a working scheduler) and safer data (managed Postgres backups).
- Older ADRs remain as historical records; where they conflict with this one, ADR-007 governs.
- **Conversation engine: hand-rolled async dispatcher** (resolves the SPEC §17 open question; supersedes ADR-001's LangGraph). Once routing moved into the System-1 `decide()` layer (ADR-008), LangGraph's conditional-edge routing became redundant, and its checkpointer would have duplicated conversation state that we instead keep in the queryable `messages` table (one source of truth for the engine, the dashboard, and persistent conversation context). Each turn is a cold reload — load lead + facts + recent messages, decide, dispatch to one handler, generate, guard, persist. Rationale in SPEC §17.1. Handlers stay plain functions, so adopting a graph later (if ever needed) is a contained refactor.
- A **typed OpenAI decision layer** supports interpretation and extraction; readiness and eligibility remain code-owned — see [ADR-008](ADR-008-system-1-decision-layer.md).
