"""The input contract — what the operator asks for."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field, field_validator

from viral_hook_generator.utils.sanitizers import sanitize_topic


class Platform(str, Enum):
    TIKTOK = "tiktok"
    REELS = "reels"
    SHORTS = "shorts"
    X = "x"


class Tone(str, Enum):
    PUNCHY = "punchy"
    STORY = "story"
    EDUCATIONAL = "educational"
    CHAOTIC = "chaotic"
    CALM = "calm"


class ContentBrief(BaseModel):
    """Everything the engine needs to produce a batch.

    ``topic`` is untrusted — sanitized on validation. ``hook_count`` is
    clamped to [1, 40] to keep provider bills bounded.
    """

    topic: str = Field(min_length=2, max_length=280)
    platform: Platform = Platform.TIKTOK
    tone: Tone = Tone.PUNCHY
    hook_count: int = Field(default=8, ge=1, le=40)
    audience: str | None = Field(default=None, max_length=120)

    @field_validator("topic")
    @classmethod
    def _clean_topic(cls, value: str) -> str:
        cleaned = sanitize_topic(value)
        if len(cleaned) < 2:
            raise ValueError("topic is empty after sanitization")
        return cleaned