"""Integration tests for export via the render pipeline."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

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

    def test_export_pdf(self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_path)
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="test-export",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        handle = render_figure(spec, formats=("pdf",))
        assert "pdf" in handle.export_paths
        assert handle.export_paths["pdf"].exists()

    def test_export_multiple_formats(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ) -> None:
        monkeypatch.chdir(tmp_path)
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="multi-fmt",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        handle = render_figure(spec, formats=("pdf", "svg", "png"))
        assert len(handle.export_paths) == 3
        for path in handle.export_paths.values():
            assert path.exists()

    def test_no_formats_no_export(self) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="no-export",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        handle = render_figure(spec)
        assert handle.export_paths == {}
