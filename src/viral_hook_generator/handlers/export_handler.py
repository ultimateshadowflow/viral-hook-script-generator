"""Handler: batch in → list of written paths out."""

from __future__ import annotations

from pathlib import Path

from viral_hook_generator.models.hook import HookBatch
from viral_hook_generator.services.export_services.script_exporter import ScriptExporter


class ExportHandler:
    def __init__(self, output_dir: Path) -> None:
        self._exporter = ScriptExporter(output_dir)

    def handle(self, batch: HookBatch) -> list[Path]:
        return self._exporter.export_batch(batch)