"""Tests for eikon.export._batch — batch export and parse_export_spec."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon.config._schema import ExportDefaults
from eikon.export._batch import batch_export, parse_export_spec
from eikon.export._config import ExportSpec
from eikon.ext._hooks import clear_hooks

matplotlib.use("Agg")


@pytest.fixture(autouse=True)
def _clean_hooks() -> None:
    """Clean hooks before each test."""
    clear_hooks()


@pytest.fixture()
def sample_figure() -> plt.Figure:
    """Create a simple test figure."""
    fig, ax = plt.subplots()
    ax.plot([1, 2, 3], [1, 4, 9])
    return fig


class TestBatchExport:
    """batch_export writes files for all configured formats."""

    def teardown_method(self) -> None:
        plt.close("all")

    def test_single_format(self, tmp_path: Path, sample_figure: plt.Figure) -> None:
        paths = batch_export(
            figure=sample_figure,
            name="fig1",
            output_dir=tmp_path,
            export_defaults=ExportDefaults(),
            cli_formats=("pdf",),
        )
        assert "pdf" in paths
        assert paths["pdf"].exists()

    def test_multiple_formats(self, tmp_path: Path, sample_figure: plt.Figure) -> None:
        paths = batch_export(
            figure=sample_figure,
            name="fig1",
            output_dir=tmp_path,
            export_defaults=ExportDefaults(),
            cli_formats=("pdf", "svg", "png"),
        )
        assert len(paths) == 3
        for fmt_name, path in paths.items():
            assert path.exists()
            assert path.suffix == f".{fmt_name}"

    def test_no_formats_returns_empty(
        self, tmp_path: Path, sample_figure: plt.Figure
    ) -> None:
        defaults = ExportDefaults(formats=())
        paths = batch_export(
            figure=sample_figure,
            name="fig1",
            output_dir=tmp_path,
            export_defaults=defaults,
        )
        assert paths == {}

    def test_spec_overrides_formats(
        self, tmp_path: Path, sample_figure: plt.Figure
    ) -> None:
        spec = ExportSpec(formats=("svg",))
        paths = batch_export(
            figure=sample_figure,
            name="fig1",
            output_dir=tmp_path,
            export_defaults=ExportDefaults(),
            export_spec=spec,
        )
        assert "svg" in paths
        assert len(paths) == 1


class TestParseExportSpec:
    """parse_export_spec converts raw dicts to ExportSpec."""

    def test_none_returns_none(self) -> None:
        assert parse_export_spec(None) is None

    def test_empty_dict_returns_none(self) -> None:
        assert parse_export_spec({}) is None

    def test_formats_parsed(self) -> None:
        spec = parse_export_spec({"formats": ["pdf", "svg"]})
        assert spec is not None
        assert spec.formats == ("pdf", "svg")

    def test_dpi_parsed(self) -> None:
        spec = parse_export_spec({"dpi": 600})
        assert spec is not None
        assert spec.dpi == 600

    def test_collision_parsed(self) -> None:
        spec = parse_export_spec({"collision": "increment"})
        assert spec is not None
        assert spec.collision == "increment"

    def test_metadata_parsed(self) -> None:
        spec = parse_export_spec({"metadata": {"Author": "Test"}})
        assert spec is not None
        assert spec.metadata == {"Author": "Test"}

    def test_transparent_parsed(self) -> None:
        spec = parse_export_spec({"transparent": True})
        assert spec is not None
        assert spec.transparent is True

    def test_filename_template_parsed(self) -> None:
        spec = parse_export_spec({"filename_template": "{name}-{date}"})
        assert spec is not None
        assert spec.filename_template == "{name}-{date}"

    def test_subdirectory_parsed(self) -> None:
        spec = parse_export_spec({"subdirectory": "sub"})
        assert spec is not None
        assert spec.subdirectory == "sub"
