"""Payment-link creation runs after the requesting conversation transaction commits."""

import uuid

from src.payments.service import process_payment
from src.tasks.broker import broker
from src.tasks.outbound import send_outbound_message


@broker.task
async def create_payment_link(order_id: str) -> None:
    message_id = await process_payment(uuid.UUID(order_id))
    if message_id:
        await send_outbound_message.kiq(str(message_id))
