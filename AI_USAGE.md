# AI usage

Update this file as work happens. Record the task, AI assistance, human review, checks actually
run, and any corrections. Do not paste full chat transcripts or claim unperformed checks.

## 2026-10-11 — unify tap field selection with adaptive guidance

- **Task:** Remove the fixed level-first tap sequence, preserve student facts during field changes,
  and isolate parent suggestions from learner state.
- **Assistance:** Codex routed student field selections through the shared guidance policy, made
  field replacement category-scoped, made level/field taps speaker-aware, and added persistence for
  resumable adaptive-signal prompts plus parent/learner regression tests.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 126 tests;
  `git diff --check` passed. Commit `dcaabdea9f7e4b2b931552212f892d2ecfb02e93` was pushed, and
  GitHub Actions `CI` run `38093609621` passed.
- **Human review:** No external facts or student outcomes were introduced; all recommendations
  remain bound to the fictional sample catalog.

## 2026-10-11 — preserve guided-exploration state on resume

- **Task:** Keep guided exploration distinct from known-field selection when pausing and resuming.
- **Assistance:** Codex traced the field-choice/resume path, found that the shared helper overwrote
  the `explore` step, and added explicit step preservation plus a turn-sequence regression test.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 124 tests;
  `git diff --check` passed. Commit `0702fe4b9e66e6e38c0be4c5b4c66eb4b8b99b88` was pushed, and
  GitHub Actions `CI` run `38093151318` passed.
- **Human review:** No claims or course facts changed; the demo remains fictional.

## 2026-10-11 — make preference corrections category-scoped

- **Task:** Preserve unaffected student/parent guidance facts while supporting corrections and
  exact withdrawals of previously saved preferences.
- **Assistance:** Codex added typed catalog-bounded retractions, category-level replacement on
  explicit correction, ambiguous-correction recovery, stale-confirmation invalidation, a routing fix
  so language corrections reach discovery, tests, and decision/feature documentation. Existing
  behavior was confirmed: processing disclosure plus opt-out, with no affirmative consent prompt.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 123 tests. No live or
  paid API calls were made. Commit `7c57d2df1e6f05a400b7690869b5706a2c35fc41` was pushed, and
  GitHub Actions `CI` run `38092799672` passed.
- **Human review:** The user clarified that no consent session or user consent prompt is needed;
  the implementation keeps the processing disclosure and opt-out behavior.

## 2026-10-11 — align lifecycle stages with payment events

- **Task:** Keep the v1 lifecycle projection consistent with actual persisted qualification and
  payment events; map implemented and deferred stages for the adaptive Telegram demo.
- **Assistance:** Codex updated test-mode link creation and verified webhook persistence to advance
  `payment_pending` and `under_review` respectively, and documented the lifecycle/readiness
  boundaries, pending staff handoff semantics, and stages not implemented by the hackathon demo.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 117 tests;
  `git diff --check` passed. Commit `67472c5b4fb2d6a538dfe141c663779ee93d053f` was pushed, and
  GitHub Actions `CI` run `38091855872` passed. Tests use local SQLite, fake HTTP, and signed
  synthetic webhook data; no live or paid API call was made.
- **Human review:** No new external claims were added; sample paid status remains distinct from
  admission and enrollment.

## 2026-10-11 — broaden the sample course catalog

- **Task:** Add 12 complete fictional offerings so the existing five catalog fields each contain
  eight examples, with all four agreed education levels represented.
- **Assistance:** Codex drafted sample catalog records and tests that verify completeness,
  idempotent seeding, supported language-support tags, and retrieval of each added offering from
  its explicit sample learning goal. No real institution data or student data was used.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 117 tests;
  `git diff --check` passed. Commit `c540d11c4c0c26ff3bcb6df2e3e783e05476b3b3` was pushed, and
  GitHub Actions `CI` run `38091492125` passed. No live or paid API call was made.
- **Human review:** Confirm the catalog remains fictional; the new records do not create eligibility
  rules for non-undergraduate programs, job guarantees, or regulated-program claims.

## 2026-10-11 — compare catalog-recorded language support

- **Task:** Let broad course matches surface a learner's optional language-support preference
  without treating language proficiency as a diagnosis or inventing course services.
- **Assistance:** Codex added an allowlisted support-preference field to stateless structured
  extraction, a one-question policy that shares the optional narrowing turn with study goals,
  student-attributed persistence, preference filtering/explanations, stale-confirmation handling,
  resume/skip behavior, and a no-match recovery that can reopen language. The UI distinguishes
  catalog-listed teaching medium from discussion support.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 105 tests;
  `git diff --check` passed. All API tests are fake and all course/dialogue data are fictional. No
  live OpenAI request, applicant data, or API credits were used. Feature commit
  `91005085048517c4c0ea86b8d1f520d3606571dc` is pushed and its GitHub Actions run `38091066242`
  passed. Follow-up parent-attribution test commit `aed4f92f65eab558f3c06ef3fc42e5694e9a0f72` is
  pushed and its 105-test GitHub Actions run `38091126893` passed.
