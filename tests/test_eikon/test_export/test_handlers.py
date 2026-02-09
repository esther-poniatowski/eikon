"""Tests for eikon.export._handlers — format-specific export."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon._types import ExportFormat
from eikon.export._config import ResolvedExportConfig
from eikon.export._handlers import export_figure, get_handler

matplotlib.use("Agg")


@pytest.fixture()
def sample_figure() -> plt.Figure:
    """Create a simple test figure."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    return fig


@pytest.fixture()
def export_config() -> ResolvedExportConfig:
    """Standard export configuration."""
    return ResolvedExportConfig(
        formats=(ExportFormat.PDF,),
        dpi=72,
        transparent=False,
        bbox_inches="tight",
        pad_inches=0.1,
        filename_template="{name}",
        subdirectory="",
        collision="overwrite",
    )


class TestGetHandler:
    """get_handler returns the correct handler for each format."""

    def test_pdf_handler(self) -> None:
        handler = get_handler(ExportFormat.PDF)
        assert callable(handler)

    def test_svg_handler(self) -> None:
        handler = get_handler(ExportFormat.SVG)
        assert callable(handler)

    def test_png_handler(self) -> None:
        handler = get_handler(ExportFormat.PNG)
        assert callable(handler)


class TestExportFigure:
    """export_figure saves to disk."""

    def teardown_method(self) -> None:
        plt.close("all")

    def test_export_pdf(
        self, tmp_path: Path, sample_figure: plt.Figure, export_config: ResolvedExportConfig
    ) -> None:
        path = tmp_path / "test.pdf"
        export_figure(sample_figure, path, ExportFormat.PDF, export_config)
        assert path.exists()
        assert path.stat().st_size > 0

    def test_export_svg(
        self, tmp_path: Path, sample_figure: plt.Figure, export_config: ResolvedExportConfig
    ) -> None:
        path = tmp_path / "test.svg"
        export_figure(sample_figure, path, ExportFormat.SVG, export_config)
        assert path.exists()
        assert path.stat().st_size > 0

    def test_export_png(
        self, tmp_path: Path, sample_figure: plt.Figure, export_config: ResolvedExportConfig
    ) -> None:
        path = tmp_path / "test.png"
        export_figure(sample_figure, path, ExportFormat.PNG, export_config)
        assert path.exists()
        assert path.stat().st_size > 0

    def test_creates_parent_dirs(
        self, tmp_path: Path, sample_figure: plt.Figure, export_config: ResolvedExportConfig
    ) -> None:
        path = tmp_path / "sub" / "dir" / "test.pdf"
        export_figure(sample_figure, path, ExportFormat.PDF, export_config)
        assert path.exists()
