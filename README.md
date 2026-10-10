# AdmitFlow

AdmitFlow is a hackathon demo of an admissions assistant. A student can explore a fictional
institution's courses in Telegram, answer eligibility questions evaluated by code, and ask
questions answered from seeded institution FAQs using OpenAI embeddings and local vector search.
Staff can inspect saved leads and conversations in a local read-only dashboard.

This is a demo using fictional sample data. Eligibility results are not real admission decisions.
Use fictional/demo answers only: Telegram user IDs, usernames, and chat messages are stored in the
local SQLite database. Configure staff credentials before viewing the dashboard. Razorpay is
restricted to test-key IDs; payment state changes only after a verified webhook.

## Requirements

- Python 3.12
- `uv`
- Telegram bot token and webhook secret for live Telegram interaction (optional for local
  dashboard/tests)
- OpenAI API key for Decisions API and embedding-backed FAQ answers (optional; RAG stays
  unavailable without it)
- Staff username, password, and session signing secret (required for dashboard access)
- Razorpay test-mode API key ID, API secret, and webhook secret (optional; payments stay disabled
  without the complete set)

## Setup and run

```bash
uv sync --python 3.12
cp .env.example .env
# Add credentials to .env locally; never commit it.
uv run uvicorn admitflow.main:app --reload
```

Open `http://127.0.0.1:8000/` for the dashboard and `/health` for health status. Configure both
`TELEGRAM_BOT_TOKEN` and `TELEGRAM_WEBHOOK_SECRET` to enable Telegram webhook handling. Generate a
webhook secret locally with `python -c "import secrets; print(secrets.token_urlsafe(32))"`; keep
the secret private. After starting the app on a public HTTPS host or tunnel, register the webhook
using the helper script. It reads the bot token and webhook secret from your local `.env` and never
prints them:

```powershell
uv run python scripts/manage_telegram_webhook.py https://YOUR-PUBLIC-HOST
```

Telegram webhooks require HTTPS, and Telegram does not allow webhook delivery and `getUpdates`
polling simultaneously. The helper checks Telegram's reported webhook URL after registration.
To remove the hook, run `uv run python scripts/manage_telegram_webhook.py --delete`. This project
currently runs webhook mode only. Configure `OPENAI_API_KEY` to enable
intent routing and semantic FAQ search. Set `STAFF_USERNAME`, `STAFF_PASSWORD`, and
`STAFF_SESSION_SECRET` in `.env` to log in. Generate the session secret locally with
`python -c "import secrets; print(secrets.token_urlsafe(48))"`; never commit `.env`.

For payments, create Razorpay **test mode** API keys and configure `RAZORPAY_KEY_ID` (must start
with `rzp_test_`), `RAZORPAY_KEY_SECRET`, and `RAZORPAY_WEBHOOK_SECRET`. Register
`POST /api/v1/webhooks/razorpay` (also accepted at `/webhooks/razorpay`) in the Razorpay test
dashboard for the `payment_link.paid` event. Local webhook delivery needs a public HTTPS tunnel;
payment creation and signature handling have fake automated tests and do not spend credits or
create network calls during CI. Do not use live keys.

## Tests and checks

Run the same quality gate used by GitHub Actions before pushing:

```bash
bash scripts/verify.sh
```

The gate runs Ruff lint and format checks, strict mypy, and pytest. Automated tests use fake
Telegram updates, fake embeddings, and temporary SQLite databases; they do not call Telegram or
OpenAI and do not spend API credits. Live API checks are manual and must be reported separately.

To check the seeded FAQ retrieval with the live embedding API, configure `OPENAI_API_KEY` and run:

```bash
uv run python scripts/evaluate_faq_retrieval.py
```

This evaluates 27 fixed, fictional question variants against the seeded SQLite corpus, reports
the expected/actual source, cosine score, margin, and API input-token usage, and exits nonzero if
any expected match/refusal fails. The request uses only synthetic demo questions; OpenAI API usage
is billable. The evaluator never reads applicant messages.
CI runs on pushes and pull requests; its status applies to the exact commit shown by GitHub.

## Demo walkthrough

1. Register the Telegram webhook as described above, then send `/start` to the configured bot.
2. Choose a seeded course, answer the two qualification prompts, and view the code-computed result.
3. Ask a seeded FAQ question; if retrieval is unavailable or uncertain, the bot says so.
4. Open the local dashboard, log in, and view the same lead and conversation.
5. If Razorpay test credentials and a reachable webhook are configured, complete the demo fee
   link and confirm the dashboard shows `paid` only after the webhook arrives.

## Current status

Check `tasks/todo.md` for completion state. `CHANGELOG.md` and `SUBMISSION.md` contain only
checks actually performed. Live payments, document uploads, deployment, and a production WhatsApp
integration are out of scope for this demo.
