"""Provider contract. One method: complete(prompt) -> raw text."""

from __future__ import annotations

from abc import ABC, abstractmethod


class ProviderError(RuntimeError):
    """Raised when a provider call fails after retries are exhausted."""


class LLMProvider(ABC):
    """Abstract LLM backend.

    Implementations must be safe to call concurrently and must raise
    :class:`ProviderError` (not bare exceptions) on failure.
    """

    name: str = "abstract"

    @abstractmethod
    async def complete(self, prompt: str, *, max_tokens: int = 900) -> str:
        """Return the raw text completion for ``prompt``."""