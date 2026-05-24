"""Grid layout specification dataclass.

A :class:`LayoutSpec` declaratively describes the grid structure of a
multi-panel figure: number of rows/columns, size ratios, and spacing.
"""

from dataclasses import dataclass

__all__ = ["LayoutSpec"]


@dataclass(frozen=True, kw_only=True, slots=True)
class LayoutSpec:
    """Declarative specification for a figure's grid layout.
    """

    rows: int = 1
    """Number of grid rows (>= 1)."""
    cols: int = 1
    """Number of grid columns (>= 1)."""
    width_ratios: tuple[float, ...] | None = None
    """Relative column widths.  Length must equal ``cols`` when set."""
    height_ratios: tuple[float, ...] | None = None
    """Relative row heights.  Length must equal ``rows`` when set."""
    wspace: float | None = None
    """Horizontal spacing between panels (fraction of average axis width)."""
    hspace: float | None = None
    """Vertical spacing between panels (fraction of average axis height)."""
    constrained_layout: bool = True
    """Whether to use matplotlib's constrained layout engine."""
