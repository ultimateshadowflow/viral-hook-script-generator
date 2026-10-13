"""Heuristic virality scorer.

Not a model — a fast, explainable rubric. Scores 0–100 from four
signals: length fit, curiosity markers, concreteness, and tone match.
Every point is attributable; the rationale string exposes the breakdown.
"""

from __future__ import annotations

from dataclasses import dataclass

from viral_hook_generator.models.brief import Platform, Tone

_CURIOSITY_MARKERS = (
    "why", "how", "nobody", "secret", "stop", "before", "until",
    "actually", "truth", "wrong", "never", "always",
)
_CONCRETE_MARKERS = (
    "1", "2", "3", "5", "7", "10", "$", "%", "day", "week", "minute",
)

_PLATFORM_MAX_WORDS: dict[Platform, int] = {
    Platform.TIKTOK: 14,
    Platform.REELS: 12,
    Platform.SHORTS: 16,
    Platform.X: 20,
}


@dataclass(frozen=True)
class ViralityScore:
    total: float
    rationale: str


class ViralityScorer:
    def score(self, text: str, platform: Platform, tone: Tone) -> ViralityScore:
        words = text.split()
        n = len(words)
        cap = _PLATFORM_MAX_WORDS[platform]

        # Length: full points at or under cap, tapering to 0 at 2x cap.
        if n <= cap:
            length_pts = 30.0
        else:
            over = n - cap
            length_pts = max(0.0, 30.0 - (over / cap) * 30.0)

        lower = text.lower()
        curiosity_hits = sum(1 for m in _CURIOSITY_MARKERS if m in lower)
        curiosity_pts = min(25.0, curiosity_hits * 8.0)

        concrete_hits = sum(1 for m in _CONCRETE_MARKERS if m in lower)
        concrete_pts = min(20.0, concrete_hits * 7.0)

        tone_pts = self._tone_fit(text, tone)

        total = round(min(100.0, length_pts + curiosity_pts + concrete_pts + tone_pts), 1)
        rationale = (
            f"len={length_pts:.0f}/30 curiosity={curiosity_pts:.0f}/25 "
            f"concrete={concrete_pts:.0f}/20 tone={tone_pts:.0f}/25"
        )
        return ViralityScore(total=total, rationale=rationale)

    @staticmethod
    def _tone_fit(text: str, tone: Tone) -> float:
        words = text.split()
        avg_len = sum(len(w) for w in words) / max(1, len(words))
        if tone is Tone.PUNCHY:
            return 25.0 if avg_len <= 5.0 else 12.0
        if tone is Tone.CALM:
            return 25.0 if avg_len >= 5.0 else 12.0
        if tone is Tone.CHAOTIC:
            return 25.0 if "!" in text or "?" in text else 10.0
        if tone is Tone.STORY:
            return 25.0 if any(w in text.lower() for w in ("i ", "we ", "when ")) else 10.0
        return 18.0  # educational — neutral