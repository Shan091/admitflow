# Changelog

## 2026-10-11 — restore the guided-exploration prompt on resume

- **Change:** Preserve `explore` as its own discovery step when showing field choices. Resume now
  returns the same open exploration question and choice set instead of replacing it with a
  field-only prompt. Known-field selection and back-to-field keep their separate state.
- **Validation:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and all 124 tests;
  `git diff --check` passed. New coverage asserts the field choices, browse/pause actions, and exact
  exploration prompt/options after resume.
- **Delivery:** Implementation commit and CI pending.
- **Reason:** Learners who are unsure can return to the question that fits their chosen exploration
  path after pausing, without being pushed into a different flow.

## 2026-10-11 — preserve unrelated preferences during corrections

- **Change:** A correction now replaces values only in categories it explicitly restates, preserves
  unmentioned learner and parent facts, supports exact catalog-bounded retractions, and clears stale
  recommendation confirmations. Ambiguous corrections ask what to change instead of reflecting old
  facts. Language-concern shortcuts now allow explicit preference corrections through to discovery.
  The flow continues without an affirmative consent step; OpenAI processing is disclosed and users
  can opt out.
- **Validation:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and all 123 tests.
  Tests cover single-category replacement, preservation of other categories, exact retractions,
  speaker attribution, stale confirmation invalidation, ambiguity, and schema allowlisting. No live
  or paid API calls were made.
