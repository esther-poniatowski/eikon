"""Margin label specification dataclasses.

Declarative types for figure-edge labels that annotate rows or columns
of a panel grid (or a virtual inset grid within a single panel).
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

__all__ = ["MarginLabelSpec", "MarginLabelStyle", "MarginTarget"]


@dataclass(frozen=True, kw_only=True, slots=True)
class MarginLabelStyle:
    """Visual style for margin label text and optional background strip.
    """

    bg_color: str | None = None
    """Background color for the label strip.  ``None`` = transparent."""
    text_color: str = "black"
    """Text color."""
    fontsize: float = 8.0
    """Font size in points."""
    fontweight: str = "normal"
    """Font weight (``"normal"``, ``"bold"``, etc.)."""
    rotation: float | None = None
    """Text rotation in degrees.  ``None`` = edge default
    (0 for top/bottom, 90 for left, 270 for right).
    """


@dataclass(frozen=True, kw_only=True, slots=True)
class MarginTarget:
    """Which axes grid the margin labels align to.

    For ``kind="layout"`` (the default), labels align to the figure's
    GridSpec cells.  For ``kind="virtual"``, labels subdivide a single
    panel's axes evenly — useful for inset grids drawn inside plot
    functions.
    """

    kind: Literal["layout", "virtual"] = "layout"
    """Targeting mode."""
    axes: str | None = None
    """Panel name whose axes to subdivide (required for ``"virtual"``)."""
    grid: tuple[int, int] | None = None
    """``(rows, cols)`` of the virtual grid (required for ``"virtual"``)."""


@dataclass(frozen=True, kw_only=True, slots=True)
class MarginLabelSpec:
    """Specification for labels on one edge of the figure.
    """

    labels: tuple[str, ...] | dict[str, Any]
    """Label content.  A flat tuple gives one label per grid cell.
    A nested dict expresses hierarchy — keys are group labels,
    values are sub-dicts (recursive) or ``None`` / tuples of
    leaf labels.
    """
    style: MarginLabelStyle = MarginLabelStyle()
    """Default style applied to all labels on this edge."""
    level_styles: tuple[MarginLabelStyle, ...] | None = None
    """Per-level style overrides (outermost level first).  Falls
    back to ``style`` for any level without an override.
    """
    target: MarginTarget = MarginTarget()
    """Which grid the labels align to."""
    strip_size: float = 0.04
    """Height (for top/bottom) or width (for left/right) of each
    label band, in figure-fraction units.
    """
    pad: float = 6.0
    """Gap between the axes edge and the first label level, in points."""
    gap: float = 2.0
    """Gap between stacked label levels, in points."""
    zorder: float = 2.1
    """Drawing order for label text and background patches."""
    label_styles: dict[str, MarginLabelStyle] | None = None
    """Per-label style overrides keyed by label text.  When a label's
    text matches a key here, this style is used instead of the
    level/edge default.
    """
    cell_range: tuple[int, int] | None = None
    """``(start, end)`` restricting which cells of the grid the labels
    cover (0-indexed, end-exclusive).  ``None`` = all cells along
    the relevant axis.
    """
