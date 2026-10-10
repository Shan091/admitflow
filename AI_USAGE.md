# AI usage

Update this file as work happens. Record the task, AI assistance, human review, checks actually
run, and any corrections. Do not paste full chat transcripts or claim unperformed checks.

## 2026-10-10 — project scaffold and demo slice

- **Task:** Create the hackathon project scaffold and first Telegram/qualification/RAG slice.
- **Assistance:** Codex drafted the project structure, Python implementation, tests, documentation,
  and CI workflow. The human still needs to review the behavior and demo content before submission.
- **Checks:** `uv sync --locked --python 3.12`, `uv lock --check --python 3.12`,
  `bash scripts/verify.sh` (24 passed; Ruff, formatting, and strict mypy passed), and
  `git diff --check` passed. No live network APIs were called because credentials were not configured.
- **Corrections:** Tests exposed a malformed SQLite upsert and a mismatched dashboard assertion;
  both were fixed. Strict mypy prompted explicit PTB typing and safe callback message narrowing.
  Review also added model-scoped vector filtering, fail-closed search errors, and immediate
  ineligibility when Grade 12 is incomplete.
