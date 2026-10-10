# Project submission

## Project

- **Project name:** AdmitFlow
- **Short description:** A Telegram admissions assistant that remembers inquiries, checks
  seeded eligibility rules in code, answers institution FAQs with fail-closed vector search,
  and supports staff login plus Razorpay test-mode application payments.
- **Code repository URL:** https://github.com/Shan091/admitflow
- **Verified implementation commit SHA:** `a780d737202863d7dd115b5fdb4a584ab1265089`
- **Working demo:** Local `/health` and the public HTTPS tunnel returned 200. The Telegram
  webhook is registered and healthy; the user confirmed the live bot flow. The authenticated
  staff dashboard reports FAQ retrieval ready and shows the verified Razorpay test payment as
  paid. The Telegram demo bot is [@crea34bot](https://t.me/crea34bot).
- **Demo access requirements:** Local `.env` with staff credentials for dashboard login; Telegram
  account and bot token for the live conversation; OpenAI API key for FAQ retrieval; optional
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
- **Demo walkthrough:** In Telegram, send `/start`, select a course, answer the qualification
  prompts, and ask a seeded FAQ. Complete the Razorpay test link to trigger a one-time success
  message; ask “Has my payment gone through?” to check stored status. Staff can log in to the
  dashboard and review the paid lead. See `README.md` for the full setup. The new notification
  behavior is fake-bot tested; the live test payment was completed before this code change.
- **Checks performed and results:** `bash scripts/verify.sh` passed locally (Ruff lint, formatting,
  strict mypy, and 41 pytest tests); `git diff --check` passed. GitHub Actions run
  [38081779987](https://github.com/Shan091/admitflow/actions/runs/38081779987) for the verified
  implementation SHA is currently in progress; update this record when it completes.
- **Live integration checks:** The live FAQ evaluator passed 27/27 fictional cases at the
  calibrated `0.58`/`0.05` thresholds; the final 27-query batch used 207 OpenAI input tokens.
  Telegram `getWebhookInfo` reports the correct path, zero pending updates, and no delivery error.
  Razorpay test mode reports the existing ₹500 Payment Link as paid; AdmitFlow recorded one
  signature-verified webhook event and the staff dashboard shows `paid`. No applicant content was
  used in the OpenAI checks.
- **Known limitations:** Single fictional tenant, seeded FAQ corpus, one environment-configured
  staff account, no uploads, production hosting, refunds, or privacy/retention controls. Payment
  links work only with Razorpay test keys and payment status requires a reachable webhook. Demo chat
  identifiers and messages are stored locally; use fictional test inputs only.
- **Libraries and APIs:** FastAPI, python-telegram-bot, OpenAI API (`gpt-6-luna`,
  `text-embedding-3-small`), Razorpay Payment Links test API, SQLite, NumPy; see
  `docs/DECISIONS.md`.
- **AI usage:** `AI_USAGE.md`
- **Development log:** `CHANGELOG.md`
