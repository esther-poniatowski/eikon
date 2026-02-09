"""Tests for eikon.contrib._matplotlib — built-in matplotlib plot types."""

from typing import Any
from unittest.mock import MagicMock

import pytest

from eikon.ext._plot_types import _clear_registry, get_plot_type

# Import contrib to register the plot types
import eikon.contrib  # noqa: F401


@pytest.fixture(autouse=True)
def _ensure_registered() -> Any:
    """Contrib plot types must be registered."""
    import importlib

    import eikon.contrib._matplotlib
    importlib.reload(eikon.contrib._matplotlib)
    yield
    _clear_registry()


class TestMatplotlibPlotTypes:
    """Built-in matplotlib plot types are registered and callable."""

    @pytest.mark.parametrize("name", [
        "line", "scatter", "bar", "barh", "hist",
        "heatmap", "contour", "errorbar",
    ])
    def test_registered(self, name: str) -> None:
        fn = get_plot_type(name)
        assert callable(fn)

    def test_line_calls_plot(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("line")
        fn(ax, x=[1, 2], y=[3, 4], color="blue")
        ax.plot.assert_called_once_with([1, 2], [3, 4], color="blue")

    def test_scatter_calls_scatter(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("scatter")
        fn(ax, x=[1], y=[2], s=10)
        ax.scatter.assert_called_once_with([1], [2], s=10)

    def test_bar_calls_bar(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("bar")
        fn(ax, x=["a", "b"], height=[1, 2])
        ax.bar.assert_called_once_with(["a", "b"], [1, 2])

    def test_hist_calls_hist(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("hist")
        fn(ax, x=[1, 2, 3], bins=5)
        ax.hist.assert_called_once_with([1, 2, 3], bins=5)

    def test_line_y_only(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("line")
        fn(ax, y=[1, 2, 3])
        ax.plot.assert_called_once_with([1, 2, 3])

    def test_line_no_args(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("line")
        fn(ax)
        ax.plot.assert_called_once_with()

    def test_barh_calls_barh(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("barh")
        fn(ax, y=["a", "b"], width=[1, 2])
        ax.barh.assert_called_once_with(["a", "b"], [1, 2])

    def test_heatmap_calls_imshow(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("heatmap")
        fn(ax, data=[[1, 2], [3, 4]])
        ax.imshow.assert_called_once_with([[1, 2], [3, 4]])

    def test_contour_with_xyz(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("contour")
        fn(ax, x=[1], y=[2], z=[[3]])
        ax.contour.assert_called_once_with([1], [2], [[3]])

    def test_contour_z_only(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("contour")
        fn(ax, z=[[1, 2], [3, 4]])
        ax.contour.assert_called_once_with([[1, 2], [3, 4]])

    def test_errorbar_calls_errorbar(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("errorbar")
        fn(ax, x=[1, 2], y=[3, 4], yerr=[0.1, 0.2])
        ax.errorbar.assert_called_once_with([1, 2], [3, 4], yerr=[0.1, 0.2])

    def test_scatter_no_data_is_noop(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("scatter")
        fn(ax)
        ax.scatter.assert_not_called()

    def test_bar_with_y_alias(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("bar")
        fn(ax, x=["a"], y=[5])
        ax.bar.assert_called_once_with(["a"], [5])

    def test_barh_with_x_alias(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("barh")
        fn(ax, y=["a"], x=[5])
        ax.barh.assert_called_once_with(["a"], [5])
