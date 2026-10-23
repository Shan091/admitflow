"""RAG knowledge base models (pgvector)."""

from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any

from pgvector.sqlalchemy import Vector
from sqlalchemy import ForeignKey, Index, Integer, String, Text, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.db.base import Base, IdMixin, TenantMixin, TimestampMixin

if TYPE_CHECKING:
    pass


class Document(IdMixin, TenantMixin, TimestampMixin, Base):
    """An uploaded document in the institution's knowledge base."""

    __tablename__ = "documents"
    __table_args__ = (UniqueConstraint("tenant_id", "id", name="uq_documents_tenant_id_id"),)

    title: Mapped[str] = mapped_column(String(255), nullable=False)
    content_hash: Mapped[str] = mapped_column(String(64), nullable=False)
    source_url: Mapped[str | None] = mapped_column(String(1024))
    metadata_json: Mapped[dict[str, Any] | None] = mapped_column(JSONB)

    # Relationships
    chunks: Mapped[list[DocumentChunk]] = relationship(
        back_populates="document", cascade="all, delete-orphan"
    )


class DocumentChunk(IdMixin, TenantMixin, TimestampMixin, Base):
    """A chunk of a document, with its embedding for vector search."""

    __tablename__ = "document_chunks"

    document_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("documents.id", ondelete="CASCADE"), index=True, nullable=False
    )
    chunk_index: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)

    # OpenAI text-embedding-3-small uses 1536 dimensions.
    # ADR-007 says: "Chunks tagged with model + dimension; switching triggers a per-tenant re-index"
    embedding_model: Mapped[str] = mapped_column(
        String(64), nullable=False, default="text-embedding-3-small"
    )
    embedding: Mapped[Any] = mapped_column(Vector(1536), nullable=False)

    document: Mapped[Document] = relationship(back_populates="chunks")

    __table_args__ = (
        UniqueConstraint("document_id", "chunk_index", name="uq_chunk_index"),
        Index(
            "ix_document_chunks_embedding",
            "embedding",
            postgresql_using="hnsw",
            postgresql_with={"m": 16, "ef_construction": 64},
            postgresql_ops={"embedding": "vector_cosine_ops"},
        ),
    )
