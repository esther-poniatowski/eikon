"""Layout engine for multi-panel figure grids.

This subpackage converts declarative layout specifications into real
matplotlib ``Figure`` and ``Axes`` objects with validated panel positions.

Public API
----------
LayoutSpec
    Declarative grid layout dataclass.
PanelPlacement
    Resolved position of a panel within the grid.
BuiltLayout
    Result of building a layout (Figure + named Axes).
build_layout
    Build a matplotlib Figure from layout + placements.
resolve_placements
    Convert panel row/col fields to grid slices.
validate_layout
    Check layout constraints and return error messages.
validate_layout_strict
    Check layout constraints and raise on errors.
link_axes
    Share x/y axes across panel groups.
add_colorbar
    Attach a colorbar to a panel.
add_inset
    Create an inset axes within a panel.
"""

from eikon.layout._builder import BuiltLayout, build_layout
from eikon.layout._colorbars import add_colorbar
from eikon.layout._constraints import validate_layout, validate_layout_strict
from eikon.layout._grid import LayoutSpec
from eikon.layout._insets import add_inset
from eikon.layout._placement import PanelPlacement, resolve_placements
from eikon.layout._shared_axes import link_axes

__all__ = [
    "BuiltLayout",
    "LayoutSpec",
    "PanelPlacement",
    "add_colorbar",
    "add_inset",
    "build_layout",
    "link_axes",
    "resolve_placements",
    "validate_layout",
    "validate_layout_strict",
]
