"""SQLite-backed exact cosine search for the small seeded FAQ corpus."""

from typing import cast

import numpy as np
from numpy.typing import NDArray

from admitflow.adapters.sqlite import Repository


class VectorStore:
    def __init__(self, repository: Repository) -> None:
        self.repository = repository

    def search(
        self, tenant_id: str, query: list[float], *, model: str, limit: int = 3
    ) -> list[dict[str, object]]:
        query_vector = np.asarray(query, dtype=np.float32)
        query_norm = float(np.linalg.norm(query_vector))
        if query_norm == 0:
            return []
        matches: list[dict[str, object]] = []
        for chunk in self.repository.ranked_chunks(tenant_id, model):
            dimension = int(chunk["embedding_dimension"] or 0)
            vector = np.frombuffer(chunk["embedding"], dtype=np.float32)
            if dimension != query_vector.size or vector.size != query_vector.size:
                continue
            norm = float(np.linalg.norm(vector))
            if norm == 0:
                continue
            similarity = float(np.dot(query_vector, vector) / (query_norm * norm))
            matches.append({**chunk, "similarity": similarity})
        matches.sort(key=lambda item: cast(float, item["similarity"]), reverse=True)
        return matches[:limit]

    @staticmethod
    def pack(vector: list[float]) -> tuple[bytes, int]:
        array: NDArray[np.float32] = np.asarray(vector, dtype=np.float32)
        return array.tobytes(), int(array.size)
