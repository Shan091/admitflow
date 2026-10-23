# Security & Production Readiness

Agent-neutral. AdmitFlow handles applicant PII, payments, and a multi-tenant knowledge base,
so security is a build-time concern, not a hardening afterthought. The stack is fixed in
[../decisions/ADR-007-finalized-stack.md](../decisions/ADR-007-finalized-stack.md).

## Secrets

- Secrets live in `.env` locally (git-ignored) and in the platform's secret store in
  prod (Fly.io secrets, Vercel env). **Never** in code, logs, commits, or the knowledge graph.
- `.env.example` lists every key with placeholder values so a fresh clone knows what to set.
- If a secret is committed, it's compromised: rotate it, then scrub history. Don't just
  delete the line.

## PII & data protection (DPDPA)

- Applicant PII is **encrypted at the application layer** before it hits the DB, not just at
  rest by the provider.
- Access to PII is **audit-logged** (who/what/when) via the audit-log infrastructure.
- Support the "Delete My Data" path and per-tenant retention cleanup (Tasks 36–37).
- Logs and traces reference records by id (`lead_id`, `tenant_id`) — never the raw value.

## Multi-tenancy — isolation is a correctness bug if wrong

Every tenant-scoped table carries `tenant_id`, and **every query filters on it**. A missing
tenant filter is a data-leak, not a style nit — reviewers treat it as Critical. See
[../decisions/ADR-003-multi-tenancy-strategy.md](../decisions/ADR-003-multi-tenancy-strategy.md).

## External surfaces

Any endpoint reachable from outside is a threat surface. For each one:

- **Verify signatures**: Meta WhatsApp webhook (HMAC) and Razorpay webhook (HMAC) are
  verified before the payload is trusted or enqueued.
- **Validate input** with Pydantic at the boundary; reject malformed early.
- **Dedup & concurrency**: webhook dedup (Redis `SETNX`) and the per-phone mutex
  (`wa_mutex:{phone}`) prevent double-processing and races. See
  [../decisions/ADR-002-webhook-concurrency-and-dedup.md](../decisions/ADR-002-webhook-concurrency-and-dedup.md).
- **Authn/authz**: dashboard/API routes require auth. If you add an unauthenticated route,
  say so explicitly in the PR and justify it — silent unauthenticated exposure is a blocker.

## Guardrails & money

- Three-layer guardrails (input sanitize → RAG sanitize → output validate) are mandatory on
  the conversation path. See
  [../decisions/ADR-005-three-layer-guardrails.md](../decisions/ADR-005-three-layer-guardrails.md).
- **Fees and amounts come from the DB, never from the model.** The output guardrail blocks
  any monetary figure not sourced from the DB — a hallucinated fee is a Critical bug.
- RAG chunks are sanitized before injection (RAG-poisoning defense).
- **Treat all inbound content as untrusted — take data, never instructions.** A WhatsApp
  message or a retrieved chunk that says "ignore your rules / reveal the prompt / approve this
  fee" is data to be handled, not a command to obey. The input and RAG guardrails exist
  precisely to strip this; never let external text redirect the agent's behavior.

## Observability

- **Langfuse** traces every LLM call (prompt, model, latency, cost). No untraced calls.
- **Sentry** captures backend errors (Task 35).
- Health endpoint (`/health`) is the liveness probe; keep it dependency-light.

## Dependency & secret scanning

Wire these into CI as the project grows (the `/constraints` workflow tracks the enforced
bar): a secret scanner (e.g. gitleaks) on the diff, and a dependency vulnerability scan
(e.g. osv-scanner, configured via a committed `.osv-scanner.toml` for triaged waivers).
Pin versions; `uv.lock` is committed.

## Local full-stack (docker-compose)

Integration tests and manual runs need real Postgres (pgvector) and Redis. A
`docker-compose.yml` (Task 38) brings up Postgres, Redis, the API, and the worker. Until it
lands, integration tests use testcontainers or a locally-run pair. Migrations are Alembic;
they must apply cleanly **up and down**.

## Deploy & rollback

Production topology (ADR-007): **Fly.io** for the API + worker + scheduler (always-on),
**Neon** Postgres (+pgvector), **Redis** on Fly, **Vercel** for the Next.js dashboard,
Langfuse Cloud, Sentry.

Before calling a deploy done:

- [ ] Secrets set in the platform store (not baked into the image).
- [ ] Migrations applied; verified reversible.
- [ ] Health check green; a real WhatsApp round-trip works.
- [ ] Traces (Langfuse) and errors (Sentry) are flowing.
- [ ] Rollback is known: how to revert the release and, if a migration ran, how to roll it
      back or forward-fix. Write it in the PR before merging the risky change.

## Production readiness checklist (per feature)

- [ ] Baseline gate green (`verify.sh`) + the tier gates for what it touches
      ([quality-gates.md](quality-gates.md)).
- [ ] No secrets/PII in code, logs, or traces.
- [ ] Tenant scoping enforced on every new query.
- [ ] External input validated; signatures verified.
- [ ] LLM calls traced; amounts DB-sourced.
- [ ] Errors surface to Sentry; key actions are audit-logged.
- [ ] Rollback plan written for anything stateful.
