"""Bounded OpenAI-only model roles; provider details never escape in errors."""

import asyncio
import logging
import time
from typing import Any

from litellm import acompletion
from litellm.exceptions import ContextWindowExceededError

from src.core.settings import get_settings

logger = logging.getLogger(__name__)


class AllProvidersFailedError(Exception):
    """Raised when the entire LLM fallback chain is exhausted."""


async def generate_completion(
    messages: list[dict[str, Any]],
    response_format: Any = None,
    temperature: float = 0.0,
    *,
    max_tokens: int = 800,
) -> Any:
    """Generate a completion with automatic provider fallback.

    Tries the fast model, then the fallback model, then the nuance model.
    """
    settings = get_settings()
    if not 200 <= max_tokens <= 2000:
        raise ValueError("Response token limit must be between 200 and 2000")

    models = [settings.llm_fast_model]
    if settings.llm_fallback_model:
        models.append(settings.llm_fallback_model)
    if settings.llm_nuance_model:
        models.append(settings.llm_nuance_model)

    if any(not (model.startswith("openai/") or model.startswith("gpt-")) for model in models):
        raise AllProvidersFailedError("Only OpenAI model roles are supported")
    if not settings.openai_api_key:
        raise AllProvidersFailedError("OpenAI credentials are not configured")

    for model in models:
        try:
            kwargs: dict[str, Any] = {
                "model": model,
                "messages": messages,
                "temperature": temperature,
                "num_retries": 1,  # let litellm retry transient errors once per model
                "timeout": settings.llm_timeout_seconds,
                "api_key": settings.openai_api_key.get_secret_value(),
                "max_tokens": max_tokens,
                "store": False,
            }
            if response_format:
                kwargs["response_format"] = response_format

            started = time.monotonic()
            async with asyncio.timeout(settings.llm_timeout_seconds + 2):
                response = await acompletion(**kwargs)
            logger.info(
                "model_completion role=%s model=%s elapsed_ms=%d input_tokens=%s output_tokens=%s",
                models.index(model),
                model.splitlines()[0],
                int((time.monotonic() - started) * 1000),
                getattr(getattr(response, "usage", None), "prompt_tokens", None),
                getattr(getattr(response, "usage", None), "completion_tokens", None),
            )
            return response
        except ContextWindowExceededError as e:
            # Fatal error, no point in falling back if context is too large
            raise e
        except Exception:
            continue

    raise AllProvidersFailedError("All configured LLM providers failed") from None
