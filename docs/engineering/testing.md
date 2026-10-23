# Testing

Agent-neutral. The goal is confidence per unit of effort — not coverage theater.

## Philosophy — pragmatic TDD

We are **test-first where it counts, test-after where it doesn't, and never untested.**

- **Test-first (RED → GREEN → REFACTOR)** for logic-heavy or risky code:
  - the `decide()` / System-1 decision layer (routing, readiness, escalation, guardrail triage)
  - the three-layer guardrails (input sanitize, RAG sanitize, output validate)
  - qualification-rule evaluation and discount-code verification
  - payments (Razorpay link creation, HMAC webhook, replay protection)
  - anything with money, PII, or tenant-scoping in the path
- **Test-after** is acceptable for thin glue: trivial CRUD, wiring, config plumbing.
- **Nothing merges untested.** New behavior ships with the tests that prove it.

## The two patterns

**New behavior:**
1. Write a test describing the expected behavior. Run it — it must **fail** (RED).
2. Write the minimum code to pass (GREEN).
3. Refactor with tests green.

**Bug fix (Prove-It):**
1. Write a test that reproduces the bug. Confirm it **fails** — this proves the bug is real
   and the test actually exercises it.
2. Fix the code. Confirm the test passes.
3. Run the full suite for regressions.

## Test layout

```
backend/
  src/…
  tests/
    test_*.py           # unit + fast integration (default)
    integration/        # tests that need real Postgres/Redis (added when Task 2+ lands)
```

Tests import from `src` (pytest is configured with `pythonpath = ["."]`). Name tests for the
behavior they assert (`test_output_guardrail_blocks_unlisted_fee`), not the function name.

## Unit vs integration

- **Unit** (the majority): pure logic, fast, no network or DB. Mock the boundaries — the
  `decide()` backend (Gemini), WhatsApp send, Razorpay, external HTTP. Assert on decisions
  and outputs, not on prompt strings.
- **Integration**: exercise real Postgres (with pgvector) and Redis, because SQL, migrations,
  vector search, the mutex, and dedup can't be trusted against mocks. Bring them up with
  docker-compose (see [security-and-production.md](security-and-production.md) /
  `docker-compose.yml` when it lands) or testcontainers. Integration tests gate any change
  that touches the schema, the engine dispatcher, RAG retrieval, or payments — see the tier
  table in [quality-gates.md](quality-gates.md).

## LLM and decision-layer tests

LLM calls are non-deterministic and cost money — **never** hit a live model in the test
suite. Test the layer around them:

- Mock `decide()` / the LLM factory to return fixed structured outputs, then assert the
  engine routes/acts correctly.
- Guardrails: feed known-bad inputs (injection, abuse, hallucinated fees) and assert they're
  blocked; feed known-good and assert they pass.
- Structured extraction: assert we parse the typed schema, not free text.

## Running tests

From `backend/`:

```bash
uv run pytest                     # whole suite (quiet, per pyproject addopts)
uv run pytest tests/test_health.py    # one file
uv run pytest -k guardrail -v     # by keyword
uv run pytest -x                  # stop at first failure while iterating
```

The full gate (lint + format + types + tests) is `bash scripts/verify.sh`.

## Coverage

We don't chase a single global number. The bar is: **every branch in the risk-heavy modules
above is exercised**, and every bug fix leaves behind a regression test. When integration
infra lands, add a coverage floor for `src/` in CI and raise it deliberately, never by
loosening tests.
