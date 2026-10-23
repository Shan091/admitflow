"""Background tasks for message processing.

For now this module holds only the ``ping`` task used to verify the broker is
operational (Task 3 acceptance criterion). The real ``process_inbound_message``
worker arrives in Task 17.
"""

from __future__ import annotations

from typing import Any

from src.core.settings import get_settings
from src.engine.dispatcher import handle_turn
from src.tasks.broker import broker


@broker.task
async def ping(payload: str = "pong") -> dict[str, str]:
    """Smoke-test task: returns ``{"result": payload}``.

    Enqueued from the ``/debug/enqueue-ping`` endpoint to prove the full
    TaskIQ pipeline (enqueue → broker → worker → result backend) is healthy.
    """
    return {"result": payload}


@broker.task
async def process_inbound_message(payload: dict[str, Any]) -> None:
    """Process an inbound WhatsApp message (Task 17).

    This is a placeholder for the actual dispatcher that will be built
    in Phase 3. The webhook enqueues messages here after deduplication.
    """
    if get_settings().legacy_whatsapp_enabled:
        await handle_turn(payload)
