"""Tests for eikon.render._pipeline — render_figure orchestrator."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon.config._defaults import DEFAULT_CONFIG
from eikon.config._resolver import resolve_paths
from eikon.exceptions import RenderError
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

    def test_title_kwargs_forwarded(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="tkw",
            title="Custom",
            title_kwargs={"fontsize": 20, "y": 0.95},
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        st = handle.figure._suptitle
        assert st.get_text() == "Custom"
        assert st.get_fontsize() == 20

    def test_hide_spines_applied(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="spines",
            panels=(
                PanelSpec(
                    name="A",
                    plot_type="noop",
                    hide_spines=("top", "right"),
                ),
            ),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        ax = handle.axes["A"]
        assert not ax.spines["top"].get_visible()
        assert not ax.spines["right"].get_visible()
        assert ax.spines["bottom"].get_visible()
        assert ax.spines["left"].get_visible()

    def test_shared_legend_placed(self, tmp_path) -> None:
        def _legend_plot(ax, **kwargs):
            ax.plot([1, 2], [3, 4], label="line-a")

        register_plot_type("legend_plot", _legend_plot)
        spec = FigureSpec(
            name="legend",
            shared_legend={"loc": "upper right"},
            panels=(PanelSpec(name="A", plot_type="legend_plot"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        fig_legends = handle.figure.legends
        assert len(fig_legends) == 1

    def test_per_panel_style(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        paths.styles_dir.mkdir(parents=True, exist_ok=True)
        spec = FigureSpec(
            name="per-panel",
            panels=(
                PanelSpec(name="A", plot_type="noop", style="publication"),
            ),
        )
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.figure is not None

    def test_user_style_extends_user_style(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        styles_dir = paths.styles_dir
        styles_dir.mkdir(parents=True, exist_ok=True)
        # Create base user style
        (styles_dir / "my-base.yaml").write_text(
            "name: my-base\nfont_size: 9.0\n", encoding="utf-8",
        )
        # Create child user style extending the base
        (styles_dir / "my-child.yaml").write_text(
            "name: my-child\nextends: [my-base]\nfont_family: monospace\n",
            encoding="utf-8",
        )
        spec = FigureSpec(
            name="chain",
            style="my-child",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.figure is not None

    def test_export_produces_files(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        paths.output_dir.mkdir(parents=True, exist_ok=True)
        spec = FigureSpec(
            name="exported",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        handle = render_figure(
            spec, config=DEFAULT_CONFIG, resolved_paths=paths, formats=("pdf",),
        )
        assert "pdf" in handle.export_paths
        assert Path(handle.export_paths["pdf"]).exists()

    def test_unknown_plot_type_raises_render_error(self, tmp_path) -> None:
        spec = FigureSpec(
            name="bad-type",
            panels=(PanelSpec(name="A", plot_type="totally_nonexistent"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        with pytest.raises(RenderError, match="totally_nonexistent"):
            render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)

    def test_render_no_config_fallback(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="no-cfg",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, resolved_paths=paths)
        assert handle.figure is not None

    def test_multi_panel_layout_with_ratios(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="ratios",
            panels=(
                PanelSpec(name="A", plot_type="noop", row=0, col=0),
                PanelSpec(name="B", plot_type="noop", row=0, col=1),
            ),
            layout={"rows": 1, "cols": 2, "width_ratios": [2.0, 1.0]},
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert "A" in handle.axes
        assert "B" in handle.axes
