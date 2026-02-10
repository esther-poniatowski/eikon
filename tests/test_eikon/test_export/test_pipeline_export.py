"""Integration tests for export via the render pipeline."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon.config._defaults import DEFAULT_CONFIG
from eikon.config._resolver import resolve_paths
from eikon.ext._hooks import clear_hooks
from eikon.ext._plot_types import _clear_registry, register_plot_type
from eikon.render._pipeline import render_figure
from eikon.spec._figure import FigureSpec
from eikon.spec._panel import PanelSpec

matplotlib.use("Agg")


def _noop_plot(ax: object, **kwargs: object) -> None:
    """Minimal plot function."""


@pytest.fixture(autouse=True)
def _clean_state() -> None:
    """Clean registry and hooks; close figures after test."""
    _clear_registry()
    clear_hooks()
    yield  # type: ignore[misc]
    plt.close("all")


class TestPipelineExport:
    """render_figure with export formats produces files."""

    def test_export_pdf(self, tmp_path: Path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="test-export",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths, formats=("pdf",))
        assert "pdf" in handle.export_paths
        assert handle.export_paths["pdf"].exists()

    def test_export_multiple_formats(
        self, tmp_path: Path
    ) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="multi-fmt",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(
            spec,
            config=DEFAULT_CONFIG,
            resolved_paths=paths,
            formats=("pdf", "svg", "png"),
        )
        assert len(handle.export_paths) == 3
        for path in handle.export_paths.values():
            assert path.exists()

    def test_no_formats_no_export(self, tmp_path: Path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="no-export",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.export_paths == {}
