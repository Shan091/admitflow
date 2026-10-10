# AdmitFlow — Hackathon Demo Spec

## Mission

Help a prospective student explore an institution's courses and get accurate, remembered
admissions guidance through a conversational channel.

## Product and audience

AdmitFlow is an admissions-engagement assistant for students and parents and a lightweight lead
view for staff. The hackathon version uses Telegram as its demo channel. It is not a production
admissions system and uses a clearly fictional institution and seeded data.

## Hackathon capability map

- **Discovery:** Telegram updates arrive through a secret-validated HTTPS webhook; buttons show
  courses and a no-pressure browse path.
- **Qualification:** Structured answers are checked by Python against course rules.
- **Memory:** SQLite persists the Telegram lead, selected course, qualification answers, and chat.
- **Knowledge:** OpenAI `text-embedding-3-small` embeds seeded FAQ questions with curated search
  phrasings; NumPy cosine search selects relevant chunks; uncertain retrieval fails closed.
- **Staff view:** A local FastAPI dashboard with environment-configured staff login shows leads,
  conversation history, and payment status.
- **Money boundary:** Application-fee answers come from structured course data; unknown tuition or
  hostel charges and refunds receive a safe response. No model calculates or negotiates fees.
  Qualified demo users can receive a Razorpay test-mode Payment Link using the server-owned
  application fee; verified webhooks update payment status.

## Demo success criteria

1. A real Telegram user can browse, select a course, and complete the seeded qualification flow.
2. Eligibility is a deterministic result of stored rules and answers.
3. The lead and messages remain after app restart and appear in the dashboard.
4. A seeded FAQ question retrieves its source; unrelated/ambiguous questions do not fabricate an
   answer; fee questions bypass RAG.
5. README setup steps work, `scripts/verify.sh` passes, and the final submitted commit SHA is
   recorded with actual check results.
6. Staff must log in before viewing lead details; a verified Razorpay test webhook can update a
   demo payment to paid, while invalid webhook signatures cannot.

## Roadmap

- **Hackathon:** Foundation, Telegram qualification, authenticated local dashboard, seeded
  embedding retrieval, Razorpay test-mode application fee links and verified payment status.
- **Deferred:** Live-mode payments, file uploads/PDF parsing, WhatsApp, workers, multi-tenant
  onboarding, deployment, notification systems, and production privacy controls.
