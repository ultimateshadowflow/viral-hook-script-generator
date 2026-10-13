"""OpenAI adapter using httpx directly (no SDK lock-in).

Retries on 429 / 5xx with exponential backoff via tenacity. Timeout is
enforced per-request; total wall time is bounded by ``max_retries``.
"""

from __future__ import annotations

import os

import httpx
from tenacity import retry, retry_if_exception_type, stop_after_attempt, wait_exponential

from viral_hook_generator.adapters.base_provider import LLMProvider, ProviderError
from viral_hook_generator.config.settings import ProviderSettings

_API_URL = "https://api.openai.com/v1/chat/completions"


class OpenAIProvider(LLMProvider):
    name = "openai"

    def __init__(self, settings: ProviderSettings) -> None:
        self._settings = settings
        key = os.environ.get(settings.api_key_env)
        if not key:
            raise ProviderError(f"missing env var {settings.api_key_env}")
        self._headers = {
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json",
        }

    @retry(
        reraise=True,
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=0.5, max=8),
        retry=retry_if_exception_type(httpx.HTTPStatusError),
    )
    async def _post(self, payload: dict) -> dict:
        async with httpx.AsyncClient(timeout=self._settings.timeout_s) as client:
            resp = await client.post(_API_URL, headers=self._headers, json=payload)
            resp.raise_for_status()
            return resp.json()

    async def complete(self, prompt: str, *, max_tokens: int = 900) -> str:
        payload = {
            "model": self._settings.model,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": max_tokens,
            "temperature": 0.9,
        }
        try:
            data = await self._post(payload)
        except httpx.HTTPStatusError as exc:
            raise ProviderError(f"openai http {exc.response.status_code}") from exc
        except httpx.HTTPError as exc:
            raise ProviderError(f"openai transport error: {exc}") from exc
        try:
            return data["choices"][0]["message"]["content"]
        except (KeyError, IndexError, TypeError) as exc:
            raise ProviderError("unexpected openai response shape") from exc