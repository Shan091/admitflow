# Project submission

## Project

- **Project name:** AdmitFlow
- **Short description:** A Telegram admissions assistant that remembers inquiries, checks
  seeded eligibility rules in code, answers institution FAQs with fail-closed vector search,
  and supports staff login plus Razorpay test-mode application payments.
- **Code repository URL:** https://github.com/Shan091/admitflow
- **Final implementation commit SHA:** `0ddc470097a08365fec07e8278fa58e32697f7de`
- **Working demo:** `/health` runs locally; dashboard requires configured staff credentials. Live
  Telegram bot username and walkthrough are pending bot-token setup and a real rehearsal.
- **Demo access requirements:** Local `.env` with staff credentials for dashboard login; Telegram
  account and bot token for the live conversation; OpenAI API key for FAQ retrieval; optional
  Razorpay test API keys and webhook secret for the test payment. Do not include credential values.

## Participants

| Participant name | GitHub handle | Contribution |
| --- | --- | --- |
| TODO | TODO | TODO |

## Run and demonstrate

- **Prerequisites and versions:** Python 3.12.5, uv 0.11.2 (verified locally)
- **Install command:** `uv sync --python 3.12`
- **Required environment variables:** `STAFF_USERNAME`, `STAFF_PASSWORD`, `STAFF_SESSION_SECRET`;
  optional `TELEGRAM_BOT_TOKEN`, `OPENAI_API_KEY`, `OPENAI_DECISIONS_MODEL`,
  `OPENAI_EMBEDDING_MODEL`, `DATABASE_PATH`, `RAZORPAY_KEY_ID`, `RAZORPAY_KEY_SECRET`,
  `RAZORPAY_WEBHOOK_SECRET`
- **Start command:** `uv run uvicorn admitflow.main:app --reload`
- **Demo walkthrough:** Pending live Telegram setup and rehearsal; see the local-only verification
  steps in `README.md`.
- **Checks performed and results:** Latest local `bash scripts/verify.sh` passed (Ruff lint,
  formatting, strict mypy, and 32 pytest tests); `uv sync --locked --python 3.12` passed;
  `git diff --check` passed. GitHub Actions result for this new commit is pending push.
- **Live integration checks:** No live OpenAI, Telegram, or Razorpay request was made. Automated
  payment tests use a fake HTTP transport and signed sample webhook; no API credits or payment
  transactions were used. GitHub Actions status for this commit is pending push.
- **Known limitations:** Single fictional tenant, seeded FAQ corpus, one environment-configured
  staff account, no uploads, production hosting, refunds, or privacy/retention controls. Payment
  links work only with Razorpay test keys and payment status requires a reachable webhook. Demo chat
  identifiers and messages are stored locally; use fictional test inputs only.
- **Libraries and APIs:** FastAPI, python-telegram-bot, OpenAI API (`gpt-6-luna`,
  `text-embedding-3-small`), Razorpay Payment Links test API, SQLite, NumPy; see
  `docs/DECISIONS.md`.
- **AI usage:** `AI_USAGE.md`
- **Development log:** `CHANGELOG.md`
