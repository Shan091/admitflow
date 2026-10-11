# Project decisions

Record consequential choices here. Each entry is short; update it when evidence changes a choice.

1. **Demo channel — Telegram webhook through FastAPI.** Telegram sends updates to the public
   HTTPS `/api/v1/webhooks/telegram` route using a configured secret-token header. The app does not
   run `getUpdates` polling; registering or clearing the webhook is an operator action.
2. **Runtime and persistence — one FastAPI process and SQLite.** This is enough for one seeded
   demo tenant; no Redis, TaskIQ, Postgres, or separate frontend in this scope.
3. **Architecture — domain/services/adapters.** Keep one real adapter per boundary; introduce a
   small Protocol only where injection or a test double needs it. No speculative ports framework.
4. **Eligibility and fees — code-owned gates, honestly labeled.** Structured seed data and Python
   rules determine undergraduate eligibility and all prices; model output cannot change
   either. For other complete catalog entries, a learner self-report against listed entry
   requirements is only an unverified test-payment gate, never a verified eligibility decision.
5. **Knowledge retrieval — OpenAI embeddings + SQLite vectors + NumPy cosine.** Embed each seeded
   FAQ's canonical question plus a few curated search phrasings with `text-embedding-3-small`;
   keep the answer as a separate stored value. Version the cached-vector key when this text profile
   changes. No general upload/parser or vector DB.
6. **Fail-closed retrieval and calibrated initial thresholds.** Use cosine `0.58` and top-result
   margin `0.05`; a live fixed set passed 15 expected FAQ variants and abstained on 12 unsupported
   questions. Its lowest expected score was `0.648`, and highest unsupported score was `0.491`.
   These small synthetic cases are calibration evidence, not guarantees. Abstain on weak,
   ambiguous, or unavailable retrieval.
7. **Fee routing and fee payment.** Route application-fee questions to structured course data
   before RAG; send unknown tuition/hostel charges and refund requests to an explicit safe response.
   Exclude amounts from free-form FAQ chunks. Qualified demo applicants may receive a Razorpay
   Payment Link created in test mode from the server-owned course fee. Never accept a client amount
   or mark a payment paid from a browser redirect; accept only signature-verified webhooks. The
   first applied paid event sends one Telegram confirmation; duplicate events do not repeat it.
   Course access is not automatically provisioned. Live payments, refunds, uploads, and production
   finance workflows are deferred.
8. **Staff dashboard access.** Protect dashboard routes with one environment-configured staff
   username/password and a signed, HTTP-only, SameSite=Lax session cookie. No self-registration,
   roles, or production identity provider in the hackathon demo. Missing credentials fail closed.
9. **Demo data reset.** Provide a staff-only dashboard reset for lead, conversation, payment, and
   webhook-event records, protected by a session-bound CSRF token and typed confirmation. Keep
   course listings and FAQs so the demo can be run again; provider-side records are unaffected.
10. **Guidance scope and entry.** Keep guidance within the institution's own course catalog; this
    is interest-led course discovery, not general career counselling. The first turn offers known
    course, known field, guided exploration, and browsing/question paths. A student can change path
    without losing unrelated profile facts.
11. **Catalog scope.** Seed an illustrative Kerala course catalog with vocational/certificate,
    diploma, undergraduate, and postgraduate examples spanning tech/data, business/accounting,
    design/media, hospitality/tourism, and non-regulated vocational skills. Only recommend offerings
    whose required attributes and entry rules are complete. Do not invent regulated-program rules,
    employment outcomes, or institution facts.
12. **Student agency and exploration.** Use short conversational prompts and tap choices, with no
    aptitude score or personality label. Student-stated goals take priority when a parent is involved;
    preserve speaker attribution. The bot may gently challenge assumptions using verified facts,
    trade-offs, and alternatives, then leaves the decision to the student.
