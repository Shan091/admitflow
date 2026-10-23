# ADR-001: Hybrid Architecture (Python Backend + Next.js Frontend)

## Status
Accepted — with one later revision: the conversation engine is a **hand-rolled async dispatcher**, not LangGraph (superseded by ADR-007 / SPEC §17.1). The hybrid Python-backend + Next.js-frontend split below stands.


## Context
AdmitFlow requires handling Meta WhatsApp webhooks within a strict 5-second timeout, executing complex AI state machine logic (LangGraph), and providing a premium, highly interactive dashboard (glassmorphism UI) for institution staff. We need to decide on the core technology stack.

## Decision
Use a Hybrid Architecture:
- **Backend**: Python (FastAPI + TaskIQ + LangGraph + PostgreSQL)
- **Frontend**: Next.js (TypeScript + React + Tailwind CSS)

## Alternatives Considered

### Full TypeScript (Next.js for API + Frontend)
- Pros: Single language (TypeScript), unified monorepo.
- Cons: The Python ecosystem for AI (LangGraph, LangChain, TaskIQ, pgvector integrations) is vastly superior and more mature than JavaScript equivalents. Heavy AI processing in Node.js event loop can cause latency spikes.
- Rejected: We need state-of-the-art AI tooling and background worker isolation, which Python handles better.

### Full Python (FastAPI + Jinja2/HTMX)
- Pros: Single codebase, very fast to build.
- Cons: Cannot easily achieve the complex, highly interactive "glassmorphism" premium UI and real-time WebSocket dashboard the product vision demands.
- Rejected: The UI needs the rich component ecosystem of React.

## Consequences
- Requires maintaining two separate deployment pipelines (Fly.io for backend, Vercel for frontend — hosting finalized in ADR-007, superseding the original Railway mention).
- Clean separation of concerns: Frontend has zero business logic, Backend is a pure REST API.
- Team needs proficiency in both Python and TypeScript.
- **Engine revision**: The backend keeps FastAPI + TaskIQ + PostgreSQL, but LangGraph was dropped in favour of a hand-rolled dispatcher once routing moved into the System-1 `decide()` layer (ADR-008). Rationale in SPEC §17.1 / ADR-007.
