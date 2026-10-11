# AdmitFlow — Hackathon Demo Spec

## Mission

Help a prospective student explore an institution's courses and get accurate, remembered
admissions guidance through a conversational channel.

## Product and audience

AdmitFlow is an admissions-engagement assistant for students and parents and a lightweight lead
view for staff. The hackathon version uses Telegram as its demo channel. It uses one seeded course
catalog with illustrative details; it does not submit real applications or make admission decisions.

## Hackathon capability map

- **Discovery:** Telegram discloses OpenAI processing, bounded recent-chat context, and local
  message storage at `/start`; free-text discovery is enabled by default and a persistent control
  turns it off or back on. While enabled, OpenAI receives the current message plus at most the
  previous eight text messages, safe catalog-allowlisted profile facts, current guidance stage, and
  selected language. No Telegram identifier or username is sent. OpenAI interprets context, leads
  the natural conversation, and drafts free-text replies. Python validates extracted facts and owns
  state, catalog matching, course details, eligibility, fees, and payment actions. FAQ answers still
  come from seeded retrieval. Opt-out prevents external AI calls for typed content while preserving
  button-based exploration. No language ability, aptitude score, or personality label is inferred.
- **Qualification:** Configured undergraduate rules are checked by Python. For other levels, the learner
  can self-report whether they meet the selected course's listed entry requirements. A
  positive response unlocks only the demo fee step; it is not verified eligibility or an admission
  decision. A negative/unsure response cannot reach payment. The app does not reuse a Grade 12 rule
  across every program.
- **Memory:** SQLite persists lifecycle stage separately from the existing qualification state,
  qualitative readiness, discovery path/step, selected course, attributed facts, language choice,
  messages, and handoffs. `/resume` restores the last discovery question. Most bot copy is still
  English despite saving a language preference; full translation remains outstanding.
- **Knowledge:** OpenAI `text-embedding-3-small` embeds seeded FAQ questions with curated search
  phrasings; NumPy cosine search selects relevant chunks; uncertain retrieval fails closed with an
  agent reply that admits the gap and offers rephrasing or catalog browsing, not an automatic
  staff handoff.
- **Staff view:** A local FastAPI dashboard with environment-configured staff login shows leads,
  attributed discovery facts, conversation history, pending handoffs, and payment status. Staff can
  delete one lead's local data or reset all demo records while preserving the course catalog.
- **Money boundary:** Application-fee answers come from structured course data; unknown tuition or
  hostel charges receive a safe, non-escalating response. Refunds or actual payment disputes remain
  staff matters. No model calculates or negotiates fees.
  A code-eligible undergraduate user or a learner who self-reports meeting the listed prerequisites
  for another level must explicitly choose to continue before receiving a Razorpay test-mode Payment
  Link using the server-owned application fee; verified webhooks update payment status and send one
  Telegram confirmation. Self-report is not verification or admission. No live follow-up contact or
  response time is configured and course access is not provisioned automatically.

## Demo success criteria

1. A Telegram user can pick an entry path and receive an explainable recommendation from complete,
   structured catalog facts, or browse without applying.
2. Undergraduate eligibility is a deterministic result of configured rules and answers; other
   education levels use a clearly explained, course-bound prerequisite self-report and are not
   misclassified by a generic Grade 12 rule.
3. The lead and messages remain after app restart and appear in the dashboard.
4. A seeded FAQ question retrieves its source; unrelated/ambiguous questions do not fabricate an
   answer; fee questions bypass RAG.
5. README setup steps work, `scripts/verify.sh` passes, and the final submitted commit SHA is
   recorded with actual check results.
6. Staff must log in before viewing lead details; a verified Razorpay test webhook can update a
   demo payment to paid, while invalid webhook signatures cannot.
7. `/start` discloses OpenAI processing, bounded recent-chat context, local storage, and demo-only
   input before free-text use. AI is enabled by default; after opt-out, typed discovery/FAQ text
   causes no OpenAI call and tap-based exploration remains available. Extraction failures and
   unsupported values never create recommendations outside the course catalog.

## Roadmap

- **Hackathon:** Foundation, Telegram qualification, authenticated local dashboard, seeded
  embedding retrieval, Razorpay test-mode application fee links and verified payment status,
  interest-led discovery, explicit/critical staff handoffs, and staff-mediated local deletion.
- **Deferred:** Live-mode payments, file uploads/PDF parsing, WhatsApp, workers, multi-tenant
  onboarding, deployment, and production privacy controls.
