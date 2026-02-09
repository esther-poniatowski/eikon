"""Tests for eikon.spec._parse."""

from pathlib import Path

import pytest

from eikon.exceptions import SpecValidationError
from eikon.spec._parse import parse_figure_file, parse_figure_spec


class TestParseFigureSpec:
    def test_minimal(self):
        spec = parse_figure_spec({"name": "fig1"})
        assert spec.name == "fig1"
        assert spec.panels == ()

    def test_with_panels(self, sample_spec_dict: dict):
        spec = parse_figure_spec(sample_spec_dict)
        assert spec.name == "test-figure"
        assert len(spec.panels) == 2
        assert spec.panels[0].name == "A"
        assert spec.panels[0].plot_type == "line"
        assert spec.panels[0].params == {"color": "blue"}
        assert spec.panels[1].name == "B"

    def test_tags_parsed(self, sample_spec_dict: dict):
        spec = parse_figure_spec(sample_spec_dict)
        assert spec.tags == ("test", "unit")

    def test_layout_preserved(self, sample_spec_dict: dict):
        spec = parse_figure_spec(sample_spec_dict)
        assert spec.layout == {"rows": 1, "cols": 2}

    def test_validation_error(self):
        with pytest.raises(SpecValidationError):
            parse_figure_spec({})  # missing name

    def test_panel_with_data_binding(self):
        raw = {
            "name": "fig",
            "panels": [{
                "name": "A",
                "plot_type": "line",
                "data": {"source": "data.csv", "x": "time", "y": "value"},
            }],
        }
        spec = parse_figure_spec(raw)
        assert spec.panels[0].data is not None
        assert spec.panels[0].data.source == "data.csv"
        assert spec.panels[0].data.x == "time"

    def test_auto_size_default_false(self):
        spec = parse_figure_spec({
            "name": "fig",
            "panels": [{"name": "A", "plot_type": "line"}],
        })
        assert spec.panels[0].auto_size is False

    def test_auto_size_parsed(self):
        spec = parse_figure_spec({
            "name": "fig",
            "panels": [{"name": "A", "plot_type": "line", "auto_size": True}],
        })
        assert spec.panels[0].auto_size is True


class TestParseFigureFile:
    def test_loads_yaml(self, tmp_path: Path, sample_spec_dict: dict):
        import yaml

        spec_file = tmp_path / "fig.yaml"
        spec_file.write_text(yaml.dump(sample_spec_dict), encoding="utf-8")
        spec = parse_figure_file(spec_file)
        assert spec.name == "test-figure"

    def test_missing_file(self, tmp_path: Path):
        with pytest.raises(Exception):
            parse_figure_file(tmp_path / "nonexistent.yaml")
