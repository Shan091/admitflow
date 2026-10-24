"""Channel-neutral input and validated plain-text reply boundary."""

import uuid
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator


class Event(BaseModel):
    model_config = ConfigDict(extra="forbid")
    update_id: StrictInt = Field(ge=0)
    user_id: StrictInt = Field(gt=0, lt=2**63)
    chat_id: StrictInt = Field(gt=0, lt=2**63)
    message_id: StrictInt = Field(gt=0)
    kind: Literal["text", "callback", "unsupported"]
    text: str = Field(default="", max_length=4096)
    callback_id: str | None = Field(default=None, max_length=256)


class Button(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1, max_length=60)
    data: str = Field(min_length=1, max_length=64)

    @field_validator("data")
    @classmethod
    def bytes_limit(cls, value: str) -> str:
        if len(value.encode()) > 64:
            raise ValueError("Callback exceeds transport limit")
        return value


class GroundingSource(BaseModel):
    """Internal evidence persisted in encrypted replies, excluded from channel payloads."""

    model_config = ConfigDict(extra="forbid")
    document_id: uuid.UUID
    chunk_id: uuid.UUID
    relative_path: str = Field(min_length=1, max_length=1024)
    passage: int = Field(ge=1)


class Reply(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1, max_length=3500)
    buttons: list[Button] = Field(default_factory=list, max_length=12)
    source: GroundingSource | None = None

    @field_validator("text")
    @classmethod
    def plain_text(cls, value: str) -> str:
        if not value.strip() or any(ord(c) < 32 and c not in "\n\t" for c in value):
            raise ValueError("Invalid reply text")
        if len(value.encode("utf-16-le")) // 2 > 4000:
            raise ValueError("Reply exceeds transport limit")
        return value
