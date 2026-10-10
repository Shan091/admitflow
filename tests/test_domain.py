import pytest

from admitflow.domain.pricing import format_inr_from_paise
from admitflow.domain.qualification import assess_eligibility


def test_eligibility_requires_grade_twelve_even_with_high_marks() -> None:
    result = assess_eligibility(completed_grade12=False, marks_percent=99, minimum_marks_percent=50)
    assert not result.eligible
    assert "Grade 12" in result.reason


def test_eligibility_threshold_is_inclusive() -> None:
    result = assess_eligibility(completed_grade12=True, marks_percent=50, minimum_marks_percent=50)
    assert result.eligible


def test_marks_below_course_threshold_are_ineligible() -> None:
    result = assess_eligibility(
        completed_grade12=True, marks_percent=49.99, minimum_marks_percent=50
    )
    assert not result.eligible


@pytest.mark.parametrize("marks", [-0.1, 100.1])
def test_qualification_rejects_out_of_range_marks(marks: float) -> None:
    with pytest.raises(ValueError):
        assess_eligibility(completed_grade12=True, marks_percent=marks, minimum_marks_percent=50)


def test_fee_formatting_uses_rupees_and_paise() -> None:
    assert format_inr_from_paise(123456) == "₹1,234.56"
    assert format_inr_from_paise(50000) == "₹500"


def test_fee_formatting_rejects_negative_amount() -> None:
    with pytest.raises(ValueError):
        format_inr_from_paise(-1)
