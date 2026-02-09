"""Lifecycle hook system for rendering and export events.

Hooks allow users to inject custom logic at well-defined points in the
render/export pipeline without modifying eikon source.
"""

from __future__ import annotations

from enum import Enum
from typing import Any

__all__ = ["HookName", "register_hook", "fire_hook", "clear_hooks"]

type HookFunction = Any
"""A hook callback — any callable accepting keyword arguments."""


class HookName(Enum):
    """Well-defined hook points in the figure lifecycle."""

    PRE_RENDER = "pre_render"
    POST_RENDER = "post_render"
    PRE_EXPORT = "pre_export"
    POST_EXPORT = "post_export"


_HOOKS: dict[HookName, list[HookFunction]] = {h: [] for h in HookName}


def register_hook(hook: HookName, fn: HookFunction) -> None:
    """Register a callback for a lifecycle hook.

    Parameters
    ----------
    hook : HookName
        The hook point to attach to.
    fn : HookFunction
        A callable invoked when the hook fires.
    """
    _HOOKS[hook].append(fn)


def fire_hook(hook: HookName, **kwargs: Any) -> None:
    """Fire all callbacks registered for a hook.

    Parameters
    ----------
    hook : HookName
        The hook point to fire.
    **kwargs : Any
        Context passed to each callback.
    """
    for fn in _HOOKS[hook]:
        fn(**kwargs)


def clear_hooks() -> None:
    """Remove all registered hooks.  For testing only."""
    for hook in HookName:
        _HOOKS[hook] = []
