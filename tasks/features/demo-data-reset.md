# Feature: staff demo-data reset

## Outcome

Staff can clear all student/demo transaction records from the dashboard and reuse the fictional
course and FAQ catalog afterward.

## Acceptance criteria

- [x] Only an authenticated staff session can invoke the reset.
- [x] The form requires a session-bound CSRF token and exact typed confirmation phrase.
- [x] A successful reset removes leads, conversations, payments, and Razorpay webhook event history.
- [x] The fictional institution, courses, FAQ content, and application configuration remain intact.
- [x] The dashboard confirms successful reset; failed confirmation/authentication does not delete.
- [x] Automated tests verify records removed, seeded content retained, and unauthorized/invalid
  requests rejected without data loss.
- [ ] GitHub Actions passes for the reset commit.

## Dependencies and decisions

- Dependencies: authenticated dashboard, SQLite repository.
- Decision: delete demo/student and payment records only; preserve the seed catalog/FAQ index so the
  running demo remains usable. Confirmation phrase: `DELETE ALL DEMO DATA`.

## Verification

- [x] `uv run pytest tests/test_app.py tests/test_repository.py -q` (12 passed)
- [x] `bash scripts/verify.sh` (42 passed; Ruff and strict mypy passed)

## Risks and limitations

- Reset cannot be undone. It is intended only for fictional hackathon demo records; staff must
  verify the phrase before submitting.
