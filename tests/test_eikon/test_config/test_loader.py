"""Tests for eikon.config._loader."""

from pathlib import Path

import pytest

from eikon._types import ExportFormat
from eikon.config._loader import load_config, merge_configs
from eikon.config._schema import ProjectConfig
from eikon.exceptions import ConfigNotFoundError, ConfigValidationError


class TestLoadConfig:
    def test_loads_from_project(self, tmp_project: Path):
        config = load_config(tmp_project / "eikon.yaml")
        assert isinstance(config, ProjectConfig)
        assert config.export.dpi == 300
        assert config.style.font_family == "serif"

    def test_raises_when_file_missing(self, tmp_path: Path):
        with pytest.raises(ConfigNotFoundError):
            load_config(tmp_path / "nonexistent.yaml")

    def test_empty_yaml_returns_defaults(self, tmp_path: Path):
        cfg = tmp_path / "eikon.yaml"
        cfg.write_text("", encoding="utf-8")
        config = load_config(cfg)
        assert config == ProjectConfig()

    def test_invalid_yaml_raises(self, tmp_path: Path):
        cfg = tmp_path / "eikon.yaml"
        cfg.write_text("{{invalid", encoding="utf-8")
        with pytest.raises(Exception):
            load_config(cfg)

    def test_validation_error(self, tmp_path: Path):
        cfg = tmp_path / "eikon.yaml"
        cfg.write_text("export:\n  dpi: -1\n", encoding="utf-8")
        with pytest.raises(ConfigValidationError):
            load_config(cfg)


class TestMergeConfigs:
    def test_override_dpi(self):
        base = ProjectConfig()
        merged = merge_configs(base, {"export": {"dpi": 600}})
        assert merged.export.dpi == 600
        # Other fields preserved
        assert merged.style.font_family == "sans-serif"

    def test_override_formats(self):
        base = ProjectConfig()
        merged = merge_configs(base, {"export": {"formats": ["svg", "png"]}})
        assert merged.export.formats == (ExportFormat.SVG, ExportFormat.PNG)

    def test_invalid_override_raises(self):
        base = ProjectConfig()
        with pytest.raises(ConfigValidationError):
            merge_configs(base, {"export": {"dpi": -1}})
