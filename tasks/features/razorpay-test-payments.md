# Feature: Razorpay test-mode application payments

## Outcome

After a student meets the fictional sample qualification rule, offer a hosted Razorpay test-mode
Payment Link for the selected course's application fee and show staff the verified payment status.

## Acceptance criteria

- [x] Link amount/currency/course/lead association are derived from server-side records.
- [x] Link creation is unavailable without Razorpay test credentials and makes no implicit live-mode
  request.
- [x] Only a valid Razorpay webhook signature and matching known payment-link ID/reference/amount
  can transition payment state to paid; duplicate events are idempotent.
- [x] The first verified paid webhook sends one Telegram confirmation with a truthful next step;
  duplicate webhooks do not send duplicate confirmations.
- [x] Students can ask for payment status and receive only the status persisted from the verified
  webhook/payment-link lifecycle.
- [x] Payment-link creation errors do not claim payment succeeded or break qualification results.
- [x] Fake HTTP/webhook tests make no live Razorpay requests.

## Dependencies and decisions

- Dependencies: successful Telegram qualification, payment storage, dashboard.
- Decisions: `docs/DECISIONS.md` #7; Razorpay test-mode Payment Links.

## Implementation slices

- [x] Add payment schema and repository methods.
- [x] Add Razorpay Payment Link adapter and wire it to successful qualification.
- [x] Add signed webhook handling and dashboard payment status.
- [x] Notify the student after a verified payment and provide a Telegram payment-status lookup.
- [x] Add fake-based tests and document test-mode credentials/webhook setup.

## Verification

- [x] `uv run pytest tests/test_payments.py`
- [x] Full quality gate: `bash scripts/verify.sh` (32 passed)
- [x] Full quality gate after Telegram confirmation/status addition: `bash scripts/verify.sh`
  (41 passed); `git diff --check` passed.

## Risks and limitations

- Requires merchant test credentials and a publicly reachable webhook URL for an end-to-end event.
- Payment Links are only demonstrated in Razorpay test mode; no real charges or refunds are in scope.
