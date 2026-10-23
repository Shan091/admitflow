import uuid
from typing import Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.engine.dispatcher import handle_turn


@pytest.fixture
def sample_whatsapp_payload() -> dict[str, Any]:
    return {
        "messaging_product": "whatsapp",
        "metadata": {"display_phone_number": "1234567890", "phone_number_id": "123"},
        "contacts": [{"profile": {"name": "Test User"}, "wa_id": "919876543210"}],
        "messages": [
            {
                "from": "919876543210",
                "id": "wamid.123",
                "timestamp": "1602056683",
                "type": "text",
                "text": {"body": "Hello"},
            }
        ],
    }


@pytest.mark.asyncio
@patch("src.engine.dispatcher.get_sessionmaker")
@patch("src.engine.dispatcher.get_redis")
@patch("src.engine.dispatcher.RedisMutex")
@patch("src.engine.dispatcher.WhatsAppSender")
@patch("src.engine.dispatcher.check_input_safety")
@patch("src.engine.dispatcher.detect_intent")
@patch("src.engine.dispatcher.present_courses")
@patch("src.engine.dispatcher.hash_phone")
@patch("src.engine.dispatcher.encrypt_pii")
async def test_handle_turn_basic_flow(
    mock_encrypt_pii: MagicMock,
    mock_hash_phone: MagicMock,
    mock_present_courses: AsyncMock,
    mock_detect_intent: AsyncMock,
    mock_check_input_safety: AsyncMock,
    mock_sender_cls: MagicMock,
    mock_redis_mutex: MagicMock,
    mock_get_redis: MagicMock,
    mock_sessionmaker: MagicMock,
    sample_whatsapp_payload: dict[str, Any],
) -> None:
    # Setup mocks
    mock_hash_phone.return_value = "mock_hash"
    mock_encrypt_pii.return_value = "mock_enc"

    mock_session = AsyncMock(spec=AsyncSession)
    mock_session_ctx = MagicMock()
    mock_session_ctx.__aenter__.return_value = mock_session
    mock_sessionmaker.return_value.return_value = mock_session_ctx

    mock_mutex_instance = AsyncMock()
    mock_redis_mutex.return_value = mock_mutex_instance
    mock_redis_mutex.return_value.__aenter__.return_value = mock_mutex_instance

    mock_sender = AsyncMock()
    mock_sender_cls.return_value = mock_sender

    mock_check_input_safety.return_value.is_safe = True
    mock_detect_intent.return_value = "discovery"

    async def mock_pass_through_state(state: Any, *args: Any, **kwargs: Any) -> Any:
        return state

    mock_present_courses.side_effect = mock_pass_through_state

    # Mock DB Lead fetching
    mock_inst = AsyncMock()
    mock_inst.id = uuid.uuid4()

    mock_lead = AsyncMock()
    mock_lead.id = uuid.uuid4()
    mock_lead.tenant_id = mock_inst.id
    mock_lead.status = "new"
    mock_lead.current_course_id = None
    mock_lead.current_batch_id = None
    mock_lead.copilot_mode = False

    mock_session.scalar.side_effect = [
        mock_inst,  # inst
        mock_lead,  # lead
        None,  # existing fact key
    ]

    mock_scalars_obj = AsyncMock()
    mock_scalars_obj.all.return_value = []  # no facts

    # We have two calls to db.scalars:
    # 1. Message history
    # 2. Lead facts
    mock_session.scalars.side_effect = [
        [],  # messages
        [],  # facts
    ]

    # Call
    await handle_turn(sample_whatsapp_payload)

    # Asserts
    mock_redis_mutex.assert_called_once()
    mock_check_input_safety.assert_called_once_with("Hello")
    mock_detect_intent.assert_called_once_with("Hello")
    mock_present_courses.assert_called_once()
