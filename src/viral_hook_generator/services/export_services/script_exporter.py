"""Writes a HookBatch to disk as markdown + json.

Guards against path traversal: every resolved output path must be
inside the configured output root. Slug collisions get a numeric suffix.
"""

from __future__ import annotations

import json
import logging
from pathlib import Path

from viral_hook_generator.models.hook import HookBatch
from viral_hook_generator.utils.slugs import slugify

log = logging.getLogger(__name__)


class ScriptExporter:
    def __init__(self, output_dir: Path) -> None:
        self._root = output_dir.resolve()
        self._root.mkdir(parents=True, exist_ok=True)

    def _safe_path(self, *parts: str) -> Path:
        candidate = (self._root.joinpath(*parts)).resolve()
        if not candidate.is_relative_to(self._root):
            raise ValueError(f"refusing to write outside output root: {candidate}")
        return candidate

    def _unique(self, base: Path) -> Path:
        if not base.exists():
            return base
        stem, suffix = base.stem, base.suffix
        for i in range(1, 1000):
            candidate = base.with_name(f"{stem}-{i}{suffix}")
            if not candidate.exists():
                return candidate
        raise RuntimeError("too many slug collisions")

    def export_batch(self, batch: HookBatch) -> list[Path]:
        slug = slugify(batch.topic)
        written: list[Path] = []

        json_path = self._unique(self._safe_path(f"{slug}.json"))
        json_path.write_text(batch.model_dump_json(indent=2), encoding="utf-8")
        written.append(json_path)

        md_path = self._unique(self._safe_path(f"{slug}.md"))
        md_path.write_text(self._render_markdown(batch), encoding="utf-8")
        written.append(md_path)

        log.info("exported %d file(s) for topic=%r", len(written), batch.topic)
        return written

    @staticmethod
    def _render_markdown(batch: HookBatch) -> str:
        lines = [
            f"# Hooks — {batch.topic}",
            "",
            f"- Platform: `{batch.platform.value}`",
            f"- Tone: `{batch.tone.value}`",
            f"- Provider: `{batch.provider}`",
            f"- Generated: {batch.generated_at.isoformat()}",
            "",
            "| # | Hook | Score | Pattern |",
            "| - | ---- | ----- | ------- |",
        ]
        for i, hook in enumerate(batch.hooks, start=1):
            safe = hook.text.replace("|", "\\|")
            lines.append(f"| {i} | {safe} | {hook.virality_score:.0f} | `{hook.pattern}` |")
        return "\n".join(lines) + "\n"