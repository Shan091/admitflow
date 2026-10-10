# Changelog

## 2026-10-10 — implementation foundation and first demo slice

- **Time:** 23:49 IST
- **Change:** Added the runnable FastAPI/SQLite project, fictional course and FAQ seeds, Telegram
  qualification flow, local lead dashboard, OpenAI Decisions/embeddings adapter, model-scoped
  NumPy cosine retrieval, task briefs/checklist, README/spec/decision records, lockfile, CI, and
  automated tests.
- **Why:** Implement the agreed hackathon demo in small, testable layers, with qualification and
  fee answers controlled by structured code and uncertain FAQ retrieval failing closed.
- **Files:** `src/admitflow/`, `tests/`, `tasks/`, `docs/`, `README.md`, `SPEC.md`, `AGENTS.md`,
  `AI_USAGE.md`, `SUBMISSION.md`, `pyproject.toml`, `uv.lock`, `scripts/`, and `.github/workflows/ci.yml`.
- **Validation:** `uv sync --locked --python 3.12` passed; `uv lock --check --python 3.12` passed;
  `bash scripts/verify.sh` passed (Ruff lint, Ruff format check, strict mypy, and 24 pytest tests);
  `git diff --check` passed. Python 3.12.5, uv 0.11.2. No live OpenAI or Telegram request was
  made; credentials were not configured in this environment.
- **Limitations:** Seed data is fictional; no live bot or OpenAI integration smoke test has been
  run, the FAQ corpus is fixed, the dashboard is local and unauthenticated, local chat identifiers
  and messages have no retention controls. Similarity thresholds remain provisional until live
  examples are calibrated.

## 2026-10-10 — smoke check and verified task status

- **Time:** 23:54 IST
- **Change:** Added environment-setting coverage, marked locally verified core/Telegram/vector
  tasks complete, and kept live Telegram/OpenAI setup and threshold calibration open.
- **Why:** Make the task board reflect evidence already gathered while separating deterministic
  local checks from real API and demo checks.
- **Files:** `tests/test_app.py`, `tasks/todo.md`, and `tasks/features/`.
- **Validation:** Latest local `bash scripts/verify.sh` passed with 25 pytest tests; locked
  dependencies and `git diff --check` passed. A local Uvicorn process returned `GET /health`
  `200` with `{"status":"ok"}` and dashboard `GET /` `200`. GitHub Actions passed on implementation
  SHA `634579532c8b77ae9f0f8c6da86cb137f9f095d8` (24 tests) and follow-up build SHA
  `41c0b4cd389ce2457e887b26d415a29296e90bec` (25 tests).
- **Limitations:** Live Telegram and OpenAI calls remain untested because credentials are not
  configured; threshold calibration, real demo rehearsal, and final participant details remain open.

## 2026-10-10

- **Time:** 23:19 IST
- **Change:** Added `tasks/todo.md` as the live checklist for the six-hour hackathon implementation plan.
- **Why:** Make milestone progress visible and define when a task can be marked complete.
- **Validation:** Read back the created checklist and confirmed the milestones and completion criteria are present. No application tests were run; there is no application code yet.
- **Limitations:** All implementation tasks remain unchecked. The checklist is a plan, not evidence that features are implemented.
