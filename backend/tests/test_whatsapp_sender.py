"""Tests for the WhatsApp Message Sending Service (Task 6).

The sender calls the Meta Graph API to send text, buttons, lists, and templates.
"""

from __future__ import annotations

from unittest.mock import AsyncMock, MagicMock, patch

import httpx2
import pytest

from src.whatsapp.sender import WhatsAppAPIError, WhatsAppSender


class TestWhatsAppSender:
    """WhatsApp sender operations."""

    @pytest.fixture
    def sender(self) -> WhatsAppSender:
        with patch("src.whatsapp.sender.get_settings") as mock_settings:
            mock_settings.return_value.whatsapp_access_token = "test-token"
            mock_settings.return_value.whatsapp_phone_number_id = "test-phone-id"
            mock_settings.return_value.meta_graph_api_version = "v21.0"
            return WhatsAppSender()

    from collections.abc import Generator

    @pytest.fixture
    def mock_httpx_post(self) -> Generator[AsyncMock, None, None]:
        with patch("httpx2.AsyncClient.post") as mock_post:
            yield mock_post

    @pytest.mark.asyncio
    async def test_send_text_success(
        self, sender: WhatsAppSender, mock_httpx_post: AsyncMock
    ) -> None:
        """Successfully sending a text message."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"messages": [{"id": "wamid.1234"}]}
        mock_httpx_post.return_value = mock_response

        message_id = await sender.send_text(to="+919876543210", text="Hello there")
        assert message_id == "wamid.1234"

        mock_httpx_post.assert_called_once()
        call_kwargs = mock_httpx_post.call_args.kwargs
        assert call_kwargs["json"]["type"] == "text"
        assert call_kwargs["json"]["text"]["body"] == "Hello there"
        assert call_kwargs["json"]["to"] == "919876543210"  # Note: API expects no '+'

    @pytest.mark.asyncio
    async def test_send_buttons_success(
        self, sender: WhatsAppSender, mock_httpx_post: AsyncMock
    ) -> None:
        """Successfully sending an interactive buttons message."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"messages": [{"id": "wamid.1234"}]}
        mock_httpx_post.return_value = mock_response

        buttons = [{"id": "btn_1", "title": "Option 1"}, {"id": "btn_2", "title": "Option 2"}]
        message_id = await sender.send_buttons(
            to="+919876543210", text="Choose one:", buttons=buttons
        )
        assert message_id == "wamid.1234"

        payload = mock_httpx_post.call_args.kwargs["json"]
        assert payload["type"] == "interactive"
        assert payload["interactive"]["type"] == "button"
        assert payload["interactive"]["body"]["text"] == "Choose one:"
        assert len(payload["interactive"]["action"]["buttons"]) == 2
        assert payload["interactive"]["action"]["buttons"][0]["reply"]["id"] == "btn_1"

    @pytest.mark.asyncio
    async def test_send_list_success(
        self, sender: WhatsAppSender, mock_httpx_post: AsyncMock
    ) -> None:
        """Successfully sending an interactive list message."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"messages": [{"id": "wamid.1234"}]}
        mock_httpx_post.return_value = mock_response

        sections = [
            {
                "title": "Courses",
                "rows": [
                    {"id": "c1", "title": "Course 1", "description": "Desc 1"},
                    {"id": "c2", "title": "Course 2", "description": "Desc 2"},
                ],
            }
        ]
        message_id = await sender.send_list(
            to="+919876543210",
            text="Available courses:",
            button_text="View Courses",
            sections=sections,
        )
        assert message_id == "wamid.1234"

        payload = mock_httpx_post.call_args.kwargs["json"]
        assert payload["type"] == "interactive"
        assert payload["interactive"]["type"] == "list"
        assert payload["interactive"]["body"]["text"] == "Available courses:"
        assert payload["interactive"]["action"]["button"] == "View Courses"
        assert payload["interactive"]["action"]["sections"] == sections

    @pytest.mark.asyncio
    async def test_send_template_success(
        self, sender: WhatsAppSender, mock_httpx_post: AsyncMock
    ) -> None:
        """Successfully sending a template message."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"messages": [{"id": "wamid.1234"}]}
        mock_httpx_post.return_value = mock_response

        message_id = await sender.send_template(
            to="+919876543210", template_name="hello_world", language_code="en_US"
        )
        assert message_id == "wamid.1234"

        payload = mock_httpx_post.call_args.kwargs["json"]
        assert payload["type"] == "template"
        assert payload["template"]["name"] == "hello_world"
        assert payload["template"]["language"]["code"] == "en_US"

    @pytest.mark.asyncio
    async def test_api_error_raises(
        self, sender: WhatsAppSender, mock_httpx_post: AsyncMock
    ) -> None:
        """API errors (non-200) raise WhatsAppAPIError."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.text = '{"error": {"message": "Invalid param"}}'
        mock_response.raise_for_status.side_effect = httpx2.HTTPStatusError(
            "400 Bad Request", request=AsyncMock(), response=mock_response
        )
        mock_httpx_post.return_value = mock_response

        with pytest.raises(WhatsAppAPIError, match="Invalid param"):
            await sender.send_text(to="+919876543210", text="Hello")

    @pytest.mark.asyncio
    async def test_missing_settings_raises(self) -> None:
        """Fails loud if access token or phone ID are missing."""
        with patch("src.whatsapp.sender.get_settings") as mock_settings:
            mock_settings.return_value.whatsapp_access_token = None
            mock_settings.return_value.whatsapp_phone_number_id = "test-phone-id"

            with pytest.raises(RuntimeError, match="WHATSAPP_ACCESS_TOKEN is not configured"):
                WhatsAppSender()

            mock_settings.return_value.whatsapp_access_token = "test"
            mock_settings.return_value.whatsapp_phone_number_id = None
            with pytest.raises(RuntimeError, match="WHATSAPP_PHONE_NUMBER_ID is not configured"):
                WhatsAppSender()
