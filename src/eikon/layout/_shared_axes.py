"""Shared-axis linking across panels.

Provides a helper to create shared-x or shared-y axis groups across
named panels after layout build.  This is a thin wrapper around
matplotlib's ``Axes.sharex`` / ``Axes.sharey``.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Literal

if TYPE_CHECKING:
    from eikon.layout._builder import BuiltLayout

from eikon.exceptions import LayoutError

__all__ = ["link_axes"]


def link_axes(
    built: BuiltLayout,
    groups: tuple[tuple[str, ...], ...],
    axis: Literal["x", "y", "both"] = "both",
) -> None:
    """Link axes across panels so they share scales.

    Within each group, the first panel becomes the reference and all
    subsequent panels share its x-axis, y-axis, or both.

    Parameters
    ----------
    built : BuiltLayout
        A built layout containing the axes dict.
    groups : tuple[tuple[str, ...], ...]
        Groups of panel names to link.  Each inner tuple is one group.
    axis : ``"x"`` | ``"y"`` | ``"both"``
        Which axis to share.

    Raises
    ------
    LayoutError
        If a panel name is not found in the built layout.
    """
    for group in groups:
        if len(group) < 2:
            continue
        ref_name = group[0]
        if ref_name not in built.axes:
            raise LayoutError(f"Panel {ref_name!r} not found in built layout.")
        ref_ax = built.axes[ref_name]
        for name in group[1:]:
            if name not in built.axes:
                raise LayoutError(f"Panel {name!r} not found in built layout.")
            ax = built.axes[name]
            if axis in ("x", "both"):
                ax.sharex(ref_ax)
            if axis in ("y", "both"):
                ax.sharey(ref_ax)
