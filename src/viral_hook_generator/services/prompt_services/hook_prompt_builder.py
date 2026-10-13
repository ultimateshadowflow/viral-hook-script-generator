"""Renders the generation prompt from a ContentBrief.

Templates are keyed by platform so TikTok prompts can lean on cold-open
energy while Shorts prompts lean on search-intent phrasing.
"""

from __future__ import annotations

from viral_hook_generator.models.brief import ContentBrief, Platform

_PLATFORM_RULES: dict[Platform, str] = {
    Platform.TIKTOK: "Open on motion or a claim. First 1.5s must stop the scroll.",
    Platform.REELS: "Lead with a visual promise. Keep it under 12 words.",
    Platform.SHORTS: "Front-load the search keyword. Answer a question fast.",
    Platform.X: "One line. No emoji spam. Punch the curiosity gap.",
}

_TONE_RULES = {
    "punchy": "Short sentences. Verbs first.",
    "story": "Open mid-scene. Withhold the payoff.",
    "educational": "Promise a specific, checkable fact.",
    "chaotic": "Break rhythm. Surprise the ear.",
    "calm": "Low stakes, high clarity.",
}


class HookPromptBuilder:
    def build(self, brief: ContentBrief) -> str:
        platform_rule = _PLATFORM_RULES[brief.platform]
        tone_rule = _TONE_RULES[brief.tone.value]
        audience = brief.audience or "a general short-form audience"
        return (
            f"You are a short-form hook writer for {brief.platform.value}.\n"
            f"Topic: {brief.topic}\n"
            f"Audience: {audience}\n"
            f"Tone: {brief.tone.value} — {tone_rule}\n"
            f"Platform rule: {platform_rule}\n\n"
            f"Write exactly {brief.hook_count} hook candidates.\n"
            "Format each line as: <pattern-id> :: <hook text>\n"
            "No numbering. No preamble. No explanations."
        )