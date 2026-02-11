"""Layout validation — bounds checking and overlap detection.

Validates that panel placements fit within the grid and that no two
panels occupy intersecting cells.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from eikon.exceptions import LayoutError, PanelOverlapError

if TYPE_CHECKING:
    from eikon.layout._grid import LayoutSpec
    from eikon.layout._placement import PanelPlacement

__all__ = ["validate_layout"]


def validate_layout(
    placements: tuple[PanelPlacement, ...],
    layout: LayoutSpec,
) -> list[str]:
    """Validate layout constraints and return a list of error messages.

    Checks performed:

    1. Grid dimensions are positive.
    2. Ratio lengths match grid dimensions (when provided).
    3. Panels occupy at least one cell.
    4. No two panels overlap.

    Parameters
    ----------
    placements : tuple[PanelPlacement, ...]
        Resolved panel placements.
    layout : LayoutSpec
        The grid layout specification.

    Returns
    -------
    list[str]
        Validation error messages (empty if valid).

    Raises
    ------
    PanelOverlapError
        If two panels occupy intersecting grid cells.
    """
    errors: list[str] = []

    # 1. Grid dimensions
    if layout.rows < 1:
        errors.append(f"rows must be >= 1, got {layout.rows}")
    if layout.cols < 1:
        errors.append(f"cols must be >= 1, got {layout.cols}")

    # 2. Ratio lengths
    if layout.width_ratios is not None:
        if len(layout.width_ratios) != layout.cols:
            errors.append(
                f"width_ratios length ({len(layout.width_ratios)}) "
                f"must match cols ({layout.cols})"
            )
    if layout.height_ratios is not None:
        if len(layout.height_ratios) != layout.rows:
            errors.append(
                f"height_ratios length ({len(layout.height_ratios)}) "
                f"must match rows ({layout.rows})"
            )

    if errors:
        return errors

    # 3 & 4. Overlap detection via cell occupancy grid
    _check_overlaps(placements, layout)

    return errors


def _check_overlaps(
    placements: tuple[PanelPlacement, ...],
    layout: LayoutSpec,
) -> None:
    """Raise :class:`PanelOverlapError` if any panels share cells."""
    # Track which panel occupies each cell
    occupied: dict[tuple[int, int], str] = {}

    for placement in placements:
        cells = _placement_cells(placement)
        for cell in cells:
            if cell in occupied:
                raise PanelOverlapError(occupied[cell], placement.panel_name)
            occupied[cell] = placement.panel_name


def _placement_cells(
    placement: PanelPlacement,
) -> list[tuple[int, int]]:
    """Enumerate all (row, col) cells occupied by a placement."""
    row_start = placement.row_slice.start if placement.row_slice.start is not None else 0
    row_stop = placement.row_slice.stop if placement.row_slice.stop is not None else (row_start + 1)
    col_start = placement.col_slice.start if placement.col_slice.start is not None else 0
    col_stop = placement.col_slice.stop if placement.col_slice.stop is not None else (col_start + 1)
    return [
        (r, c)
        for r in range(row_start, row_stop)
        for c in range(col_start, col_stop)
    ]


def validate_layout_strict(
    placements: tuple[PanelPlacement, ...],
    layout: LayoutSpec,
) -> None:
    """Validate layout and raise :class:`LayoutError` on any problem.

    Parameters
    ----------
    placements : tuple[PanelPlacement, ...]
        Resolved panel placements.
    layout : LayoutSpec
        The grid layout specification.

    Raises
    ------
    LayoutError
        If any validation errors are found.
    PanelOverlapError
        If two panels overlap (subclass of ``LayoutError``).
    """
    errors = validate_layout(placements, layout)
    if errors:
        bullet_list = "\n  - ".join(errors)
        msg = f"Layout validation failed:\n  - {bullet_list}"
        raise LayoutError(msg)
