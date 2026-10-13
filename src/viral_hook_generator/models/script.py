"""Script model — a hook expanded into timed beats."""

from __future__ import annotations

from pydantic import BaseModel, Field


class ScriptBeat(BaseModel):
    start_s: float = Field(ge=0.0)
    end_s: float = Field(ge=0.0)
    on_screen: str = ""
    voiceover: str = ""
    b_roll: str = ""

    def duration(self) -> float:
        return max(0.0, self.end_s - self.start_s)


class Script(BaseModel):
    hook_text: str
    platform: str
    total_duration_s: float = Field(ge=0.0)
    beats: list[ScriptBeat]
    cta: str = ""

    def is_valid(self) -> bool:
        if not self.beats:
            return False
        ordered = sorted(self.beats, key=lambda b: b.start_s)
        return all(b.end_s > b.start_s for b in ordered)