"""HookPipeline — the generate → parse → score → sort flow.

Deterministic orchestration. Every provider call is wrapped in retry
by the provider adapter itself; this layer only sequences steps.
"""

from __future__ import annotations

import logging

from viral_hook_generator.adapters.base_provider import LLMProvider
from viral_hook_generator.models.brief import ContentBrief
from viral_hook_generator.models.hook import Hook, HookBatch
from viral_hook_generator.services.prompt_services.hook_prompt_builder import HookPromptBuilder
from viral_hook_generator.services.scoring_services.virality_scorer import ViralityScorer
from viral_hook_generator.utils.parsers import parse_hook_lines

log = logging.getLogger(__name__)


class HookPipeline:
    def __init__(
        self,
        provider: LLMProvider,
        prompt_builder: HookPromptBuilder,
        scorer: ViralityScorer,
    ) -> None:
        self._provider = provider
        self._prompt_builder = prompt_builder
        self._scorer = scorer

    async def run(self, brief: ContentBrief) -> HookBatch:
        prompt = self._prompt_builder.build(brief)
        log.debug("rendered prompt for topic=%r platform=%s", brief.topic, brief.platform.value)

        raw = await self._provider.complete(prompt, max_tokens=900)
        candidates = parse_hook_lines(raw, limit=brief.hook_count)

        hooks: list[Hook] = []
        for pattern, text in candidates:
            score = self._scorer.score(text, brief.platform, brief.tone)
            hooks.append(
                Hook(
                    text=text,
                    virality_score=score.total,
                    pattern=pattern,
                    rationale=score.rationale,
                )
            )

        hooks.sort(key=lambda h: h.virality_score, reverse=True)
        return HookBatch(
            topic=brief.topic,
            platform=brief.platform,
            tone=brief.tone,
            hooks=hooks,
            provider=self._provider.name,
        )