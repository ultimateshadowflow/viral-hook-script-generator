"""Layered settings loader.

Precedence (lowest → highest):
1. Built-in defaults
2. ``config/default.toml`` shipped with the package
3. ``config.local.toml`` in CWD (gitignored)
4. Environment variables prefixed ``VHG_``
"""

from __future__ import annotations

import os
import tomllib
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field

_DEFAULT_TOML = Path(__file__).with_name("default.toml")
_ENV_PREFIX = "VHG_"


class ProviderSettings(BaseModel):
    name: str = "openai"
    model: str = "gpt-4o-mini"
    api_key_env: str = "OPENAI_API_KEY"
    timeout_s: float = 30.0
    max_retries: int = 3


class Settings(BaseModel):
    provider: ProviderSettings = Field(default_factory=ProviderSettings)
    output_dir: Path = Path("generated_hooks")
    default_hook_count: int = 8
    log_level: str = "INFO"


def _read_toml(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    with path.open("rb") as fh:
        return tomllib.load(fh)


def _apply_env_overrides(data: dict[str, Any]) -> dict[str, Any]:
    """Flatten ``VHG_SECTION__FIELD=value`` into nested dict overrides."""
    for key, value in os.environ.items():
        if not key.startswith(_ENV_PREFIX):
            continue
        path = key[len(_ENV_PREFIX):].lower().split("__")
        cursor = data
        for part in path[:-1]:
            cursor = cursor.setdefault(part, {})
        cursor[path[-1]] = value
    return data


def load_settings(local_path: Path | None = None) -> Settings:
    merged: dict[str, Any] = {}
    merged.update(_read_toml(_DEFAULT_TOML))
    merged.update(_read_toml(local_path or Path("config.local.toml")))
    _apply_env_overrides(merged)
    return Settings.model_validate(merged)