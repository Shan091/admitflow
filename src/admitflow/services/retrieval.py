"""Seed indexing and fail-closed semantic FAQ retrieval."""

import logging
from typing import cast

from admitflow.adapters.sqlite import Repository
from admitflow.adapters.vector_store import VectorStore
from admitflow.services.contracts import Embedder

logger = logging.getLogger(__name__)


class RetrievalService:
    def __init__(
        self,
        repository: Repository,
        vector_store: VectorStore,
        embedder: Embedder | None,
        model: str,
        min_similarity: float,
        min_margin: float,
    ) -> None:
        self.repository = repository
        self.vector_store = vector_store
        self.embedder = embedder
        self.model = model
        self.min_similarity = min_similarity
        self.min_margin = min_margin

    async def index_seeded_faqs(self, tenant_id: str) -> int:
        if self.embedder is None:
            return 0
        pending = self.repository.get_unembedded_faqs(tenant_id, self.model)
        if not pending:
            return 0
        texts = [f"{item['title']}\n{item['question']}\n{item['answer']}" for item in pending]
        vectors = await self.embedder.embed(texts)
        if len(vectors) != len(pending):
            raise RuntimeError("Embedding response count did not match FAQ count")
        for item, vector in zip(pending, vectors, strict=True):
            packed, dimension = self.vector_store.pack(vector)
            self.repository.save_embedding(tenant_id, item["id"], self.model, packed, dimension)
        return len(pending)

    async def answer(self, tenant_id: str, question: str) -> tuple[str, str] | None:
        if self.embedder is None:
            return None
        try:
            query = (await self.embedder.embed([question]))[0]
        except Exception:
            logger.exception("FAQ query embedding failed")
            return None
        try:
            matches = self.vector_store.search(tenant_id, query, model=self.model, limit=2)
        except Exception:
            logger.exception("FAQ vector search failed")
            return None
        if not matches:
            return None
        best = matches[0]
        score = cast(float, best["similarity"])
        second_score = cast(float, matches[1]["similarity"]) if len(matches) > 1 else -1.0
        if score < self.min_similarity or score - second_score < self.min_margin:
            return None
        content = str(best["answer"])
        source = str(best["source"])
        if not content.strip() or not source.strip():
            return None
        return content, source
