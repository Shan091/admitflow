"""Only explicitly supplied application details may be reused in an encrypted draft."""

import re
from datetime import date
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from src.core.rag import JAILBREAK_PATTERN

DetailKey = Literal["full_name", "dob", "parent_name", "address", "previous_school"]
GREETING = re.compile(
    r"^(?:hi|hello|hey|hello there|good (?:morning|afternoon|evening))[.! ]*$", re.I
)
ACKNOWLEDGMENT = re.compile(
    r"^(?:ok(?:ay)?|yes(?: please)?|no|thanks?|thank you|continue)[.! ]*$", re.I
)
REFUSAL = re.compile(
    r"\b(?:skip|prefer not|don't (?:want to|know)|do not (?:want to|know)|not now)\b", re.I
)


class Detail(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
    key: DetailKey
    value: str = Field(min_length=1, max_length=1000)
    evidence: str = Field(min_length=1, max_length=1200)


def validated_details(details: list[Detail], text: str) -> dict[str, str]:
    result: dict[str, str] = {}
    for item in details:
        value = item.value
        if (
            item.evidence not in text
            or value.casefold() not in item.evidence.casefold()
            or GREETING.fullmatch(value)
            or ACKNOWLEDGMENT.fullmatch(value)
            or JAILBREAK_PATTERN.search(value)
            or value.startswith("/")
            or "?" in value
            or len(value) > (1000 if item.key == "address" else 200)
        ):
            continue
        if item.key == "dob":
            try:
                born = date.fromisoformat(value)
                if (
                    not re.fullmatch(r"\d{4}-\d{2}-\d{2}", value)
                    or not date(1900, 1, 1) <= born <= date.today()
                ):
                    continue
            except ValueError:
                continue
        result[item.key] = value
    return result
