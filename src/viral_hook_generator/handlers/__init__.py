"""Thin handlers — parse input, call a service, format output. No logic."""

from viral_hook_generator.handlers.generate_handler import GenerateHandler
from viral_hook_generator.handlers.export_handler import ExportHandler

__all__ = ["GenerateHandler", "ExportHandler"]