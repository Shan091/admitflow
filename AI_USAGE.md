# AI usage

Update this file as work happens. Record the task, AI assistance, human review, checks actually
run, and any corrections. Do not paste full chat transcripts or claim unperformed checks.

## 2026-10-11 — staff login and test-mode payments

- **Task:** Implement environment-configured staff dashboard login and Razorpay test-mode
  application Payment Links with verified payment status.
- **Assistance:** Codex updated the scope/decision/task records, implemented the signed staff
  session, payment persistence/API/webhook path, Telegram checkout handoff, dashboard status, and
  fake-backed tests. Human review is still needed for demo credentials, Razorpay setup, and the
  final payment experience.
- **Checks:** `uv sync --locked --python 3.12` passed; `bash scripts/verify.sh` passed (Ruff,
  formatting, strict mypy, and 32 pytest tests); `git diff --check` passed. No live Razorpay,
  Telegram, or OpenAI API was called.
- **Corrections:** TestClient follows redirects unless explicitly disabled; auth tests were updated
  to inspect actual 303 responses. The payment adapter rejects non-test `rzp_live_` key IDs.

## 2026-10-10 — project scaffold and demo slice

- **Task:** Create the hackathon project scaffold and first Telegram/qualification/RAG slice.
- **Assistance:** Codex drafted the project structure, Python implementation, tests, documentation,
  and CI workflow. The human still needs to review the behavior and demo content before submission.
- **Checks:** `uv sync --locked --python 3.12`, `uv lock --check --python 3.12`,
  latest `bash scripts/verify.sh` (25 passed; Ruff, formatting, and strict mypy passed),
  local Uvicorn `/health` and dashboard returned `200`, and `git diff --check` passed. GitHub
  Actions passed on build commit `41c0b4cd389ce2457e887b26d415a29296e90bec` with 25 tests. No live
  network APIs were called because credentials were not configured.
- **Corrections:** Tests exposed a malformed SQLite upsert and a mismatched dashboard assertion;
  both were fixed. Strict mypy prompted explicit PTB typing and safe callback message narrowing.
  Review also added model-scoped vector filtering, fail-closed search errors, and immediate
  ineligibility when Grade 12 is incomplete. A later test verifies environment-backed settings.
