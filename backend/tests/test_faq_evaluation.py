"""Scoring checks internal evidence, plain answers and language-specific abstention."""

import uuid

from src.engine.contracts import GroundingSource, Reply
from src.scripts.evaluate_faq import Case, score_answer


def source(path: str = "synthetic-campus-reference.txt") -> GroundingSource:
    return GroundingSource(
        document_id=uuid.uuid4(), chunk_id=uuid.uuid4(), relative_path=path, passage=1
    )


def test_supported_answer_requires_expected_fact_and_internal_reference() -> None:
    case = Case(id="en-campus", language="en", question="Where?", expected="campus is in Kochi")
    text = "The demo campus is in Kochi."
    assert score_answer(case, Reply(text=text, source=source()))
    assert not score_answer(case, Reply(text=text))
    assert not score_answer(case, Reply(text="A hostel exists.", source=source()))
    assert not score_answer(case, Reply(text=text, source=source("other.txt")))
    assert not score_answer(case, Reply(text=text + "\n\nSource: reference", source=source()))
    assert not score_answer(
        case, Reply(text=text + " synthetic-campus-reference.txt", source=source())
    )


def test_unsupported_answer_requires_language_specific_abstention() -> None:
    from src.engine.journey import copy

    case = Case(id="ml-unknown", language="ml", question="Unsupported?", expected=None)
    text = copy("unknown", {"language": "ml"})
    assert score_answer(case, Reply(text=text))
    assert not score_answer(case, Reply(text=text, source=source()))
    assert not score_answer(case, Reply(text=copy("unavailable", {"language": "ml"})))
    assert not score_answer(case, Reply(text="The campus is in Kochi."))
