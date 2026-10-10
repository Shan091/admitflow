# Hackathon implementation checklist

Update this checklist at the start of each work slice. A checkbox is complete only after its
acceptance criteria pass and the corresponding milestone is committed.

## Foundation and repository

- [x] Confirm feature scope, decisions, and dependency order against `SPEC.md` and `docs/DECISIONS.md`.
- [x] Install the locked Python 3.12 environment and record the lockfile.
- [x] Verify seed/schema initialization, configuration, health endpoint, dashboard, and CI setup.
- [x] Commit and push the verified foundation milestone; record its exact test commands/results.

## Telegram course discovery and qualification

- [x] Replace long-polling with the authenticated Telegram webhook requested for the demo; add
  `TELEGRAM_WEBHOOK_SECRET`, reject invalid requests, and document webhook registration and reset.
- [x] Verify webhook authorization, update parsing/queueing, disabled configuration, and clean bot
  lifecycle locally; then run `bash scripts/verify.sh` and record the actual result.
- [x] Test eligible, ineligible, malformed, missing, and boundary qualification inputs.
- [x] Test lead/message persistence and idempotent handling of duplicate Telegram updates.
- [x] Test Telegram flow service behavior with fake updates; no live API in automated tests.
- [x] Verify dashboard lead list/detail from the same SQLite records.
- [x] Complete and record a live Telegram walkthrough; user confirmed the bot flow, and the
  registered webhook remains healthy with no pending updates.

## Adaptive, interest-led course discovery

See `tasks/features/adaptive-course-discovery.md`. This feature replaces the fixed course-first
opening; do not mark a task complete until the acceptance criteria pass and the milestone is
committed.

- [x] Add and migrate structured catalog metadata; seed clearly fictional offerings across the
  agreed levels and fields. **Open:** fill and verify all requirements/language facts before
  recommending every offering.
- [x] Persist attributed facts, discovery path/step, lifecycle, and qualitative readiness separately
  from hard eligibility; migration tests prove existing lead/message/payment rows survive.
- [x] Build four entry paths, optional field/level/activity prompts, catalog recommendations,
  back/skip, path switching, and pause/resume. **Open:** finish the full interrupt matrix across
  FAQ, fees, language switching, stop, and restart.
- [x] Record student and parent preferences separately; require learner confirmation before a
  parent's course choice advances.
- [ ] Localize all student-facing discovery, qualification, FAQ, payment, and handoff responses to
  English/Malayalam/Hindi/Hinglish; review the translations with fluent speakers.
- [ ] Provide deterministic course-specific eligibility for every recommended level, or keep the
  offering in staff handoff until verified rules are configured.
- [x] Create staff-dashboard handoffs for unsupported/missing facts and state truthfully that no
  live contact or response-time commitment is configured.
- [x] Provide staff-mediated per-lead deletion. **Open:** choose, configure, and test an
  admissions-cycle retention expiry policy.
- [x] Run `bash scripts/verify.sh` (63 tests) and `git diff --check` for the pushed slice. **Open:**
  complete translated-copy, full language-flow, and remaining privacy/eligibility tests.
- [x] Record test results in CHANGELOG/AI_USAGE/SUBMISSION; implementation commit
  `53e78e44809c8c9714d70c13b08c07582bacfdad` was pushed and its matching GitHub Actions CI run
  `38085663111` passed. The checklist and submission-record update was pushed as
  `9315a93f9c2557d3c00008a775458397b8554837`; its GitHub Actions run `38085770102` passed.

## FAQ embeddings and vector retrieval

- [x] Test vector packing during seed indexing, cosine ranking, dimension mismatch, and tenant scoping.
- [x] Test embedding reuse/content invalidation, score threshold, margin, and fail-closed behavior.
- [x] Test fee questions use structured prices before intent routing or FAQ retrieval.
- [x] Verify fixed expected question-to-FAQ matches with fake vectors.
- [x] Calibrate similarity and margin thresholds using live embedding/query examples; use the
  recorded `0.58`/`0.05` values as provisional demo defaults.
