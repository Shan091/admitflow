# Feature: Telegram course discovery and qualification

## Outcome

A prospective student can select a fictional course, answer two questions, receive a deterministic
eligibility result, and be visible with the conversation in the local staff dashboard.

## Acceptance criteria

- [ ] `/start` creates or resumes a lead and offers course buttons plus a browse-only option.
- [ ] Selecting a course asks whether Grade 12 is complete and then asks for overall marks.
- [ ] Python evaluates the seeded course rules; the model never sets eligibility.
- [ ] A browse-only student receives information without being forced into qualification.
- [ ] Inbound/outbound messages and answers persist across app restarts.
- [ ] The local dashboard shows the same lead, conversation, course, and result.
- [ ] Demo copy identifies the institution and results as fictional/sample.

## Verification

- [ ] Test eligible, ineligible, missing, malformed, and boundary answers.
- [ ] Test callback handling and persistence using fake Telegram updates.
- [ ] Test dashboard list/detail against the same SQLite records.
- [ ] Run `bash scripts/verify.sh` and one live Telegram walkthrough when a token is configured.
