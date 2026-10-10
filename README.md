# AdmitFlow

AdmitFlow is a hackathon demo of an admissions assistant. In Telegram, a student can opt in to
OpenAI processing for free-text discovery, name a known course, describe interests, explore through
short prompts, or browse/ask a question. Declining or switching OpenAI processing off leaves the
button-based demo usable. Recommendations stay inside the fictional catalog and use no aptitude
score. Eligible undergraduate demo applicants can choose whether to request a Razorpay test-mode fee
link. FAQ answers use seeded institution content, OpenAI embeddings, and local vector search. Staff
can inspect leads, attributed discovery facts, and handoffs in a dashboard.

This is a demo using fictional sample data. Eligibility results are not real admission decisions.
The language selector stores English, Malayalam, Hindi, or Hinglish preferences, but most current
bot responses remain English; translated copy is incomplete and needs fluent-speaker review.
Use fictional/demo answers only: Telegram user IDs, usernames, and chat messages are stored in the
local SQLite database. Before free-text AI features are enabled, the bot explains that the current
message may be sent to OpenAI and asks for explicit consent. The extraction request uses only the
current message and allowlisted fictional catalog vocabulary with API storage disabled; it does not
include chat ID, name, or transcript. This is not a production privacy review. Configure staff
credentials before viewing the dashboard. Razorpay is restricted to test-key IDs; payment state
changes only after a verified webhook.

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

Staff can delete one lead from its detail page or use **Delete all demo data** at the bottom of the
authenticated dashboard to reset the
local demo. It requires typing `DELETE ALL DEMO DATA` and deletes leads, conversations, payment
records, and Razorpay webhook history from SQLite. Seeded fictional courses and FAQs remain so the
demo can continue. This does not delete external records held by Telegram or Razorpay.

Telegram webhooks require HTTPS, and Telegram does not allow webhook delivery and `getUpdates`
polling simultaneously. The helper checks Telegram's reported webhook URL after registration.
To remove the hook, run `uv run python scripts/manage_telegram_webhook.py --delete`. This project
currently runs webhook mode only. Configure `OPENAI_API_KEY` to enable consented discovery and
semantic FAQ search. Set `STAFF_USERNAME`, `STAFF_PASSWORD`, and
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
2. Read the OpenAI processing notice. Agree to enable free-text course discovery or choose
   **No, use buttons only**. After consent, describe a known course, interest, activity, or study
   level in one message, or use the shortcuts. Without consent, use the field/course/browse buttons.
   A learner can pause with the inline action and resume with `/resume`.
3. Select a course. Sample undergraduate options can continue through the code-computed eligibility
   check; other levels show sample prerequisites and create a staff handoff instead of using a
   Grade 12 rule that may not apply.
4. Ask a seeded FAQ question; if retrieval is unavailable or uncertain, the bot says so.
5. Open the local dashboard, log in, and view the same lead, attributed facts, and any pending
   handoff. Staff can delete an individual lead or reset all local demo records.
6. If Razorpay test credentials and a reachable webhook are configured, meet the sample rules and
   tap **Continue to demo fee** before a link is created. The verified `payment_link.paid` webhook
   marks the payment paid and sends one confirmation. If delivery fails, ask “Has my payment gone
   through?” to check the stored status. The dashboard records the next staff-review step; no live
   contact or response time is configured, and course access is not provisioned automatically.

The language menu is available at each bot turn and saves the selected preference, but most current
replies remain in English. Do not present the four language selector options as complete translated
support yet.

## Current status

Check `tasks/todo.md` for completion state. `CHANGELOG.md` and `SUBMISSION.md` contain only
checks actually performed. Live payments, document uploads, deployment, and a production WhatsApp
integration are out of scope for this demo.
