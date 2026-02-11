"""Parse figure specifications from YAML files or dictionaries.

Converts raw dictionaries (typically loaded from YAML) into validated
:class:`FigureSpec` instances.
"""

from pathlib import Path
from typing import Any

import yaml

from eikon.config._validation import validate_figure_spec
from eikon.exceptions import ConfigError, SpecValidationError
from eikon.layout._grid import LayoutSpec
from eikon.spec._data import DataBinding
from eikon.spec._figure import FigureSpec
from eikon.spec._margin_labels import MarginLabelSpec, MarginLabelStyle, MarginTarget
from eikon.spec._panel import PanelSpec

__all__ = ["parse_figure_file", "parse_figure_spec", "parse_layout_spec"]


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

    margin_labels = (
        _build_margin_labels(raw["margin_labels"])
        if "margin_labels" in raw
        else None
    )

    title_kwargs = dict(raw["title_kwargs"]) if "title_kwargs" in raw else None
    shared_legend = dict(raw["shared_legend"]) if "shared_legend" in raw else None

    return FigureSpec(
        name=raw["name"],
        title=raw.get("title", ""),
        tags=tuple(raw.get("tags", [])),
        group=raw.get("group", ""),
        panels=panels,
        layout=raw.get("layout"),
        style=raw.get("style"),
        export=raw.get("export"),
        title_kwargs=title_kwargs,
        shared_legend=shared_legend,
        margin_labels=margin_labels,
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

    hide_spines_raw = raw.get("hide_spines")
    hide_spines = tuple(hide_spines_raw) if hide_spines_raw is not None else None

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
        hide_spines=hide_spines,
    )


def _build_margin_labels(raw: dict[str, Any]) -> dict[str, MarginLabelSpec]:
    """Construct margin label specs from a raw YAML mapping."""
    result: dict[str, MarginLabelSpec] = {}
    for edge, edge_raw in raw.items():
        labels = _normalize_labels(edge_raw["labels"])

        style = _build_margin_style(edge_raw.get("style", {}))

        level_styles = None
        if "level_styles" in edge_raw:
            level_styles = tuple(
                _build_margin_style(ls) for ls in edge_raw["level_styles"]
            )

        label_styles = None
        if "label_styles" in edge_raw:
            label_styles = {
                text: _build_margin_style(s)
                for text, s in edge_raw["label_styles"].items()
            }

        target = MarginTarget()
        if "target" in edge_raw:
            tgt = edge_raw["target"]
            grid = None
            if "grid" in tgt:
                g = tgt["grid"]
                grid = (int(g[0]), int(g[1]))
            target = MarginTarget(
                kind=tgt.get("kind", "layout"),
                axes=tgt.get("axes"),
                grid=grid,
            )

        cell_range = None
        if "cell_range" in edge_raw:
            cr = edge_raw["cell_range"]
            cell_range = (int(cr[0]), int(cr[1]))

        result[edge] = MarginLabelSpec(
            labels=labels,
            style=style,
            level_styles=level_styles,
            target=target,
            strip_size=float(edge_raw.get("strip_size", 0.04)),
            pad=float(edge_raw.get("pad", 6.0)),
            gap=float(edge_raw.get("gap", 2.0)),
            zorder=float(edge_raw.get("zorder", 2.1)),
            label_styles=label_styles,
            cell_range=cell_range,
        )
    return result


def _normalize_labels(raw: Any) -> Any:
    """Normalize YAML-loaded labels: convert lists to tuples recursively."""
    if isinstance(raw, list):
        return tuple(raw)
    if isinstance(raw, dict):
        return {k: _normalize_labels(v) if v is not None else None for k, v in raw.items()}
    return raw


def _build_margin_style(raw: dict[str, Any]) -> MarginLabelStyle:
    """Construct a MarginLabelStyle from a raw dictionary."""
    rotation = raw.get("rotation")
    if rotation is not None:
        rotation = float(rotation)
    return MarginLabelStyle(
        bg_color=raw.get("bg_color"),
        text_color=raw.get("text_color", "black"),
        fontsize=float(raw.get("fontsize", 8.0)),
        fontweight=raw.get("fontweight", "normal"),
        rotation=rotation,
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


def parse_layout_spec(raw: dict[str, Any]) -> LayoutSpec:
    """Convert a raw layout dictionary to a :class:`LayoutSpec`.

    Parameters
    ----------
    raw : dict
        Dictionary representation of a layout specification, typically
        from the ``layout`` key of a figure YAML file.

    Returns
    -------
    LayoutSpec
        Parsed layout specification.
    """
    kwargs: dict[str, Any] = {}
    if "rows" in raw:
        kwargs["rows"] = int(raw["rows"])
    if "cols" in raw:
        kwargs["cols"] = int(raw["cols"])
    if "width_ratios" in raw:
        kwargs["width_ratios"] = tuple(float(r) for r in raw["width_ratios"])
    if "height_ratios" in raw:
        kwargs["height_ratios"] = tuple(float(r) for r in raw["height_ratios"])
    if "wspace" in raw:
        kwargs["wspace"] = float(raw["wspace"])
    if "hspace" in raw:
        kwargs["hspace"] = float(raw["hspace"])
    if "constrained_layout" in raw:
        kwargs["constrained_layout"] = bool(raw["constrained_layout"])
    return LayoutSpec(**kwargs)
