"""Parse figure specifications from YAML files or dictionaries.

Converts raw dictionaries (typically loaded from YAML) into validated
:class:`FigureSpec` instances.
"""

from pathlib import Path
from typing import Any

import yaml

from eikon.config._validation import validate_figure_spec
from eikon.exceptions import ConfigError, SpecValidationError
from eikon.spec._data import DataBinding
from eikon.spec._figure import FigureSpec
from eikon.spec._panel import PanelSpec

__all__ = ["parse_figure_spec", "parse_figure_file"]


def parse_figure_file(path: Path) -> FigureSpec:
    """Load and parse a figure specification from a YAML file.

    Parameters
    ----------
    path : Path
        Path to the YAML file.

    Returns
    -------
    FigureSpec
        Parsed and validated figure specification.

    Raises
    ------
    ConfigError
        If the file cannot be read or parsed.
    SpecValidationError
        If the specification fails validation.
    """
    path = Path(path).resolve()
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, yaml.YAMLError) as exc:
        raise ConfigError(f"Failed to load figure spec from {path}: {exc}") from exc

    if not isinstance(raw, dict):
        raise ConfigError(f"Expected a YAML mapping in {path}, got {type(raw).__name__}.")

    return parse_figure_spec(raw)


def parse_figure_spec(raw: dict[str, Any]) -> FigureSpec:
    """Parse a figure specification from a dictionary.

    Parameters
    ----------
    raw : dict
        Dictionary representation of a figure specification.

    Returns
    -------
    FigureSpec
        Parsed and validated figure specification.

    Raises
    ------
    SpecValidationError
        If the specification fails validation.
    """
    errors = validate_figure_spec(raw)
    if errors:
        raise SpecValidationError(errors)

    panels = tuple(_build_panel(p) for p in raw.get("panels", []))

    return FigureSpec(
        name=raw["name"],
        title=raw.get("title", ""),
        tags=tuple(raw.get("tags", [])),
        group=raw.get("group", ""),
        panels=panels,
        layout=raw.get("layout"),
        style=raw.get("style"),
        export=raw.get("export"),
        metadata=dict(raw.get("metadata", {})),
    )


def _build_panel(raw: dict[str, Any]) -> PanelSpec:
    """Construct a :class:`PanelSpec` from a raw dictionary."""
    data = _build_data_binding(raw["data"]) if "data" in raw else None

    row = raw.get("row", 0)
    if isinstance(row, list):
        row = tuple(row)

    col = raw.get("col", 0)
    if isinstance(col, list):
        col = tuple(col)

    return PanelSpec(
        name=raw["name"],
        plot_type=raw["plot_type"],
        data=data,
        row=row,
        col=col,
        style=raw.get("style"),
        params=dict(raw.get("params", {})),
        label=raw.get("label", ""),
        auto_size=bool(raw.get("auto_size", False)),
    )


def _build_data_binding(raw: dict[str, Any]) -> DataBinding:
    """Construct a :class:`DataBinding` from a raw dictionary."""
    return DataBinding(
        source=raw.get("source", ""),
        x=raw.get("x", ""),
        y=raw.get("y", ""),
        hue=raw.get("hue", ""),
        transforms=tuple(raw.get("transforms", [])),
        params=dict(raw.get("params", {})),
    )
