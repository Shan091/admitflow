# Feature: Telegram course discovery and qualification

## Outcome

A prospective student can select a fictional course, answer two questions, receive a deterministic
eligibility result, and be visible with the conversation in the local staff dashboard.

## Acceptance criteria

- [x] Telegram updates arrive through `POST /api/v1/webhooks/telegram`; no long-polling runs.
- [x] The endpoint returns 401 for a missing or incorrect `X-Telegram-Bot-Api-Secret-Token`,
  rejects malformed updates, and queues valid updates for the running PTB application.
- [x] Telegram handling starts only when both `TELEGRAM_BOT_TOKEN` and
  `TELEGRAM_WEBHOOK_SECRET` are configured; teardown closes the PTB lifecycle cleanly.
- [x] README documents registering, checking, and removing the webhook without exposing secrets.
- [x] `/start` creates or resumes a lead and offers course buttons plus a browse-only option.
- [x] Selecting a course asks whether Grade 12 is complete and asks for marks when applicable.
- [x] Python evaluates the seeded course rules; the model never sets eligibility.
- [x] A browse-only student receives information without being forced into qualification.
- [x] Inbound/outbound messages and answers persist in SQLite.
- [x] The local dashboard shows saved leads and conversations.
- [x] Demo copy identifies the institution and results as fictional/sample.

## Verification

- [x] Test eligible, ineligible, missing, malformed, and boundary answers.
- [x] Test callback handling and persistence using fake Telegram updates.
- [x] Test dashboard list/detail against the same SQLite records.
- [x] Run `bash scripts/verify.sh` (35 passed); no live Telegram request or webhook registration.
- [ ] Run one live Telegram walkthrough after configuring a bot token and registering the webhook.
