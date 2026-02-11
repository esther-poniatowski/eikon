"""Tests for eikon.layout._constraints — layout validation."""

import pytest

from eikon.exceptions import LayoutError, PanelOverlapError
from eikon.layout import (
    LayoutSpec,
    PanelPlacement,
    validate_layout,
    validate_layout_strict,
)


def _placement(
    name: str,
    row: tuple[int, int],
    col: tuple[int, int],
) -> PanelPlacement:
    """Helper to create a PanelPlacement from row/col tuples."""
    return PanelPlacement(
        panel_name=name,
        row_slice=slice(*row),
        col_slice=slice(*col),
    )


class TestValidateLayout:
    """Validation of layout constraints."""

    def test_valid_layout(self) -> None:
        layout = LayoutSpec(rows=2, cols=2)
        placements = (
            _placement("A", (0, 1), (0, 1)),
            _placement("B", (0, 1), (1, 2)),
            _placement("C", (1, 2), (0, 1)),
            _placement("D", (1, 2), (1, 2)),
        )
        errors = validate_layout(placements, layout)
        assert errors == []

    def test_invalid_rows(self) -> None:
        layout = LayoutSpec(rows=0, cols=1)
        errors = validate_layout((), layout)
        assert any("rows" in e for e in errors)

    def test_invalid_cols(self) -> None:
        layout = LayoutSpec(rows=1, cols=0)
        errors = validate_layout((), layout)
        assert any("cols" in e for e in errors)

    def test_width_ratios_mismatch(self) -> None:
        layout = LayoutSpec(rows=1, cols=2, width_ratios=(1.0,))
        errors = validate_layout((), layout)
        assert any("width_ratios" in e for e in errors)

    def test_height_ratios_mismatch(self) -> None:
        layout = LayoutSpec(rows=2, cols=1, height_ratios=(1.0, 2.0, 3.0))
        errors = validate_layout((), layout)
        assert any("height_ratios" in e for e in errors)

    def test_overlap_detected(self) -> None:
        layout = LayoutSpec(rows=2, cols=2)
        placements = (
            _placement("A", (0, 2), (0, 1)),  # spans both rows, col 0
            _placement("B", (1, 2), (0, 1)),  # row 1, col 0 — overlaps A
        )
        with pytest.raises(PanelOverlapError, match="A.*B"):
            validate_layout(placements, layout)

    def test_no_overlap_adjacent(self) -> None:
        layout = LayoutSpec(rows=1, cols=2)
        placements = (
            _placement("A", (0, 1), (0, 1)),
            _placement("B", (0, 1), (1, 2)),
        )
        errors = validate_layout(placements, layout)
        assert errors == []

    def test_overlap_spanning_panels(self) -> None:
        layout = LayoutSpec(rows=2, cols=2)
        placements = (
            _placement("A", (0, 2), (0, 2)),  # full grid
            _placement("B", (0, 1), (0, 1)),  # top-left — overlaps
        )
        with pytest.raises(PanelOverlapError):
            validate_layout(placements, layout)


class TestPlacementCellsZero:
    """Regression: _placement_cells must handle zero-valued slice attributes."""

    def test_zero_start_row(self) -> None:
        layout = LayoutSpec(rows=2, cols=1)
        placements = (_placement("A", (0, 1), (0, 1)),)
        errors = validate_layout(placements, layout)
        assert errors == []

    def test_zero_start_col(self) -> None:
        layout = LayoutSpec(rows=1, cols=2)
        placements = (_placement("A", (0, 1), (0, 1)),)
        errors = validate_layout(placements, layout)
        assert errors == []

    def test_zero_stop_no_false_expansion(self) -> None:
        """slice(0, 0) should produce an empty range, not expand to (0, 1)."""
        layout = LayoutSpec(rows=2, cols=2)
        p = PanelPlacement(
            panel_name="empty",
            row_slice=slice(0, 0),
            col_slice=slice(0, 1),
        )
        from eikon.layout._constraints import _placement_cells

        cells = _placement_cells(p)
        assert cells == []


class TestValidateLayoutStrict:
    """Strict validation raises LayoutError."""

    def test_valid_passes(self) -> None:
        layout = LayoutSpec(rows=1, cols=1)
        placements = (_placement("A", (0, 1), (0, 1)),)
        validate_layout_strict(placements, layout)  # should not raise

    def test_invalid_raises_layout_error(self) -> None:
        layout = LayoutSpec(rows=0, cols=1)
        with pytest.raises(LayoutError, match="validation failed"):
            validate_layout_strict((), layout)

    def test_overlap_raises_panel_overlap_error(self) -> None:
        layout = LayoutSpec(rows=1, cols=1)
        placements = (
            _placement("A", (0, 1), (0, 1)),
            _placement("B", (0, 1), (0, 1)),
        )
        with pytest.raises(PanelOverlapError):
            validate_layout_strict(placements, layout)
