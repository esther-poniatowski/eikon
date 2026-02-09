"""Tests for eikon.layout._colorbars — colorbar attachment."""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest

from eikon.exceptions import LayoutError
from eikon.layout import BuiltLayout, LayoutSpec, PanelPlacement, add_colorbar, build_layout

matplotlib.use("Agg")


def _placement(name: str, row: tuple[int, int], col: tuple[int, int]) -> PanelPlacement:
    return PanelPlacement(panel_name=name, row_slice=slice(*row), col_slice=slice(*col))


def _single_panel_with_image() -> tuple[BuiltLayout, matplotlib.image.AxesImage]:
    layout = LayoutSpec(rows=1, cols=1)
    placements = (_placement("A", (0, 1), (0, 1)),)
    built = build_layout(layout, placements)
    data = np.random.default_rng(42).random((10, 10))
    img = built.axes["A"].imshow(data)
    return built, img


class TestAddColorbar:
    """add_colorbar attaches a colorbar to a panel."""

    def teardown_method(self) -> None:
        plt.close("all")

    def test_basic_colorbar(self) -> None:
        built, img = _single_panel_with_image()
        cbar = add_colorbar(built, "A", img)
        assert cbar is not None

    def test_position_left(self) -> None:
        built, img = _single_panel_with_image()
        cbar = add_colorbar(built, "A", img, position="left")
        assert cbar is not None

    def test_unknown_panel_raises(self) -> None:
        built, img = _single_panel_with_image()
        with pytest.raises(LayoutError, match="not found"):
            add_colorbar(built, "MISSING", img)

    def test_custom_size_and_pad(self) -> None:
        built, img = _single_panel_with_image()
        cbar = add_colorbar(built, "A", img, size="10%", pad=0.1)
        assert cbar is not None
