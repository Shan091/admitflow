# Feature: adaptive, interest-led course discovery

## Outcome

Replace the fixed course-first opening with a Telegram conversation that supports students who
already know a course, students who know a field but not a course, and students who want help
exploring. Recommendations come only from the institution's course catalog and explain their fit
using confirmed catalog facts. The first catalog is fictional and clearly marked as sample data.

The feature is a course-discovery and admissions guide, not a general career-counselling service,
aptitude test, personality assessment, or promise of a career outcome.

## Agreed product behavior

- The audience spans vocational/certificate, diploma, undergraduate, and postgraduate learners;
  parent/guardian participation is supported. The student's stated goals lead, and the bot records
  whether information came from the student or parent.
- The fictional Kerala catalog covers tech/data, business/accounting, design/media,
  hospitality/tourism, and non-regulated vocational skills. Do not seed regulated professional
  programs without authoritative requirements and review.
- `/start` offers four paths: **I know the course**, **I know the field**, **Help me explore**, and
  **Just browsing / ask a question**. A student may switch paths without losing useful profile
  facts, and can skip, edit, pause, resume, or change language at any time.
- Support English, Malayalam, Hindi, and Hinglish. Language changes must not reset conversation
  state. Until localized copy is reviewed by fluent speakers, label it as demo copy and do not claim
  production-grade localization.
- Exploration uses short conversational prompts and tap choices. Do not assign aptitude scores,
  personality types, or a single “right course.” The formal-assessment choice is conversation-only
  for now; revisit instruments only after local, age, language, cultural, and license review.
- It is acceptable to gently challenge an assumption with verified facts, trade-offs, and
  alternatives, then let the student decide. For language concerns, distinguish medium of
  instruction, required proficiency, and available language support. Explain possible benefits of
  learning another language only when supported by an identified source; never promise employment
  or success from doing so.
- A recommendation must be supported by complete course facts. Present a small set of alternatives
  with reasons and trade-offs, not a psychological match score. If no offer fits or required facts
  are missing, say so and create a staff-dashboard handoff containing the conversation context.
  No counsellor contact or response time is configured for this demo; say follow-up details are not
  configured and never invent an SLA.
- Continue to use the v1 lifecycle, with lifecycle stage, hard eligibility, and soft enrollment
  readiness stored as separate concepts. Eligibility and fees remain code-owned. Payment links are
  downstream and only offered when the student chooses to continue.
- Keep the conversation/profile through the admissions cycle, expire it under an explicitly stated
  retention policy, and honor deletion requests through staff. The retention interval is not yet
  selected; make it configurable and do not claim automatic expiration until implemented and tested.

## Current implementation boundary

- Implemented locally in this milestone: additive course/lead migrations, fictional offerings,
  four entry paths, field/level/activity prompts, explainable catalog matching, pause/resume,
  student/parent fact attribution, staff handoffs/dashboard visibility, per-lead deletion, and an
  explicit pre-payment continuation tap.
- Not complete: translated discovery and qualification copy (the language preference is saved and
  can be switched, but most replies remain English); authoritative verification of any fictional
  self-reported prerequisite; and automatic admissions-cycle expiry.
- Production gates still open: exact retention interval, privacy/legal review, and fluent-speaker
  review of all localized copy. Do not imply any of these are finished in the demo.

## Acceptance criteria

- [ ] `/start` does not immediately list courses. It presents the four entry paths and a language
  change action.
- [ ] A known course is looked up directly; ambiguous names are clarified; unlisted courses are
  disclosed as unavailable and offered a catalog browse or staff handoff.
- [ ] A known field and an unsure student receive different next prompts; prompts are short,
  optional, resumable, and preserve profile facts across path changes.
- [ ] Supported education levels and student/parent speaker roles are persisted distinctly.
- [ ] A recommendation contains only catalog course IDs and verified attributes; missing facts are
  described as unknown. It explains why options appeared and includes meaningful differences.
- [ ] Undergraduate eligibility is evaluated by course-specific deterministic rules. For other
  levels, the bot clearly labels the learner's prerequisite answer as self-reported and demo-only;
  it does not call that verification or admission. Changing a course clears answers that no longer
  apply, but preserves unrelated student-stated interests.
