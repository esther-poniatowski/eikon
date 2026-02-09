"""Tests for eikon.config._schema."""

from pathlib import Path

from eikon._types import ExportFormat
from eikon.config._schema import (
    ExportDefaults,
    PathsConfig,
    ProjectConfig,
    StyleDefaults,
)


class TestPathsConfig:
    def test_defaults(self):
        paths = PathsConfig()
        assert paths.output_dir == Path("figures")
        assert paths.styles_dir == Path("styles")
        assert paths.specs_dir == Path("specs")
        assert paths.data_dir == Path("data")

    def test_custom_values(self):
        paths = PathsConfig(output_dir=Path("out"), data_dir=Path("my_data"))
        assert paths.output_dir == Path("out")
        assert paths.data_dir == Path("my_data")

    def test_frozen(self):
        paths = PathsConfig()
        try:
            paths.output_dir = Path("new")  # type: ignore[misc]
            assert False, "Should have raised"
        except AttributeError:
            pass


class TestExportDefaults:
    def test_defaults(self):
        export = ExportDefaults()
        assert export.formats == (ExportFormat.PDF,)
        assert export.dpi == 300
        assert export.transparent is False
        assert export.bbox_inches == "tight"
        assert export.pad_inches == 0.1
        assert export.metadata == {}


class TestStyleDefaults:
    def test_defaults(self):
        style = StyleDefaults()
        assert style.base_style == "default"
        assert style.font_family == "serif"
        assert style.font_size == 10.0
        assert style.figure_size == (6.4, 4.8)


class TestProjectConfig:
    def test_defaults(self):
        config = ProjectConfig()
        assert isinstance(config.paths, PathsConfig)
        assert isinstance(config.export, ExportDefaults)
        assert isinstance(config.style, StyleDefaults)
        assert config.registry_file == Path("eikon-registry.yaml")
