"""Resolve panel positions to grid slices.

Converts the ``row`` / ``col`` fields of :class:`PanelSpec` (which accept
either a single ``int`` or a ``(start, end)`` tuple) into ``slice`` objects
suitable for subscripting a matplotlib ``GridSpec``.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from eikon.layout._grid import LayoutSpec
    from eikon.spec._panel import PanelSpec

__all__ = ["PanelPlacement", "resolve_placements"]


@dataclass(frozen=True, kw_only=True, slots=True)
class PanelPlacement:
    """Resolved position of a panel within the grid.

    Attributes
    ----------
    panel_name : str
        Name of the panel this placement belongs to.
    row_slice : slice
        Row span as a ``slice`` for ``GridSpec`` subscripting.
    col_slice : slice
        Column span as a ``slice`` for ``GridSpec`` subscripting.
    """

    panel_name: str
    row_slice: slice
    col_slice: slice


def resolve_placements(
    panels: tuple[PanelSpec, ...],
    layout: LayoutSpec,
) -> tuple[PanelPlacement, ...]:
    """Convert panel row/col fields to grid slice placements.

    Parameters
    ----------
    panels : tuple[PanelSpec, ...]
        Panel specifications with ``row`` and ``col`` fields.
    layout : LayoutSpec
        The grid layout to place panels within.

    Returns
    -------
    tuple[PanelPlacement, ...]
        One placement per panel, in the same order.
    """
    return tuple(
        PanelPlacement(
            panel_name=panel.name,
            row_slice=_to_slice(panel.row, layout.rows, "row", panel.name),
            col_slice=_to_slice(panel.col, layout.cols, "col", panel.name),
        )
        for panel in panels
    )


def _to_slice(
    value: int | tuple[int, int],
    size: int,
    axis: str,
    panel_name: str,
) -> slice:
    """Convert a single int or (start, end) tuple to a slice.

    Parameters
    ----------
    value : int | tuple[int, int]
        Cell index or ``(start, end)`` span (end exclusive).
    size : int
        Grid dimension for bounds checking.
    axis : str
        ``"row"`` or ``"col"`` — used in error messages.
    panel_name : str
        Panel name — used in error messages.

    Returns
    -------
    slice

    Raises
    ------
    ValueError
        If indices are out of bounds or the span is invalid.
    """
    if isinstance(value, int):
        if value < 0 or value >= size:
            msg = (
                f"Panel {panel_name!r}: {axis} index {value} "
                f"out of bounds for grid size {size}"
            )
            raise ValueError(msg)
        return slice(value, value + 1)

    start, end = value
    if start < 0 or end > size or start >= end:
        msg = (
            f"Panel {panel_name!r}: {axis} span ({start}, {end}) "
            f"invalid for grid size {size}"
        )
        raise ValueError(msg)
    return slice(start, end)
