"""viral-hook-script-generator — generate viral hooks and short-form scripts.

Public surface is intentionally small: construct a :class:`HookEngine`,
call :meth:`HookEngine.generate`, get back a :class:`HookBatch`.
"""

from viral_hook_generator.core.engine import HookEngine
from viral_hook_generator.models.hook import Hook, HookBatch
from viral_hook_generator.models.brief import ContentBrief

__all__ = ["HookEngine", "Hook", "HookBatch", "ContentBrief"]
__version__ = "0.4.2"