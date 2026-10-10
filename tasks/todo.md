# AdmitFlow Hackathon Build Checklist

Use this file as the live status board. Start every task unchecked. Change `[ ]` to `[x]` only after the acceptance condition is met and the result has been verified. If a task is started but incomplete, leave it unchecked and add a short note under the milestone.

## M0 — Rails (target: 35 minutes)

- [ ] Initialize the fresh project from the hackathon documentation template; keep implementation code newly written at the event.
- [ ] Add Python project configuration and required dependencies.
- [ ] Add `.env.example` with variable names only; keep credentials out of Git.
- [ ] Implement FastAPI app and `GET /health`.
- [ ] Create SQLite schema for the seeded tenant, courses, qualification rules, leads, messages, and knowledge chunks.
- [ ] Seed one institution, at least two courses, batches, deterministic eligibility rules, and a small FAQ corpus.
- [ ] Confirm the app starts and the seed data can be read.

**Milestone complete when:** FastAPI starts, `/health` succeeds, and seeded records are available from SQLite.

## M1 — Telegram and conversation (target: 2 hours 15 minutes total from start)

- [ ] Configure Telegram bot token through environment variables.
- [ ] Start Telegram long-polling and receive a real message.
- [ ] Reply to `/start` and display course choices using Telegram buttons.
- [ ] Persist Telegram user/lead identity and every inbound/outbound message.
- [ ] Handle course selection and load that course’s batch and rules.
- [ ] Ask the two seeded qualification questions.
- [ ] Evaluate eligibility in Python; do not let model output set eligibility.
- [ ] Save and display the qualification outcome.
- [ ] Keep a browse/no-pressure path for students who are not ready to qualify.

**Milestone complete when:** A real phone can complete discovery and qualification, and the lead plus conversation survive an app restart.

## M2 — Embeddings and vector search (target: 1 hour 20 minutes)

- [ ] Add OpenAI embedding configuration using `text-embedding-3-small` at the default 1,536 dimensions.
- [ ] Implement seeded FAQ chunk preparation; each FAQ question and answer forms one chunk with source metadata.
- [ ] Implement batched embedding generation for seed content.
- [ ] Store each chunk’s content, tenant/source metadata, embedding model, content hash, and float32 vector in SQLite.
- [ ] Reuse an embedding when its content hash and model match; re-embed changed content or model versions.
- [ ] Implement query embedding and tenant-scoped cosine ranking with NumPy.
- [ ] Start with a `0.72` minimum similarity and `0.05` top-result margin; tune against the seeded examples before the demo.
- [ ] Return the curated answer and source only when the match rule passes.
- [ ] Abstain or ask for clarification when no result passes or the top results are too close.
- [ ] Route fee questions to structured course data before retrieval; keep monetary amounts out of FAQ chunks.
- [ ] Handle embedding API failures with a clear retrieval-unavailable response; do not silently answer without retrieval.
- [ ] Verify known FAQ queries, unrelated queries, ambiguous queries, fee routing, and one live embedding API call.

**Milestone complete when:** Known questions retrieve the intended FAQ, unrelated/ambiguous questions do not produce unsupported answers, and fee questions use structured data.

## M3 — Staff dashboard (target: 55 minutes)

- [ ] Add a local read-only dashboard route.
- [ ] List leads with course, qualification outcome, and last activity.
- [ ] Show a selected lead’s saved conversation and relevant facts.
- [ ] Confirm the dashboard reflects the same state as the Telegram interaction.

**Milestone complete when:** The live demo lead and its conversation are visible in the local dashboard.

## M4 — Verify, document, rehearse (target: 55 minutes)

- [ ] Run the documented install and start commands from a clean environment or explain any limitation.
- [ ] Run the focused checks for eligibility and retrieval behavior.
- [ ] Walk through the complete Telegram-to-dashboard demo.
- [ ] Confirm all required credentials are absent from tracked files and logs.
- [ ] Complete README setup and demo steps.
- [ ] Complete `AI_USAGE.md` with actual Codex assistance and human review.
- [ ] Complete `SUBMISSION.md` with repository, demo, checks, libraries/APIs, and limitations.
- [ ] Update `CHANGELOG.md` with actual changes, time/timezone, validation, and limitations.
- [ ] Review `git status` and diff; commit the completed milestone and push when the team has authorized the remote.

**Milestone complete when:** The walkthrough works from documented instructions and the submission records match what was actually built and checked.

## Stretch — only after M0–M4

- [ ] Add Razorpay test-mode application payment using the actual test flow.
- [ ] Show payment status in the dashboard and Telegram only after confirming it from Razorpay.
- [ ] Add Langfuse tracing or dashboard styling if there is time.
- [ ] Add document upload or general PDF ingestion only after the core demo remains reliable.

## Current status / blockers

- Current project contents: no application files are present yet.
- Keep every task unchecked until its acceptance condition is met.
- Record blockers or scope cuts here with the date and the next action.
