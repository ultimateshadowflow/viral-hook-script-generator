"""Platform / provider adapters — the boundary to the outside world."""

from viral_hook_generator.adapters.base_provider import LLMProvider, ProviderError
from viral_hook_generator.adapters.provider_factory import build_provider

__all__ = ["LLMProvider", "ProviderError", "build_provider"]