13. **Language and handoff.** Offer English, Malayalam, Hindi, and Hinglish as selectable
    preferences at any stage. Full translated response coverage and fluent-speaker review are not
    implemented yet; the demo must disclose that most replies remain English. Routine out-of-catalog
    questions and missing course facts get an agent-led, fail-closed recovery, not an automatic
    staff handoff. Keep staff handoff for explicit human requests, staff-only operations such as
    deletion, and critical real-world matters such as a payment dispute. Never imply a live contact
    or response time is configured.
14. **Admissions-cycle memory.** Retain the conversation and confirmed discovery facts through the
    admissions cycle, then expire them under a stated, configurable policy. Students request deletion
    through staff; staff perform the deletion. The exact retention interval and production privacy
    review remain open release gates.
15. **Level-aware discovery and application boundary.** Rank at most three complete illustrative
    catalog entries from explicit field, optional study-level, and optional activity choices. Use no
    aptitude score. Existing undergraduate rules remain deterministic. For other levels, show
    listed entry requirements and ask for a clearly explained self-report; do not reuse Grade 12
    rules or imply independent verification/admission. A positive response may unlock only the
    explicit demo application-fee step.
16. **Explicit fee continuation and honest payment follow-up.** Eligibility alone does not create a
    Razorpay link; the student must tap the demo fee continuation action. Payment confirmation says
    the dashboard shows paid status, while disclosing that live contact, response time, and course
    access are not configured.

17. **Disclosed OpenAI text processing with user controls.** Explain at `/start` that typed
    messages and bounded recent-chat context are sent to OpenAI while processing is enabled,
    messages are stored locally, and inputs must contain demo data only. Enable free-text AI by
    default; provide persistent opt-out/re-enable controls plus button-only exploration. This
    supersedes the earlier affirmative-consent gate as the hackathon product behavior; it is not a
    legal/privacy determination. Send at most the previous eight text messages, catalog-allowlisted
    facts, current stage, and selected language; never send a name, Telegram ID, or username. OpenAI
    leads conversational replies; Python validates facts and owns catalog matching, course details,
    eligibility, fees, payment, and state transitions. Disable Responses API storage; production
    privacy review remains a release gate.

18. **Study goals are catalog-owned evidence.** Every course carries a small set of catalog
    learning-goal tags. Extract only goals explicitly stated by the learner and validated against
    those tags. Ask one optional goal question only when a broad candidate set contains materially
    different goals; skip it when it is not useful or the learner declines. A stated goal filters
    recommendations and appears as an explanation. Do not infer a job, occupation, or outcome.

19. **Language support is a course-recorded trade-off.** Keep teaching medium distinct from listed
    discussion support. Offer at most one optional language-support question on a broad match when
    candidates share a teaching medium but list different support, unless another optional narrowing
    question was already used for that fact set. A stated preference filters to courses that list it;
    no-match recovery can reopen the set. Never infer proficiency or promise unlisted services.

20. **Project lifecycle from verified events.** Keep lifecycle stage separate from qualitative
    readiness, discovery step, hard eligibility, and payment status. Enter `payment_pending` only
    after a qualified learner explicitly requests and the app persists a Razorpay test link; enter
    `under_review` only after a signed event matches the stored link, reference, currency, and full
    amount. A dashboard handoff means queued for staff, not staff acceptance. Leave v1 form,
    enrollment, rejection, waitlist, and cold-lead stages unclaimed until those workflows exist.
    Numeric System-1 readiness scoring is not part of the hackathon demo.

21. **Preference corrections are scoped and explicit.** Do not reset a learner's whole profile
    because one message corrects one fact. Replace scalar values when a replacement is explicit;
    retract list values only when the current turn names the exact stored catalog value and
    category. Preserve unmentioned facts and other-speaker facts, and invalidate the prior match
    confirmation whenever preferences are corrected.

22. **Tap choices use the same adaptive student profile.** A student field tap replaces only the
    field choice; keep separate level, activity, goal, and support facts, then choose the next
    question from the resulting profile. Parent field/level taps are parent-attributed suggestions
    and must not mutate the student's lead mirror, profile, lifecycle step, or recommendation
    confirmation.

