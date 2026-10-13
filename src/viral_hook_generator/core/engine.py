"""HookEngine — the top-level orchestrator.

Composes:
- a provider adapter (LLM backend)
- the prompt service (renders the generation prompt)
- the scoring service (ranks candidates)
- the pipeline (generate → parse → score → sort)
"""

from __future__ import annotations

from viral_hook_generator.config.settings import Settings, load_settings
from viral_hook_generator.core.pipeline import HookPipeline
from viral_hook_generator.models.brief import ContentBrief
from viral_hook_generator.models.hook import HookBatch
from viral_hook_generator.services.prompt_services.hook_prompt_builder import HookPromptBuilder
from viral_hook_generator.services.scoring_services.virality_scorer import ViralityScorer
from viral_hook_generator.adapters.provider_factory import build_provider


class HookEngine:
    def __init__(
        self,
        pipeline: HookPipeline,
        settings: Settings,
    ) -> None:
        self._pipeline = pipeline
        self._settings = settings

    @classmethod
    def from_config(cls, settings: Settings | None = None) -> "HookEngine":
        resolved = settings or load_settings()
        provider = build_provider(resolved.provider)
        prompt_builder = HookPromptBuilder()
        scorer = ViralityScorer()
        pipeline = HookPipeline(
            provider=provider,
            prompt_builder=prompt_builder,
            scorer=scorer,
        )
        return cls(pipeline=pipeline, settings=resolved)

    async def generate(self, brief: ContentBrief) -> HookBatch:
        return await self._pipeline.run(brief)