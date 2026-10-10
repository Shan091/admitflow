# Project decisions

Record consequential choices here. Each entry is short; update it when evidence changes a choice.

1. **Demo channel — Telegram webhook through FastAPI.** Telegram sends updates to the public
   HTTPS `/api/v1/webhooks/telegram` route using a configured secret-token header. The app does not
   run `getUpdates` polling; registering or clearing the webhook is an operator action.
2. **Runtime and persistence — one FastAPI process and SQLite.** This is enough for one seeded
   demo tenant; no Redis, TaskIQ, Postgres, or separate frontend in this scope.
3. **Architecture — domain/services/adapters.** Keep one real adapter per boundary; introduce a
   small Protocol only where injection or a test double needs it. No speculative ports framework.
4. **Eligibility and fees — code-owned.** Structured seed data and Python rules determine
   eligibility and prices; model output cannot change either.
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
   fictional courses and FAQs so the demo can be run again; provider-side records are unaffected.
10. **Guidance scope and entry.** Keep guidance within the institution's own course catalog; this
    is interest-led course discovery, not general career counselling. The first turn offers known
    course, known field, guided exploration, and browsing/question paths. A student can change path
    without losing unrelated profile facts.
11. **Catalog scope.** Seed a clearly fictional Kerala institution with vocational/certificate,
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
    implemented yet; the demo must disclose that most replies remain English. Out-of-catalog or
    sensitive needs create a staff-dashboard handoff with conversation context. The demo has no
    live contact or confirmed response time, so it must say those details are not configured.
14. **Admissions-cycle memory.** Retain the conversation and confirmed discovery facts through the
    admissions cycle, then expire them under a stated, configurable policy. Students request deletion
    through staff; staff perform the deletion. The exact retention interval and production privacy
    review remain open release gates.
15. **Level-aware discovery and application boundary.** Rank at most three complete fictional
    catalog entries from explicit field, optional study-level, and optional activity choices. Use no
    aptitude score. Existing undergraduate sample rules remain deterministic; other levels are
    handed to staff for eligibility confirmation until course-specific rules are implemented.
16. **Explicit fee continuation and honest payment follow-up.** Eligibility alone does not create a
    Razorpay link; the student must tap the demo fee continuation action. Payment confirmation says
    the dashboard shows paid status, while disclosing that live contact, response time, and course
    access are not configured.

17. **Disclosed OpenAI text processing with user controls.** Explain at `/start` that typed
    messages are sent to OpenAI, locally stored, and must contain demo data only. Enable free-text
    AI by default; provide persistent opt-out and re-enable controls plus button-only exploration.
    This supersedes the earlier affirmative-consent gate as the hackathon product behavior; it is
    not a legal/privacy determination. Use stateless structured extraction of only the current
    message and fictional allowlisted course vocabulary. Code validates extracted facts and owns
    questions, recommendations, fees, and eligibility. No user name, chat ID, or transcript is sent
    as context; privacy/legal review remains a production gate.

18. **Study goals are catalog-owned evidence.** Every fictional course carries a small set of sample
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
    remain unsure, stop asking the same open question and offer browse, pause, or staff handoff;
    never recommend before the learner shares a relevant preference.

24. **Study format is an optional catalog-backed trade-off.** Ask only when a broad comparable set
    has more than one recorded delivery mode and no other optional narrowing prompt was used for
    that fact set. A learner may leave it open; an explicit preference filters recommendations and
    appears as a catalog-grounded reason. Do not imply a specific schedule, accessibility, or
    availability. Widen honestly when no complete sample course matches.

25. **Recommendation exploration does not imply course commitment.** Guided match cards open
    verified fictional course details; the learner can return to the same current match list or
    explicitly continue to the existing code-owned eligibility/staff path. Only that explicit
    continuation sets the selected course. Known-course selection stays direct. Stale detail/list
    callbacks must revalidate the current confirmed learner facts and ranked matches.

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
