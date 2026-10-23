"""Deterministic clear support signals and institution-local office hours."""

import re
from datetime import datetime, time
from typing import Literal
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError

Reason = Literal["human_request", "frustration", "safety", "staff_review"]
SIGNALS: list[tuple[Reason, re.Pattern[str]]] = [
    (
        "safety",
        re.compile(
            r"\b(?:i (?:want to |am going to |will |might )?(?:kill|hurt) myself|"
            r"i (?:want to die|am suicidal|am being (?:harassed|abused)))\b|"
            r"मैं.*(?:आत्महत्या|खुद को (?:मार|नुकसान))|"
            r"(?:main|mai).*(?:khud ko.*(?:maar|nuksan)|jaan dena)|"
            r"ഞാൻ.*(?:ആത്മഹത്യ|ജീവൻ അവസാനിപ്പി)",
            re.I,
        ),
    ),
    (
        "human_request",
        re.compile(
            r"^/human(?:\s|@|$)|(?:speak|talk|connect).*(?:human|staff|counsel[lo]+r)|"
            r"(?:स्टाफ|इंसान|काउंसलर).*(?:बात|मिल)|"
            r"(?:staff|insaan|counsellor).*(?:baat|baath)|"
            r"(?:സ്റ്റാഫി|കൗൺസില).*സംസാര",
            re.I,
        ),
    ),
    (
        "frustration",
        re.compile(
            r"\b(?:i (?:am|'m)(?: really| very| so)? (?:angry|frustrated)|"
            r"you (?:are|'re) useless|this is (?:a fraud|not helping)|"
            r"(?:mujhe|main|mai).*gussa|i want to (?:complain|make a complaint))\b|"
            r"(?:मुझे|मैं).*गुस्सा|എനിക്ക്.*ദേഷ്യം",
            re.I,
        ),
    ),
]


def escalation_reason(text: str) -> Reason | None:
    return next((reason for reason, pattern in SIGNALS if pattern.search(text)), None)


def office_open(
    timezone: str, hours: dict[str, dict[str, str]] | None, now: datetime
) -> bool | None:
    if hours is None or now.tzinfo is None:
        return None
    try:
        local = now.astimezone(ZoneInfo(timezone))
        day = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")[local.weekday()]
        opening = hours.get(day)
        return bool(
            opening
            and time.fromisoformat(opening["start"])
            <= local.time()
            < time.fromisoformat(opening["end"])
        )
    except (ZoneInfoNotFoundError, ValueError, KeyError, TypeError):
        return None  # Invalid legacy configuration must not imply staff availability.
