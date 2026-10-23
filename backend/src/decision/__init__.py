"""Typed decisions through the existing OpenAI-only provider boundary."""

from typing import Any

from pydantic import BaseModel, ValidationError

from src.engine.llm_factory import AllProvidersFailedError, generate_completion


async def decide[T: BaseModel](schema: type[T], messages: list[dict[str, Any]]) -> T:
    """Validate structured model output; refusal/malformed output is never a decision.

    Schemas describe bounded interpretation, not authorization or calibrated
    probabilities. Business rules and consequential actions remain code-owned.
    """
    response = await generate_completion(messages, response_format=schema, temperature=0.0)
    try:
        message = response.choices[0].message
        if getattr(message, "refusal", None) or not message.content:
            raise ValueError("No decision")
        return schema.model_validate_json(message.content)
    except (ValidationError, ValueError, TypeError, AttributeError, IndexError):
        raise AllProvidersFailedError("OpenAI did not return a valid decision") from None
