"""TaskIQ entry point for institution document indexing."""

import uuid

from src.knowledge.processing import process_upload
from src.tasks.broker import broker


@broker.task
async def ingest_upload(tenant_id: str, upload_id: str) -> None:
    await process_upload(uuid.UUID(tenant_id), uuid.UUID(upload_id))
