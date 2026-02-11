"""Margin label rendering — hierarchy resolution, geometry, and drawing.

Converts declarative :class:`MarginLabelSpec` definitions into positioned
text and optional background patches on a matplotlib Figure.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import numpy as np
from matplotlib.patches import Rectangle

if TYPE_CHECKING:
    from matplotlib.figure import Figure

    from eikon.layout._builder import BuiltLayout
    from eikon.spec._margin_labels import MarginLabelSpec, MarginLabelStyle, MarginTarget

__all__ = ["draw_margin_labels"]

_VALID_EDGES = frozenset({"top", "bottom", "left", "right"})

# Default text rotation per edge (degrees).
_EDGE_ROTATION: dict[str, float] = {
    "top": 0.0,
    "bottom": 0.0,
    "left": 90.0,
    "right": 270.0,
}

# Default text alignment per edge.
_EDGE_ALIGNMENT: dict[str, dict[str, Any]] = {
    "top": {"ha": "center", "va": "center"},
    "bottom": {"ha": "center", "va": "center"},
    "left": {"ha": "center", "va": "center"},
    "right": {"ha": "center", "va": "center"},
}


# ---------------------------------------------------------------------------
# Internal data structure
# ---------------------------------------------------------------------------

@dataclass(frozen=True, slots=True)
class LabelSpan:
    """A resolved label with its position in the grid."""

    text: str
    level: int   # 0 = outermost
    start: int   # starting cell index
    span: int    # number of cells spanned


# ---------------------------------------------------------------------------
# Hierarchy resolution
# ---------------------------------------------------------------------------

def resolve_label_hierarchy(
    labels: tuple[str, ...] | dict[str, Any],
) -> tuple[list[LabelSpan], int]:
    """Convert user-facing label declaration into flat spans.

    Parameters
    ----------
    labels : tuple[str, ...] | dict[str, Any]
        Flat tuple (one label per cell) or nested dict for hierarchy.

    Returns
    -------
    spans : list[LabelSpan]
        All resolved spans across all levels.
    n_levels : int
        Total number of hierarchy levels.
    """
    if isinstance(labels, tuple):
        return (
            [LabelSpan(text=t, level=0, start=i, span=1) for i, t in enumerate(labels)],
            1,
        )

    spans: list[LabelSpan] = []
    n_levels = _resolve_dict(labels, level=0, offset=0, spans=spans)
    return spans, n_levels


def _resolve_dict(
    d: dict[str, Any],
    level: int,
    offset: int,
    spans: list[LabelSpan],
) -> int:
    """Recursively resolve a nested dict into LabelSpan entries.

    Returns the maximum depth (number of levels).
    """
    max_depth = level + 1
    cursor = offset

    for key, value in d.items():
        if value is None:
            # Leaf — single cell
            child_count = 1
            max_depth = max(max_depth, level + 1)
        elif isinstance(value, tuple):
            # Flat sub-labels
            child_count = len(value)
            for i, text in enumerate(value):
                spans.append(LabelSpan(text=text, level=level + 1, start=cursor + i, span=1))
            max_depth = max(max_depth, level + 2)
        elif isinstance(value, dict):
            # Recursive sub-groups
            child_count = _count_leaves(value)
            sub_depth = _resolve_dict(value, level=level + 1, offset=cursor, spans=spans)
            max_depth = max(max_depth, sub_depth)
        else:
            msg = f"Unsupported label value type: {type(value).__name__}"
            raise TypeError(msg)

        spans.append(LabelSpan(text=key, level=level, start=cursor, span=child_count))
        cursor += child_count

    return max_depth


def _count_leaves(d: dict[str, Any]) -> int:
    """Count total leaf labels in a nested dict."""
    total = 0
    for value in d.values():
        if value is None:
            total += 1
        elif isinstance(value, tuple):
            total += len(value)
        elif isinstance(value, dict):
            total += _count_leaves(value)
        else:
            msg = f"Unsupported label value type: {type(value).__name__}"
            raise TypeError(msg)
    return total


# ---------------------------------------------------------------------------
# Geometry resolution
# ---------------------------------------------------------------------------

def compute_cell_edges(
    fig: Figure,
    built: BuiltLayout,
    target: MarginTarget,
    edge: str,
) -> tuple[
    np.ndarray[Any, np.dtype[np.float64]],
    np.ndarray[Any, np.dtype[np.float64]],
    float,
    float,
]:
    """Compute per-cell start and end positions along the label axis.

    Parameters
    ----------
    fig : Figure
        The matplotlib figure.
    built : BuiltLayout
        The built layout (with ``grid_spec``).
    target : MarginTarget
        Targeting mode.
    edge : str
        One of ``"top"``, ``"bottom"``, ``"left"``, ``"right"``.

    Returns
    -------
    cell_starts : ndarray
        1-D array of cell start positions in figure coords (one per cell).
    cell_ends : ndarray
        1-D array of cell end positions in figure coords (one per cell).
    anchor_min : float
        Minimum extent perpendicular to the label axis.
    anchor_max : float
        Maximum extent perpendicular to the label axis.
    """
    if target.kind == "virtual":
        return _cell_edges_virtual(built, target, edge)
    return _cell_edges_layout(fig, built, edge)


def _cell_edges_layout(
    fig: Figure,
    built: BuiltLayout,
    edge: str,
) -> tuple[
    np.ndarray[Any, np.dtype[np.float64]],
    np.ndarray[Any, np.dtype[np.float64]],
    float,
    float,
]:
    """Cell edges from the figure's GridSpec.

    Returns per-cell start/end arrays that are correct regardless of
    ``wspace``/``hspace`` values.
    """
    gs = built.grid_spec
    # get_grid_positions returns (bottom, top, left, right) arrays
    bot, top, left, right = gs.get_grid_positions(fig)

    if edge in ("top", "bottom"):
        # Columns: left[j] and right[j] give the extent of column j.
        cell_starts = np.asarray(left, dtype=np.float64)
        cell_ends = np.asarray(right, dtype=np.float64)
        anchor_min = float(np.min(bot))
        anchor_max = float(np.max(top))
    else:
        # Rows: bot[i] and top[i] give the extent of row i.
        # Row 0 is the topmost (highest y); ordering is preserved.
        cell_starts = np.asarray(bot, dtype=np.float64)
        cell_ends = np.asarray(top, dtype=np.float64)
        anchor_min = float(np.min(left))
        anchor_max = float(np.max(right))

    return cell_starts, cell_ends, anchor_min, anchor_max


def _cell_edges_virtual(
    built: BuiltLayout,
    target: MarginTarget,
    edge: str,
) -> tuple[
    np.ndarray[Any, np.dtype[np.float64]],
    np.ndarray[Any, np.dtype[np.float64]],
    float,
    float,
]:
    """Cell edges from even subdivision of a single panel's axes."""
    if target.axes is None:
        msg = "MarginTarget with kind='virtual' requires 'axes' to be set."
        raise ValueError(msg)
    if target.grid is None:
        msg = "MarginTarget with kind='virtual' requires 'grid' to be set."
        raise ValueError(msg)
    if target.axes not in built.axes:
        msg = f"Panel {target.axes!r} not found in built layout."
        raise ValueError(msg)

    ax = built.axes[target.axes]
    bbox = ax.get_position()
    rows, cols = target.grid

    if edge in ("top", "bottom"):
        all_edges = np.linspace(bbox.x0, bbox.x1, cols + 1)
        cell_starts = all_edges[:-1]
        cell_ends = all_edges[1:]
        anchor_min = float(bbox.y0)
        anchor_max = float(bbox.y1)
    else:
        all_edges = np.linspace(bbox.y0, bbox.y1, rows + 1)
        # Reverse: row 0 = top of figure = highest y values.
        cell_starts = all_edges[:-1][::-1].copy()
        cell_ends = all_edges[1:][::-1].copy()
        anchor_min = float(bbox.x0)
        anchor_max = float(bbox.x1)

    return cell_starts, cell_ends, anchor_min, anchor_max


