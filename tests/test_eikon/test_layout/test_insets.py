"""Tests for eikon.layout._insets — inset axes creation."""

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon.exceptions import LayoutError
from eikon.layout import BuiltLayout, LayoutSpec, PanelPlacement, add_inset, build_layout

matplotlib.use("Agg")


def _placement(name: str, row: tuple[int, int], col: tuple[int, int]) -> PanelPlacement:
    return PanelPlacement(panel_name=name, row_slice=slice(*row), col_slice=slice(*col))


def _single_panel() -> BuiltLayout:
    layout = LayoutSpec(rows=1, cols=1)
    placements = (_placement("A", (0, 1), (0, 1)),)
    return build_layout(layout, placements)


class TestAddInset:
    """add_inset creates an inset axes within a panel."""

    def teardown_method(self) -> None:
        plt.close("all")

    def test_basic_inset(self) -> None:
        built = _single_panel()
        new_built = add_inset(built, "A", "inset", (0.6, 0.6, 0.3, 0.3))
        assert "inset" in new_built.axes
        assert "A" in new_built.axes

    def test_returns_new_built_layout(self) -> None:
        built = _single_panel()
        new_built = add_inset(built, "A", "inset", (0.1, 0.1, 0.4, 0.4))
        assert new_built is not built
        assert "inset" not in built.axes

    def test_unknown_parent_raises(self) -> None:
        built = _single_panel()
        with pytest.raises(LayoutError, match="not found"):
            add_inset(built, "MISSING", "inset", (0.5, 0.5, 0.3, 0.3))

    def test_duplicate_name_raises(self) -> None:
        built = _single_panel()
        with pytest.raises(LayoutError, match="already exists"):
            add_inset(built, "A", "A", (0.5, 0.5, 0.3, 0.3))
