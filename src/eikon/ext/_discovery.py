"""Entry-point based plugin discovery.

Discovers and loads third-party plot types and hooks registered via
the ``eikon.plot_types`` entry-point group in ``pyproject.toml``.
"""

from __future__ import annotations

import importlib.metadata
import logging

__all__ = ["discover_plugins"]

logger = logging.getLogger(__name__)

PLOT_TYPES_GROUP = "eikon.plot_types"
"""Entry-point group name for plot type plugins."""


def discover_plugins(group: str = PLOT_TYPES_GROUP) -> int:
    """Load all entry points in the given group.

    Each entry point should be a module that, when imported, registers
    its plot types via ``@plot_type("name")`` or
    ``register_plot_type(name, fn)``.

    Parameters
    ----------
    group : str
        Entry-point group name to discover.

    Returns
    -------
    int
        Number of entry points successfully loaded.
    """
    loaded = 0
    for ep in importlib.metadata.entry_points(group=group):
        try:
            ep.load()
            loaded += 1
        except Exception:
            logger.warning("Failed to load plugin %r from %s", ep.name, ep.value, exc_info=True)
    return loaded
