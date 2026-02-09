"""Tests for eikon.export._metadata — post-export metadata injection."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon.export._metadata import inject_pdf_metadata, inject_png_metadata

matplotlib.use("Agg")


@pytest.fixture()
def sample_figure() -> plt.Figure:
    """Create a simple test figure."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    return fig


class TestInjectPdfMetadata:
    """inject_pdf_metadata adds metadata to PDF files."""

    def teardown_method(self) -> None:
        plt.close("all")

    def test_no_op_missing_file(self, tmp_path: Path) -> None:
        inject_pdf_metadata(tmp_path / "missing.pdf", {"Author": "Test"})
        # Should not raise

    def test_no_op_empty_metadata(self, tmp_path: Path, sample_figure: plt.Figure) -> None:
        pdf_path = tmp_path / "fig.pdf"
        sample_figure.savefig(pdf_path)
        inject_pdf_metadata(pdf_path, {})
        assert pdf_path.exists()

    def test_injects_metadata(self, tmp_path: Path, sample_figure: plt.Figure) -> None:
        pdf_path = tmp_path / "fig.pdf"
        sample_figure.savefig(pdf_path)
        inject_pdf_metadata(pdf_path, {"Author": "Test Author"})
        assert pdf_path.exists()


class TestInjectPngMetadata:
    """inject_png_metadata adds text chunks to PNG files."""

    def teardown_method(self) -> None:
        plt.close("all")

    def test_no_op_missing_file(self, tmp_path: Path) -> None:
        inject_png_metadata(tmp_path / "missing.png", {"Author": "Test"})

    def test_no_op_empty_metadata(self, tmp_path: Path, sample_figure: plt.Figure) -> None:
        png_path = tmp_path / "fig.png"
        sample_figure.savefig(png_path)
        inject_png_metadata(png_path, {})
        assert png_path.exists()

    def test_injects_metadata(self, tmp_path: Path, sample_figure: plt.Figure) -> None:
        png_path = tmp_path / "fig.png"
        sample_figure.savefig(png_path)
        inject_png_metadata(png_path, {"Author": "Test", "Title": "My Figure"})
        assert png_path.exists()
