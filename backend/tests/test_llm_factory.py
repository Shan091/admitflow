from unittest.mock import AsyncMock, patch

import pytest
from litellm.exceptions import ContextWindowExceededError
from pydantic import SecretStr

from src.core.settings import get_settings
from src.engine.llm_factory import AllProvidersFailedError, generate_completion


@pytest.fixture
def mock_settings(monkeypatch: pytest.MonkeyPatch) -> None:
    """Ensure all three models are configured for fallback testing."""
    monkeypatch.setattr(get_settings(), "openai_api_key", SecretStr("synthetic-key"))
    monkeypatch.setattr(get_settings(), "llm_fast_model", "openai/gpt-4.1-mini")
    monkeypatch.setattr(get_settings(), "llm_fallback_model", "openai/gpt-4.1")
    monkeypatch.setattr(get_settings(), "llm_nuance_model", "openai/gpt-4o-mini")


@pytest.mark.asyncio
async def test_generate_completion_success(mock_settings: None) -> None:
    """Test that it returns successfully on the primary model."""
    mock_response = {"choices": [{"message": {"content": "Hello!"}}]}

    with patch("src.engine.llm_factory.acompletion", new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.return_value = mock_response

        response = await generate_completion([{"role": "user", "content": "Hi"}])

        assert response == mock_response
        mock_acompletion.assert_called_once()
        assert mock_acompletion.call_args[1]["model"] == "openai/gpt-4.1-mini"


async def test_guidance_can_request_a_larger_bounded_structured_reply(mock_settings: None) -> None:
    with patch("src.engine.llm_factory.acompletion", new_callable=AsyncMock) as call:
        call.return_value = {"choices": []}
        await generate_completion(
            [{"role": "user", "content": "Synthetic guidance"}], max_tokens=1800
        )
        assert call.call_args.kwargs["max_tokens"] == 1800
        assert call.call_args.kwargs["store"] is False


@pytest.mark.parametrize("limit", [0, 199, 2001])
async def test_invalid_response_budget_never_calls_a_provider(
    mock_settings: None, limit: int
) -> None:
    with patch("src.engine.llm_factory.acompletion", new_callable=AsyncMock) as call:
        with pytest.raises(ValueError):
            await generate_completion([], max_tokens=limit)
        call.assert_not_called()


@pytest.mark.asyncio
async def test_generate_completion_fallback(mock_settings: None) -> None:
    """Test that it falls back to OpenAI if primary OpenAI model fails."""
    mock_response = {"choices": [{"message": {"content": "Hello from fallback!"}}]}

    with patch("src.engine.llm_factory.acompletion", new_callable=AsyncMock) as mock_acompletion:
        # First call raises a generic error, second call succeeds
        mock_acompletion.side_effect = [Exception("primary OpenAI model is down"), mock_response]

        response = await generate_completion([{"role": "user", "content": "Hi"}])

        assert response == mock_response
        assert mock_acompletion.call_count == 2

        # Verify it tried primary OpenAI model first, then OpenAI
        assert mock_acompletion.call_args_list[0][1]["model"] == "openai/gpt-4.1-mini"
        assert mock_acompletion.call_args_list[1][1]["model"] == "openai/gpt-4.1"


@pytest.mark.asyncio
async def test_generate_completion_all_fail(mock_settings: None) -> None:
    """Test that AllProvidersFailedError is raised if everything fails."""
    with patch("src.engine.llm_factory.acompletion", new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.side_effect = Exception("API Error")

        with pytest.raises(AllProvidersFailedError, match="All configured LLM providers failed"):
            await generate_completion([{"role": "user", "content": "Hi"}])

        # Should have tried all 3 models
        assert mock_acompletion.call_count == 3


@pytest.mark.asyncio
async def test_generate_completion_context_exceeded(mock_settings: None) -> None:
    """Test that ContextWindowExceededError is not caught by the fallback loop."""
    with patch("src.engine.llm_factory.acompletion", new_callable=AsyncMock) as mock_acompletion:
        mock_acompletion.side_effect = ContextWindowExceededError(
            "Too many tokens", model="gemini", llm_provider="gemini"
        )

        with pytest.raises(ContextWindowExceededError):
            await generate_completion([{"role": "user", "content": "Huge payload"}])

        # Should not have fallen back
        assert mock_acompletion.call_count == 1
