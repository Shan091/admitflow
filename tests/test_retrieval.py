from pathlib import Path

import pytest

from admitflow.adapters.sqlite import Repository
from admitflow.adapters.vector_store import VectorStore
from admitflow.services.retrieval import RetrievalService


class FixedEmbedder:
    def __init__(self, vectors: list[list[float]]) -> None:
        self.vectors = vectors
        self.texts: list[str] = []

    async def embed(self, texts: list[str]) -> list[list[float]]:
        self.texts.extend(texts)
        return self.vectors[: len(texts)]


def make_repository(tmp_path: Path) -> Repository:
    repository = Repository(tmp_path / "demo.sqlite3")
    repository.initialize()
    repository.seed_catalog()
    return repository


@pytest.mark.asyncio
async def test_retrieval_indexes_seeded_faqs_and_returns_source(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)
    embedder = FixedEmbedder([[1.0, 0.0]] * 4)
    service = RetrievalService(repository, VectorStore(repository), embedder, "fake", 0.72, 0.05)

    assert await service.index_seeded_faqs(repository.tenant_id) == 4
    indexed_text = "\n".join(embedder.texts)
    assert "Is hostel accommodation available?" in indexed_text
    assert "Can students stay in a hostel?" in indexed_text
    assert "This fictional demo institution" not in indexed_text
    # First FAQ is the best match; other seeded vectors deliberately have lower scores.
    repository.save_embedding(
        repository.tenant_id, "class-format", "fake", b"\x00\x00\x00\x00\x00\x00\x80?", 2
    )
    repository.save_embedding(
        repository.tenant_id, "language-support", "fake", b"\x00\x00\x00\x00\x00\x00\x80?", 2
    )
    repository.save_embedding(
        repository.tenant_id, "course-duration", "fake", b"\x00\x00\x00\x00\x00\x00\x80?", 2
    )

    answer = await service.answer(repository.tenant_id, "hostel question")

    assert answer is not None
    assert answer[1] == "Accommodation information"


@pytest.mark.asyncio
async def test_retrieval_abstains_on_low_score_and_missing_embedder(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)
    for faq in repository.get_unembedded_faqs(repository.tenant_id, "fake"):
        repository.save_embedding(
            repository.tenant_id, faq["id"], "fake", b"\x00\x00\x80?\x00\x00\x00\x00", 2
        )

    low_score = RetrievalService(
        repository, VectorStore(repository), FixedEmbedder([[0.0, 1.0]]), "fake", 0.72, 0.05
    )
    unavailable = RetrievalService(repository, VectorStore(repository), None, "fake", 0.72, 0.05)

    assert await low_score.answer(repository.tenant_id, "unrelated") is None
    assert await unavailable.answer(repository.tenant_id, "anything") is None


@pytest.mark.asyncio
async def test_retrieval_abstains_when_top_matches_are_ambiguous(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)
    for faq in repository.get_unembedded_faqs(repository.tenant_id, "fake"):
        repository.save_embedding(
            repository.tenant_id, faq["id"], "fake", b"\x00\x00\x80?\x00\x00\x00\x00", 2
        )
    service = RetrievalService(
        repository, VectorStore(repository), FixedEmbedder([[1.0, 0.0]]), "fake", 0.72, 0.05
    )

    assert await service.answer(repository.tenant_id, "ambiguous") is None


def test_vector_search_ignores_embeddings_from_a_different_model(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)
    faq = repository.get_unembedded_faqs(repository.tenant_id, "old-model")[0]
    repository.save_embedding(repository.tenant_id, faq["id"], "old-model", b"\x00\x00\x80?", 1)
    vectors = VectorStore(repository)

    assert vectors.search(repository.tenant_id, [1.0], model="current-model") == []
    assert vectors.search(repository.tenant_id, [1.0], model="old-model")
    assert vectors.search("another-tenant", [1.0], model="old-model") == []


def test_vector_search_skips_dimension_mismatch(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)
    faq = repository.get_unembedded_faqs(repository.tenant_id, "fake")[0]
    repository.save_embedding(repository.tenant_id, faq["id"], "fake", b"\x00\x00\x80?", 1)

    assert VectorStore(repository).search(repository.tenant_id, [1.0, 0.0], model="fake") == []


@pytest.mark.asyncio
async def test_retrieval_fails_closed_when_vector_search_errors(tmp_path: Path) -> None:
    repository = make_repository(tmp_path)

    class BrokenVectorStore:
        def search(self, tenant_id: str, query: list[float], *, model: str, limit: int = 3):
            raise RuntimeError("simulated vector storage failure")

    service = RetrievalService(
        repository,
        BrokenVectorStore(),  # type: ignore[arg-type]
        FixedEmbedder([[1.0, 0.0]]),
        "fake",
        0.72,
        0.05,
    )

    assert await service.answer(repository.tenant_id, "question") is None
