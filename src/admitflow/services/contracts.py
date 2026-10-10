"""Small replaceable boundaries used by application services."""

from typing import Protocol


class Embedder(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]: ...


class IntentRouter(Protocol):
    async def route(self, text: str) -> str: ...