- **Delivery:** Pushed as `7c57d2df1e6f05a400b7690869b5706a2c35fc41`; GitHub Actions `CI` run
  [38092799672](https://github.com/Shan091/admitflow/actions/runs/38092799672) passed.
- **Reason:** Keep conversational preferences accurate when a learner changes one part of their
  guidance profile without silently erasing other relevant facts.

## 2026-10-11 — align lifecycle with verified payment progress

- **Change:** Project the lead lifecycle to `payment_pending` only after a valid Razorpay test link
  is stored, and to `under_review` only in the transaction that records a signature-verified paid
  webhook whose link, reference, currency, and full amount match. Retried links reuse the same
  persisted link. The feature brief maps the v1 stages and calls out deferred states and the
  pending-versus-accepted staff handoff distinction.
- **Validation:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and all 117 tests;
  `git diff --check` passed. New assertions cover successful/retried and failed link creation,
  invalid/mismatched/partial webhook events, valid payment, duplicate event, and lifecycle/readiness
  separation. GitHub Actions `CI` passed for the pushed implementation commit.
- **Delivery:** Pushed as `67472c5b4fb2d6a538dfe141c663779ee93d053f`; GitHub Actions `CI` run
  [38091855872](https://github.com/Shan091/admitflow/actions/runs/38091855872) passed.
- **Reason:** Keep the lifecycle dashboard truthful to verified progress and the v1 event-based
  stage semantics without letting a payment or conversational tone claim enrollment.

## 2026-10-11 — expand fictional course catalog to 40 offerings

- **Change:** Add 12 complete fictional offerings, bringing the catalog to exactly 40 with eight
  per agreed field and examples across certificate/vocational, diploma, undergraduate, and
  postgraduate levels. New offerings are non-regulated sample subjects; their prerequisites, fees,
  language-support labels, and learning goals remain catalog-owned. No job or outcome claims were
  added.
- **Validation:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and all 117 tests.
  The suite checks exact catalog size, field/level spread, unique IDs, completeness, idempotent
  seeding, support-label validity, and exact recommendation retrieval for each added offering.
  `git diff --check` passed. Automated tests use fictional data and fake APIs only.
- **Delivery:** Pushed as `c540d11c4c0c26ff3bcb6df2e3e783e05476b3b3`; GitHub Actions `CI` run
  [38091492125](https://github.com/Shan091/admitflow/actions/runs/38091492125) passed.
- **Reason:** Give undecided learners more realistic sample options while preserving the existing
  code-owned catalog matching and fictional-demo boundary.

## 2026-10-11 — add optional catalog-grounded language support preference

- **Change:** For a broad set of more than three matching sample courses, offer one optional
  language-support question only when the candidates share a teaching medium but list different
  support. A goal question already used for the same fact set suppresses this extra prompt. The
  learner may leave language open; a chosen exact catalog label filters results and becomes part of
  correction/confirmation fingerprints. Recommendations disclose the listed teaching medium and
  support separately. No language ability or outcome is inferred. Unsupported language-medium
  requests receive the existing factual boundary and staff handoff.
- **Validation:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and all 105 tests;
  `git diff --check` passed. Tests use fictional catalog data and fake OpenAI responses only; no
  live or paid API call was made.
- **Delivery:** Feature commit `91005085048517c4c0ea86b8d1f520d3606571dc` and follow-up
  attribution-test commit `aed4f92f65eab558f3c06ef3fc42e5694e9a0f72` were pushed. GitHub Actions
  `CI` run [38091126893](https://github.com/Shan091/admitflow/actions/runs/38091126893) passed for
  the 105-test tree; the implementation commit's run [38091066242](https://github.com/Shan091/admitflow/actions/runs/38091066242)
  also passed.
- **Reason:** Let learners weigh recorded language support as one course trade-off while preserving
  a direct path for students who already know their course.

## 2026-10-11 — add optional catalog-grounded study goals

- **Change:** Add sample learning-goal tags to the 28 fictional courses and an additive SQLite
  migration. For broad candidate sets with more than one represented learning goal, ask one optional
  follow-up; learners can skip or resume it. Explicit goals are validated against course metadata,
  included in stale-confirmation fingerprints, used to filter matches, and shown as fit reasons.
  Known-course routing remains direct. No job or occupation predictions were added.
- **Validation:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and all 96 tests;
  `git diff --check` passed. Tests use fictional data and fake OpenAI responses only; no paid API
  call was made.
- **Delivery:** Pushed as `bdacf0b1cb1d6fd7c91e72e2530ac8ceaadfa77e`; GitHub Actions `CI` run
  [38090277836](https://github.com/Shan091/admitflow/actions/runs/38090277836) passed for this SHA.
- **Reason:** Give undecided learners one more relevant way to distinguish a broad set of sample
  courses while keeping the question optional, course-bounded, and based on explicit preferences.

## 2026-10-11 — reflect and confirm preferences before recommendations

- **Change:** Require a brief reflection and explicit confirmation before showing matches from both
  free-text discovery and field/level buttons. Learners can revise, pause, and resume; confirmation
  buttons are tied to current preferences and become stale after changes or path switches. A known
  course still enters selection immediately.
- **Validation:** `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and all 93 tests;
  `git diff --check` passed. Includes tests for correction-to-same-values, stale callbacks,
  path-switch invalidation, pause/resume, and Telegram callback routing.
- **Delivery:** Pushed as `6a412fa60a6ae1f3eb9ab6e2efc23d09d3fc7039`; GitHub Actions `verify` run
  `38089498466` passed.
- **Reason:** Give learners a chance to correct the bot's understanding before it displays options,
  and prevent a confirmation for one set of preferences from authorizing another.

## 2026-10-11 — require more than a broad interest before recommending

- **Change:** Add a domain policy requiring an expressed interest plus an activity or study level
  before conversational discovery recommends courses. Thin context now produces one targeted
  follow-up with validated activity/level tap replies; known-course lookup remains a direct path.
- **Validation:** Focused domain/admissions tests passed (49 tests). `bash scripts/verify.sh` passed
  Ruff lint/format, strict mypy, and all 89 tests after formatting; `git diff --check` passed.
  Pushed as `fb57f78fd495d9ec1c2c828fa21ac220097777e4`; GitHub Actions `verify` run
  `38088864278` passed.
- **Reason:** A broad interest such as “I like design” should lead to useful exploration rather than
  an immediate course list, while learners who already know their course should not be forced
  through extra questions.

## 2026-10-11 — remove affirmative OpenAI consent gate

- **Change:** Start AI-assisted discovery after disclosing OpenAI processing and local storage.
  Enable it by default, persist opt-out/re-enable preferences, and keep button-only exploration
  available while processing is off. Preserve older opt-out records.
- **Validation:** `bash scripts/verify.sh` passed: Ruff lint, formatting, strict mypy, and 82 pytest
  tests; `git diff --check` passed. Commit and push are pending.
- **Reason:** The hackathon product decision removes the consent prompt while keeping the data use
  visible and giving users an ongoing processing control. This is not a legal/privacy determination.

## 2026-10-11 — opt-out priority across conversation states

- **Change:** Move textual OpenAI opt-out handling ahead of qualification-state parsing, so a
  student can revoke consent even while the bot is waiting for marks. Cover common apostrophe and
  spacing variants.
- **Validation:** `bash scripts/verify.sh` passed with 73 tests (Ruff, format, strict mypy, pytest);
  `git diff --check` passed. Push and matching GitHub Actions result are pending.
- **Reason:** Consent withdrawal must work at any point in a conversation.

## 2026-10-11 — public landing page and visual system

- **Change:** Added the public `/welcome` admissions-demo page, a shared self-hosted type and
  color foundation, brand marks, static assets, and consistent dashboard/login styling. Reworked
  the landing page with a responsive split hero, an explicitly illustrative and credited Pexels
  photo, a four-step explanation, grounded-claims section, and working Telegram CTA. `/` remains
  staff-login protected. Added a public-route/static-asset regression check.
- **Why:** Give AdmitFlow a clear, professional first impression for students and families while
  keeping the fictional demo boundary and the staff dashboard visible.
- **Validation:** `bash scripts/verify.sh` passed: Ruff lint, formatting, strict mypy, and 72
  pytest tests. `git diff --check` passed. Manual Playwright checks confirmed `/welcome` loads,
  the hero image loads, and the mobile layout at 390px has no horizontal overflow. Reduced-motion
  and no-JavaScript content behavior are implemented progressively in CSS/JS.
- **Limitations:** No real institution, course offering, admission outcome, or payment is shown.
  The illustrative Pexels image requires an internet connection. No dedicated social preview image
  is included.

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
