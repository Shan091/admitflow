"""Triage Node (Task 11).

Routes incoming messages to the appropriate downstream node:
- Discovery: user is exploring courses
- RAG: user is asking a knowledge question
- Qualification: user is answering our qualification questions
- Handoff: user explicitly wants to speak to a human
"""

from typing import Literal

from pydantic import BaseModel, Field

from src.engine.llm_factory import generate_completion

TriageIntent = Literal["discovery", "rag", "qualification", "handoff"]


class TriageResponse(BaseModel):
    """Structured output expected from the LLM triage classifier."""

    intent: TriageIntent = Field(
        description=(
            "The detected intent of the user's message. "
            "'discovery' for exploring courses/programs. "
            "'rag' for factual questions about the institution. "
            "'qualification' for answering form-like questions. "
            "'handoff' for explicitly asking for a human agent."
        )
    )
    reason: str = Field(description="Brief reasoning for the chosen intent.")


async def detect_intent(text: str) -> TriageIntent:
    """Classify the user's intent to route to the correct node.

    Design Decision:
    If a message is empty, unclear, or just conversational (e.g., "Hello"),
    we NEVER default to 'handoff'. Defaulting to handoff for unknown inputs
    would spam human agents with accidental media or empty texts.
    Instead, we default to 'discovery', allowing the AI to naturally respond
    and guide the user back on track.
    """
    if not text.strip():
        # Empty messages (like an image without caption) default to discovery
        return "discovery"

    prompt = f"""
    You are the triage router for a university admissions WhatsApp bot.
    Analyze the following user message and classify it into one of four intents:
    
    - "discovery": Exploring courses or programs.
    - "rag": Asking factual questions about the institution (fees, location, facilities).
    - "qualification": Providing personal details, marks, or answering an application question.
    - "handoff": Explicitly asks to speak to a human, is angry, or needs support.
    
    CRITICAL RULE: If the message is a greeting, unclear, or out-of-domain, 
    you MUST classify it as "discovery" so the bot can handle it. DO NOT classify as "handoff" 
    unless the user explicitly demands a human or is angry.
    
    User message: "{text}"
    """

    response = await generate_completion(
        messages=[{"role": "user", "content": prompt}],
        response_format=TriageResponse,
        temperature=0.0,
    )

    content = response.choices[0].message.content
    if not content:
        # Fail safe to discovery so the AI handles it, not a human
        return "discovery"

    parsed = TriageResponse.model_validate_json(content)
    return parsed.intent