23. **Repeated uncertainty changes the next move.** Offer an unsure learner a small set of
    catalog-grounded activity/field starting points with no pressure to know a course name. If they
    remain unsure, stop asking the same open question and offer browse, field exploration, or pause;
    never recommend before the learner shares a relevant preference. Do not surface staff as the
    default recovery for uncertainty.

24. **Study format is an optional catalog-backed trade-off.** Ask only when a broad comparable set
    has more than one recorded delivery mode and no other optional narrowing prompt was used for
    that fact set. A learner may leave it open; an explicit preference filters recommendations and
    appears as a catalog-grounded reason. Do not imply a specific schedule, accessibility, or
    availability. Widen honestly when no complete course matches.

25. **Recommendation exploration does not imply course commitment.** Guided match cards open
    verified course details; the learner can return to the same current match list or
    explicitly continue to the applicable eligibility step (undergraduate code checks or the other-level
    prerequisite self-report). Only that explicit continuation sets the selected course. Known-
    course selection stays direct. Stale detail/list callbacks must revalidate current confirmed
    learner facts and ranked matches.

26. **Non-informative turns are interruptions, not answers to the pending prompt.** If text adds
    no explicit preference, correction, or uncertainty and is not a routed FAQ/course/staff action,
    acknowledge the request without replaying the same discovery poll. Preserve facts and pending
    state, and offer relevant next actions. When processing the message cannot be classified or
    handled, do not invent a preference.

27. **AI leads free-text conversation; code owns consequential actions.** For AI-enabled turns,
    provide the model the current message, at most the previous eight chat messages, safe catalog-
    allowlisted profile facts, current conversation stage, and selected response language. The model
    handles greetings and assistant-identity questions naturally, uses context to avoid repetitive
    questions, and drafts the next response. Python still validates extracted preferences, enforces
    state and stale-callback checks, grounds FAQ answers in retrieval, and calculates course
    matches, eligibility, and fees. Only an explicit staff request creates a staff-request handoff.

28. **Escalate only for a person-requested or critical staff action.** Course exploration, unsupported
    preferences, out-of-catalog questions, weak FAQ retrieval, and unavailable course facts remain
    agent-led. The agent must admit uncertainty, never invent a fact, and offer a useful next step.
    Create staff handoffs only when the learner explicitly asks for a person or when a staff-only or
    critical real-world action requires it, such as deletion or a payment dispute. This updates the
    earlier default to refer unsupported or sensitive needs to staff.

29. **Every complete course may reach test payment through its disclosed eligibility step.**
    Undergraduate offerings keep their code-checked Grade 12/marks rules. Other complete offerings
    ask whether the learner meets that course's listed entry requirements. Record the
    student's self-report with course attribution; a positive response can proceed to the existing
    explicit, server-priced Razorpay test-fee action, while a negative/unsure response cannot. Never
    present a self-report as verified eligibility, admission, or enrollment. Stale prerequisite
    buttons must not qualify a different selected course.

30. **Langfuse debugging traces include content and identifiers.** When both Langfuse project
    keys are configured, trace inbound messages, AI replies, Telegram user/chat IDs, and saved
    learner facts alongside OpenAI generations. Tell users this at `/start`; this is a third-party
    transfer, not local-only telemetry. Tracing is optional and failures must not stop admissions
    behavior. Keep Langfuse credentials in `.env`, out of Git.

## References

- OpenAI embeddings: https://developers.openai.com/api/docs/guides/embeddings
- OpenAI Decisions: https://developers.openai.com/api/docs/guides/decisions
- OpenAI Structured Outputs: https://developers.openai.com/api/docs/guides/structured-outputs?api-mode=responses
- Python Telegram Bot async lifecycle:
  https://github.com/python-telegram-bot/python-telegram-bot/wiki/Frequently-requested-design-patterns
- Razorpay Payment Links API: https://razorpay.com/docs/api/payments/payment-links/
- Razorpay webhook security checklist: https://razorpay.com/security/checklist/
- UNESCO, Languages matter: global guidance on multilingual education:
  https://www.unesco.org/en/articles/languages-matter-global-guidance-multilingual-education
