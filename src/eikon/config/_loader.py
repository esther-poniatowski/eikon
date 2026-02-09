"""YAML configuration loading and deep merging.

Loads ``eikon.yaml`` from disk, validates the content, and constructs a
:class:`ProjectConfig` with proper layered merging of defaults.
"""

from pathlib import Path
from typing import Any

import yaml

from eikon._types import ExportFormat
from eikon.config._defaults import CONFIG_FILENAME, DEFAULT_CONFIG
from eikon.config._resolver import discover_project_root
from eikon.config._schema import (
    ExportDefaults,
    PathsConfig,
    ProjectConfig,
    StyleDefaults,
)
from eikon.config._validation import validate_config
from eikon.exceptions import ConfigError, ConfigNotFoundError, ConfigValidationError

__all__ = ["load_config", "merge_configs"]


def load_config(path: Path | None = None) -> ProjectConfig:
    """Load and validate the project configuration.

    Parameters
    ----------
    path : Path, optional
        Explicit path to an ``eikon.yaml`` file.  If ``None``, the file is
        discovered by walking upward from the current working directory.

    Returns
    -------
    ProjectConfig
        Validated project configuration.

    Raises
    ------
    ConfigNotFoundError
        If no configuration file is found.
    ConfigValidationError
        If the configuration fails schema validation.
    ConfigError
        If the YAML file cannot be parsed.
    """
    if path is None:
        root = discover_project_root()
        path = root / CONFIG_FILENAME

    path = path.resolve()
    if not path.is_file():
        raise ConfigNotFoundError(str(path.parent))

    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        raise ConfigError(f"Failed to parse {path}: {exc}") from exc

    if raw is None:
        return DEFAULT_CONFIG

    if not isinstance(raw, dict):
        raise ConfigError(f"Expected a YAML mapping in {path}, got {type(raw).__name__}.")

    errors = validate_config(raw)
    if errors:
        raise ConfigValidationError(errors)

    return _build_config(raw)


def merge_configs(base: ProjectConfig, override: dict[str, Any]) -> ProjectConfig:
    """Deep-merge an override dictionary into an existing configuration.

    Parameters
    ----------
    base : ProjectConfig
        The base configuration to merge onto.
    override : dict
        A dictionary of overrides (same structure as ``eikon.yaml``).

    Returns
    -------
    ProjectConfig
        A new configuration with overrides applied.
    """
    errors = validate_config(override)
    if errors:
        raise ConfigValidationError(errors)

    raw_base = _config_to_dict(base)
    merged = _deep_merge(raw_base, override)
    return _build_config(merged)


# --- Internal helpers ---


def _build_config(raw: dict[str, Any]) -> ProjectConfig:
    """Construct a :class:`ProjectConfig` from a validated dictionary."""
    paths = _build_paths(raw.get("paths", {}))
    export = _build_export(raw.get("export", {}))
    style = _build_style(raw.get("style", {}))
    registry_file = (
        Path(raw["registry_file"]) if "registry_file" in raw else DEFAULT_CONFIG.registry_file
    )
    return ProjectConfig(
        paths=paths,
        export=export,
        style=style,
        registry_file=registry_file,
    )


def _build_paths(raw: dict[str, Any]) -> PathsConfig:
    kwargs: dict[str, Any] = {}
    for key in ("output_dir", "styles_dir", "specs_dir", "data_dir"):
        if key in raw:
            kwargs[key] = Path(raw[key])
    return PathsConfig(**kwargs)


def _build_export(raw: dict[str, Any]) -> ExportDefaults:
    kwargs: dict[str, Any] = {}
    if "formats" in raw:
        kwargs["formats"] = tuple(ExportFormat.from_string(str(f)) for f in raw["formats"])
    if "dpi" in raw:
        kwargs["dpi"] = int(raw["dpi"])
    if "transparent" in raw:
        kwargs["transparent"] = bool(raw["transparent"])
    if "bbox_inches" in raw:
        kwargs["bbox_inches"] = str(raw["bbox_inches"])
    if "pad_inches" in raw:
        kwargs["pad_inches"] = float(raw["pad_inches"])
    if "metadata" in raw:
        kwargs["metadata"] = dict(raw["metadata"])
    return ExportDefaults(**kwargs)


def _build_style(raw: dict[str, Any]) -> StyleDefaults:
    kwargs: dict[str, Any] = {}
    if "base_style" in raw:
        kwargs["base_style"] = str(raw["base_style"])
    if "font_family" in raw:
        kwargs["font_family"] = str(raw["font_family"])
    if "font_size" in raw:
        kwargs["font_size"] = float(raw["font_size"])
    if "figure_size" in raw:
        kwargs["figure_size"] = tuple(float(v) for v in raw["figure_size"])
    return StyleDefaults(**kwargs)


def _config_to_dict(config: ProjectConfig) -> dict[str, Any]:
    """Serialize a :class:`ProjectConfig` back to a plain dictionary."""
    return {
        "paths": {
            "output_dir": str(config.paths.output_dir),
            "styles_dir": str(config.paths.styles_dir),
            "specs_dir": str(config.paths.specs_dir),
            "data_dir": str(config.paths.data_dir),
        },
        "export": {
            "formats": [f.value for f in config.export.formats],
            "dpi": config.export.dpi,
            "transparent": config.export.transparent,
            "bbox_inches": config.export.bbox_inches,
            "pad_inches": config.export.pad_inches,
            "metadata": dict(config.export.metadata),
        },
        "style": {
            "base_style": config.style.base_style,
            "font_family": config.style.font_family,
            "font_size": config.style.font_size,
            "figure_size": list(config.style.figure_size),
        },
        "registry_file": str(config.registry_file),
    }


def _deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    """Recursively merge *override* into *base*, returning a new dict."""
    result = dict(base)
    for key, value in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            result[key] = _deep_merge(result[key], value)
        else:
            result[key] = value
    return result
