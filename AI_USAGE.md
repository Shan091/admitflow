# AI usage

Update this file as work happens. Record the task, AI assistance, human review, checks actually
run, and any corrections. Do not paste full chat transcripts or claim unperformed checks.

## 2026-10-11 — consent-gated conversational intake

- **Task:** Add a broader fictional catalog and let students describe interests or known courses
  naturally, while preserving the institution-only and student-first boundaries.
- **Assistance:** Codex wired an explicit OpenAI consent/opt-out, a structured stateless extraction
  request using only the current message and allowlisted fictional catalog values, deterministic
  fact persistence and catalog matching, and test coverage for refusals, invalid values, course
  lookup, corrections, and failure behavior. The human explicitly approved this processing only
  with affirmative consent and a no-real-student-data warning.
- **Checks:** `bash scripts/verify.sh` passed with 71 tests and `git diff --check` passed locally.
  Tests use synthetic text, fake APIs, and temporary SQLite. A separate live OpenAI smoke used
  seven synthetic prompts across English, Hindi, Malayalam, and Hinglish, plus known-course,
  out-of-catalog, and instruction-injection cases. It returned the expected bounded catalog output;
  usage was 12,308 input and 992 output tokens total. No real student text or other external API was
  used.
- **Human review/limitations:** The UI disclosure warns that messages are stored locally, are sent
  to OpenAI only after consent, and must be fictional. Translations, minors/guardian privacy review,
  adversarial multilingual evaluations, and production privacy review remain outstanding.
- **Push/CI:** Pushed as `0e45565fe4dbbd434435bf264bc8ce8e8d86a7b8`; matching GitHub Actions CI run
  [38087034051](https://github.com/Shan091/admitflow/actions/runs/38087034051) passed.

## 2026-10-11 — interest-led discovery first slice

- **Task:** Extend the Telegram hackathon demo from a fixed course-first opening to an adaptive,
  catalog-only discovery path based on the user's settled product choices.
- **Assistance:** Codex reviewed the attached Claude plan, the v1 product notes, local build rules,
  and organizer instructions; added fictional course metadata and migrations, deterministic matching,
  persisted discovery paths/facts, Telegram choices and resume flow, parent/student attribution,
  staff handoffs and individual deletion, payment-consent gating, tests, and docs. Codex also
  corrected payment copy that had promised an unconfigured live follow-up. No v1 implementation
  code was copied.
- **Checks:** `bash scripts/verify.sh` passed (Ruff lint, format, strict mypy, and 63 pytest tests);
  `git diff --check` passed. Automated tests used fake integrations and temporary SQLite data. No
  live OpenAI, Telegram, Razorpay, or other network request was made. The implementation was pushed
  as `53e78e44809c8c9714d70c13b08c07582bacfdad`; matching GitHub Actions run
  [38085663111](https://github.com/Shan091/admitflow/actions/runs/38085663111) passed.
- **Human direction/review:** The human selected conversation-only discovery, student-first
  parent handling, four language preferences, a fictional broad Kerala course catalog, and no
  invented staff contact/response time. Human review of translated copy and the final bot flow
  remains needed.
- **Corrections/limitations:** Full language coverage, verified course-specific eligibility for
  non-undergraduate offerings, and configured retention expiry are not complete. Do not call the
  product fully localized or production-ready.

## 2026-10-11 — staff demo-data reset

- **Task:** Add a deliberate staff-only action to clear demo/student records so the Telegram and
  payment flow can be reset for another rehearsal.
- **Assistance:** Codex traced staff-session and SQLite ownership, added a reset route/form with a
  session-bound CSRF token and typed confirmation, and covered clearing records while retaining
  the fictional catalog and FAQs.
- **Checks:** Targeted `uv run pytest tests/test_app.py tests/test_repository.py -q` passed 12
  tests. `bash scripts/verify.sh` passed Ruff lint/formatting, strict mypy, and 42 tests;
  `git diff --check` passed. Reset tests used a temporary SQLite database.
- **Human review:** The dashboard explains that app-local records are cleared but Telegram and
  Razorpay provider-side records are not. The reset cannot be undone.

## 2026-10-11 — Telegram payment confirmation and status lookup

- **Task:** Notify a student after Razorpay confirms a test payment and let them query their
  persisted payment status.
- **Assistance:** Codex traced the signed webhook flow, added the one-time Telegram confirmation,
  read-only payment status response, repository lookup, tests, and documentation. The confirmation
  says an admissions team member will reach out with course access instructions; it clarifies that
  the demo does not enable access automatically.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/formatting, strict mypy, and 41 tests;
  `git diff --check` passed. Tests used a fake Telegram bot and local database. No live API or
  notification was triggered.
- **Human direction:** The user requested a success message with a clear staff follow-up/course
  access next step. Copy says an admissions team member will reach out, while clarifying that the
  demo does not enable access automatically. Delivery is best-effort; if it fails, the student can
  ask “Has my payment gone through?” in Telegram and read the persisted status.

## 2026-10-11 — live FAQ retrieval calibration

- **Task:** Improve the fixed seeded FAQ retrieval using live OpenAI embeddings, calibrate the
  abstention threshold, and add safe responses for unsupported fee categories and refunds.
- **Assistance:** Codex reviewed the seeded corpus, added curated search phrasing fixtures and a
  repeatable evaluator, versioned embedding cache entries, updated retrieval thresholds and
  code-owned fee/refund policy, and documented the results. The human authorized using the
  configured OpenAI credit balance and previously confirmed the bot/payment demo paths.
- **Checks:** The live `uv run python scripts/evaluate_faq_retrieval.py` used only synthetic FAQ
  phrases and passed 27/27 (15 expected answers, 12 abstentions); the final 27-query batch used
  207 input tokens. `bash scripts/verify.sh` passed with Ruff, formatting, strict mypy, and 37
  tests. Local staff login showed FAQ retrieval ready and the test payment as paid; local and
  public health endpoints returned 200, and Telegram reported a healthy webhook. Additional
  calibration requests also used only synthetic text; the final-batch count is not a total spend
  figure.
- **Human review/follow-up:** The selected `0.58`/`0.05` thresholds are backed by a small fixed
  demo set, not broad user testing. Confirm common demo phrasing in the live bot before
  submission; this is not a general FAQ ingestion system.

## 2026-10-11 — Telegram webhook transport

- **Task:** Replace Telegram polling with secret-validated FastAPI webhook delivery and document
  local Telegram registration.
- **Assistance:** Codex implemented the receiver, PTB queue lifecycle, environment setting,
  registration/removal helper, tests, and documentation updates. Human review is still needed for
  the bot token and the live Telegram conversation.
- **Checks:** `bash scripts/verify.sh` passed (Ruff, formatting, strict mypy, and 35 pytest tests);
  `git diff --check` passed. The existing HTTPS tunnel returned HTTP 200 for `/health`. No Telegram
  Bot API request was made because no bot token is configured.
- **Follow-up:** Add the bot token to local `.env`, restart the app, register the HTTPS webhook with
  `scripts/manage_telegram_webhook.py`, verify `getWebhookInfo`, then complete a live walkthrough.

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
- **Follow-up:** Added and verified the `/api/v1/webhooks/razorpay` route alias for the supplied
  ngrok URL; the full gate still passes with 32 tests. The Razorpay webhook secret is not yet set.

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
