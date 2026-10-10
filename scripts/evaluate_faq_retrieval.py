"""Evaluate the fixed seeded FAQ corpus with short, fictional live query examples."""

import asyncio
from dataclasses import dataclass

from dotenv import load_dotenv

from admitflow.adapters.openai import OpenAIAdapter
from admitflow.adapters.sqlite import Repository
from admitflow.adapters.vector_store import VectorStore
from admitflow.config import get_settings
from admitflow.services.retrieval import RetrievalService, embedding_index_key

load_dotenv()


@dataclass(frozen=True, slots=True)
class Case:
    name: str
    question: str
    expected_id: str | None


CASES = (
    Case("hostel / canonical", "Is hostel accommodation available?", "hostel"),
    Case("hostel / accommodation", "Can students stay in a hostel?", "hostel"),
    Case("hostel / housing", "Do you provide a place to live during the course?", "hostel"),
    Case("hostel / availability", "Is accommodation available for learners?", "hostel"),
    Case("classes / canonical", "How are classes conducted?", "class-format"),
    Case("classes / format", "Are the classes instructor-led or self-paced?", "class-format"),
    Case("classes / practice", "Do students get guided practical sessions?", "class-format"),
    Case("classes / structure", "What happens in a typical class?", "class-format"),
    Case("language / canonical", "Which languages can I use?", "language-support"),
    Case("language / English", "Can I interact in English?", "language-support"),
    Case("language / Hinglish", "Can I chat with the bot in Hinglish?", "language-support"),
    Case("language / options", "Which languages are supported for questions?", "language-support"),
    Case("duration / canonical", "How long does a course take?", "course-duration"),
    Case("duration / length", "How many months does a course take?", "course-duration"),
    Case("out of scope / schedule", "When will the program be finished?", None),
    Case("duration / time", "How long should I expect the course to run?", "course-duration"),
    Case("out of scope / aid", "Do you offer scholarships or financial aid?", None),
    Case("out of scope / weather", "What is today's weather forecast in Kochi?", None),
    Case("out of scope / sports", "Who won the cricket match last night?", None),
    Case("out of scope / Wi-Fi", "What is the campus Wi-Fi password?", None),
    Case("unsupported / online", "Are the courses taught online?", None),
    Case("unsupported / location", "Which city is the institution located in?", None),
    Case("unsupported / dates", "When does the next course start?", None),
    Case("unsupported / admission", "How do I apply for admission?", None),
    Case("unsupported / refunds", "Can I get a refund for the application fee?", None),
    Case("unsupported / placement", "Does the institution provide placement assistance?", None),
    Case("unsupported / certificate", "Will I receive a certificate after the course?", None),
)


class OneVectorEmbedder:
    """Feed the live query vector through the same retrieval decision path."""

    def __init__(self, vector: list[float]) -> None:
        self.vector = vector

    async def embed(self, texts: list[str]) -> list[list[float]]:
        if len(texts) != 1:
            raise ValueError("Evaluation decision expects one query at a time")
        return [self.vector]


async def evaluate() -> int:
    settings = get_settings()
    if not settings.openai_api_key:
        print("OPENAI_API_KEY is required for live retrieval evaluation.")
        return 2

    repository = Repository(settings.database_path)
    repository.initialize()
    repository.seed_catalog()
    index_key = embedding_index_key(settings.openai_embedding_model)
    adapter = OpenAIAdapter(
        settings.openai_api_key,
        settings.openai_decisions_model,
        settings.openai_embedding_model,
    )
    try:
        vector_store = VectorStore(repository)
        indexer = RetrievalService(
            repository,
            vector_store,
            adapter,
            index_key,
            settings.rag_min_similarity,
            settings.rag_min_margin,
        )
        indexed = await indexer.index_seeded_faqs(repository.tenant_id)
        query_vectors = await adapter.embed([case.question for case in CASES])
        if len(query_vectors) != len(CASES):
            print("OpenAI returned an unexpected number of query embeddings.")
            return 2

        sources = {
            str(chunk["id"]): str(chunk["source"])
            for chunk in repository.ranked_chunks(repository.tenant_id, index_key)
        }
        print(
            f"Model={settings.openai_embedding_model}; profile={index_key}; "
            f"cases={len(CASES)}; "
            f"min_similarity={settings.rag_min_similarity:.2f}; "
            f"min_margin={settings.rag_min_margin:.2f}; "
            f"newly_indexed_faqs={indexed}; "
            f"input_tokens={adapter.total_embedding_prompt_tokens}"
        )
        print("case | expected | actual | top score | margin | result")
        passed = 0
        for case, query_vector in zip(CASES, query_vectors, strict=True):
            matches = vector_store.search(
                repository.tenant_id,
                query_vector,
                model=index_key,
                limit=2,
            )
            service = RetrievalService(
                repository,
                vector_store,
                OneVectorEmbedder(query_vector),
                index_key,
                settings.rag_min_similarity,
                settings.rag_min_margin,
            )
            answer = await service.answer(repository.tenant_id, case.question)
            actual_source = answer[1] if answer else None
            expected_source = sources.get(case.expected_id) if case.expected_id else None
            top_score = float(matches[0]["similarity"]) if matches else None
            second_score = float(matches[1]["similarity"]) if len(matches) > 1 else -1.0
            margin = top_score - second_score if top_score is not None else None
            success = actual_source == expected_source
            passed += int(success)
            score_display = f"{top_score:.3f}" if top_score is not None else "n/a"
            margin_display = f"{margin:.3f}" if margin is not None else "n/a"
            print(
                f"{case.name} | {expected_source or 'ABSTAIN'} | "
                f"{actual_source or 'ABSTAIN'} | {score_display} | {margin_display} | "
                f"{'PASS' if success else 'FAIL'}"
            )
        print(f"Result: {passed}/{len(CASES)} cases passed")
        return 0 if passed == len(CASES) else 1
    finally:
        await adapter.close()


if __name__ == "__main__":
    raise SystemExit(asyncio.run(evaluate()))
