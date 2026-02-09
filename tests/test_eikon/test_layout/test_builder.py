"""Tests for eikon.layout._builder — build matplotlib Figure + Axes."""

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon.layout import BuiltLayout, LayoutSpec, PanelPlacement, build_layout

# Use non-interactive backend for tests
matplotlib.use("Agg")


def _placement(
    name: str,
    row: tuple[int, int],
    col: tuple[int, int],
) -> PanelPlacement:
    """Helper to create a PanelPlacement."""
    return PanelPlacement(
        panel_name=name,
        row_slice=slice(*row),
        col_slice=slice(*col),
    )


class TestBuildLayout:
    """Build matplotlib Figure with positioned Axes."""

    def teardown_method(self) -> None:
        plt.close("all")

    def test_single_panel(self) -> None:
        layout = LayoutSpec(rows=1, cols=1)
        placements = (_placement("A", (0, 1), (0, 1)),)
        result = build_layout(layout, placements)

        assert isinstance(result, BuiltLayout)
        assert "A" in result.axes
        assert result.figure is not None

    def test_two_by_two(self) -> None:
        layout = LayoutSpec(rows=2, cols=2)
        placements = (
            _placement("A", (0, 1), (0, 1)),
            _placement("B", (0, 1), (1, 2)),
            _placement("C", (1, 2), (0, 1)),
            _placement("D", (1, 2), (1, 2)),
        )
        result = build_layout(layout, placements)
        assert len(result.axes) == 4
        assert set(result.axes.keys()) == {"A", "B", "C", "D"}

    def test_spanning_panel(self) -> None:
        layout = LayoutSpec(rows=2, cols=2)
        placements = (
            _placement("wide", (0, 1), (0, 2)),  # top row, full width
            _placement("left", (1, 2), (0, 1)),
            _placement("right", (1, 2), (1, 2)),
        )
        result = build_layout(layout, placements)
        assert len(result.axes) == 3
        assert "wide" in result.axes

    def test_custom_figure_size(self) -> None:
        layout = LayoutSpec(rows=1, cols=1)
        placements = (_placement("A", (0, 1), (0, 1)),)
        result = build_layout(
            layout, placements, figure_size=(10.0, 8.0),
        )
        fig_size = result.figure.get_size_inches()
        assert fig_size[0] == pytest.approx(10.0)
        assert fig_size[1] == pytest.approx(8.0)

    def test_custom_dpi(self) -> None:
        layout = LayoutSpec(rows=1, cols=1)
        placements = (_placement("A", (0, 1), (0, 1)),)
        result = build_layout(layout, placements, dpi=150)
        assert result.figure.dpi == 150

    def test_width_ratios(self) -> None:
        layout = LayoutSpec(
            rows=1, cols=2, width_ratios=(2.0, 1.0),
        )
        placements = (
            _placement("A", (0, 1), (0, 1)),
            _placement("B", (0, 1), (1, 2)),
        )
        result = build_layout(layout, placements)
        assert len(result.axes) == 2

    def test_constrained_layout_disabled(self) -> None:
        layout = LayoutSpec(rows=1, cols=1, constrained_layout=False)
        placements = (_placement("A", (0, 1), (0, 1)),)
        result = build_layout(layout, placements)
        assert result.figure is not None

    def test_empty_placements(self) -> None:
        layout = LayoutSpec(rows=1, cols=1)
        result = build_layout(layout, ())
        assert result.axes == {}
        assert result.figure is not None

    def test_spacing_parameters(self) -> None:
        layout = LayoutSpec(
            rows=2, cols=2, wspace=0.5, hspace=0.5,
            constrained_layout=False,
        )
        placements = (
            _placement("A", (0, 1), (0, 1)),
            _placement("B", (0, 1), (1, 2)),
        )
        result = build_layout(layout, placements)
        assert len(result.axes) == 2


class TestBuiltLayout:
    """BuiltLayout dataclass."""

    def test_frozen(self) -> None:
        layout = LayoutSpec(rows=1, cols=1)
        placements = (_placement("A", (0, 1), (0, 1)),)
        result = build_layout(layout, placements)
        with pytest.raises(AttributeError):
            result.figure = None  # type: ignore[misc]
        plt.close("all")
