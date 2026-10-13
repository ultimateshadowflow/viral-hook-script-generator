"""Handler: brief in → batch out. Delegates all work to HookEngine."""

from __future__ import annotations

from viral_hook_generator.core.engine import HookEngine
from viral_hook_generator.models.brief import ContentBrief
from viral_hook_generator.models.hook import HookBatch


class GenerateHandler:
    """Thin adapter around :class:`HookEngine` for CLI / GUI callers."""

    def __init__(self, engine: HookEngine) -> None:
        self._engine = engine

    async def handle(self, brief: ContentBrief) -> HookBatch:
        return await self._engine.generate(brief)