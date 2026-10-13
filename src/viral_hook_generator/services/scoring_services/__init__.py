"""Scoring services — rank candidates before they reach the user."""

from viral_hook_generator.services.scoring_services.virality_scorer import (
    ViralityScorer,
    ViralityScore,
)

__all__ = ["ViralityScorer", "ViralityScore"]