- [x] Run and separately record a live OpenAI embedding smoke check with fictional query examples.

## Live FAQ retrieval calibration

- [x] Add a repeatable evaluator with fixed, fictional FAQ paraphrases and out-of-scope questions;
  report expected source, chosen source, top cosine score, margin, and pass/fail without printing
  credentials or sending non-demo content to OpenAI.
- [x] Add the evaluator and curated query phrasings; version cached vectors when their embedding
  text profile changes.
- [x] Run it against live `text-embedding-3-small` and the seeded SQLite vectors; measured `0.58`/
  `0.05` cleanly separates the fixed expected and unsupported cases.
- [x] Route unconfigured hostel/tuition charges and refund requests to safe, code-owned responses
  instead of returning an unrelated application fee or entering FAQ retrieval.
- [x] Record actual cases, scores, API usage, and the decision in the feature brief, `CHANGELOG.md`,
  and `AI_USAGE.md`; rerun `bash scripts/verify.sh` and `git diff --check`.
- [x] Commit and push the verified milestone; confirm GitHub Actions passed for
  `e19bd2be7f8e401a3bfa21e9e4ddd97f01dfeedf` (run `38081259866`).

## Staff login

- [x] Add a feature brief and auth/session settings; require configured credentials for dashboard
  and login/logout behavior, failing closed if credentials are missing.
- [x] Test anonymous redirects, valid/invalid login, logout, protected lead detail, and missing
  auth configuration using the app test client.
- [x] Document local staff credentials/session secret setup without committing secrets.

## Razorpay test-mode application payments

- [x] Add a feature brief and payment schema/repository operations; price and lead association must
  come from server-side course/lead records.
- [x] Create a Razorpay test-mode Payment Link after successful demo qualification and send it to
  Telegram; do not create links when payment credentials are absent.
- [x] Verify webhook HMAC signatures, event idempotency, known link association, and expected amount
  before changing a payment to paid.
- [x] Test Payment Link request payload and errors with a fake HTTP transport; automated tests must
  make no Razorpay network requests.
- [x] Document Razorpay test credentials and webhook setup, test commands, and live-mode limitation.
- [x] Run `bash scripts/verify.sh`, review the diff, commit and push, and record the exact pushed SHA
  plus GitHub Actions test result.

  Verified 32 tests locally and GitHub Actions run 38076997956 passed on
  `182c27689544f21a6536146db870a553b03e14a5` (including the `/api/v1/webhooks/razorpay` alias).

## Final verification and submission

- [x] Add a staff-only “delete all demo data” action with a server-verified confirmation phrase
  and session-bound CSRF token. Delete leads, conversations, payments, and webhook history while
  preserving seeded course/FAQ content; test success and rejection paths.
- [x] Run the full verification gate, document actual results, commit/push, and record the exact
  GitHub Actions result for the reset milestone.
- [x] Send a one-time, truthful Telegram confirmation after a verified paid webhook; add a
  payment-status lookup backed only by persisted Razorpay state and cover the flows with tests.
- [x] Run the full verification gate, update feature/docs/logs, commit and push the milestone, and
  record the matching GitHub Actions result.
- [x] Finalize the hackathon submission metadata and demo access details.

- [x] Run `bash scripts/verify.sh`; record actual output and results in `CHANGELOG.md` and `SUBMISSION.md`.
- [x] Review diff, claims, credentials, and AI usage record; ensure no real applicant data is seeded.
- [x] Confirm GitHub Actions result for the pushed build commit and record its exact SHA/results.
- [x] Record live demo steps, limitations, access details, and submission metadata.
- [ ] Live-rehearse the new payment confirmation with a fresh eligible demo account and test
  payment; the current live demo lead already has a paid payment intent.
