# Feature: Razorpay test-mode application payments

## Outcome

After a student meets the fictional sample qualification rule, offer a hosted Razorpay test-mode
Payment Link for the selected course's application fee and show staff the verified payment status.

## Acceptance criteria

- [ ] Link amount/currency/course/lead association are derived from server-side records.
- [ ] Link creation is unavailable without Razorpay test credentials and makes no implicit live-mode
  request.
- [ ] Only a valid Razorpay webhook signature and matching known payment-link ID/reference/amount
  can transition payment state to paid; duplicate events are idempotent.
- [ ] Payment-link creation errors do not claim payment succeeded or break qualification results.
- [ ] Fake HTTP/webhook tests make no live Razorpay requests.

## Dependencies and decisions

- Dependencies: successful Telegram qualification, payment storage, dashboard.
- Decisions: `docs/DECISIONS.md` #7; Razorpay test-mode Payment Links.

## Implementation slices

- [ ] Add payment schema and repository methods.
- [ ] Add Razorpay Payment Link adapter and wire it to successful qualification.
- [ ] Add signed webhook handling and dashboard payment status.
- [ ] Add fake-based tests and document test-mode credentials/webhook setup.

## Verification

- [ ] `uv run pytest tests/test_payments.py`
- [ ] Full quality gate: `bash scripts/verify.sh`

## Risks and limitations

- Requires merchant test credentials and a publicly reachable webhook URL for an end-to-end event.
- Payment Links are only demonstrated in Razorpay test mode; no real charges or refunds are in scope.
