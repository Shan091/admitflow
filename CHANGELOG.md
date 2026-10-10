# Changelog

## 2026-10-11 — consent-gated adaptive text discovery

- **Change:** Expanded the fictional seed catalog to 28 complete sample offerings across five
  fields and four levels. `/start` now discloses OpenAI processing and requires an explicit choice;
  typed discovery remains button-only after decline/opt-out. Consented free text uses a stateless
  structured extraction of the current message and allowlisted catalog vocabulary; code validates
  facts, preserves speaker attribution, selects the next response, and ranks catalog matches. Added
  direct known-course entry, interest accumulation/correction, safe extraction-failure fallback,
  and offline schema/flow tests.
- **Why:** Let students start from their own words without making recommendations or eligibility
  decisions model-owned, and make the AI data boundary visible before use.
- **Validation:** `bash scripts/verify.sh` passed with 71 tests (Ruff, format, strict mypy, pytest);
  `git diff --check` passed. Tests use fake API responses and temporary SQLite. No live API request
  was made by the tests. A separate live smoke test with seven synthetic prompts checked English,
  Hindi, Malayalam, and Hinglish activity extraction, exact known-course lookup, out-of-catalog
  medicine, and an instruction-injection attempt. All returned the expected bounded catalog output
  (12,308 input and 992 output tokens total). Pushed to `main` as
  `0e45565fe4dbbd434435bf264bc8ce8e8d86a7b8`; matching GitHub Actions run
  [38087034051](https://github.com/Shan091/admitflow/actions/runs/38087034051) passed.
- **Limitations:** No fluent-speaker language review, broad adversarial extraction evaluation,
  real-catalog validation, non-undergraduate eligibility engine, retention expiry, or production
  privacy/legal review is included in this slice.

## 2026-10-11 — adaptive course discovery first slice

- **Time:** 02:23 IST
- **Change:** Added a fictional catalog spanning the requested education levels and fields; additive
  SQLite migrations for course attributes, attributed discovery facts, lifecycle/readiness, language,
  and handoff state; four Telegram entry paths; field/level/activity prompts with skip/back/pause/
  resume; explainable catalog matching; parent/student preference attribution; dashboard handoffs;
  staff-mediated individual deletion; and explicit student consent before creating a test payment
  link. Corrected payment confirmation copy so it no longer promises an unconfigured staff contact.
- **Why:** Turn the existing course-first hackathon bot into the first working slice of the agreed
  interest-led admissions guide while keeping eligibility, prices, and course facts code-owned.
- **Files:** `src/admitflow/`, `tests/`, `README.md`, `SPEC.md`, `SUBMISSION.md`, `docs/DECISIONS.md`,
  `tasks/features/adaptive-course-discovery.md`, and `tasks/todo.md`.
- **Validation:** `bash scripts/verify.sh` passed with 63 tests (Ruff, format, strict mypy, pytest);
  `git diff --check` passed. Tests use temporary SQLite files and fake APIs; no paid or external API
  request was made. Pushed to `main` as
  `53e78e44809c8c9714d70c13b08c07582bacfdad`; GitHub Actions CI run
  [38085663111](https://github.com/Shan091/admitflow/actions/runs/38085663111) passed for that SHA.
- **Limitations:** Most user-facing replies are still English despite saving a language preference;
  non-undergraduate eligibility is sent to staff for confirmation; automatic admissions-cycle
  expiry is not implemented and its exact interval remains open. The fictional catalog is not a real
  institution offer. No counsellor contact or response-time SLA is configured.

## 2026-10-11 — staff demo-data reset

- **Change:** Added a staff-only dashboard reset form requiring the exact phrase
  `DELETE ALL DEMO DATA` and a CSRF token bound to the staff session. It deletes local leads,
  conversations, payments, and Razorpay webhook-event history while retaining fictional course and
  FAQ seeds. The dashboard reports success or explains that no records were deleted.
- **Why:** Allow staff to reset the hackathon demo before another end-to-end rehearsal without
  losing the content the bot needs.
- **Files:** `src/admitflow/`, `tests/test_app.py`, `README.md`, `SPEC.md`, `docs/DECISIONS.md`,
  `tasks/`, `AI_USAGE.md`, and `SUBMISSION.md`.
- **Validation:** `bash scripts/verify.sh` passed Ruff lint/format checks, strict mypy, and 42
  pytest tests. `git diff --check` passed. Automated reset checks use temporary SQLite data.
- **Limitations:** Reset affects this app's database only; it cannot delete provider-side Telegram
  or Razorpay records. It is permanent and cannot be undone.
- **Push/CI:** Pushed to `main` as `77de766e1056c187c982344978fe7200fd2eb742`; GitHub Actions CI
  run [38082903212](https://github.com/Shan091/admitflow/actions/runs/38082903212) passed.

## 2026-10-11 — Telegram payment confirmation and status lookup

- **Change:** After a signature-verified Razorpay paid event is applied, send one Telegram
  confirmation describing the next step. Add a student-facing status query backed by the stored
  payment state, and link a Razorpay Payment Link back to its Telegram user for notification.
- **Why:** Students need confirmation after checkout and a truthful next action. The demo does not
  automatically provision course access, so the message says an admissions team member will reach
  out with instructions without implying access is already enabled.
- **Files:** `src/admitflow/`, `tests/`, `README.md`, `SPEC.md`, `docs/DECISIONS.md`, `tasks/`, and
  `AI_USAGE.md`.
- **Validation:** `bash scripts/verify.sh` passed: Ruff lint and format checks, strict mypy, and
  41 pytest tests. `git diff --check` passed. Tests use a fake Telegram bot and local SQLite; no
  live payment or notification was triggered.
- **Limitations:** If Telegram delivery fails after payment is recorded, the webhook remains
  accepted; the student can ask the bot “Has my payment gone through?” to read the saved status.
  Course access is a staff follow-up and is not provisioned by the demo.
- **Push/CI:** Pushed to `main` as `88aca11d187040292b48675d1fe9a04594bbbcae`; GitHub Actions CI
  run [38081876118](https://github.com/Shan091/admitflow/actions/runs/38081876118) passed.

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
- **Push/CI:** Pushed to `main` as `e19bd2be7f8e401a3bfa21e9e4ddd97f01dfeedf`;
  GitHub Actions CI run `38081259866` passed:
  https://github.com/Shan091/admitflow/actions/runs/38081259866

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