- **Human review:** Language support is represented only by sample catalog labels; it does not
  establish a student's proficiency or any actual accommodation. No consent session was added;
  OpenAI processing remains disclosed and on by default with the existing opt-out.

## 2026-10-11 — optional study-goal signal for broad course matches

- **Task:** Make course exploration adapt when several offerings match, without expanding into job
  predictions or requiring every learner to answer the same prompts.
- **Assistance:** Codex added sample course-owned goal tags, an additive database migration,
  current-message structured extraction with allowlist validation, a one-time optional goal prompt
  for broad matches, skip/resume handling, and goal-aware ranking/explanations. Corrections update
  the confirmation fingerprint. OpenAI processing remains enabled by default, with the existing
  user-controlled opt-out.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 96 tests;
  `git diff --check` passed. All test inputs were fictional and OpenAI calls were mocked. No
  applicant data or API credits were used. Pushed as `bdacf0b1cb1d6fd7c91e72e2530ac8ceaadfa77e`;
  GitHub Actions `CI` run [38090277836](https://github.com/Shan091/admitflow/actions/runs/38090277836)
  passed for that SHA.
- **Human review:** Recommendations remain within the fictional course catalog. Goal tags are demo
  metadata, not independently validated career or employment outcomes. Production quality and
  privacy reviews remain open.

## 2026-10-11 — confirm the learner's summary before showing matches

- **Task:** Extend adaptive discovery so every interest-led route reflects facts before course cards
  appear, and stale confirmations cannot expose recommendations for changed preferences.
- **Assistance:** Codex persisted a digest of the learner's confirmed interest/activity/level,
  connected the confirmation and revision actions to the same policy for typed and button-led
  discovery, and preserved pending/recommendation state across pause/resume. A known-course lookup
  remains direct.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 93 tests;
  `git diff --check` passed. Fake interpreters only; no live API call or student data.
- **Human review:** Existing product scope remains course guidance within the fictional institution
  catalog; occupation/job advice stays out of scope until explicitly changed.

## 2026-10-11 — adaptive follow-up before a course recommendation

- **Task:** Make free-text course guidance multi-turn when a learner has shared only a broad
  interest, without adding a gate for learners who already name a course.
- **Assistance:** Codex added a tested two-signal domain rule, a tailored activity/level follow-up,
  validated tap callbacks that feed the existing discovery policy, and removed outdated consented-
  message wording from the domain model. The product has no affirmative-consent prompt.
- **Checks:** Focused domain/admissions tests passed (49); `bash scripts/verify.sh` passed Ruff
  lint/format, strict mypy, and 89 tests. No live API call or real student data was used.
- **Human review:** Product owner explicitly confirmed that the conversation should not require
  user consent before OpenAI-assisted guidance.

## 2026-10-11 — remove affirmative OpenAI consent gate

- **Task:** Implement the updated hackathon product decision that AI processing should start
  without an affirmative-consent step.
- **Assistance:** Codex changed `/start` to show an OpenAI/local-storage/demo-data disclosure and
  continue into discovery, added persistent opt-out/re-enable preference controls, preserved legacy
  opt-out records, and revised the feature, spec, and submission documentation. The disclosure is
  not a legal/privacy determination.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 82 tests;
  `git diff --check` passed. No live API call or student data was used for this change.
- **Human review:** The product owner requested removal of the affirmative consent prompt. Fluent
  review of translated disclosure text and privacy/legal review remain outstanding.

## 2026-10-11 — AdmitFlow public visual design

- **Task:** Finish the public landing page and align it with the existing staff dashboard styles.
- **Assistance:** Codex audited the product spec and existing design checklist, completed the
  responsive `/welcome` page and shared visual styles, added an openly usable Pexels photo with
  visible credit, clarified public vs. staff routes in the README, and added an unauthenticated
  route/static-asset regression test. Copy continues to identify the institution and catalog as
  fictional. No real applicant data or secrets were used.
- **Checks:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 72 tests;
  `git diff --check` passed. Playwright checked the rendered desktop and 390px layouts, image load,
  and mobile horizontal overflow. Automated requests used a temporary SQLite database.
- **Human review/limitations:** The selected brand direction is calm, navy-led, and trust-focused.
  The page still needs an eventual dedicated social preview image; the included student photo is
  illustrative and credited to its Pexels creator.

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
- **Follow-up:** Moved textual opt-out before the marks state handler and normalized apostrophe
  spacing variants, then verified the in-progress consent can be revoked from that state. The full
  73-test local gate passed. Pushed as `a2c3582cbf36945841a9c5f7ae58f885038c7de4`; matching
  GitHub Actions CI run [38087386606](https://github.com/Shan091/admitflow/actions/runs/38087386606)
  passed.

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
