from unittest.mock import AsyncMock, patch

import pytest

from src.engine.nodes.triage import detect_intent


@pytest.mark.asyncio
async def test_triage_discovery() -> None:
    """Test routing for course discovery."""

    class MockMessage:
        content = '{"intent": "discovery", "reason": "Asking for course list"}'

    class MockChoice:
        message = MockMessage()

    class MockResponse:
        choices = [MockChoice()]

    with patch("src.decision.generate_completion", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = MockResponse()
        intent = await detect_intent("What B.Tech courses do you offer?")
        assert intent == "discovery"
        mock_llm.assert_called_once()


@pytest.mark.asyncio
async def test_triage_rag() -> None:
    """Test routing for knowledge questions."""

    class MockMessage:
        content = '{"intent": "rag", "reason": "Asking about placement"}'

    class MockChoice:
        message = MockMessage()

    class MockResponse:
        choices = [MockChoice()]

    with patch("src.decision.generate_completion", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = MockResponse()
        intent = await detect_intent("What is the average placement package?")
        assert intent == "rag"


@pytest.mark.asyncio
async def test_triage_qualification() -> None:
    """Test routing for qualification answers."""

    class MockMessage:
        content = '{"intent": "qualification", "reason": "Providing 12th marks"}'

    class MockChoice:
        message = MockMessage()

    class MockResponse:
        choices = [MockChoice()]

    with patch("src.decision.generate_completion", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = MockResponse()
        intent = await detect_intent("I got 85% in CBSE 12th board.")
        assert intent == "qualification"


@pytest.mark.asyncio
async def test_triage_handoff() -> None:
    """Test routing for human handoff."""

    class MockMessage:
        content = '{"intent": "handoff", "reason": "Explicit human request"}'

    class MockChoice:
        message = MockMessage()

    class MockResponse:
        choices = [MockChoice()]

    with patch("src.decision.generate_completion", new_callable=AsyncMock) as mock_llm:
        mock_llm.return_value = MockResponse()
        intent = await detect_intent("I want to speak to a human agent right now.")
        assert intent == "handoff"


@pytest.mark.asyncio
async def test_triage_empty_message() -> None:
    """Test routing for empty messages without calling LLM defaults to discovery."""
    with patch("src.decision.generate_completion", new_callable=AsyncMock) as mock_llm:
        intent = await detect_intent("   ")
        assert intent == "discovery"
        mock_llm.assert_not_called()
