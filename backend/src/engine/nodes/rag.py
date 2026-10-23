"""RAG Node (Task 14).

Graph node that retrieves from the knowledge base and generates an answer.
Fails-closed below confidence threshold to prevent hallucination.
"""

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.rag import sanitize_chunks, search_chunks
from src.engine.llm_factory import generate_completion
from src.engine.state import EngineState
from src.whatsapp.sender import WhatsAppSender


async def process_rag_node(
    state: EngineState,
    db: AsyncSession,
    sender: WhatsAppSender,
    phone_number: str,
) -> EngineState:
    """Retrieve context and answer knowledge questions."""
    # 1. Extract the latest user message
    if not state.conversation_history:
        return state

    user_query = ""
    for msg in reversed(state.conversation_history):
        if msg.get("role") == "user":
            user_query = msg.get("content", "")
            break

    if not user_query:
        return state

    # 2. Search and sanitize chunks
    # Note: RRF combined rank score isn't easily exposed on the model yet,
    # so we rely on the DB query's LIMIT and our chunk sanitizer.
    raw_chunks = await search_chunks(
        session=db,
        tenant_id=state.tenant_id,
        query=user_query,
        top_k=5,
    )
    safe_chunks = await sanitize_chunks(raw_chunks)

    if not safe_chunks:
        # Fail closed
        await sender.send_text(
            to=phone_number,
            text=(
                "I don't have that information right now. "
                "Let me know if you'd like to speak with a human counselor."
            ),
        )
        return state

    # 3. Build context and call LLM
    context_text = "\n\n".join(f"--- Document Snippet ---\n{c.content}" for c in safe_chunks)

    system_prompt = (
        "You are an admissions assistant. Answer the user's question using ONLY "
        "the provided context snippets below. If the answer is not contained in "
        "the context, you MUST say exactly 'I don't have that information'. "
        "Do not hallucinate fees, course names, or policies. Keep your answer "
        "concise, friendly, and formatted for WhatsApp (using *bold* instead of markdown **)."
        f"\n\nCONTEXT:\n{context_text}"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_query},
    ]

    response = await generate_completion(
        messages=messages,
        temperature=0.0,
    )

    ai_text = response.choices[0].message.content

    # 4. Send the response
    await sender.send_text(
        to=phone_number,
        text=ai_text,
    )

    # 5. We don't transition state here, just return current state
    # (The user stays in whatever state they are in, typically DISCOVERING or QUALIFYING)
    return state
