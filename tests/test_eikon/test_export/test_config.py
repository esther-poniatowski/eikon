"""Tests for eikon.export._config — ExportSpec, ResolvedExportConfig."""

from eikon._types import ExportFormat
from eikon.config._schema import ExportDefaults
from eikon.export._config import ExportSpec, ResolvedExportConfig, resolve_export_config


class TestExportSpec:
    """ExportSpec construction and defaults."""

    def test_defaults(self) -> None:
        spec = ExportSpec()
        assert spec.formats is None
        assert spec.dpi is None
        assert spec.transparent is None
        assert spec.filename_template is None
        assert spec.subdirectory is None
        assert spec.collision is None
        assert spec.metadata is None

    def test_custom_values(self) -> None:
        spec = ExportSpec(
            formats=("pdf", "svg"),
            dpi=600,
            transparent=True,
            filename_template="{name}_{date}",
            subdirectory="figures",
            collision="increment",
            metadata={"Author": "Test"},
        )
        assert spec.formats == ("pdf", "svg")
        assert spec.dpi == 600
        assert spec.collision == "increment"


class TestResolvedExportConfig:
    """ResolvedExportConfig has no optional fields."""

    def test_all_fields_present(self) -> None:
        config = ResolvedExportConfig(
            formats=(ExportFormat.PDF,),
            dpi=300,
            transparent=False,
            bbox_inches="tight",
            pad_inches=0.1,
            filename_template="{name}",
            subdirectory="",
            collision="overwrite",
        )
        assert config.formats == (ExportFormat.PDF,)
        assert config.dpi == 300
        assert config.collision == "overwrite"


class TestResolveExportConfig:
    """resolve_export_config merges spec on top of defaults."""

    def test_defaults_only(self) -> None:
        defaults = ExportDefaults()
        result = resolve_export_config(defaults)
        assert result.formats == defaults.formats
        assert result.dpi == defaults.dpi
        assert result.transparent == defaults.transparent

    def test_spec_overrides_dpi(self) -> None:
        defaults = ExportDefaults()
        spec = ExportSpec(dpi=600)
        result = resolve_export_config(defaults, spec)
        assert result.dpi == 600

    def test_spec_overrides_formats(self) -> None:
        defaults = ExportDefaults()
        spec = ExportSpec(formats=("svg", "png"))
        result = resolve_export_config(defaults, spec)
        assert result.formats == (ExportFormat.SVG, ExportFormat.PNG)

    def test_cli_formats_override_all(self) -> None:
        defaults = ExportDefaults()
        spec = ExportSpec(formats=("pdf",))
        result = resolve_export_config(defaults, spec, cli_formats=("svg",))
        assert result.formats == (ExportFormat.SVG,)

    def test_metadata_merged(self) -> None:
        defaults = ExportDefaults(metadata={"Author": "Default"})
        spec = ExportSpec(metadata={"Project": "Test"})
        result = resolve_export_config(defaults, spec)
        assert result.metadata == {"Author": "Default", "Project": "Test"}

    def test_filename_template_default(self) -> None:
        defaults = ExportDefaults()
        result = resolve_export_config(defaults)
        assert result.filename_template == "{name}"

    def test_collision_default(self) -> None:
        defaults = ExportDefaults()
        result = resolve_export_config(defaults)
        assert result.collision == "overwrite"
