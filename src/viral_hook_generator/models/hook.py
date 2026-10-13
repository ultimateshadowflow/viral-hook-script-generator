"""Hook + batch models. A hook is one opening line candidate."""

from __future__ import annotations

from datetime import datetime, timezone

from pydantic import BaseModel, Field

from viral_hook_generator.models.brief import Platform, Tone


class Hook(BaseModel):
    text: str = Field(min_length=1, max_length=400)
    virality_score: float = Field(ge=0.0, le=100.0)
    pattern: str = Field(description="Template id, e.g. 'cold-open-question'.")
    rationale: str = ""


class HookBatch(BaseModel):
    topic: str
    platform: Platform
    tone: Tone
    hooks: list[Hook]
    generated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    provider: str = "unknown"

    def top(self, n: int = 3) -> list[Hook]:
        return sorted(self.hooks, key=lambda h: h.virality_score, reverse=True)[:n]