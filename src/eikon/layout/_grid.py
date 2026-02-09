"""Grid layout specification dataclass.

A :class:`LayoutSpec` declaratively describes the grid structure of a
multi-panel figure: number of rows/columns, size ratios, and spacing.
"""

from dataclasses import dataclass

__all__ = ["LayoutSpec"]


@dataclass(frozen=True, kw_only=True, slots=True)
class LayoutSpec:
    """Declarative specification for a figure's grid layout.

    Attributes
    ----------
    rows : int
        Number of grid rows (>= 1).
    cols : int
        Number of grid columns (>= 1).
    width_ratios : tuple[float, ...] | None
        Relative column widths.  Length must equal ``cols`` when set.
    height_ratios : tuple[float, ...] | None
        Relative row heights.  Length must equal ``rows`` when set.
    wspace : float | None
        Horizontal spacing between panels (fraction of average axis width).
    hspace : float | None
        Vertical spacing between panels (fraction of average axis height).
    constrained_layout : bool
        Whether to use matplotlib's constrained layout engine.
    """

    rows: int = 1
    cols: int = 1
    width_ratios: tuple[float, ...] | None = None
    height_ratios: tuple[float, ...] | None = None
    wspace: float | None = None
    hspace: float | None = None
    constrained_layout: bool = True
