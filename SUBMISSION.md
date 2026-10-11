# Project submission

## Project

- **Project name:** AdmitFlow
- **Short description:** A Telegram admissions assistant that remembers student interests,
  uses contextual OpenAI-led conversation to guide discovery, recommends from a fictional course
  catalog, checks supported sample eligibility rules in code,
  answers institution FAQs with fail-closed vector search, and supports staff handoffs/login plus
  Razorpay test-mode application payments.
- **Code repository URL:** https://github.com/Shan091/admitflow
- **Verified implementation commit SHA:** `d1fad4115b60d0d9864ca6355d601a3782a133d0`
- **Sample course catalog:** 50 clearly fictional, complete offerings across the five agreed
  fields, ten per field. The catalog does not offer every education level in every field.
- **Working demo:** The live Telegram webhook, public HTTPS tunnel, staff dashboard, and Razorpay
  test payment were verified during earlier milestones; the user confirmed the live bot flow. The
  adaptive language-support, study-format, inspect-before-continue course guidance, unrelated-
  message recovery, and contextual AI-led replies in this SHA passed local tests and CI. The AI-led
  changes were live-smoked with synthetic OpenAI inputs, but have not yet been rehearsed through
  Telegram or deployed to the running tunnel. The agent-led recovery and escalation-boundary
  agent-led recovery changes in `40cc1ea` and the all-level demo-fee path in `ac9e7ba` passed the
  full local verification gate and were pushed to `main`. The latest commit `d1fad41` also ensures
  every seeded threshold appears in the self-report prompt. The Telegram-to-payment flow passed
  with a fake payment adapter; it has not yet been rehearsed with the live bot or a real Razorpay
  test link. The Telegram demo bot is
  [@crea34bot](https://t.me/crea34bot).
- **Demo access requirements:** Local `.env` with staff credentials for dashboard login; Telegram
  account and bot token for the live conversation; OpenAI API key for disclosed discovery and FAQ
  retrieval; optional
  Razorpay test API keys and webhook secret for the test payment. Do not include credential values.

## Participants

| Participant name | GitHub handle | Contribution |
| --- | --- | --- |
| shan | Shan091 | Solo builder; designed and implemented AdmitFlow. |

## Run and demonstrate

- **Prerequisites and versions:** Python 3.12.5, uv 0.11.2 (verified locally)
- **Install command:** `uv sync --python 3.12`
- **Required environment variables:** `STAFF_USERNAME`, `STAFF_PASSWORD`, `STAFF_SESSION_SECRET`;
  optional `TELEGRAM_BOT_TOKEN`, `TELEGRAM_WEBHOOK_SECRET`, `OPENAI_API_KEY`, `OPENAI_DECISIONS_MODEL`,
  `OPENAI_EMBEDDING_MODEL`, `DATABASE_PATH`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`,
  `RAZORPAY_WEBHOOK_SECRET`
- **Start command:** `uv run uvicorn admitflow.main:app --reload`
- **Demo walkthrough:** In Telegram, send `/start` and read the OpenAI processing notice; there is
  no separate consent step. Free-text discovery is enabled by default and recent chat context is
  included to let the AI lead naturally; name a known course or
  describe interest/activity/goal/language-support preference/level in your own words. A broad
  match may get one optional prompt when catalog goals, listed language support, or study formats
  meaningfully differ. Answer or skip a goal prompt; for a language prompt, choose a listed support
  or leave language open; for format, choose in-person/online/hybrid or leave it open. Then inspect
  the bounded catalog recommendation; tap a match to inspect its sample prerequisites, listed
  supports/formats, and fee, then return to compare or explicitly check sample eligibility when
  that level has configured rules. For other levels, inspect the displayed fictional prerequisites
  and choose whether you meet them; clearly label this as an unverified self-report, not admission.
  A positive response offers the existing explicit demo fee action, while no/unsure cannot proceed.
  If a message is unrelated or contains no usable preference, AdmitFlow explains its scope,
  keeps the pending guidance state, and offers a relevant way forward instead of repeating the
  same question. The learner may pause and `/resume`. Supported sample undergraduate options
  continue to code-based
  qualification and require an explicit tap before a test payment link. Other course levels use an
  explicit, course-bound self-report of the displayed sample prerequisites to reach that fee step;
  no independent verification or admission decision is claimed. Routine missing facts, retrieval
  abstentions, and no-match preferences receive useful agent-led recovery. Handoff is reserved for
  explicit human requests and
  staff-authority/critical cases. Staff can inspect attributed facts and pending
  handoffs, delete one lead's local data, or reset all local demo data.
  See `README.md` for the full setup. The notification is fake-bot tested; the existing live test
  payment was completed before this code change, so the new live notification has not yet been
  rehearsed.
- **Checks performed and results:** Implementation SHA `d1fad4115b60d0d9864ca6355d601a3782a133d0`
  passed `bash scripts/verify.sh` (Ruff lint/format, strict mypy, 189 tests), `git diff --check`,
  and was pushed to `origin/main`. A fake Telegram-to-payment-link test exercised the diploma flow;
  no live Razorpay payment was created. GitHub Actions was not independently verified for this SHA.
  The preceding agent-led recovery SHA `40cc1ea7778431d76b2d71cf645b73531aa5a808` passed the
  full local verification gate with 181 tests. The earlier AI-led implementation SHA
  `ab63f88a7118a435c40a8e848b997b1f851705bf` passed `bash scripts/verify.sh` (Ruff lint/format,
  strict mypy, 174 tests), `git diff --check`, and GitHub Actions `CI` run
  [38097802190](https://github.com/Shan091/admitflow/actions/runs/38097802190).
  Synthetic live OpenAI conversation smoke used 21,990 input and 682 output tokens. Earlier, commit
  `5d33787eec9aa64bf5b79e36f517847779c68646` passed `bash scripts/verify.sh` (Ruff lint/format,
  strict mypy, and 172 pytest tests), `git diff --check`, and GitHub Actions CI run
  [38096405684](https://github.com/Shan091/admitflow/actions/runs/38096405684). No live or paid API
  calls were made for the stale guided-continuation slice. The preceding unrelated-message recovery
  commit `7a02b9cf6b977d8534336056fe54c50266975fb6` also passed the same full local gate and
  [CI run 38096233572](https://github.com/Shan091/admitflow/actions/runs/38096233572). The preceding course detail commit
  `6d66e2744b19607c78d49012f8a32982114f4732` passed `bash scripts/verify.sh` (Ruff lint/format,
  strict mypy, and 168 pytest tests), `git diff --check`, and GitHub Actions CI run
  [38095745687](https://github.com/Shan091/admitflow/actions/runs/38095745687). No live or paid API
  calls were made for the course exploration slice. On `a252c2ff438f4027181d32ecb41514325e6e4da7`,
  `bash scripts/verify.sh` passed Ruff lint/format, strict mypy, and 165 pytest tests; `git diff
  --check` passed. GitHub Actions `CI` run
  [38095320062](https://github.com/Shan091/admitflow/actions/runs/38095320062) passed. No live or
  paid API calls were made for the study-format slice. On `aed4f92f65eab558f3c06ef3fc42e5694e9a0f72`,
  the prior milestone passed `bash scripts/verify.sh` (Ruff lint/format, strict mypy, and 105
  pytest tests) with `git diff --check` passing; GitHub Actions run
  [38091126893](https://github.com/Shan091/admitflow/actions/runs/38091126893) passed. The current
  prior 40-course catalog commit `c540d11c4c0c26ff3bcb6df2e3e783e05476b3b3` also passed
  `bash scripts/verify.sh` (Ruff lint/format, strict mypy, and 117 pytest tests), `git diff --check`,
  and GitHub Actions `CI` run
  [38091492125](https://github.com/Shan091/admitflow/actions/runs/38091492125). The lifecycle
  projection follow-up `67472c5b4fb2d6a538dfe141c663779ee93d053f` passed the same local gate with
  117 tests and `git diff --check`; GitHub Actions run
  [38091855872](https://github.com/Shan091/admitflow/actions/runs/38091855872) passed. The current
  50-course catalog commit `d36a221d743081e3000208cc5294c5132f0a2ee2` passed the full local gate
  (160 tests), `git diff --check`, and GitHub Actions `CI` run
  [38094573591](https://github.com/Shan091/admitflow/actions/runs/38094573591).
- **Live integration checks:** The live FAQ evaluator passed 27/27 fictional cases at the
  calibrated `0.58`/`0.05` thresholds; the final 27-query batch used 207 OpenAI input tokens.
  Telegram `getWebhookInfo` reports the correct path, zero pending updates, and no delivery error.
  Razorpay test mode reports the existing ₹500 Payment Link as paid; AdmitFlow recorded one
  signature-verified webhook event and the staff dashboard shows `paid`. No applicant content was
  used in the OpenAI checks. A separate synthetic extraction smoke across English, Hindi,
  Malayalam, and Hinglish plus known-course, out-of-catalog, and injection cases used 12,308 input
  and 992 output tokens; see `AI_USAGE.md`. No applicant text was used.
- **Known limitations:** Single fictional tenant, seeded FAQ corpus, one environment-configured
  staff account, incomplete localized response copy, self-reported and unverified prerequisites for
  non-undergraduate offerings, no automatic retention expiry, uploads, production hosting, refunds,
  or production privacy controls. Payment
  links work only with Razorpay test keys and payment status requires a reachable webhook. Demo chat
  identifiers and messages are stored locally; use fictional test inputs only. Payment confirmation
  delivery is best-effort, no real staff follow-up contact or response time is configured, and
  course access is not enabled automatically; a live rehearsal of the
  new confirmation requires another eligible Telegram demo account and test payment. Reset clears
  local app records only; Telegram/Razorpay provider-side records are unaffected.
- **Libraries and APIs:** FastAPI, python-telegram-bot, OpenAI API (`gpt-6-luna`,
  `text-embedding-3-small`), Razorpay Payment Links test API, SQLite, NumPy; see
  `docs/DECISIONS.md`.
- **AI usage:** `AI_USAGE.md`
- **Development log:** `CHANGELOG.md`
