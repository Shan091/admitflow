"""Unit tests for the RAG node."""

import uuid
from unittest.mock import AsyncMock, patch

import pytest

from src.db.enums import LeadStatus
from src.db.models.knowledge import DocumentChunk
from src.engine.nodes.rag import process_rag_node
from src.engine.state import EngineState


@pytest.fixture
def mock_state() -> EngineState:
    return EngineState(
        lead_id=uuid.uuid4(),
        tenant_id=uuid.uuid4(),
        status=LeadStatus.DISCOVERING,
        conversation_history=[{"role": "user", "content": "What is the fee for B.Tech?"}],
    )


@pytest.mark.asyncio
@patch("src.engine.nodes.rag.generate_completion")
@patch("src.engine.nodes.rag.search_chunks")
@patch("src.engine.nodes.rag.sanitize_chunks")
async def test_process_rag_node_success(
    mock_sanitize: AsyncMock,
    mock_search: AsyncMock,
    mock_generate: AsyncMock,
    mock_state: EngineState,
) -> None:
    mock_session = AsyncMock()
    mock_sender = AsyncMock()

    # Mock chunk retrieval
    mock_search.return_value = [DocumentChunk(content="B.Tech fee is 100,000 INR.")]
    mock_sanitize.return_value = mock_search.return_value

    # Mock LLM generation
    class MockMessage:
        content = "The fee for the B.Tech program is *100,000 INR*."

    class MockChoice:
        message = MockMessage()

    class MockResponse:
        choices = [MockChoice()]

    mock_generate.return_value = MockResponse()

    new_state = await process_rag_node(
        state=mock_state,
        db=mock_session,
        sender=mock_sender,
        phone_number="1234567890",
    )

    # Should send the LLM response
    mock_sender.send_text.assert_called_once_with(
        to="1234567890",
        text="The fee for the B.Tech program is *100,000 INR*.",
    )

    # State should remain unchanged
    assert new_state.status == LeadStatus.DISCOVERING


@pytest.mark.asyncio
@patch("src.engine.nodes.rag.search_chunks")
@patch("src.engine.nodes.rag.sanitize_chunks")
async def test_process_rag_node_no_chunks(
    mock_sanitize: AsyncMock,
    mock_search: AsyncMock,
    mock_state: EngineState,
) -> None:
    mock_session = AsyncMock()
    mock_sender = AsyncMock()

    # Mock empty chunks
    mock_search.return_value = []
    mock_sanitize.return_value = []

    new_state = await process_rag_node(
        state=mock_state,
        db=mock_session,
        sender=mock_sender,
        phone_number="1234567890",
    )

    # Should send fail-closed message
    mock_sender.send_text.assert_called_once()
    args, kwargs = mock_sender.send_text.call_args
    assert "I don't have that information" in kwargs["text"]

    # State should remain unchanged
    assert new_state.status == LeadStatus.DISCOVERING
