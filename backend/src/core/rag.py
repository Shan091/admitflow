"""RAG pipeline core logic (Task 13).

Handles ingestion (chunking, embedding), hybrid search (dense + lexical), and
chunk sanitization.
"""

import hashlib
import re
import uuid
from typing import Any

from litellm import aembedding
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.settings import get_settings
from src.db.models.knowledge import Document, DocumentChunk


async def embed_text(text: str) -> list[float]:
    """Generate embedding for text using configured model."""
    settings = get_settings()
    response = await aembedding(
        model=settings.llm_embedding_model,
        input=text,
    )
    # litellm returns an object that mimics OpenAI's response
    # We can access it as a dict or object
    try:
        return response.data[0]["embedding"]  # type: ignore
    except (AttributeError, TypeError):
        return response["data"][0]["embedding"]  # type: ignore


def chunk_text(text: str, chunk_size: int = 1000, overlap: int = 200) -> list[str]:
    """Simple sliding window chunker."""
    chunks = []
    start = 0
    text_len = len(text)
    while start < text_len:
        end = min(start + chunk_size, text_len)
        chunks.append(text[start:end])
        if end == text_len:
            break
        start += chunk_size - overlap
    return chunks


async def ingest_document(
    session: AsyncSession,
    tenant_id: uuid.UUID,
    title: str,
    content: str,
    source_url: str | None = None,
    metadata_json: dict[str, Any] | None = None,
) -> Document:
    """Chunk, embed, and store a document in pgvector."""
    settings = get_settings()

    # Check content hash
    content_hash = hashlib.sha256(content.encode()).hexdigest()

    doc = Document(
        tenant_id=tenant_id,
        title=title,
        content_hash=content_hash,
        source_url=source_url,
        metadata_json=metadata_json,
    )
    session.add(doc)
    await session.flush()

    raw_chunks = chunk_text(content)

    # litellm aembedding supports batching
    response = await aembedding(
        model=settings.llm_embedding_model,
        input=raw_chunks,
    )

    try:
        embeddings = [item["embedding"] for item in response.data]
    except (AttributeError, TypeError):
        embeddings = [item["embedding"] for item in response["data"]]

    for i, (chunk_content, emb) in enumerate(zip(raw_chunks, embeddings, strict=True)):
        chunk = DocumentChunk(
            tenant_id=tenant_id,
            document_id=doc.id,
            chunk_index=i,
            content=chunk_content,
            embedding_model=settings.llm_embedding_model,
            embedding=emb,
        )
        session.add(chunk)

    return doc


async def search_chunks(
    session: AsyncSession,
    tenant_id: uuid.UUID,
    query: str,
    top_k: int = 5,
) -> list[DocumentChunk]:
    """Hybrid search (dense + lexical with RRF)."""
    query_emb = await embed_text(query)

    # Format the embedding for pgvector SQL
    query_str = f"[{','.join(map(str, query_emb))}]"

    # We use a CTE to rank dense and lexical separately, then combine via RRF formula: 1 / (60 + rank)  # noqa: E501
    stmt = (
        select(DocumentChunk)
        .from_statement(
            text("""
        WITH dense AS (
            SELECT id, ROW_NUMBER() OVER (ORDER BY embedding <=> :query_emb_str) as dense_rank
            FROM document_chunks
            WHERE tenant_id = :tenant_id
        ),
        lexical AS (
            SELECT id, ROW_NUMBER() OVER (
                ORDER BY ts_rank_cd(
                    to_tsvector('english', content), 
                    plainto_tsquery('english', :query)
                ) DESC
            ) as lexical_rank
            FROM document_chunks
            WHERE tenant_id = :tenant_id
        )
        SELECT dc.*
        FROM document_chunks dc
        JOIN dense d ON d.id = dc.id
        JOIN lexical l ON l.id = dc.id
        ORDER BY COALESCE(1.0 / (60 + d.dense_rank), 0.0) + 
                 COALESCE(1.0 / (60 + l.lexical_rank), 0.0) DESC
        LIMIT :top_k
        """)
        )
        .params(
            query_emb_str=query_str,
            query=query,
            tenant_id=tenant_id,
            top_k=top_k,
        )
    )

    result = await session.scalars(stmt)
    return list(result.all())


# Pre-compiled regex for zero-latency prompt injection/RAG poisoning detection
# Matches common jailbreak signatures, role-play overrides, and instruction ignores.
JAILBREAK_PATTERN = re.compile(
    r"(?i)\b("
    r"ignore previous instructions|"
    r"system prompt|"
    r"forget all commands|"
    r"you are now a|"
    r"new role|"
    r"disregard previous|"
    r"bypassing|"
    r"jailbreak|"
    r"dan mode|"
    r"developer mode|"
    r"admin mode|"
    r"do anything now"
    r")\b"
)


async def sanitize_chunks(chunks: list[DocumentChunk]) -> list[DocumentChunk]:
    """Sanitizer to prevent RAG poisoning.

    Blocks chunks that contain obvious prompt injection attempts using a
    zero-latency pre-compiled regex pattern.
    """
    safe_chunks = []
    for chunk in chunks:
        if JAILBREAK_PATTERN.search(chunk.content):
            continue
        safe_chunks.append(chunk)
    return safe_chunks
