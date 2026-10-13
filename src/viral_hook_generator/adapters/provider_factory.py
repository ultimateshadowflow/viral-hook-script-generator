"""Provider factory — name → adapter instance."""

from __future__ import annotations

from viral_hook_generator.adapters.base_provider import LLMProvider, ProviderError
from viral_hook_generator.adapters.openai_provider import OpenAIProvider
from viral_hook_generator.config.settings import ProviderSettings

_REGISTRY: dict[str, type[LLMProvider]] = {
    "openai": OpenAIProvider,
}


def build_provider(settings: ProviderSettings) -> LLMProvider:
    try:
        cls = _REGISTRY[settings.name]
    except KeyError as exc:
        raise ProviderError(f"unknown provider {settings.name!r}") from exc
    return cls(settings)