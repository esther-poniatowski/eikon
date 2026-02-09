"""Tests for eikon.layout._shared_axes — shared-axis linking."""

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon.exceptions import LayoutError
from eikon.layout import BuiltLayout, LayoutSpec, PanelPlacement, build_layout, link_axes

matplotlib.use("Agg")


def _placement(name: str, row: tuple[int, int], col: tuple[int, int]) -> PanelPlacement:
    return PanelPlacement(panel_name=name, row_slice=slice(*row), col_slice=slice(*col))


def _two_panel_layout() -> BuiltLayout:
    layout = LayoutSpec(rows=1, cols=2)
    placements = (_placement("A", (0, 1), (0, 1)), _placement("B", (0, 1), (1, 2)))
    return build_layout(layout, placements)


class TestLinkAxes:
    """link_axes shares x/y scales across panels."""

    def teardown_method(self) -> None:
        plt.close("all")

    def test_share_x(self) -> None:
        built = _two_panel_layout()
        link_axes(built, (("A", "B"),), axis="x")
        built.axes["A"].set_xlim(0, 10)
        assert built.axes["B"].get_xlim() == (0, 10)

    def test_share_y(self) -> None:
        built = _two_panel_layout()
        link_axes(built, (("A", "B"),), axis="y")
        built.axes["A"].set_ylim(-5, 5)
        assert built.axes["B"].get_ylim() == (-5, 5)

    def test_share_both(self) -> None:
        built = _two_panel_layout()
        link_axes(built, (("A", "B"),), axis="both")
        built.axes["A"].set_xlim(0, 10)
        built.axes["A"].set_ylim(-1, 1)
        assert built.axes["B"].get_xlim() == (0, 10)
        assert built.axes["B"].get_ylim() == (-1, 1)

    def test_unknown_panel_raises(self) -> None:
        built = _two_panel_layout()
        with pytest.raises(LayoutError, match="not found"):
            link_axes(built, (("A", "MISSING"),), axis="x")

    def test_unknown_ref_panel_raises(self) -> None:
        built = _two_panel_layout()
        with pytest.raises(LayoutError, match="not found"):
            link_axes(built, (("MISSING", "A"),), axis="x")

    def test_single_panel_group_is_noop(self) -> None:
        built = _two_panel_layout()
        link_axes(built, (("A",),), axis="x")  # should not raise
