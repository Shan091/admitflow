"""Translate retrieval queries without weakening the relevance floor."""

from types import SimpleNamespace
from typing import Any

import pytest

from src.knowledge.retrieval import contextual_query, retrieval_query


async def test_english_query_does_not_call_model(monkeypatch: pytest.MonkeyPatch) -> None:
    async def unavailable(*args: Any, **kwargs: Any) -> None:
        raise AssertionError("English queries do not need translation")

    monkeypatch.setattr("src.knowledge.retrieval.generate_completion", unavailable)
    assert await retrieval_query("Where is campus?") == "Where is campus?"


async def test_non_ascii_query_uses_validated_translation(monkeypatch: pytest.MonkeyPatch) -> None:
    async def response(*args: Any, **kwargs: Any) -> Any:
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(content='{"query":"Where is the demo campus?"}')
                )
            ]
        )

    monkeypatch.setattr("src.knowledge.retrieval.generate_completion", response)
    assert await retrieval_query("ഡെമോ ക്യാമ്പസ് എവിടെയാണ്?") == "Where is the demo campus?"


async def test_context_rewrite_is_bounded_and_treats_history_as_data(monkeypatch) -> None:
    captured = []

    async def response(messages, **kwargs):
        captured.append(messages)
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content='{"query":"What is the hostel fee?","needs_clarification":false}'
                    )
                )
            ]
        )

    monkeypatch.setattr("src.decision.generate_completion", response)
    history = [{"role": "user", "content": "x" * 2000} for _ in range(20)]
    history[-1] = {"role": "assistant", "content": "Hostel accommodation is available."}
    assert (
        await contextual_query("What does it cost?", history, "Nursing")
        == "What is the hostel fee?"
    )
    import json

    sent = json.loads(captured[0][-1]["content"])
    assert len(sent["history"]) == 6
    assert all(len(turn["content"]) <= 1000 for turn in sent["history"])
    assert "What does it cost?" not in captured[0][0]["content"]


async def test_complete_contract_sized_question_reaches_resolution(monkeypatch) -> None:
    import json

    captured = []

    async def response(messages, **kwargs):
        captured.append(json.loads(messages[-1]["content"])["question"])
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content='{"query":"Where is the library?","needs_clarification":false}'
                    )
                )
            ]
        )

    monkeypatch.setattr("src.decision.generate_completion", response)
    question = "Please help. " * 100 + "Where is the library?"
    await contextual_query(question, [{"role": "assistant", "content": "Hello"}])
    assert captured == [question]


async def test_unresolved_reference_is_not_searched(monkeypatch) -> None:
    async def response(*args, **kwargs):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content='{"query":"Which fee?","needs_clarification":true}'
                    )
                )
            ]
        )

    monkeypatch.setattr("src.decision.generate_completion", response)
    assert await contextual_query("How much is that?", [{"role": "user", "content": "Hi"}]) is None


async def test_rewrite_cannot_invent_numbers(monkeypatch) -> None:
    from src.engine.llm_factory import AllProvidersFailedError

    async def response(*args, **kwargs):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content='{"query":"Is tuition 9999 rupees?","needs_clarification":false}'
                    )
                )
            ]
        )

    monkeypatch.setattr("src.decision.generate_completion", response)
    with pytest.raises(AllProvidersFailedError, match="unsupported"):
        await contextual_query("What about fees?", [{"role": "assistant", "content": "Course A"}])


@pytest.mark.parametrize(
    ("original", "rewritten"),
    [
        ("फीस १००० रुपये", "Is the fee 1000 rupees?"),
        ("Fee is 1,00,000", "Is the fee 100000.00 rupees?"),
    ],
)
async def test_equivalent_number_formats_are_preserved(monkeypatch, original, rewritten) -> None:
    import json

    async def response(*args, **kwargs):
        return SimpleNamespace(
            choices=[
                SimpleNamespace(
                    message=SimpleNamespace(
                        content=json.dumps(
                            {
                                "query": rewritten,
                                "needs_clarification": False,
                            }
                        )
                    )
                )
            ]
        )

    monkeypatch.setattr("src.decision.generate_completion", response)
    assert (
        await contextual_query("What about that fee?", [{"role": "user", "content": original}])
        == rewritten
    )
