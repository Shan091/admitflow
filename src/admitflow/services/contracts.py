"""Small replaceable boundaries used by application services."""

from typing import Protocol

from admitflow.domain.models import Course, DiscoveryTurn


class Embedder(Protocol):
    async def embed(self, texts: list[str]) -> list[list[float]]: ...


class IntentRouter(Protocol):
    async def route(self, text: str) -> str: ...


class DiscoveryInterpreter(Protocol):
    async def extract_discovery(self, text: str, courses: list[Course]) -> DiscoveryTurn: ...
