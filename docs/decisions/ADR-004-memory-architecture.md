# ADR-004: Dual Memory Architecture

## Status
Accepted — with one later revision: episodic memory is stored in our own `messages` table, not LangGraph's `AsyncPostgresSaver` (the engine is now hand-rolled — SPEC §17.1 / ADR-007). The dual-memory principle below is unchanged.


## Context
The AI must remember the full context of a conversation so parents don't have to repeat themselves. However, passing the entire uncompressed chat history of a 3-month lead into every LLM prompt will hit token limits and become prohibitively expensive.

## Decision
Implement a **Dual Memory Architecture**:
1. **Episodic Memory**: Persist every turn as rows in a queryable `messages` table (PostgreSQL). Each `handle_turn()` reloads the recent N turns (or a rolling summary once the thread grows) to maintain conversational continuity. This is the single source of truth — also read by the dashboard and used for persistent conversational context. *(Originally specified as LangGraph `AsyncPostgresSaver`; revised when the engine went hand-rolled — SPEC §17.1. A checkpointer would have duplicated this state in an opaque blob.)*
2. **Semantic Memory**: Create a custom `lead_facts` table in PostgreSQL. After each turn, extract key facts (name, age, course interest, timeline, budget) and save them to this table. Inject these facts into the system prompt as a `{memory_block}`.

## Alternatives Considered

### External Memory Providers (e.g., mem0, Zep)
- Pros: Off-the-shelf solution for semantic extraction and search.
- Cons: Adds an external network dependency, latency, potential point of failure, and complicates data privacy (DPDPA compliance) by sending PII to a third party.
- Rejected: We already have PostgreSQL; keeping semantic facts in our own DB ensures data locality and security.

### Summarization Window
- Pros: Cheap on tokens.
- Cons: Loses exact phrasing and granular context over time.
- Rejected: Harms the premium UX required for admissions counseling.

## Consequences
- Requires a dedicated LLM extraction step after the main conversation turn to update `lead_facts`.
- DPDPA compliance ("Delete My Data") is straightforward because both episodic and semantic memory live in our controlled database.
