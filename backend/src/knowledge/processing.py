"""Durable upload claims, bounded embedding and atomic publication of ready knowledge."""

import asyncio
import logging
import math
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from litellm import aembedding
from sqlalchemy import select, update

from src.core.rag import chunk_text
from src.core.security import decrypt_bytes
from src.core.settings import get_settings
from src.db.audit import write_audit_log
from src.db.models import Document, DocumentChunk, KnowledgeUpload
from src.db.session import get_sessionmaker
from src.knowledge.extraction import ExtractionError, extract_file

logger = logging.getLogger(__name__)


async def embed_chunks(chunks: list[str]) -> list[list[float]]:
    """Use the configured OpenAI model with the database's explicit 1536 dimensions."""
    settings = get_settings()
    model = settings.llm_embedding_model
    if not (model.startswith("text-embedding-") or model.startswith("openai/")):
        raise ValueError("An OpenAI embedding model is required")
    if not settings.openai_api_key:
        raise ValueError("OpenAI embedding credentials are not configured")
    embeddings: list[list[float]] = []
    for start in range(0, len(chunks), 64):
        batch = chunks[start : start + 64]
        response: Any = await aembedding(
            model=model,
            input=batch,
            dimensions=1536,
            timeout=30,
            num_retries=1,
            api_key=settings.openai_api_key.get_secret_value(),
        )
        items = sorted(response.data, key=lambda item: item["index"])
        if len(items) != len(batch) or [i["index"] for i in items] != list(range(len(batch))):
            raise ValueError("Invalid embedding batch")
        for item in items:
            vector = [float(v) for v in item["embedding"]]
            if len(vector) != 1536 or not all(math.isfinite(v) for v in vector) or not any(vector):
                raise ValueError("Invalid embedding dimensions")
            embeddings.append(vector)
    return embeddings


async def process_upload(tenant_id: uuid.UUID, upload_id: uuid.UUID) -> None:
    """Claim once, process outside the transaction, then publish only the current attempt."""
    attempt = uuid.uuid4()
    sessions = get_sessionmaker()
    async with sessions() as db:
        result = await db.execute(
            update(KnowledgeUpload)
            .where(
                KnowledgeUpload.id == upload_id,
                KnowledgeUpload.tenant_id == tenant_id,
                KnowledgeUpload.status == "queued",
            )
            .values(
                status="processing",
                attempt_id=attempt,
                error_code=None,
                attempts=KnowledgeUpload.attempts + 1,
            )
            .returning(
                KnowledgeUpload.source_enc,
                KnowledgeUpload.filename,
                KnowledgeUpload.relative_path,
                KnowledgeUpload.content_hash,
            )
        )
        row = result.first()
        await db.commit()
    if row is None:
        return
    try:
        async with asyncio.timeout(get_settings().ingestion_timeout_seconds):
            raw = decrypt_bytes(row.source_enc)
            text = await asyncio.to_thread(extract_file, row.filename, raw)
            chunks = chunk_text(text)
            if len(chunks) > 500:
                raise ExtractionError("text_limit")
            vectors = await embed_chunks(chunks)
            async with sessions() as db:
                upload = await db.scalar(
                    select(KnowledgeUpload)
                    .where(
                        KnowledgeUpload.id == upload_id,
                        KnowledgeUpload.tenant_id == tenant_id,
                        KnowledgeUpload.status == "processing",
                        KnowledgeUpload.attempt_id == attempt,
                    )
                    .with_for_update()
                )
                if upload is None:
                    return  # Deleted, cancelled or superseded during processing.
                doc = Document(
                    tenant_id=tenant_id,
                    title=row.filename,
                    content_hash=row.content_hash,
                    metadata_json={"source": "institution-upload", "path": row.relative_path},
                )
                db.add(doc)
                await db.flush()
                for index, (content, vector) in enumerate(zip(chunks, vectors, strict=True)):
                    db.add(
                        DocumentChunk(
                            tenant_id=tenant_id,
                            document_id=doc.id,
                            chunk_index=index,
                            content=content,
                            embedding=vector,
                            embedding_model=get_settings().llm_embedding_model,
                        )
                    )
                upload.document_id = doc.id
                upload.chunk_count = len(chunks)
                upload.status = "ready"
                upload.error_code = None
                await write_audit_log(
                    db,
                    tenant_id=tenant_id,
                    actor="ingestion-worker",
                    action="knowledge.ready",
                    details={"upload_id": str(upload_id), "chunks": len(chunks)},
                )
                await db.commit()
    except asyncio.CancelledError:
        raise  # A crashed/cancelled worker is recovered after its lease expires.
    except Exception as error:
        code = (
            str(error)
            if isinstance(error, ExtractionError)
            else ("processing_timeout" if isinstance(error, TimeoutError) else "indexing_failed")
        )
        async with sessions() as db:
            await db.execute(
                update(KnowledgeUpload)
                .where(
                    KnowledgeUpload.id == upload_id,
                    KnowledgeUpload.tenant_id == tenant_id,
                    KnowledgeUpload.attempt_id == attempt,
                    KnowledgeUpload.status == "processing",
                )
                .values(status="failed", error_code=code)
            )
            await db.commit()
        logger.warning("knowledge_ingestion_failed upload=%s code=%s", upload_id, code)


async def dispatch_pending() -> None:
    """A database-backed inbox survives enqueue failures and lost worker leases."""
    from src.tasks.knowledge import ingest_upload

    cutoff = datetime.now(UTC) - timedelta(seconds=get_settings().ingestion_timeout_seconds + 120)
    async with get_sessionmaker()() as db:
        await db.execute(
            update(KnowledgeUpload)
            .where(
                KnowledgeUpload.status == "processing",
                KnowledgeUpload.updated_at < cutoff,
            )
            .values(status="queued", attempt_id=None)
        )
        rows = (
            await db.execute(
                select(KnowledgeUpload.tenant_id, KnowledgeUpload.id)
                .where(KnowledgeUpload.status == "queued")
                .order_by(KnowledgeUpload.created_at)
                .limit(100)
            )
        ).all()
        await db.commit()
    for tenant_id, upload_id in rows:
        await ingest_upload.kiq(str(tenant_id), str(upload_id))


async def recovery_loop() -> None:
    while True:
        try:
            await dispatch_pending()
        except asyncio.CancelledError:
            raise
        except Exception:
            logger.warning("knowledge_dispatch_unavailable; durable jobs will be retried")
        await asyncio.sleep(15)
