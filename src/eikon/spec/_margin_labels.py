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

    Attributes
    ----------
    bg_color : str | None
        Background color for the label strip.  ``None`` = transparent.
    text_color : str
        Text color.
    fontsize : float
        Font size in points.
    fontweight : str
        Font weight (``"normal"``, ``"bold"``, etc.).
    rotation : float | None
        Text rotation in degrees.  ``None`` = edge default
        (0 for top/bottom, 90 for left, 270 for right).
    """

    bg_color: str | None = None
    text_color: str = "black"
    fontsize: float = 8.0
    fontweight: str = "normal"
    rotation: float | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class MarginTarget:
    """Which axes grid the margin labels align to.

    For ``kind="layout"`` (the default), labels align to the figure's
    GridSpec cells.  For ``kind="virtual"``, labels subdivide a single
    panel's axes evenly — useful for inset grids drawn inside plot
    functions.

    Attributes
    ----------
    kind : ``"layout"`` or ``"virtual"``
        Targeting mode.
    axes : str | None
        Panel name whose axes to subdivide (required for ``"virtual"``).
    grid : tuple[int, int] | None
        ``(rows, cols)`` of the virtual grid (required for ``"virtual"``).
    """

    kind: Literal["layout", "virtual"] = "layout"
    axes: str | None = None
    grid: tuple[int, int] | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class MarginLabelSpec:
    """Specification for labels on one edge of the figure.

    Attributes
    ----------
    labels : tuple[str, ...] | dict[str, Any]
        Label content.  A flat tuple gives one label per grid cell.
        A nested dict expresses hierarchy — keys are group labels,
        values are sub-dicts (recursive) or ``None`` / tuples of
        leaf labels.
    style : MarginLabelStyle
        Default style applied to all labels on this edge.
    level_styles : tuple[MarginLabelStyle, ...] | None
        Per-level style overrides (outermost level first).  Falls
        back to ``style`` for any level without an override.
    target : MarginTarget
        Which grid the labels align to.
    strip_size : float
        Height (for top/bottom) or width (for left/right) of each
        label band, in figure-fraction units.
    pad : float
        Gap between the axes edge and the first label level, in points.
    gap : float
        Gap between stacked label levels, in points.
    zorder : float
        Drawing order for label text and background patches.
    label_styles : dict[str, MarginLabelStyle] | None
        Per-label style overrides keyed by label text.  When a label's
        text matches a key here, this style is used instead of the
        level/edge default.
    cell_range : tuple[int, int] | None
        ``(start, end)`` restricting which cells of the grid the labels
        cover (0-indexed, end-exclusive).  ``None`` = all cells along
        the relevant axis.
    """

    labels: tuple[str, ...] | dict[str, Any]
    style: MarginLabelStyle = MarginLabelStyle()
    level_styles: tuple[MarginLabelStyle, ...] | None = None
    target: MarginTarget = MarginTarget()
    strip_size: float = 0.04
    pad: float = 6.0
    gap: float = 2.0
    zorder: float = 2.1
    label_styles: dict[str, MarginLabelStyle] | None = None
    cell_range: tuple[int, int] | None = None
