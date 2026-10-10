# Changelog

## 2026-10-11 — live calibration of seeded FAQ retrieval

- **Time:** 01:14 IST
- **Change:** Added a fixed set of curated FAQ search phrasings; embeddings now index question
  text separately from answers and use a versioned cache key. Calibrated the minimum cosine score
  to `0.58` and kept the top-result margin at `0.05`. Added explicit safe handling for tuition/
  hostel charges and refund questions rather than misreporting the application fee.
- **Why:** Live checks showed the old `0.72` threshold refused even exact seeded questions. A
  question-only embedding representation plus curated aliases improved useful matches while
  unsupported fee/refund topics remained outside the RAG path.
- **Files:** `src/admitflow/`, `src/admitflow/seed/data/faqs.json`, `scripts/evaluate_faq_retrieval.py`,
  `tests/`, `README.md`, `SPEC.md`, `docs/DECISIONS.md`, `tasks/`, and `AI_USAGE.md`.
- **Validation:** Live `uv run python scripts/evaluate_faq_retrieval.py` passed all 27 synthetic
  cases (15 expected source matches, 12 expected abstentions); the lowest accepted score was
  `0.648` and the highest abstention score was `0.491`. The final 27-query API batch used 207 input
  tokens; earlier calibration probes were also synthetic. `bash scripts/verify.sh` passed Ruff,
  formatting, strict mypy, and all 37 tests. The local staff dashboard showed RAG ready and the
  existing test payment as paid; local/public health returned 200. Telegram reports the correct
  webhook path, zero pending updates, and no delivery error.
- **Limitations:** This is a small hand-written calibration set, not a production quality
  guarantee. Thresholds remain provisional and should be checked against actual demo phrasing.
- **Push/CI:** Pending commit and matching GitHub Actions result.

## 2026-10-11 — Telegram webhook transport

- **Change:** Replaced Telegram long-polling with a FastAPI webhook endpoint protected by
  `X-Telegram-Bot-Api-Secret-Token`, added `TELEGRAM_WEBHOOK_SECRET`, a helper to register/check or
  remove the Telegram webhook, and setup documentation.
- **Why:** The demo will receive Telegram updates through the HTTPS tunnel alongside its other
  webhook integration.
- **Files:** `src/admitflow/`, `scripts/manage_telegram_webhook.py`, `tests/test_app.py`, `.env.example`,
  `README.md`, `SPEC.md`, `docs/DECISIONS.md`, `tasks/`, and `AGENTS.md`.
- **Validation:** `bash scripts/verify.sh` passed (Ruff, formatting, strict mypy, and 35 tests);
  `git diff --check` passed. The existing public tunnel returned HTTP 200 for `/health`.
- **Limitations:** No Telegram bot token is configured in `.env`, so I could not register a live
  webhook or run a live bot walkthrough. A local webhook secret was generated and stored in the
  ignored `.env`; it was not added to Git. Do not claim Telegram delivery is live until registration
  and a real `/start` walkthrough succeed.

## 2026-10-11 — accept the supplied ngrok webhook path

- **Time:** 00:14 IST
- **Change:** Added `/api/v1/webhooks/razorpay` as an alias for the existing signed Razorpay
  webhook handler, matching the user's ngrok URL; documented both accepted paths.
- **Why:** The application had no `/api/v1` prefix or proxy rewrite, so the supplied endpoint path
  would otherwise miss the registered route.
- **Files:** `src/admitflow/dashboard/payment_routes.py`, `tests/test_app.py`, and `README.md`.
- **Validation:** `bash scripts/verify.sh` passed with 32 tests; `git diff --check` passed. No
  live webhook or API request was made. GitHub Actions passed for pushed SHA
  `182c27689544f21a6536146db870a553b03e14a5`:
  https://github.com/Shan091/admitflow/actions/runs/38076997956
- **Limitations:** Razorpay webhook signature verification still requires the webhook secret saved
  in Razorpay Dashboard and configured as `RAZORPAY_WEBHOOK_SECRET` locally.

## 2026-10-11 — verified payment handoff and failure handling

- **Time:** 00:04 IST
- **Change:** Added tests covering the Telegram delivery of a generated Razorpay test link and the
  behavior when Razorpay link creation fails; qualification remains successful in that case.
- **Why:** Verify the full student-facing handoff and ensure provider failures are visible without
  changing the code-computed eligibility result.
- **Files:** `tests/test_telegram.py`, `tests/test_payments.py`.
- **Validation:** `bash scripts/verify.sh` passed with Ruff, formatting, strict mypy, and 32 pytest
  tests; `git diff --check` passed. No live API call was made. GitHub Actions passed for pushed SHA
  `5c04b5982e7d97d0fccf75236605b9e466f8c9e0`:
  https://github.com/Shan091/admitflow/actions/runs/38076330518
- **Limitations:** Razorpay test credentials and a public webhook URL are still needed to rehearse
  the payment flow end to end.

## 2026-10-11 — staff login and Razorpay test-mode payments

- **Time:** 00:02 IST
- **Change:** Added an environment-configured staff login with signed, expiring HTTP-only sessions;
  protected lead pages; Razorpay test-mode Payment Links created after successful qualification;
  payment persistence and a signature-verified, idempotent webhook; and payment status on staff
  lead details.
- **Why:** Include the requested staff access and application payment demo without trusting client
  prices or browser redirects for payment status.
- **Files:** `src/admitflow/`, `tests/test_app.py`, `tests/test_payments.py`, `.env.example`,
  `README.md`, `SPEC.md`, `SUBMISSION.md`, `docs/DECISIONS.md`, `tasks/`, `AI_USAGE.md`,
  `pyproject.toml`, and `uv.lock`.
- **Validation:** `uv sync --locked --python 3.12` passed; latest `bash scripts/verify.sh` passed
  (Ruff, formatting, strict mypy, and 32 pytest tests); `git diff --check` passed. No live
  Razorpay, Telegram, or OpenAI request was made.
- **Limitations:** Payment links require all three Razorpay test credentials and a public webhook
  URL for status updates; payment creation cannot be retried automatically after an ambiguous API
  failure. Staff login is one local demo account, not production identity management.

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
