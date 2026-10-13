"""CLI entrypoint. `viral-hooks generate --topic ... --platform tiktok`."""

from __future__ import annotations

import asyncio
from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from viral_hook_generator.core.engine import HookEngine
from viral_hook_generator.models.brief import ContentBrief, Platform, Tone
from viral_hook_generator.services.export_services.script_exporter import ScriptExporter

app = typer.Typer(help="Generate viral hooks and short-form scripts.", no_args_is_help=True)
console = Console()


@app.command()
def generate(
    topic: str = typer.Option(..., "--topic", "-t", help="Subject of the content."),
    platform: Platform = typer.Option(Platform.TIKTOK, "--platform", "-p"),
    tone: Tone = typer.Option(Tone.PUNCHY, "--tone"),
    count: int = typer.Option(8, "--count", "-n", min=1, max=40),
    out: Path = typer.Option(Path("generated_hooks"), "--out", "-o"),
    export: bool = typer.Option(False, "--export", help="Write scripts to disk."),
) -> None:
    """Generate a batch of hooks and optionally export the scripts."""
    brief = ContentBrief(topic=topic, platform=platform, tone=tone, hook_count=count)
    engine = HookEngine.from_config()
    batch = asyncio.run(engine.generate(brief))

    table = Table(title=f"Hooks for: {topic}  [{platform.value}]")
    table.add_column("#", justify="right", style="dim")
    table.add_column("Hook", style="bold")
    table.add_column("Score", justify="right")
    for i, hook in enumerate(batch.hooks, start=1):
        table.add_row(str(i), hook.text, f"{hook.virality_score:.0f}")
    console.print(table)

    if export:
        exporter = ScriptExporter(out)
        written = exporter.export_batch(batch)
        console.print(f"[green]wrote {len(written)} script(s) to {out}[/green]")


if __name__ == "__main__":
    app()