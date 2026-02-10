"""Extension and plugin system for eikon.

Provides plot type registration, lifecycle hooks, and entry-point
based plugin discovery.
"""

from eikon.ext._discovery import discover_plugins
from eikon.ext._hooks import HookName, clear_hooks, fire_hook, register_hook
from eikon.ext._plot_types import (
    get_plot_type,
    list_plot_types,
    plot_type,
    register_plot_type,
)
from eikon.ext._transforms import (
    apply_transforms,
    clear_transforms,
    list_transforms,
    register_transform,
)

__all__ = [
    "HookName",
    "clear_hooks",
    "discover_plugins",
    "fire_hook",
    "get_plot_type",
    "list_plot_types",
    "plot_type",
    "register_hook",
    "register_plot_type",
    "apply_transforms",
    "clear_transforms",
    "list_transforms",
    "register_transform",
]
