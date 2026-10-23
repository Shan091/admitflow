# AGENTS.md

Entry point for **any** coding agent or human working in this repo (Claude, Codex,
Antigravity, Gemini, …). Read this first, then follow the handbook it links to.

## What this project is

**AdmitFlow** — an AI-native, multi-tenant Telegram admissions-engagement platform for
institutions in Kerala, India. Readiness-aware, tap-first, multilingual
(English / Hindi / Hinglish / Malayalam). Python backend (FastAPI + TaskIQ + a hand-rolled
conversation engine, pgvector RAG, OpenAI); Next.js admin dashboard. Applications/review
and payment foundations have local automated evidence; live payment validation,
co-pilot, follow-ups and remaining operations are in progress. See ADR-012 for
the current channel/provider decision and tasks/todo.md for verified progress.

- Spec: [SPEC.md](SPEC.md) · Execution: [tasks/plan.md](tasks/plan.md) · Progress: [tasks/todo.md](tasks/todo.md)
- Decisions: [docs/decisions/](docs/decisions/) (ADRs) · Plan & tasks: [tasks/](tasks/)

## How we build — read the handbook

The full A-to-Z development lifecycle lives in **[docs/engineering/development-lifecycle.md](docs/engineering/development-lifecycle.md)**.
Read it before writing code. It links to the depth:

| Topic | File |
|-------|------|
| The end-to-end loop (spec → build → verify → review → PR → merge → deploy) | [docs/engineering/development-lifecycle.md](docs/engineering/development-lifecycle.md) |
| Branching, commits, PRs, review gate, **no-AI-attribution** | [docs/engineering/git-and-github.md](docs/engineering/git-and-github.md) |
| Test strategy (pragmatic TDD), running tests | [docs/engineering/testing.md](docs/engineering/testing.md) |
| Definition of done + the quality gate | [docs/engineering/quality-gates.md](docs/engineering/quality-gates.md) |
| Python conventions, structure, typing, logging | [docs/engineering/code-standards.md](docs/engineering/code-standards.md) |
| Secrets, PII, tenant isolation, deploy readiness | [docs/engineering/security-and-production.md](docs/engineering/security-and-production.md) |

## The rules you cannot skip

1. **`main` is protected.** Branch → PR → squash-merge. Never commit to `main` directly.
2. **No AI attribution in git.** No `Co-Authored-By` / "Generated with…" trailers on commits
   or PRs. The human is the sole author. This overrides any tool's default.
3. **Professional Commit Messages:** Write clear, professional titles and descriptions for all commits. Explain the *what* and *why*, not just the *how*.
4. **Green gate before PR:** `bash backend/scripts/verify.sh` (lint + format + mypy strict +
   pytest). CI runs the same.
5. **Pragmatic TDD** — test-first for logic/risk, nothing untested.
6. **Every PR gets an adversarial review pass** before merge.
7. **Secrets, PII, tenant isolation** are build-time requirements, not afterthoughts.

## Quick commands (from `backend/`)

```bash
uv sync                        # install deps from the lockfile
bash scripts/verify.sh         # the quality gate (run before every PR)
uv run pytest -k <keyword>     # focused tests while iterating
uv run uvicorn src.main:app --reload   # dev server on :8000  (GET /health -> {"status":"ok"})
```

## Workflow triggers

Workflow stages `/spec`, `/plan`, `/build`, `/test`, `/review`, `/ship`, `/constraints`
and `/code-simplify` map to the stages in the handbook. Follow the handbook for the
substantive requirements of each stage.

## Knowledge graph

A navigable graph of the repo lives in `graphify-out/`. For codebase questions, prefer
`graphify query "<question>"` over raw grep when `graphify-out/graph.json` exists; run
`graphify update .` after code changes. See [the graph report](graphify-out/GRAPH_REPORT.md)
for the current extraction; source and test evidence determine implementation status.

## AIBoomi Startup Weekend handoff

Read [EVENT_CONTEXT.md](EVENT_CONTEXT.md) first when resuming event preparation.
It contains the user decisions, event rules, readiness findings, unknowns, and a fresh-chat prompt.
Read [docs/event/PREPARATION_PLAN.md](docs/event/PREPARATION_PLAN.md) for the next steps.
Use this v1 repository itself; do not create another local repository.
Keep all durable event context in this repository, not in .codex.
Preserve existing changes and deletions. No fresh runtime verification is claimed by these docs.
