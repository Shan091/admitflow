# Implementation Plan: AdmitFlow

Current user direction (2026-10-23): retain this full institutional MVP roadmap in this repository.
The phases are product milestones, not a claim that the entire roadmap fits into the hackathon.
Use [the resource plan](../docs/event/RESOURCE_PLAN.md) when selecting provider resources; changes
to hosting or model backends still need an explicit implementation decision and verification.

## Overview
AdmitFlow is an AI-native WhatsApp admissions engagement platform. The system uses Python (FastAPI, TaskIQ, a hand-rolled conversation engine) for the backend/AI, pgvector for RAG, Razorpay for payments, Langfuse for tracing, and Next.js for the admin dashboard.

## Architecture Decisions
- **FastAPI + TaskIQ**: Webhook returns 200 OK instantly; all LLM work happens in a background worker.
- **Conversation engine**: Hand-rolled async dispatcher (decided — SPEC §17.1, ADR-007). Readiness-aware, adaptive routing lives in the `decide()` layer; each turn is a cold reload from the `messages` table (no LangGraph, no checkpointer).
- **pgvector**: Per-institution RAG knowledge base for course FAQs and policies.
- **Three-Layer Guardrails**: Input sanitize → RAG sanitize → Output validate.
- **Razorpay**: Application fee collection via Payment Links, gated by explicit user confirmation.
- **Langfuse**: LLM tracing for every call (Langfuse Cloud, free tier).
- **Redis**: Message mutex, webhook dedup, rate-limit tracking.
- **System-1 Decision Layer**: routing / guardrail-triage / readiness / escalation as typed, calibrated decisions behind a `decide()` interface — Gemini Flash for the demo, self-hosted Laya (Jev-compatible) later. See ADR-008.
- **LLM efficiency**: model IDs pinned in settings (roles in docs), prompt caching on the static system+institution prefix, and native structured outputs as the default for all extraction. See ADR-007 "LLM efficiency".

## Task List

### Phase 1: Foundation
- [x] Task 1: Initialize Python project, FastAPI, settings, and Docker
- [ ] Task 2: PostgreSQL schema (SQLAlchemy + Alembic) — all core models including `discount_codes`
- [x] Task 3: TaskIQ + Redis broker setup
- [ ] Task 4: PII encryption utilities and audit log infrastructure

### Checkpoint: Foundation
- [ ] FastAPI boots, DB migrations run, worker connects to Redis
- [ ] Audit log writes verified

### Phase 2: WhatsApp Ingress
- [x] Task 5: Meta WhatsApp webhook (HMAC verify + Redis SETNX dedup + enqueue)
- [x] Task 6: WhatsApp message sending service (text, interactive buttons/lists, templates)
- [x] Task 7: Redis distributed mutex (`wa_mutex:{phone_number}`)

### Checkpoint: WhatsApp Ingress
- [x] Webhook returns 200 OK, dedup prevents double processing
- [x] Can send test messages to a verified number

### Phase 3: AI Core (Engine + RAG)
- [x] Task 8: Engine state definition and lead lifecycle states (hand-rolled dispatcher; including review states)
- [x] Task 9: Multi-provider LLM factory with fallback chain
- [x] Task 10: Input guardrail node (abuse, injection, profanity detection)
- [x] Task 11: Triage node (intent detection and routing)
- [x] Task 12: Discovery node (course exploration via tap menus)
- [x] Task 13: RAG pipeline (pgvector ingestion, hybrid search, RAG guardrail)
- [x] Task 14: RAG node (answer knowledge questions from institution docs)
- [x] Task 15: Qualification node (structured-output rule extraction + code verification)
- [x] Task 16: Output guardrail (validate AI response before WhatsApp send)
- [ ] Task 17: Wire webhook → TaskIQ worker → engine dispatcher → WhatsApp send
- [ ] Task 40 (spans Phase 3–4): `decide()` System-1 decision-layer abstraction (choice/score/noul); demo backend = Gemini Flash structured outputs; used by guardrail, triage, readiness & escalation (ADR-008)

