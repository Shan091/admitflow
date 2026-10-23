"""Evaluation rejects irrelevant quotations and does not count provider errors as abstention."""

from src.scripts.evaluate_faq import Case, score_answer


def test_supported_answer_requires_expected_fact_and_reference() -> None:
    case = Case(id="en-campus", language="en", question="Where?", expected="campus is in Kochi")
    assert score_answer(
        case, "The demo campus is in Kochi.\n\nSource: synthetic-campus-reference.txt, passage 1."
    )
    assert not score_answer(case, "The demo campus is in Kochi.")
    assert not score_answer(
        case, "A hostel exists.\n\nSource: synthetic-campus-reference.txt, passage 1."
    )
    assert not score_answer(case, "The demo campus is in Kochi.\n\nSource: other.txt, passage 1.")


def test_unsupported_answer_requires_language_specific_abstention() -> None:
    from src.engine.journey import copy

    case = Case(id="ml-unknown", language="ml", question="Unsupported?", expected=None)
    assert score_answer(case, copy("unknown", {"language": "ml"}))
    assert not score_answer(case, copy("unavailable", {"language": "ml"}))
    assert not score_answer(case, "The campus is in Kochi.")
