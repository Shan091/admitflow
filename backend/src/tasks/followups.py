"""Follow-up jobs carry only tenant and lead identifiers, never student content."""

import uuid

from src.outreach.followups import process_followup
from src.tasks.broker import broker
from src.tasks.outbound import send_outbound_message


@broker.task
async def send_followup(tenant_id: str, lead_id: str) -> None:
    message_id = await process_followup(uuid.UUID(tenant_id), uuid.UUID(lead_id))
    if message_id:
        await send_outbound_message.kiq(str(message_id))
