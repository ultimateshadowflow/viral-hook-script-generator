"""Input sanitizers. Topic strings are untrusted."""

from __future__ import annotations

import re

_CONTROL_CHARS = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]")
_INJECTION_HINTS = re.compile(
    r"(ignore (all|previous) instructions|system prompt|you are now|disregard)",
    re.IGNORECASE,
)
_WHITESPACE = re.compile(r"\s+")


def sanitize_topic(raw: str) -> str:
    """Strip control chars, collapse whitespace, defang obvious injections.

    Injection hints are removed rather than rejected so the operator still
    gets a usable topic instead of a hard failure.
    """
    cleaned = _CONT