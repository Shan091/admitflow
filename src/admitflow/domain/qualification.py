"""Code-owned qualification rules."""

from admitflow.domain.models import QualificationResult


def assess_eligibility(
    *, completed_grade12: bool, marks_percent: float, minimum_marks_percent: float
) -> QualificationResult:
    """Evaluate the demo course's two hard requirements without involving a model."""
    if not 0 <= marks_percent <= 100:
        raise ValueError("Marks must be between 0 and 100.")
    if not completed_grade12:
        return QualificationResult(False, "Grade 12 completion is required for this demo course.")
    if marks_percent < minimum_marks_percent:
        return QualificationResult(
            False,
            f"The demo course requires at least {minimum_marks_percent:g}% overall marks.",
        )
    return QualificationResult(True, "The supplied answers meet the demo course requirements.")
