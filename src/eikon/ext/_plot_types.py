"""Plot type registry — string-keyed dictionary of plot functions.

Provides a global registry of plot functions, a ``@plot_type`` decorator
for registration, and a lookup function used by the drawing module.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import TypeVar

from eikon.exceptions import UnknownPlotTypeError

_F = TypeVar("_F", bound=Callable[..., None])

__all__ = ["register_plot_type", "get_plot_type", "plot_type", "list_plot_types"]

_REGISTRY: dict[str, Callable[..., None]] = {}


def register_plot_type(name: str, fn: Callable[..., None]) -> None:
    """Register a plot function under a string key.

    Parameters
    ----------
    name : str
        The plot type name (e.g. ``"line"``, ``"scatter"``).
    fn : PlotFunction
        A callable matching the :class:`PlotFunction` protocol.
    """
    _REGISTRY[name] = fn


def get_plot_type(name: str) -> Callable[..., None]:
    """Look up a registered plot function by name.

    Parameters
    ----------
    name : str
        The plot type name.

    Returns
    -------
    PlotFunction
        The registered plot function.

    Raises
    ------
    UnknownPlotTypeError
        If no plot type is registered under *name*.
    """
    fn = _REGISTRY.get(name)
    if fn is None:
        raise UnknownPlotTypeError(name, list(_REGISTRY.keys()))
    return fn


def list_plot_types() -> list[str]:
    """Return a sorted list of all registered plot type names."""
    return sorted(_REGISTRY.keys())


def plot_type(name: str) -> Callable[[_F], _F]:
    """Decorator to register a function as a named plot type.

    Usage::

        @plot_type("line")
        def draw_line(ax, /, **kwargs):
            ax.plot(kwargs.get("x", []), kwargs.get("y", []))

    Parameters
    ----------
    name : str
        The plot type name to register under.

    Returns
    -------
    Callable
        The original function, unmodified.
    """

    def decorator(fn: _F) -> _F:
        register_plot_type(name, fn)
        return fn

    return decorator


def _clear_registry() -> None:
    """Clear all registered plot types.  For testing only."""
    _REGISTRY.clear()
