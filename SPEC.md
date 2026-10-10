# AdmitFlow — Hackathon Demo Spec

## Mission

Help a prospective student explore an institution's courses and get accurate, remembered
admissions guidance through a conversational channel.

## Product and audience

AdmitFlow is an admissions-engagement assistant for students and parents and a lightweight lead
view for staff. The hackathon version uses Telegram as its demo channel. It is not a production
admissions system and uses a clearly fictional institution and seeded data.

## Hackathon capability map

- **Discovery:** Telegram starts with known-course, known-field, guided-exploration, and browse/
  question paths. Short optional field, education-level, and activity choices produce at most three
  catalog-only matches with reasons; no aptitude score or personality label is created. The seeded
  Kerala institute and all course facts are fictional.
- **Qualification:** Undergraduate sample rules are checked by Python. Other levels show their
  sample prerequisites and create a staff handoff for confirmation; the app does not reuse a Grade
  12 rule across every program.
- **Memory:** SQLite persists lifecycle stage separately from the existing qualification state,
  qualitative readiness, discovery path/step, selected course, attributed facts, language choice,
  messages, and handoffs. `/resume` restores the last discovery question. Most bot copy is still
  English despite saving a language preference; full translation remains outstanding.
- **Knowledge:** OpenAI `text-embedding-3-small` embeds seeded FAQ questions with curated search
  phrasings; NumPy cosine search selects relevant chunks; uncertain retrieval fails closed.
- **Staff view:** A local FastAPI dashboard with environment-configured staff login shows leads,
  attributed discovery facts, conversation history, pending handoffs, and payment status. Staff can
  delete one lead's local data or reset all demo records while preserving the fictional catalog.
- **Money boundary:** Application-fee answers come from structured course data; unknown tuition or
  hostel charges and refunds receive a safe response. No model calculates or negotiates fees.
  A code-eligible undergraduate user must explicitly choose to continue before receiving a Razorpay
  test-mode Payment Link using the server-owned application fee; verified webhooks update payment
  status and send one Telegram confirmation. No live follow-up contact or response time is
  configured and course access is not provisioned automatically.

## Demo success criteria

1. A Telegram user can pick an entry path and receive an explainable recommendation from complete,
   structured sample catalog facts, or browse without applying.
2. Demo undergraduate eligibility is a deterministic result of stored rules and answers; other
   sample education levels are not misclassified by a generic Grade 12 rule.
3. The lead and messages remain after app restart and appear in the dashboard.
4. A seeded FAQ question retrieves its source; unrelated/ambiguous questions do not fabricate an
   answer; fee questions bypass RAG.
5. README setup steps work, `scripts/verify.sh` passes, and the final submitted commit SHA is
   recorded with actual check results.
6. Staff must log in before viewing lead details; a verified Razorpay test webhook can update a
   demo payment to paid, while invalid webhook signatures cannot.

## Roadmap

- **Hackathon:** Foundation, Telegram qualification, authenticated local dashboard, seeded
  embedding retrieval, Razorpay test-mode application fee links and verified payment status,
  interest-led discovery, staff handoffs, and staff-mediated local deletion.
- **Deferred:** Live-mode payments, file uploads/PDF parsing, WhatsApp, workers, multi-tenant
  onboarding, deployment, and production privacy controls.
