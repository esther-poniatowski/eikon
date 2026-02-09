"""Tests for eikon.layout._placement — panel position resolution."""

import pytest

from eikon.layout import LayoutSpec, PanelPlacement, resolve_placements
from eikon.spec import PanelSpec


class TestToSlice:
    """_to_slice conversion via resolve_placements."""

    def test_single_int_row(self) -> None:
        panel = PanelSpec(name="A", plot_type="line", row=0, col=0)
        layout = LayoutSpec(rows=2, cols=2)
        (placement,) = resolve_placements((panel,), layout)
        assert placement.row_slice == slice(0, 1)

    def test_single_int_col(self) -> None:
        panel = PanelSpec(name="A", plot_type="line", row=0, col=1)
        layout = LayoutSpec(rows=1, cols=3)
        (placement,) = resolve_placements((panel,), layout)
        assert placement.col_slice == slice(1, 2)

    def test_tuple_span_row(self) -> None:
        panel = PanelSpec(name="A", plot_type="line", row=(0, 2), col=0)
        layout = LayoutSpec(rows=3, cols=1)
        (placement,) = resolve_placements((panel,), layout)
        assert placement.row_slice == slice(0, 2)

    def test_tuple_span_col(self) -> None:
        panel = PanelSpec(name="A", plot_type="line", row=0, col=(1, 3))
        layout = LayoutSpec(rows=1, cols=4)
        (placement,) = resolve_placements((panel,), layout)
        assert placement.col_slice == slice(1, 3)

    def test_out_of_bounds_row(self) -> None:
        panel = PanelSpec(name="A", plot_type="line", row=5, col=0)
        layout = LayoutSpec(rows=2, cols=1)
        with pytest.raises(ValueError, match="out of bounds"):
            resolve_placements((panel,), layout)

    def test_out_of_bounds_col(self) -> None:
        panel = PanelSpec(name="A", plot_type="line", row=0, col=3)
        layout = LayoutSpec(rows=1, cols=2)
        with pytest.raises(ValueError, match="out of bounds"):
            resolve_placements((panel,), layout)

    def test_invalid_span(self) -> None:
        panel = PanelSpec(name="A", plot_type="line", row=(2, 1), col=0)
        layout = LayoutSpec(rows=3, cols=1)
        with pytest.raises(ValueError, match="invalid"):
            resolve_placements((panel,), layout)

    def test_span_exceeds_grid(self) -> None:
        panel = PanelSpec(name="A", plot_type="line", row=(0, 5), col=0)
        layout = LayoutSpec(rows=3, cols=1)
        with pytest.raises(ValueError, match="invalid"):
            resolve_placements((panel,), layout)


class TestResolvePlacements:
    """Resolve multiple panels to placements."""

    def test_two_panels(self) -> None:
        panels = (
            PanelSpec(name="A", plot_type="line", row=0, col=0),
            PanelSpec(name="B", plot_type="scatter", row=0, col=1),
        )
        layout = LayoutSpec(rows=1, cols=2)
        placements = resolve_placements(panels, layout)
        assert len(placements) == 2
        assert placements[0].panel_name == "A"
        assert placements[1].panel_name == "B"

    def test_empty_panels(self) -> None:
        layout = LayoutSpec(rows=1, cols=1)
        placements = resolve_placements((), layout)
        assert placements == ()

    def test_panel_placement_is_frozen(self) -> None:
        placement = PanelPlacement(
            panel_name="A",
            row_slice=slice(0, 1),
            col_slice=slice(0, 1),
        )
        with pytest.raises(AttributeError):
            placement.panel_name = "B"  # type: ignore[misc]
