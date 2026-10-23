"""Only consented inactive inquiries may receive bounded outreach."""

import json
from datetime import UTC, datetime, timedelta
from types import SimpleNamespace

import pytest

from src.db.enums import LeadStatus
from src.outreach import followups
from src.outreach.followups import eligible, safe_hook


def test_eligibility_requires_consent_inactivity_and_an_early_stage():
    now = datetime(2026, 10, 24, 10, tzinfo=UTC)
    lead = SimpleNamespace(
        followup_consent=False,
        copilot_mode=False,
        status=LeadStatus.DISCOVERING,
        reengagement_attempts=0,
        last_inbound_at=now - timedelta(days=4),
        last_outbound_at=None,
    )
    assert not eligible(lead, 3, now)
    lead.followup_consent = True
    assert eligible(lead, 3, now)
    for stage in (
        LeadStatus.HANDED_OFF,
        LeadStatus.PAYMENT_PENDING,
        LeadStatus.UNDER_REVIEW,
        LeadStatus.ENROLLED,
        LeadStatus.REJECTED,
        LeadStatus.WAITLISTED,
        LeadStatus.COLD,
    ):
        lead.status = stage
        assert not eligible(lead, 3, now)
    lead.status = LeadStatus.QUALIFYING
    lead.reengagement_attempts = 2
    assert not eligible(lead, 3, now)
    lead.reengagement_attempts = 1
    lead.copilot_mode = True
    assert not eligible(lead, 3, now)
    lead.copilot_mode = False
    lead.last_outbound_at = now - timedelta(hours=2)
    assert not eligible(lead, 3, now)


def test_hook_rejects_urgency_prices_and_external_actions():
    assert safe_hook("Would you like to continue exploring this course?")
    for text in (
        "Only 2 seats left!",
        "Pay ₹100 today",
        "Hurry, last chance!",
        "visit https://example.test",
        "Guaranteed admission",
        "जल्दी करें",
        "അവസാന അവസരം",
    ):
        assert not safe_hook(text)


@pytest.mark.parametrize("mode", ["unsafe", "rejected", "unavailable"])
async def test_generated_hooks_fall_back_without_inventing_claims(monkeypatch, mode):
    async def complete(messages, response_format=None, **kwargs):
        if mode == "unavailable":
            raise ConnectionError("Synthetic provider outage")
        data = (
            {
                "text": "Only 2 seats left?"
                if mode == "unsafe"
                else "Would you like to continue this inquiry?"
            }
            if response_format.__name__ == "Hook"
            else {"safe": False}
        )
        return SimpleNamespace(
            choices=[SimpleNamespace(message=SimpleNamespace(content=json.dumps(data)))]
        )

    monkeypatch.setattr(followups, "generate_completion", complete)
    assert (
        await followups.generate_hook({"language": "en"}, {"language": "en"})
        == "Would you like to continue this inquiry or ask a question?"
    )
