"""Tests for eikon.render._pipeline — render_figure orchestrator."""

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon.config._defaults import DEFAULT_CONFIG
from eikon.config._resolver import resolve_paths
from eikon.ext._hooks import HookName, clear_hooks, register_hook
from eikon.ext._plot_types import _clear_registry, register_plot_type
from eikon.render._handle import FigureHandle
from eikon.render._pipeline import render_figure
from eikon.spec._figure import FigureSpec
from eikon.spec._panel import PanelSpec

matplotlib.use("Agg")


@pytest.fixture(autouse=True)
def _clean_state() -> None:
    """Clean plot-type registry and hooks before each test; close figs after."""
    _clear_registry()
    clear_hooks()
    yield  # type: ignore[misc]
    plt.close("all")


def _noop_plot(ax: object, **kwargs: object) -> None:
    """Minimal plot function that does nothing."""


class TestRenderFigure:
    """Integration tests for the pipeline orchestrator."""

    def test_single_panel_render(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="test-fig",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert isinstance(handle, FigureHandle)
        assert handle.spec is spec
        assert handle.figure is not None
        assert "A" in handle.axes

    def test_multi_panel_render(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="multi",
            panels=(
                PanelSpec(name="A", plot_type="noop", row=0, col=0),
                PanelSpec(name="B", plot_type="noop", row=0, col=1),
            ),
            layout={"rows": 1, "cols": 2},
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert "A" in handle.axes
        assert "B" in handle.axes

    def test_figure_title_applied(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="titled",
            title="Test Title",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.figure is not None
        assert handle.figure._suptitle.get_text() == "Test Title"

    def test_panel_label_applied(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="labeled",
            panels=(PanelSpec(name="A", plot_type="noop", label="(a)"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.axes["A"].get_title() == "(a)"

    def test_hooks_fired(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        calls: list[str] = []
        register_hook(HookName.PRE_RENDER, lambda **kw: calls.append("pre"))
        register_hook(HookName.POST_RENDER, lambda **kw: calls.append("post"))

        spec = FigureSpec(
            name="hooked",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert calls == ["pre", "post"]

    def test_custom_config(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="custom-cfg",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.figure is not None

    def test_render_error_on_unknown_plot_type(self, tmp_path) -> None:
        spec = FigureSpec(
            name="bad",
            panels=(PanelSpec(name="A", plot_type="does_not_exist"),),
        )
        with pytest.raises(Exception):
            paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
            render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)

    def test_style_ref_resolved(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="styled",
            style="publication",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.figure is not None

    def test_empty_style_ref(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="no-style",
            style="",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.figure is not None
