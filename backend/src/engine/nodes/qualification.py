"""Qualification Node (Task 15).

Extracts rule fields using the LLM and runs deterministic code verification.
"""

from typing import Any

from pydantic import BaseModel, Field
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.db.enums import LeadStatus
from src.db.models.catalog import QualificationRule
from src.engine.llm_factory import generate_completion
from src.engine.state import EngineState
from src.logic.rules import evaluate_rule
from src.whatsapp.sender import WhatsAppSender


class ExtractionResponse(BaseModel):
    """Structured output expected from the LLM when extracting fields."""

    extracted_fields: dict[str, Any] = Field(
        description="A dictionary of field names to extracted values based on the rules. Omit fields that are not mentioned in the chat."  # noqa: E501
    )
    next_question: str | None = Field(
        description="A conversational question to ask the user to collect the NEXT missing field. None if no fields are missing."  # noqa: E501
    )


async def run_qualification(
    state: EngineState,
    db: AsyncSession,
    sender: WhatsAppSender,
    phone_number: str,
) -> EngineState:
    """Run the qualification loop."""
    if not state.current_course_id:
        # Failsafe: if we ended up here without a course, go back to discovery
        try:
            state.transition_to(LeadStatus.DISCOVERING)
        except Exception:
            pass
        await sender.send_text(
            to=phone_number,
            text="I'm not sure which course we were discussing. Let's look at the available courses again.",  # noqa: E501
        )
        return state

    # Fetch rules
    query = select(QualificationRule).where(QualificationRule.course_id == state.current_course_id)
    result = await db.execute(query)
    rules = result.scalars().all()

    if not rules:
        # No rules, auto-qualify
        try:
            state.transition_to(LeadStatus.ADMISSION_READY)
        except Exception:
            pass
        await sender.send_text(
            to=phone_number,
            text="Great! You qualify for this course. Let's proceed.",
        )
        return state

    # Define the fields we are looking for
    required_fields = {rule.field for rule in rules}
    missing_fields = required_fields - set(state.extracted_facts.keys())

    content = None
    parsed = None

    # If there are missing fields, ask LLM to extract from history
    if missing_fields:
        # Extract last user message or last few messages
        history_text = "\n".join(
            [f"{msg['role']}: {msg['content']}" for msg in state.conversation_history[-3:]]
        )

        prompt = f"""
        You are an admissions assistant.
        We need to collect the following missing fields from the user to evaluate their eligibility:
        {list(missing_fields)}
        
        Recent conversation:
        {history_text}
        
        1. Extract any values the user provided for the missing fields. Format values 
           appropriately (numbers as ints/floats, etc.).
        2. If there are still missing fields AFTER extraction, generate a polite, conversational 
           question to ask the user for ONE of the remaining missing fields. If no missing fields 
           remain, set next_question to null.
        """

        response = await generate_completion(
            messages=[{"role": "user", "content": prompt}],
            response_format=ExtractionResponse,
            temperature=0.0,
        )

        content = response.choices[0].message.content
        if content:
            parsed = ExtractionResponse.model_validate_json(content)
            for k, v in parsed.extracted_fields.items():
                if k in required_fields:
                    state.extracted_facts[k] = v

    # Re-calculate missing fields after extraction
    missing_fields = required_fields - set(state.extracted_facts.keys())

    if missing_fields:
        # Ask the user the next question
        question = (
            parsed.next_question
            if parsed and parsed.next_question
            else f"Could you please provide your {list(missing_fields)[0]}?"
        )
        await sender.send_text(to=phone_number, text=question)
        return state

    # All fields extracted, evaluate rules deterministically
    failed_rules = []
    for rule in rules:
        val = state.extracted_facts.get(rule.field)
        if not evaluate_rule(rule.operator, rule.value, val):
            failed_rules.append(rule)

    if failed_rules:
        # Failed qualification
        try:
            state.transition_to(LeadStatus.DISCOVERING)
        except Exception:
            pass
        await sender.send_text(
            to=phone_number,
            text="Based on your answers, it looks like you don't meet the criteria for this specific course. Let's explore other options.",  # noqa: E501
        )
    else:
        # Passed qualification
        try:
            state.transition_to(LeadStatus.ADMISSION_READY)
        except Exception:
            pass
        await sender.send_text(
            to=phone_number,
            text="Excellent news! You qualify for the batch. Let's get your application started.",
        )

    return state
