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

## Conversational career-guidance agent (production objective)

See `tasks/features/conversational-guidance-agent.md`. This extends course discovery into an
adaptive, evidence-grounded, multi-turn guidance experience; do not treat lifecycle stages as a
mandatory linear interview.

- [x] Confirm institution-course-only recommendations, with goal exploration and staff referral for
  out-of-catalog requests; no job or occupation predictions. Production age/privacy policy remains
  an open gate; hackathon testing uses fictional data only.
- [ ] Map current conversation behavior and v1 lifecycle semantics to a turn-by-turn adaptive
  interaction model; define the user's open-question start, known-course fast path, exploration,
  recommendation comparison, interrupts, and safe handoffs.
- [ ] Extend catalog/course knowledge only from verified complete records; keep invented facts,
  unsupported eligibility, and job-outcome promises out of recommendations.
- [ ] Implement a multi-turn question policy that uses existing attributed facts, asks only useful
  next questions, reflects understanding for correction, and preserves path switching/resume.
- [x] Current slice: require a complementary signal before recommending from broad interests;
  when context is thin, ask one tailored follow-up and preserve the known-course fast path.
- [x] Current slice: reflect the learner's stated interests, activity, and level before surfacing
  recommendations; show options only after explicit confirmation, and reject stale confirmations
  after the learner changes their preferences.
- [ ] Define and test coverage for contradictory/corrected preferences, mixed interests, constraints,
  parent/student conflict, unknown/out-of-catalog requests, sensitive disclosures, provider/RAG
  failures, language switching, deletion, and concurrent/duplicate updates.
- [x] Add a catalog-grounded optional study-goal signal for broad/ambiguous interest matches:
  persist only explicit goals, ask at most one useful follow-up, allow skip/resume, and include goals
  in correction/confirmation fingerprints and transparent recommendation reasons. Full gate passed
  (96 tests); pushed as `bdacf0b1cb1d6fd7c91e72e2530ac8ceaadfa77e`; GitHub Actions CI run
  `38090277836` passed.