# ---------------------------------------------------------------------------
# Drawing
# ---------------------------------------------------------------------------

def draw_margin_labels(
    fig: Figure,
    built: BuiltLayout,
    margin_labels: dict[str, MarginLabelSpec],
) -> None:
    """Render margin labels on the figure.

    Parameters
    ----------
    fig : Figure
        The matplotlib figure to draw on.
    built : BuiltLayout
        The built layout (provides ``grid_spec`` and ``axes``).
    margin_labels : dict[str, MarginLabelSpec]
        Mapping from edge name to label spec.
    """
    for edge, spec in margin_labels.items():
        if edge not in _VALID_EDGES:
            msg = f"Invalid margin label edge: {edge!r}"
            raise ValueError(msg)
        _draw_edge(fig, built, edge, spec)


def _draw_edge(
    fig: Figure,
    built: BuiltLayout,
    edge: str,
    spec: MarginLabelSpec,
) -> None:
    """Draw all label levels for a single edge."""
    spans, n_levels = resolve_label_hierarchy(spec.labels)
    cell_starts, cell_ends, anchor_min_perp, anchor_max_perp = compute_cell_edges(
        fig, built, spec.target, edge,
    )

    # Apply cell_range restriction.
    if spec.cell_range is not None:
        r0, r1 = spec.cell_range
        cell_starts = cell_starts[r0:r1]
        cell_ends = cell_ends[r0:r1]

    # Validate: label hierarchy must span exactly as many cells as
    # the geometry provides.
    n_cells = len(cell_starts)
    total_cells = sum(s.span for s in spans if s.level == 0)
    if total_cells != n_cells:
        msg = (
            f"Margin labels on {edge!r}: label hierarchy spans "
            f"{total_cells} cells but the grid has {n_cells}"
        )
        raise ValueError(msg)

    # Figure dimension along the perpendicular axis (for pt→fig conversion).
    fig_w, fig_h = fig.get_size_inches()

    if edge in ("top", "bottom"):
        fig_dim = fig_h
    else:
        fig_dim = fig_w

    # Convert point-based values to figure-fraction.
    pad_fig = spec.pad / (72.0 * fig_dim)
    gap_fig = spec.gap / (72.0 * fig_dim)
    strip = spec.strip_size

    # Determine starting anchor and direction.
    if edge == "top":
        anchor = anchor_max_perp + pad_fig
        sign = 1.0
    elif edge == "bottom":
        anchor = anchor_min_perp - pad_fig
        sign = -1.0
    elif edge == "right":
        anchor = anchor_max_perp + pad_fig
        sign = 1.0
    else:  # left
        anchor = anchor_min_perp - pad_fig
        sign = -1.0

    # Draw levels from innermost (highest level number) to outermost (0),
    # stacking outward from the axes edge.
    for lvl in range(n_levels - 1, -1, -1):
        align = _EDGE_ALIGNMENT[edge]

        band_lo = anchor
        band_hi = anchor + sign * strip
        band_center = (band_lo + band_hi) / 2.0

        level_spans = [s for s in spans if s.level == lvl]
        for ls in level_spans:
            style = _style_for_label(spec, lvl, ls.text)
            rotation = style.rotation if style.rotation is not None else _EDGE_ROTATION[edge]

            # Cell extent along the label axis.  Use min/max so the
            # geometry is correct for both ascending (columns) and
            # descending (rows) cell orderings.
            s_idx = ls.start
            e_idx = ls.start + ls.span
            c0 = float(np.min(cell_starts[s_idx:e_idx]))
            c1 = float(np.max(cell_ends[s_idx:e_idx]))
            mid = (c0 + c1) / 2.0

            # Position depends on edge orientation.
            if edge in ("top", "bottom"):
                text_x, text_y = mid, band_center
                rect_x, rect_y = c0, min(band_lo, band_hi)
                rect_w, rect_h = c1 - c0, abs(band_hi - band_lo)
            else:
                text_x, text_y = band_center, mid
                rect_x, rect_y = min(band_lo, band_hi), c0
                rect_w, rect_h = abs(band_hi - band_lo), c1 - c0

            # Optional background rectangle.
            if style.bg_color is not None:
                rect = Rectangle(
                    (rect_x, rect_y),
                    rect_w,
                    rect_h,
                    transform=fig.transFigure,
                    facecolor=style.bg_color,
                    edgecolor="none",
                    clip_on=False,
                    zorder=spec.zorder - 0.1,
                )
                fig.patches.append(rect)

            fig.text(
                text_x,
                text_y,
                ls.text,
                color=style.text_color,
                fontsize=style.fontsize,
                fontweight=style.fontweight,
                rotation=rotation,
                zorder=spec.zorder,
                transform=fig.transFigure,
                clip_on=False,
                **align,
            )

        # Advance anchor outward.
        anchor += sign * (strip + gap_fig)


def _style_for_level(
    spec: MarginLabelSpec,
    level: int,
) -> MarginLabelStyle:
    """Return the style for *level*, falling back to the edge default."""
    if spec.level_styles is not None and level < len(spec.level_styles):
        return spec.level_styles[level]
    return spec.style


def _style_for_label(
    spec: MarginLabelSpec,
    level: int,
    text: str,
) -> MarginLabelStyle:
    """Return the style for a specific label, checking per-label overrides first."""
    if spec.label_styles is not None and text in spec.label_styles:
        return spec.label_styles[text]
    return _style_for_level(spec, level)
