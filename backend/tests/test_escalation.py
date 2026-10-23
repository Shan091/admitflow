"""Clear support signals escalate; office hours never promise an immediate reply."""

from datetime import UTC, datetime

import pytest

from src.engine.escalation import escalation_reason, office_open


@pytest.mark.parametrize(
    ("text", "reason"),
    [
        ("Can I speak to a human?", "human_request"),
        ("I am really frustrated with this", "frustration"),
        ("मुझे बहुत गुस्सा आ रहा है", "frustration"),
        ("mujhe gussa aa raha hai", "frustration"),
        ("എനിക്ക് ദേഷ്യം വരുന്നു", "frustration"),
        ("I want to hurt myself", "safety"),
        ("मैं आत्महत्या करना चाहता हूँ", "safety"),
        ("Does this course cover workplace harassment?", None),
        ("Actually my age is 17", None),
        ("I do not want to share my age", None),
    ],
)
def test_clear_escalation_signals(text, reason):
    assert escalation_reason(text) == reason


def test_office_hours_use_institution_timezone_and_end_exclusive():
    hours = {"mon": {"start": "09:00", "end": "17:00"}}
    assert office_open("Asia/Kolkata", hours, datetime(2026, 10, 26, 3, 30, tzinfo=UTC)) is True
    assert office_open("Asia/Kolkata", hours, datetime(2026, 10, 26, 11, 30, tzinfo=UTC)) is False
    assert office_open("Asia/Kolkata", hours, datetime(2026, 10, 25, 5, tzinfo=UTC)) is False
    assert office_open("Asia/Kolkata", None, datetime.now(UTC)) is None
    assert office_open("Asia/Kolkata", {}, datetime.now(UTC)) is False
    assert office_open("Unknown/Zone", hours, datetime.now(UTC)) is None
