"""Config package — loads layered TOML + env overrides."""

from viral_hook_generator.config.settings import Settings, load_settings

__all__ = ["Settings", "load_settings"]