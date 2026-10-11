# Feature: conversational career-informed course guidance

## Outcome

Replace a course-menu-first experience with a natural multi-turn conversation that helps a learner
understand what they want to study, then compare suitable courses. The agent should adapt to what a
learner has already said: a student who knows a course can jump to it, one who knows a field can
compare relevant offerings, and an undecided student can explore from concrete interests and goals.
Learners can ask unrelated admissions questions, change direction, pause, resume, and correct the
agent without restarting or losing unrelated facts.

The long-term goal is production-grade guidance. The current Telegram app remains a fictional
single-tenant hackathon demo until real institution data, privacy controls, age policy, localization,
human escalation, and operational requirements are verified.

## Evidence and design basis

- The v1 product defines lifecycle stages as a record of where a lead stands, not a mandatory
  sequence. Each turn reloads recent messages and facts, routes the message, updates the readiness
  signal, dispatches to a handler, validates the response, then persists the turn.
- Career-guidance research supports conversations and active exploration. Social Cognitive Career
  Theory offers a useful non-test lens: interests develop alongside learning experiences,
  self-efficacy, expected outcomes, goals, supports, and barriers. This is a conversation-design
  framework, not a basis for diagnosing or scoring a learner.
- Sources currently reviewed: OECD, [*Career Conversations* (2021)](https://doi.org/10.1787/15b83760-en);
  Lent, Brown & Hackett, [*Toward a Unifying Social Cognitive Theory of Career and Academic
  Interest, Choice, and Performance* (1994)](https://doi.org/10.1006/jvbe.1994.1027); [NCERT Career
  Guide](https://ncert.ncert.org.in/CareerGuide.php?ln=en); [NCERT My Career
  Advisor](https://mycareeradvisor.ncert.gov.in/); and India's [National Career
  Service](https://www.dge.gov.in/ncs).
- These sources do not establish that an AI conversation is equivalent to a trained career
  counsellor. Claims about AI effectiveness require direct evaluation.

## Current-state findings

- `/start` already opens with an exploratory question and shortcuts; it no longer lists courses as
  the first response.
- The seed now contains 50 fictional course offerings, ten in each of five fields, spanning four
  education levels. This does not imply that every field offers every level.
- Discovery extraction currently records course, field, education level, interest, activity,
  uncertainty, and correction. The extractor sees the current message and the allowlisted catalog.
- The service now asks for one complementary signal when context is thin, then reflects the
  learner's stated interests/activity/level and waits for confirmation before showing course cards.
  Confirmation is tied to a fingerprint of the current facts, so corrections and path changes make
  old buttons stale. A broad match may now receive one optional follow-up based on fictional
  course learning-goal tags. It still does not explore learning experiences, expected outcomes,
  constraints, or barriers in a coherent adaptive dialogue.
- The user confirmed institution-course guidance only, using career-guidance conversation methods
  to explore interests and study goals. Requests beyond the fictional catalog remain out of scope
  and are referred to the staff handoff; do not add occupation or job predictions.
- No affirmative consent step is required. Typed messages are disclosed as OpenAI-processed, and
  the learner can still turn that processing off.
- Current follow-up implementation adds fictional course-owned learning-goal tags and one optional
  question when a broad candidate set differs on those tags. It can be skipped or resumed and is
  evidence of only a small adaptive slice, not a complete goals/barriers exploration or production
  quality evaluation.
- Course records also distinguish the teaching medium from discussion/language support. For a broad
  match whose candidates have one teaching medium and materially different recorded support, the
  service can offer one optional support preference, unless it already used the optional goal
  question for that fact set. It filters only on a listed support label; it does not infer
  proficiency or promise support outside the course record. A learner may leave it open.
- Course matching uses direct overlap with seeded interests and activities. It has a deterministic
  sufficiency/confirmation policy and a fixed catalog-verified matrix across all 20 field/level
  pairs, plus mixed-field and abstention cases. This checks consistency with the fictional catalog;
  it is not a counsellor-reviewed dialogue evaluation, and there is no validated general-career
  evidence corpus.
- A student correction turn now preserves preferences it does not mention. It can retract only
  exact catalog-allowlisted values for the active speaker; student additions, retractions, and
  replacements invalidate old recommendation confirmations. Parent-only notes remain attributed
  separately and do not rewrite the learner's recommendation signature. This is still not a general
  fact-provenance or conflict-resolution system and needs broader dialogue evaluation.
- Field and guided-exploration entry paths expose their intended field choices. A prior step-state
  bug that changed `explore` to `field` and replaced its prompt on resume was fixed and verified in
  the current demo.
- The tap-based known-field handler still asks a fixed level question even when another signal
  would be more useful. Parent field/level taps also previously mutated learner-level state. The
  current slice routes student field choices into the shared adaptive policy, preserves independent
  profile facts when the field changes, and keeps parent suggestions separate.
- Repeated “not sure” turns previously returned the same open question indefinitely. The current
  policy gives one concrete catalog-grounded exploration prompt and then switches to browse, pause,
  or staff options without implying a course match.

## v1 lifecycle mapping

The v1 spec describes lifecycle as a record of observed progress rather than a mandatory dialogue.
The Telegram demo keeps that idea while not importing v1's WhatsApp, numeric System-1 readiness
score, application-form, or re-engagement machinery:

| v1 lifecycle stage | AdmitFlow demo meaning and transition |
| --- | --- |
| `new` | Lead exists, but the learner has not chosen a path yet. |
| `discovering` | Learner has entered browsing or course exploration; pauses are separately recorded as the demo-only `paused` stage and `/resume` restores the saved step. |
| `qualifying` | Learner selected an undergraduate sample whose eligibility rule is configured in code; collecting Grade 12 and marks answers stays here. |
| `admission_ready` | Code confirms the fictional undergraduate sample rule. It is not an admissions decision. |
| `payment_pending` | A qualified learner explicitly continued and a valid Razorpay test link was persisted. A failed/unconfigured creation does not advance here. |
| `under_review` | A matching paid event passed signature, link/reference, currency, and full-amount checks and was saved. Staff review is still required; this does not enroll the learner. |
| `handed_off` | A request is queued in the staff dashboard with `handoff_status=pending`; the demo does not track a staff acceptance, so this does not mean a counsellor has responded. |
| `form_collecting`, `enrolled`, `rejected`, `waitlisted`, `cold` | Not implemented. The demo must not claim these states or infer them from conversational tone or a payment. |

`readiness_status` remains a separate qualitative operational hint (`unknown`, `exploring`,
`considering`, `ready_to_apply`, or `needs_staff`); hard eligibility stays in the code-owned
qualification result. The numeric readiness score and automatic cold-lead transitions in v1 are not
part of this hackathon slice.

## Proposed turn model

Each incoming turn should use the same loop, while selecting the next action from current context:

1. **Triage and interrupts:** handle opt-out, explicit human request, urgent/sensitive content,
   language change, FAQ/fee/payment questions, deletion, and course/path changes before discovery.
2. **Rebuild context:** load the recent conversation and attributed facts; retain verified facts,
   unresolved questions, corrections, current learner/speaker, selected course, and lifecycle stage.
3. **Interpret this turn:** extract only explicitly stated facts using a strict schema. Keep learner
   and parent statements attributed separately. Never infer ability, personality, marks, identity,
   or likely outcomes from demographics or writing style.
4. **Choose one useful next move:** if the learner knows a course, resolve it directly; if they know
   a field, clarify desired study level or course differences only when needed; if unsure, ask one
   short question about a concrete activity, learning experience, goal, or practical concern. Do
   not repeat facts already established. Offer optional tap replies without forcing a path.
5. **Reflect and correct:** when enough facts exist to compare options, briefly summarize what the
   agent understood and invite a correction before relying on a material assumption.
6. **Compare, do not pronounce a winner:** show at most three complete catalog offerings with
   source-backed fit reasons, meaningful differences, prerequisites, trade-offs, and unknowns.
   Explain that the learner chooses; provide an ask-more, revise, browse, or staff-handoff action.
7. **Transition only when appropriate:** move to code-owned qualification after a learner selects
   an offering or asks about applying. Eligibility and money remain deterministic. Enrollment
   readiness is soft and separate from hard eligibility.
8. **Persist and resume:** store the exchange, fact provenance, last useful question, and state so a
   later turn can continue without forcing the learner to repeat themselves.

This is an adaptive turn loop, not an eight-question script. Greetings, uncertain replies, and
unsupported media should receive a graceful clarification or available action, not a spurious
handoff. Repeated ambiguity, unsupported catalog claims, sensitive situations, or user-requested
human support should produce a truthful staff-dashboard handoff; no contact/SLA may be invented.

## Existing decisions to preserve

- Scope is institution-course recommendations only, with unsupported needs handed to staff. Use
  career-guidance conversation techniques while recommending only verified institution offerings.
- Use conversation and optional taps; no aptitude score, personality label, or single objectively
  “right” course.
- Support vocational/certificate, diploma, undergraduate, and postgraduate learners; the fictional
  Kerala catalog presently covers tech/data, business/accounting, design/media, hospitality/tourism,
  and non-regulated vocational skills.
- Student preferences lead when a parent participates; record whose preference is whose.
- Gently challenge a mistaken assumption using verified facts, alternatives, and trade-offs, then
  leave the choice with the learner.
- English, Malayalam, Hindi, and Hinglish are selectable. Most non-discovery replies still require
  translation and fluent-speaker review.
- Use complete verified course facts only. Keep fees, hard eligibility, payment, and course facts
  code-owned. Do not invent regulated requirements, institution details, job prospects, or placement
  guarantees.
- The demo has no real counsellor contact or response-time promise. Human work appears in the staff
  dashboard; the reply says contact details are not configured.
- OpenAI text processing is disclosed and on by default. The learner is not asked for consent or
  required to complete a consent step; persistent opt-out/re-enable controls remain. The demo uses
  fictional text only. This does not resolve
  production legal/privacy obligations or age-appropriate processing.

## Acceptance criteria

- `/start` asks an open question before displaying a course list and offers optional shortcuts for
  known course, known field, exploration, and browsing/questions.
- A learner can answer in natural language over multiple turns. The next question uses the learner's
  existing facts and asks only for information that can change the next recommendation or action.
- For broad candidates, ask at most one optional narrowing question per current fact set: a
  catalog-grounded goal question when goals differ; otherwise a language-support preference when
  candidates share a teaching medium but differ in recorded support; otherwise study format when
  the explicit sample-catalog modes differ. Skip optional prompts when a course is known, the
  relevant preference is already stated, or the candidate set does not differ. The learner may
  leave any preference open. Never infer language proficiency, schedule, access, or unrecorded
  teaching/support services.
- A known-course learner can jump directly to that offering; ambiguous/unlisted names are clarified
  without inventing a match.
- An unsure learner receives a short, low-pressure prompt anchored in things they enjoy, have tried,
  want to learn, or hope study will help them do. No formal assessment or score is produced.
- If the learner remains unsure, the next response changes to browse/pause/staff choices rather than
  repeating the same prompt; no recommendation is shown until they share a relevant preference.
- Before a material recommendation, the system reflects its understanding and requires a clear
  confirmation; typed corrections or stale tap replies cannot surface recommendations from old
  facts, while unrelated valid facts remain intact.
- Correcting or withdrawing one preference preserves other explicit facts and the other speaker's
  profile. A retraction must match a stored, catalog-allowlisted fact for the current speaker;
  arbitrary model text cannot delete or overwrite unrelated facts.
- A recommendation is based on complete catalog records, includes provenance/fit reasons and real
  trade-offs, and does not imply admission, employment, earnings, or that one option is objectively
  best.
- A guided recommendation opens verified fictional course details first. Returning restores the
  current confirmed match list; only an explicit continue action enters eligibility or staff
  review. Detail and continue callbacks revalidate the current confirmed profile and top matches;
  stale actions cannot select an old course or enter eligibility. The known-course shortcut remains
  direct.
- Course selection, eligibility, costs, FAQ answers, parent attribution, and payment remain safe and
  code-verified; unsupported levels or missing data create a truthful handoff.
- A learner can interrupt discovery to ask an FAQ/fee question, change language/path, pause, resume,
  request staff, or delete data without the bot becoming stuck in a questionnaire.
- With OpenAI processing enabled, the model receives the current text and at most eight preceding
  text messages, safe profile facts, the current guidance stage, and selected response language.
  Its natural reply uses context and leads one useful next turn. Greetings and questions about
  AdmitFlow itself never become unsupported-FAQ handoffs. Staff handoff is created only for an
  explicit human request or a verified policy requiring staff.
- The `/start` notice discloses that recent conversation context can be sent to OpenAI. Telegram
  identifiers and usernames are excluded; Responses API storage is disabled; opt-out sends no typed
  content or history to OpenAI. Code still owns catalog facts, eligibility, prices, payment, and
  state transitions.
- A message that adds no preference, correction, or explicit uncertainty does not silently get
  treated as an answer to the current poll. Acknowledge unrelated/non-informative text, keep saved
  facts and the pending step intact, and offer relevant actions without repeating the same question.
  FAQ, fee, browse, and staff requests continue through their explicit interrupt routes.
- After AI opt-out, typed content does not go to the discovery model, intent router, or embedder.
- Add deterministic fake-API coverage for greetings, "who are you?", contextual follow-up,
  bounded history inclusion/exclusion, selected language, and human-request versus bot-identity
  routing. Verify that no identifier reaches the model and opt-out prevents model calls.
- Failure of extraction, retrieval, database, messaging, or the model does not create partial facts,
  fabricate an answer, send duplicate payment actions, or strand the learner without an available
  recovery action.

## Verification plan

- Add turn-sequence tests rather than testing only isolated extractions: vague opening, follow-up,
  correction, known-course shortcut, interest change, recommendation, interruption, and resume.
- Test unrelated free text during each pending guidance state (including confirmation), zero-signal
  model extractions across `other`/`out_of_scope`/`discovery`, and verify no repeated poll, lost
  facts, or accidental state advance through Telegram text handling.
- Verify study-goal extraction, metadata completeness, skip, correction, signature freshness, and
  expected-course ranking tests for the optional goal question.
- Verify language-support extraction allowlisting and preference behavior, including no prompt for
  known-course/uniform candidates, skip/resume/correction, stale-button invalidation, and recovery
  when no complete candidate matches a stated support preference.
- Verify study-format extraction and catalog allowlisting, adaptive prompt policy, skip/resume,
  stale-button invalidation, preference filtering/explanations, parent attribution, and honest
  widening when a selected format leaves no complete match.
- Verify match -> detail -> back-to-matches -> pause/resume -> explicit eligibility/staff
  continuation, including stale detail/continue callbacks, expired results state, and Telegram
  callback dispatch.
- Evaluate fixed fictional dialogues in English, Hindi, Malayalam, and Hinglish; test code-switching,
  short/empty answers, spelling variation, ambiguity, contradictions, prompt injection, parent-child
  disagreement, and unsupported/regulated interests.
- Evaluate retrieval and recommendations against a human-reviewed golden set with expected matches,
  acceptable alternatives, required facts, and abstentions. Track coverage as well as incorrect-match
  rate; do not tune to maximize recommendations at the expense of honesty.
- Keep the catalog-verified field/level matrix current when sample offerings change; it must list
  exact expected IDs, including empty catalog cells, and assert that unsupported or conflicting
  preferences abstain.
- Verify that model output cannot create a course, prerequisite, fee, eligibility result, factual
  career claim, or unverified institutional promise.
- Run `bash scripts/verify.sh`, `git diff --check`, migration/data-preservation tests, and end-to-end
  Telegram/dashboard tests. Record the exact SHA and CI result before marking implementation tasks
  complete.

## Production gates and open decisions

- **Age policy:** youngest user, treatment of minors, guardian participation and privacy obligations.
- **Catalog:** new domains/courses, first real institution's catalog, official source ownership,
  completeness and update cadence. Fictional seed data is demo-only.
- **Guidance data:** complete source ownership and review for the first real institution's course
  facts; provenance, effective date, update cadence, stale-data behavior, and referral when absent.
- **People and operations:** real counsellor contact, escalation SLA, business hours, staff takeover,
  monitoring, audit, incident response, and model/provider outage policy.
- **Privacy/security:** documented purpose and lawful processing basis, age-appropriate notice,
  data minimization, retention/expiry implementation, deletion verification, tenant isolation,
  encryption, access controls, and external processor review.
- **Quality:** native-speaker review, counsellor review, bias/equity testing, evidence-based
  recommendation evaluation, safety review, and production monitoring thresholds.

No hackathon smoke test or green unit suite alone satisfies the production gates above.