- [ ] An unsupported interest, missing catalog details, or no plausible match never causes the bot
  to invent an offering or requirement; it creates a staff handoff and truthfully explains that no
  live contact or response time is configured.
- [ ] A knowledge question, fee question, explicit staff request, language switch, stop, or restart
  can interrupt discovery safely and resume without losing unrelated state.
- [ ] Student preferences take priority over parent preferences; the bot records speaker attribution
  and avoids treating a parent's preference as the student's own.
- [ ] English, Malayalam, Hindi, and Hinglish are selectable at every stage; localized responses
  preserve the same facts, options, safety rules, and state transitions.
- [ ] Dashboard staff can see lifecycle stage, discovery facts with attribution, the full conversation,
  and pending handoffs. Staff-mediated deletion and admissions-cycle expiration remove the intended
  records without deleting catalog content.
- [ ] Payment creation remains impossible before the applicable sample gate (code-checked
  undergraduate rules or positive self-report for another course) and an explicit choice to
  proceed; amounts remain server-owned.

## Dependencies and decisions

- Dependencies: current Telegram webhook, SQLite repository, course seed catalog, AdmissionsService,
  FAQ retrieval, staff dashboard, Razorpay test payment flow, `tasks/todo.md`.
- Settled decisions: institution catalog only; fictional broad catalog; Telegram first; four
  supported languages; conversational exploration without formal tests/scores; student-first
  preferences; staff-mediated deletion; staff dashboard handoff with no fabricated contact/SLA;
  admissions-cycle retention with a configurable interval.
- See `docs/DECISIONS.md` entries 10–16.

## Implementation slices

- [ ] Expand and validate the fictional course schema/catalog across the agreed education levels and
  fields; add an additive SQLite migration that preserves existing records.
- [ ] Add attributed, editable discovery facts and separate lifecycle stage from qualification
  substate and enrollment-readiness signals.
- [ ] Add direct-course, known-field, explore, and browse entry paths, including skip/back/change/
  pause/resume and safe interrupt handling.
- [ ] Implement explainable catalog matching over structured interest/activity/level/constraint
  facts. Hard requirements filter candidates; soft preferences rank alternatives. No psychometric
  score is produced.
- [ ] Add staff handoff state and dashboard visibility; tell students that live contact/response
  details are unconfigured.
- [ ] Add supported-language flow copy and language switching; record localization review as a
  release gate.
- [ ] Add staff-mediated individual deletion and configured admissions-cycle expiration, preserving
  necessary operational audit data without retaining deleted chat content.
- [ ] Integrate deterministic course-specific qualification, grounded FAQ interruptions, and
  downstream test payment without regressing current protections.

## Verification

- [ ] Unit-test catalog validation, candidate filtering/ranking, explanation provenance, and
  qualification invalidation when the selected course changes.
- [ ] Test Telegram branches: known course, ambiguous course, known field, unsure, browse, no match,
  missing facts, parent/student attribution, language change, interrupt/resume, and duplicate updates.
- [ ] Test handoff persistence and truthful fallback with no contact/SLA configured.
- [ ] Test staff access, individual deletion, retention expiry, and the existing full-demo reset;
  test that catalog/FAQ seed data remains available.
- [ ] Add a fixed, fictional recommendation evaluation set across all catalog fields and levels,
  including unsupported interests, contradictory constraints, and language concerns.
- [ ] Run `bash scripts/verify.sh`; review privacy, credential safety, and demo claims; record exact
  test output and GitHub Actions result before marking checklist items complete or pushing.

## Risks and limitations

- The first catalog is fictional. It must be labeled clearly and must not be presented as a real
  college's offer, fee, eligibility, schedule, or placement outcome.
- Broad education-level coverage makes complete and consistent prerequisites essential. Incomplete
  records must be excluded from recommendations rather than filled by model guesswork.
- Localized copy needs fluent-speaker review before production claims. A user's language choice is
  not evidence of course-language proficiency.
- The current app is a single-tenant SQLite hackathon demo. Production readiness still requires a
  reviewed privacy/retention policy, appropriate consent for minors, tenant isolation, operational
  monitoring, and a real staff contact/escalation workflow.

## Open decisions

- Exact retention interval and applicable privacy/legal review before production rollout.
- Real staff contact/response-time configuration for a future deployment; none is configured for
  the current demo.
- Native-speaker review of each supported language before production release.
