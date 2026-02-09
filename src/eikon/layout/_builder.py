"""Build a matplotlib Figure with positioned Axes from layout specs.

The builder is the final step of the layout pipeline: it takes a
validated :class:`LayoutSpec` and resolved :class:`PanelPlacement` objects
and produces a real ``matplotlib.figure.Figure`` with one ``Axes`` per
panel.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.gridspec import GridSpec

if TYPE_CHECKING:
    from eikon.layout._placement import PanelPlacement

from eikon.layout._grid import LayoutSpec

__all__ = ["BuiltLayout", "build_layout"]


@dataclass(frozen=True, kw_only=True, slots=True)
class BuiltLayout:
    """Result of building a layout: a Figure and its named Axes.

    Attributes
    ----------
    figure : Figure
        The matplotlib Figure object.
    axes : dict[str, Axes]
        Mapping from panel names to their Axes objects.
    """

    figure: Figure
    axes: dict[str, Any]  # dict[str, Axes] — Any for frozen dataclass compat


def build_layout(
    layout: LayoutSpec,
    placements: tuple[PanelPlacement, ...],
    *,
    figure_size: tuple[float, float] = (6.4, 4.8),
    dpi: int | float = 100,
) -> BuiltLayout:
    """Create a matplotlib Figure with positioned Axes.

    Parameters
    ----------
    layout : LayoutSpec
        Grid layout specification.
    placements : tuple[PanelPlacement, ...]
        Resolved panel placements (from :func:`resolve_placements`).
    figure_size : tuple[float, float]
        Figure dimensions ``(width, height)`` in inches.
    dpi : int | float
        Resolution in dots per inch.

    Returns
    -------
    BuiltLayout
        The Figure and a ``dict[str, Axes]`` mapping panel names.
    """
    engine = "constrained" if layout.constrained_layout else "none"
    fig = plt.figure(figsize=figure_size, dpi=dpi, layout=engine)

    gs_kwargs: dict[str, Any] = {}
    if layout.width_ratios is not None:
        gs_kwargs["width_ratios"] = list(layout.width_ratios)
    if layout.height_ratios is not None:
        gs_kwargs["height_ratios"] = list(layout.height_ratios)
    if layout.wspace is not None:
        gs_kwargs["wspace"] = layout.wspace
    if layout.hspace is not None:
        gs_kwargs["hspace"] = layout.hspace

    gs = GridSpec(
        nrows=layout.rows,
        ncols=layout.cols,
        figure=fig,
        **gs_kwargs,
    )

    axes: dict[str, Any] = {}
    for placement in placements:
        subplot_spec = gs[placement.row_slice, placement.col_slice]
        ax = fig.add_subplot(subplot_spec)
        axes[placement.panel_name] = ax

    return BuiltLayout(figure=fig, axes=axes)
