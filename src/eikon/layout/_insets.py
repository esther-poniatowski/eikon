"""Inset axes creation and registration.

Provides a helper to create an inset axes within an existing panel and
register it in the ``BuiltLayout.axes`` dict for downstream use.
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from eikon.layout._builder import BuiltLayout

from eikon.exceptions import LayoutError

__all__ = ["add_inset"]


def add_inset(
    built: BuiltLayout,
    parent_panel: str,
    name: str,
    bounds: tuple[float, float, float, float],
) -> BuiltLayout:
    """Create an inset axes and register it in the layout.

    Parameters
    ----------
    built : BuiltLayout
        A built layout containing the figure and axes dict.
    parent_panel : str
        Name of the panel to create the inset within.
    name : str
        Name for the new inset axes.
    bounds : tuple[float, float, float, float]
        ``(x, y, width, height)`` in axes-relative coordinates (0–1).

    Returns
    -------
    BuiltLayout
        A new ``BuiltLayout`` with the inset axes added to the ``axes`` dict.

    Raises
    ------
    LayoutError
        If *parent_panel* is not found or *name* already exists.
    """
    if parent_panel not in built.axes:
        raise LayoutError(f"Panel {parent_panel!r} not found in built layout.")
    if name in built.axes:
        raise LayoutError(f"Axes name {name!r} already exists in the layout.")

    parent_ax = built.axes[parent_panel]
    inset_ax: Any = parent_ax.inset_axes(bounds)

    new_axes = {**built.axes, name: inset_ax}
    return replace(built, axes=new_axes)