### Checkpoint: AI Core
- [ ] End-to-end: message in → AI reply out via WhatsApp
- [ ] Guardrails block injection and hallucinated fees
- [ ] RAG answers knowledge questions from uploaded docs

### Phase 4: Advanced Bot Features
- [ ] Task 18: Application form collection node (structured data via WhatsApp)
- [ ] Task 19: Razorpay integration (discount code validation, payment link creation, HMAC webhook, confirmation)
- [ ] Task 20: Human handoff node + co-pilot mode (suggested replies)
- [ ] Task 21: Cold lead re-engagement worker (scheduled follow-ups with AI hooks)
- [ ] Task 22: WhatsApp rate-limit tracking and send queue
- [ ] Task 23: Langfuse tracing integration across all LLM calls

### Checkpoint: Advanced Features
- [ ] Bot collects application form data and sends Razorpay payment link
- [ ] Payment confirmed via webhook, bot confirms in chat
- [ ] Human takeover activates co-pilot mode
- [ ] Cold leads get personalized re-engagement after X days

### Phase 5: Dashboard Frontend (Next.js)
- [ ] Task 24: Initialize Next.js project with dark mode + glassmorphism Tailwind config
- [ ] Task 25: Authentication (email + password login)
- [ ] Task 26: Dashboard home (funnel analytics with charts)
- [ ] Task 27: Leads CRM page (list, filter, status indicators)
- [ ] Task 28: Course & batch management page (CRUD + qualification rules builder)
- [ ] Task 29: Chat takeover + co-pilot UI (message history, suggested replies, approve/send)
- [ ] Task 30: Document management page (RAG upload/delete)
- [ ] Task 31: Application submissions view (review queue with approve/reject/waitlist)
- [ ] Task 32: Data export (CSV/Excel) + outbound webhook configuration
- [ ] Task 33: Real-time WebSocket notifications (bell/badge)
- [ ] Task 34: Institution settings (business hours, re-engagement config)

### Checkpoint: Dashboard Complete
- [ ] Staff can log in, view leads, manage courses, take over chats
- [ ] Analytics show funnel conversion rates
- [ ] End-to-end: course rules updated in dashboard instantly affect bot behavior

### Phase 6: Production Hardening
- [ ] Task 35: Sentry error monitoring integration
- [ ] Task 36: Delete My Data endpoint (DPDPA compliance)
- [ ] Task 37: Data retention auto-cleanup (configurable per tenant)
- [ ] Task 38: Docker Compose for local development (all services)
- [ ] Task 39: Production deployment (Vercel frontend; Fly.io backend + worker + scheduler, always-on; Neon Postgres; Redis on Fly; Langfuse Cloud) — see ADR-007
- [ ] Task 41 (post-demo): Distill high-frequency decisions into self-hosted Laya (Jev-compatible); per-decision Malayalam/Hinglish eval + calibration before switching (ADR-008)
- [ ] Task 42: Advanced RAG Strategy (ADR-011)
  - [ ] Task 42.1: Complex Document Parsing & Semantic Chunking (Docling/Unstructured)
  - [ ] Task 42.2: Contextual Query Rewriting (Gemini Flash)
  - [ ] Task 42.3: Pluggable Reranker (Cohere API vs Local)

### Checkpoint: Production Ready
- [ ] All success criteria from SPEC.md verified
- [ ] Observability, tracing, and error monitoring operational
- [ ] Security audit passed

## Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| Dual codebase complexity | Med | Keep Next.js frontend simple; ALL business logic in Python |
| Meta Webhook Timeouts | High | TaskIQ background workers guarantee instant 200 OK |
| LLM Hallucinations (fees) | High | Output guardrail blocks any monetary figure not from DB |
| WhatsApp number suspension | High | Rate-limit awareness + send queue |
| RAG poisoning | Med | RAG guardrail sanitizes chunks before LLM injection |
| Payment replay | High | `payment_link_sent` flag + webhook clears pending order |
| Data breach (PII) | Critical | Application-level PII encryption + audit trail |
