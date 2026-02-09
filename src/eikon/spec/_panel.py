"""Panel specification for a single axes region within a figure.

A :class:`PanelSpec` describes one axes panel: its plot type, position
in the grid layout, data binding, and per-panel style overrides.
"""

from dataclasses import dataclass, field
from typing import Any

from eikon._types import StyleRef
from eikon.spec._data import DataBinding

__all__ = ["PanelSpec"]


@dataclass(frozen=True, kw_only=True, slots=True)
class PanelSpec:
    """Specification for one axes panel within a figure.

    Attributes
    ----------
    name : str
        Panel identifier (e.g. ``"A"``, ``"top-left"``).
    plot_type : str
        Registry key for the plot function to invoke.
    data : DataBinding | None
        Data source reference. ``None`` if data is passed via ``params``.
    row : int | tuple[int, int]
        Row index (zero-based) or ``(start, end)`` span in the grid.
    col : int | tuple[int, int]
        Column index (zero-based) or ``(start, end)`` span in the grid.
    style : StyleRef | None
        Per-panel style override.
    params : dict[str, Any]
        Keyword arguments forwarded to the plot function.
    label : str
        Panel label rendered on the axes (e.g. ``"(a)"``, ``"(b)"``).
    auto_size : bool
        When ``True``, defer figure size to the constrained-layout solver
        rather than using the explicit ``figure_size``.
    """

    name: str
    plot_type: str
    data: DataBinding | None = None
    row: int | tuple[int, int] = 0
    col: int | tuple[int, int] = 0
    style: StyleRef | None = None
    params: dict[str, Any] = field(default_factory=dict)
    label: str = ""
    auto_size: bool = False
