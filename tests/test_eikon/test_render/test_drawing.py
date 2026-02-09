"""Tests for eikon.render._drawing — panel draw dispatch."""

from unittest.mock import MagicMock

import pytest

from eikon.ext._plot_types import _clear_registry, register_plot_type
from eikon.render._drawing import draw_all_panels, draw_panel
from eikon.spec._panel import PanelSpec


@pytest.fixture(autouse=True)
def _clean_registry() -> None:
    """Ensure a clean plot-type registry for every test."""
    _clear_registry()


class TestDrawPanel:
    """draw_panel dispatches to the registered plot function."""

    def test_calls_registered_function(self) -> None:
        fn = MagicMock()
        register_plot_type("mock_type", fn)
        ax = MagicMock()
        panel = PanelSpec(name="A", plot_type="mock_type", params={"color": "red"})
        draw_panel(ax, panel)
        fn.assert_called_once_with(ax, color="red")

    def test_raises_for_unknown_type(self) -> None:
        ax = MagicMock()
        panel = PanelSpec(name="A", plot_type="nonexistent")
        with pytest.raises(Exception, match="nonexistent"):
            draw_panel(ax, panel)

    def test_empty_params(self) -> None:
        fn = MagicMock()
        register_plot_type("bare", fn)
        ax = MagicMock()
        panel = PanelSpec(name="A", plot_type="bare")
        draw_panel(ax, panel)
        fn.assert_called_once_with(ax)


class TestDrawAllPanels:
    """draw_all_panels iterates panels and matches them to axes."""

    def test_draws_matching_panels(self) -> None:
        fn = MagicMock()
        register_plot_type("t", fn)
        ax_a = MagicMock()
        ax_b = MagicMock()
        panels = (
            PanelSpec(name="A", plot_type="t", params={"x": 1}),
            PanelSpec(name="B", plot_type="t", params={"x": 2}),
        )
        axes = {"A": ax_a, "B": ax_b}
        draw_all_panels(axes, panels)
        assert fn.call_count == 2
        fn.assert_any_call(ax_a, x=1)
        fn.assert_any_call(ax_b, x=2)

    def test_skips_panel_without_matching_axes(self) -> None:
        fn = MagicMock()
        register_plot_type("t", fn)
        panels = (PanelSpec(name="missing", plot_type="t"),)
        axes: dict[str, MagicMock] = {"A": MagicMock()}
        draw_all_panels(axes, panels)
        fn.assert_not_called()

    def test_empty_panels(self) -> None:
        draw_all_panels({"A": MagicMock()}, ())
