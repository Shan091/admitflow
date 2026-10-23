# ADR-002: Webhook Concurrency and Deduplication

## Status
Accepted


## Context
Meta's WhatsApp Business API has two known behaviors that cause issues in stateful bots:
1. It frequently sends duplicate webhooks for the same message if the initial response is delayed.
2. Users can send multiple messages in rapid succession (e.g., "Hi", "I want to apply", "My name is John" within 2 seconds). 
If two background workers process these messages simultaneously, they will read the same conversation state and one will overwrite the other, corrupting the conversation history.

## Decision
Implement a two-layer Redis strategy:
1. **Deduplication**: Use Redis `SETNX` on the webhook `message.id` with a 5-minute TTL.
2. **Concurrency**: Use a Redis distributed lock (mutex) keyed by `wa_mutex:{phone_number}` around the `handle_turn()` execution.

## Alternatives Considered

### PostgreSQL Database Locks (`SELECT FOR UPDATE`)
- Pros: No need for an external Redis dependency.
- Cons: Holding database connections open while waiting for external LLM calls to complete will quickly exhaust the connection pool.
- Rejected: Too risky for scalability.

### In-Memory Locks (Asyncio Locks)
- Pros: Simplest implementation.
- Cons: Only works if there is exactly one backend worker process. Fails in horizontal scaling or multi-worker deployments (which we need).
- Rejected: Not horizontally scalable.

## Consequences
- Requires Redis as a hard dependency in the infrastructure stack (which we already need for TaskIQ).
- Duplicate messages from Meta will be silently dropped at the edge (FastAPI layer) before hitting the workers.
- Sequential messages from the same user will correctly queue and process in order, preserving state integrity.
