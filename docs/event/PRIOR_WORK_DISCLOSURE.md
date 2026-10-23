# Prior-work disclosure draft

AdmitFlow continues an existing repository. It was not created entirely during this
event. Confirm this disclosure with the organizers and their current eligibility rules
before submitting it.

The starting foundation included FastAPI, PostgreSQL models and migrations,
Redis/TaskIQ, encryption and audit helpers, rule evaluation, retrieval and guardrail
modules, and a WhatsApp dispatcher/transport. Actual WhatsApp delivery was blocked
by a provider account restriction. Existing modules and historical tests did not
establish a complete student journey or staff dashboard.

The current work introduces Telegram institution/lead identities, private-chat
transport, durable encrypted inbox/outbox, conversation memory and corrections,
course/batch callbacks, integrated eligibility, source-quoted FAQs and abstention.
It also introduces authenticated institution file/folder ingestion and the Next.js
knowledge, inquiry, conversation and human-request screens. OpenAI is the active
inference and embedding provider. Applications, payments, co-pilot and follow-ups
remain later milestones.

The saved baseline is in docs/planning/archive/. Current implementation and actual
validation results are in tasks/todo.md, including failures and delivery uncertainty.
Development demonstrations use synthetic institution references and student answers;
no customer, revenue or measured efficiency claim is made.

The user reports that no surprise requirement or revised deadline has been announced.
This is not organizer approval or proof that a required surprise element is complete.
Repository publication, owner/team attribution and the source-code license require
completion before submission. Third-party dependencies keep their own licenses.
