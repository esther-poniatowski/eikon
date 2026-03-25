"""Tests for eikon.config._validation."""

from eikon.config._validation import validate_config, validate_figure_spec


class TestValidateConfig:
    def test_valid_minimal(self):
        errors = validate_config({})
        assert errors == []

    def test_valid_full(self):
        raw = {
            "paths": {"output_dir": "figures", "styles_dir": "styles"},
            "export": {"formats": ["pdf", "svg"], "dpi": 300, "transparent": False},
            "style": {"base_style": "default", "font_size": 10.0, "figure_size": [6.4, 4.8]},
            "registry_file": "registry.yaml",
        }
        errors = validate_config(raw)
        assert errors == []

    def test_unknown_root_key(self):
        errors = validate_config({"unknown_key": "value"})
        assert any("Unknown key" in e for e in errors)

    def test_absolute_path_rejected(self):
        errors = validate_config({"paths": {"output_dir": "/absolute/path"}})
        assert any("relative" in e for e in errors)

    def test_invalid_export_format(self):
        errors = validate_config({"export": {"formats": ["bmp"]}})
        assert any("Invalid export format" in e for e in errors)

    def test_negative_dpi(self):
        errors = validate_config({"export": {"dpi": -100}})
        assert any("positive" in e for e in errors)

    def test_invalid_figure_size(self):
        errors = validate_config({"style": {"figure_size": [1]}})
        assert any("figure_size" in e for e in errors)

    def test_not_a_dict(self):
        errors = validate_config("not a dict")  # type: ignore[arg-type]
        assert errors == ["Configuration must be a YAML mapping (dict)."]


class TestValidateFigureSpec:
    def test_valid_minimal(self):
        errors = validate_figure_spec({"name": "fig1"})
        assert errors == []

    def test_missing_name(self):
        errors = validate_figure_spec({})
        assert any("name" in e and "required" in e for e in errors)

    def test_empty_name(self):
        errors = validate_figure_spec({"name": ""})
        assert any("non-empty" in e for e in errors)

    def test_panel_missing_fields(self):
        errors = validate_figure_spec({
            "name": "fig",
            "panels": [{"name": "A"}],
        })
        assert any("plot_type" in e for e in errors)

    def test_invalid_layout_rows(self):
        errors = validate_figure_spec({
            "name": "fig",
            "layout": {"rows": 0, "cols": 1},
        })
        assert any("rows" in e for e in errors)

    def test_invalid_panel_span_shape(self):
        errors = validate_figure_spec({
            "name": "fig",
            "panels": [{"name": "A", "plot_type": "line", "row": [0], "col": 0}],
        })
        assert any("two-item span" in e for e in errors)
