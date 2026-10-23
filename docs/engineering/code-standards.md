# Code Standards

Agent-neutral conventions for the AdmitFlow backend (Python 3.12+, FastAPI). Match the
surrounding code; when in doubt, follow what `src/` already does.

## Project layout

```
backend/
  src/
    main.py            # FastAPI app factory (create_app) + app instance
    core/              # cross-cutting: settings, security, schemas, guardrails, tracing
    …                  # feature packages added per task
  tests/
  scripts/verify.sh    # the local quality gate
  pyproject.toml       # deps, tool config (ruff, mypy, pytest)
```

- The backend is a **virtual project** (`[tool.uv] package = false`) — a deployable app, not
  a published library. No build step, no editable self-install.
- Every package has an explicit `__init__.py` with a one-line docstring. We use explicit
  package markers, not PEP 420 namespace packages.

## Typing — `mypy --strict`, no escapes

All of `src/` type-checks under `--strict`. No `# type: ignore` without a reason comment and
a linked issue. Prefer precise types: `str | None`, `Literal[...]`, `TypedDict`/Pydantic
models over bare `dict`. Public functions get full annotations including the return type.

## Configuration — settings, not literals

Config comes from a cached `Settings` singleton (`src/core/settings.py`,
`pydantic-settings` + `@lru_cache`), loaded from env / `.env`. Rules:

- **No hard-coded secrets, URLs, or tunables.** Add a field to `Settings` and read it.
- **LLM model IDs live in settings, keyed by role** (`llm_fast_model`, `llm_fallback_model`,
  `llm_nuance_model`) — never inline in code or prose. Model versions churn monthly; the
  provider layer is pluggable, so only the config changes. See
  [../decisions/ADR-007-finalized-stack.md](../decisions/ADR-007-finalized-stack.md).
- `.env.example` documents every setting; real values go in `.env` (git-ignored).

## Async & I/O

FastAPI handlers and anything doing I/O are `async`. Never block the event loop with sync
network/DB calls or `time.sleep`. Webhooks return `200 OK` immediately and hand real work to
the TaskIQ worker — the request path stays thin.

## LLM calls

- Route every call through the provider factory / `decide()` layer — no direct SDK calls
  scattered in feature code.
- **Structured outputs are the default** for extraction: define a typed schema (Pydantic /
  JSON-schema) and let the model fill it. Do not parse free text with regex.
- Wrap calls in Langfuse tracing (see [security-and-production.md](security-and-production.md)).
- Prompt-cache the static system + institution prefix; keep the volatile part small.

## Errors

- Fail loud and specific. Raise typed exceptions; don't swallow with bare `except:`.
- Validate all external input (webhook payloads, form data) with Pydantic at the boundary.
- User-facing bot replies never leak stack traces or internal IDs — the output guardrail is
  the last line, but code shouldn't rely on it to hide sloppiness.

## Logging & observability

- Structured logs, no `print`. Never log secrets, tokens, or raw PII — log a reference
  (lead id, tenant id), not the value.
- LLM work is traced in Langfuse; errors go to Sentry (see production doc).

## Dependencies

- Managed by `uv`; `uv.lock` **is** committed. Add with `uv add <pkg>` / `uv add --dev <pkg>`.
- Pin meaningfully (`>=` floors for libs we track; the lock pins exact resolved versions).
- Vet new deps: actively maintained, sane license, no typosquat lookalikes. Prefer the
  standard choice for the ecosystem over a novel one.

## Formatting

`ruff format` (line length 100) is the arbiter — don't hand-format. `ruff check` lint
selection is `E, F, I, UP, B, ASYNC` (see `pyproject.toml`). Run both via `verify.sh`.

## Simplicity

Solve the task, not hypothetical futures. No speculative abstraction, no dead config, no
"might need it later." Guard clauses over deep nesting; small functions; names that say what
they do. When code gets tangled, the `/code-simplify` workflow exists — use it, keeping
behavior identical and tests green.