- [x] Add optional course-language support exploration. Ask only when a broad, otherwise
  comparable candidate set has materially different catalog-recorded support languages (the current
  seed's teaching medium is English for every course); explain that distinction without
  predicting ability or outcomes, and let the learner choose, leave it open, or skip. Keep the
  preference speaker-attributed, allowlisted to course records, correction-safe, resumable, and in
  recommendation explanations. **Verified:** fake-API extraction, no prompt for known-course or
  uniform-language matches, skip/correction/resume, stale confirmation invalidation, empty-match
  recovery, parent attribution, and bounded language claims. `bash scripts/verify.sh` passed
  Ruff lint/format, strict mypy, and 105 tests; pushed as
  `aed4f92f65eab558f3c06ef3fc42e5694e9a0f72`; GitHub Actions `CI` run `38091126893` passed.
- [x] Expand the fictional demo catalog from 28 to 40 complete offerings, with eight in each
  agreed field and examples across certificate/vocational, diploma, undergraduate, and postgraduate
  levels. Added only fictional, non-regulated sample subjects. **Verified:** exact catalog count,
  unique IDs, idempotent seeding, field/level coverage, complete attributes, allowed support tags,
  and expected retrieval for every new course; `bash scripts/verify.sh` passed (117 tests), and
  `git diff --check` passed. Pushed as `c540d11c4c0c26ff3bcb6df2e3e783e05476b3b3`; GitHub Actions
  `CI` run `38091492125` passed.
- [ ] Establish production gates for real institution/catalog onboarding, age-appropriate privacy,
  retention/deletion, localization review, human escalation, monitoring, and independent evaluation.

## AI-assisted adaptive intake and larger catalog

See `tasks/features/conversational-intake.md`. Preserve the existing demo boundary: fictional
courses, no scores, student-first attribution, and truthful staff handoff.

- [x] Expand the seed catalog to 28+ complete sample courses, at least five per agreed field; test
  unique IDs, all levels, complete facts, and recommendation provenance.
- [x] Keep discovery available without an affirmative-consent step; disclose OpenAI processing and
  demo-only data use at start, enable AI by default, and verify opt-out/re-enable behavior locally.
- [x] Extract only current-turn, catalog-allowlisted discovery facts with a strict schema and
  stateless API request; validate model output before any persistence or response.
- [x] Replace the mandatory field/level/activity sequence with deterministic next-question choice
  based on already-known facts; support known-course natural-language entry and unsure learners.
- [x] Add fake-API tests for opt-out, catalog allowlisting, injection instructions, known-course
  entry, corrections, handoff, dynamic responses, and extraction failure; run synthetic live
  language checks in English, Hindi, Malayalam, and Hinglish.
- [x] Run `bash scripts/verify.sh` (71 tests), review privacy/claims, commit and push this slice as
  `0e45565fe4dbbd434435bf264bc8ce8e8d86a7b8`; GitHub Actions CI run `38087034051` passed.
- [x] Verify opt-out still works while collecting marks; full gate passed with 73 tests. Pushed as
  `a2c3582cbf36945841a9c5f7ae58f885038c7de4`; CI run `38087386606` passed.
- [ ] Localize the OpenAI processing notice, tap-only response, opt-out/re-enable controls to
  English, Hindi, Malayalam, and Hinglish; have a fluent speaker review translations.

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

## Visual identity: brand kit, landing page, dashboard restyle

Calm editorial / trust-first design, implemented in plain HTML + native CSS + a little vanilla
JS (no Node, no new runtime deps). `StaticFiles` ships with Starlette. Acceptance criteria below
must pass and the milestone be committed before any box is marked `[x]`.

**Current work slice:** finish the in-progress public landing route and shared visual foundation.
Preserve other working-tree changes. Verify `/welcome` without a staff cookie, `/`'s staff-login
redirect, static asset delivery, responsive layout, no-JS content, and reduced-motion behavior.
Do not claim production admissions, live staff contact, or real institutional offerings.

- [ ] Add `static/tokens.css` design tokens (locked navy accent `#1f3a5f`, existing status colors
  preserved, Noto Serif/Sans with system fallbacks, type/space/radius/shadow scales). **AC:**
  single source of truth consumed by both surfaces; white-on-`--danger` passes WCAG AA.
- [ ] Mount `/static` and add an unauthenticated `GET /welcome` landing route in a new
  `landing_routes.py`. **AC:** `/welcome` returns 200 with no cookie; `/` still 303s to `/login`;
  new Python is fully typed and passes strict mypy + ruff format.
- [ ] Author brand assets: hand-written `brand/logo.svg` + `favicon.svg` (code), and generate the
  brand board + `og-image.png` via `/brandkit` (images). **AC:** logo themeable via `currentColor`;
  code vs image split documented in SUBMISSION/README.
- [ ] Build `templates/landing.html` + `static/landing.css` (AIDA, prominent fictional-demo badge,
  single Telegram CTA, honest copy, no em-dashes). **AC:** hero fits viewport; no fabricated claims;
  renders with no-JS and reduced-motion.
- [ ] Restyle dashboard: extract inline CSS to `static/app.css`, swap `<style>`→`<link>` in
  `base.html`/`login.html` only; leave `leads.html`/`lead_detail.html` markup untouched. **AC:**
  every test-asserted string/markup preserved; all pages render correctly.
- [ ] Hybrid motion: dashboard CSS hover/focus only; landing uses one IntersectionObserver reveal as
  progressive enhancement; both honor `prefers-reduced-motion`. **Dependencies:** tokens.css first.
- [ ] Run `bash scripts/verify.sh` (ruff, ruff format, strict mypy, pytest) and manual page checks;
  record actual results in CHANGELOG/SUBMISSION; commit the milestone with a plain message.

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
