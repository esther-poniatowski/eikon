"""Lifecycle hook system for rendering and export events.

Hooks allow users to inject custom logic at well-defined points in the
render/export pipeline without modifying eikon source.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

from eikon.ext._registry import get_default_registry

__all__ = ["HookName", "register_hook", "fire_hook", "clear_hooks"]

type HookFunction = Any
"""A hook callback — any callable accepting keyword arguments."""


class HookName(Enum):
    """Well-defined hook points in the figure lifecycle."""

    PRE_RENDER = "pre_render"
    POST_RENDER = "post_render"
    PRE_EXPORT = "pre_export"
    POST_EXPORT = "post_export"


def register_hook(hook: HookName, fn: HookFunction) -> None:
    """Register a callback for a lifecycle hook.

    Parameters
    ----------
    hook : HookName
        The hook point to attach to.
    fn : HookFunction
        A callable invoked when the hook fires.
    """
    get_default_registry().register_hook(hook, fn)


def fire_hook(hook: HookName, **kwargs: Any) -> None:
    """Fire all callbacks registered for a hook.

    Parameters
    ----------
    hook : HookName
        The hook point to fire.
    **kwargs : Any
        Context passed to each callback.
    """
    get_default_registry().fire_hook(hook, **kwargs)


def clear_hooks() -> None:
    """Remove all registered hooks.  For testing only."""
    registry = get_default_registry()
    for hook in HookName:
        registry.hooks.setdefault(hook, [])
    registry.clear_hooks()
