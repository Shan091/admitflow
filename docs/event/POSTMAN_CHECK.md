# One final WhatsApp check with Postman

Import `whatsapp-diagnostic.postman_collection.json`. It contains placeholders only.

Create/select a local Postman environment and set these values from ignored `backend/.env`:

- `WHATSAPP_ACCESS_TOKEN`
- `WHATSAPP_PHONE_NUMBER_ID`
- `WHATSAPP_TEST_RECIPIENT` (digits with country code, without `+`)

Keep secrets local; do not export an environment containing them or share response bodies with phone numbers. All three values must refer to the intended new app/test sender and its allowed recipient.

1. Send **1 - Read sender and account health**. Read `health_status.can_send_message` and the errors for each entity. If `BLOCKED`, Postman cannot fix the Meta restriction. The collection runner stops before sending when blocked.
2. If sending is allowed, send **2 - Send hello_world once**. Do not repeat it through a runner loop.
3. HTTP 200 plus a message id means Meta accepted the submission. Confirm delivery on the phone or inspect the signed webhook status. `failed` with 131031 was the last observed result on the configured new test account; do not interpret HTTP 200 as delivered.

The existing readiness receiver logs only authenticated status, a hashed message reference, and numeric error codes. Current temporary callback at the latest configuration checkpoint: `https://lopez-monitor-lets-sections.trycloudflare.com/api/webhook`. Recheck it before relying on status callbacks; a quick tunnel expires when its process stops. Postman's outgoing send request does not use this callback URL.

This collection does not change app/account subscriptions, register a number, add payment details, publish an app, or lift Meta restrictions.

## Executed final check

After the user explicitly requested handling the entire test, installed Newman 6 in a temporary directory and executed this v2.1 collection using `backend/scripts/run_postman_check.cjs`. The desktop app was not installed. Credentials were read from ignored `.env` into memory, with no credential export or raw response reporting. The runner defaults to a read-only health request; `--send-once` separately runs exactly one send even when the health check is blocked, for an explicitly requested final diagnostic retry.

Observed: health HTTP 200, sending BLOCKED (account flag 141006; business flag 141010). The single send returned HTTP 200 and a message ID. The signed webhook then reported **failed, 131031**, correlated using hashed message reference `f3fc27bca826`. The callback's public challenge passed before the send. This confirms successful API submission and failure at Meta's delivery stage. No handset delivery claimed; no additional retries planned while restricted.

An initial Newman sandbox syntax collision prevented collection assertions from executing, without preventing either HTTP request. Corrected the scripts to use redeclarable variables; read-only reruns confirmed **2 health assertions, 1 expected failure because Meta reports BLOCKED**, with no syntax/runtime failure beyond that assertion. No additional send was used to verify this fix. The send outcome above is established by its real HTTP response and signed failure webhook, not by the initially skipped assertion.

For future read-only checks, install the `newman` module in an isolated temporary directory, then run `node backend/scripts/run_postman_check.cjs <absolute-path-to-node_modules/newman>`. No runner dependency was added to the application. Syntax was checked with `node --check`. Newman is deprecated but supports the v2.1 collection used here; this is a one-off diagnostic, not a new production dependency.
