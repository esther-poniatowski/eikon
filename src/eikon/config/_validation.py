"""Schema validation for raw configuration dictionaries.

Validates YAML-loaded dicts before they are converted into typed
dataclasses, producing descriptive error messages.
"""

from pathlib import Path
from typing import Any

from eikon._types import ExportFormat

__all__ = ["validate_config", "validate_figure_spec"]

# --- Helpers ---

CURRENT_CONFIG_VERSION = 1
CURRENT_SPEC_VERSION = 1

_VALID_CONFIG_SECTIONS = {"config_version", "paths", "export", "style", "registry_file"}
_VALID_PATHS_KEYS = {"output_dir", "styles_dir", "specs_dir", "data_dir"}
_VALID_EXPORT_KEYS = {
    "formats", "dpi", "transparent", "bbox_inches", "pad_inches", "metadata",
}
_VALID_STYLE_KEYS = {"base_style", "font_family", "font_size", "figure_size"}


def _check_unknown_keys(
    data: dict[str, Any],
    valid: set[str],
    section: str,
) -> list[str]:
    """Return warnings for unrecognized keys."""
    unknown = set(data.keys()) - valid
    return [f"Unknown key '{k}' in {section}" for k in sorted(unknown)]


def _check_type(
    value: Any,
    expected: type | tuple[type, ...],
    name: str,
) -> list[str]:
    """Return an error if *value* is not of the expected type."""
    if not isinstance(value, expected):
        return [f"'{name}' must be {expected}, got {type(value).__name__}"]
    return []


# --- Public API ---


def validate_config(raw: dict[str, Any]) -> list[str]:
    """Validate a raw project configuration dictionary.

    Parameters
    ----------
    raw : dict
        Dictionary loaded from ``eikon.yaml``.

    Returns
    -------
    list[str]
        Validation error messages.  Empty list means valid.
    """
    errors: list[str] = []

    if not isinstance(raw, dict):
        return ["Configuration must be a YAML mapping (dict)."]

    # --- schema version ---
    if "config_version" in raw:
        ver = raw["config_version"]
        if not isinstance(ver, int):
            errors.append("'config_version' must be an integer.")
        elif ver > CURRENT_CONFIG_VERSION:
            errors.append(
                f"'config_version' {ver} is newer than supported "
                f"({CURRENT_CONFIG_VERSION}). Please upgrade eikon."
            )

    errors.extend(_check_unknown_keys(raw, _VALID_CONFIG_SECTIONS, "config root"))

    # --- paths ---
    if "paths" in raw:
        paths = raw["paths"]
        if not isinstance(paths, dict):
            errors.append("'paths' must be a mapping.")
        else:
            errors.extend(_check_unknown_keys(paths, _VALID_PATHS_KEYS, "paths"))
            for key in _VALID_PATHS_KEYS:
                if key in paths:
                    val = paths[key]
                    if not isinstance(val, str):
                        errors.append(f"'paths.{key}' must be a string, got {type(val).__name__}")
                    elif Path(val).is_absolute():
                        errors.append(
                            f"'paths.{key}' must be a relative path, got absolute: {val!r}"
                        )

    # --- export ---
    if "export" in raw:
        export = raw["export"]
        if not isinstance(export, dict):
            errors.append("'export' must be a mapping.")
        else:
            errors.extend(_check_unknown_keys(export, _VALID_EXPORT_KEYS, "export"))
            if "formats" in export:
                fmts = export["formats"]
                if not isinstance(fmts, list):
                    errors.append("'export.formats' must be a list.")
                else:
                    for fmt in fmts:
                        try:
                            ExportFormat.from_string(str(fmt))
                        except ValueError:
                            errors.append(f"Invalid export format: {fmt!r}")
            if "dpi" in export:
                errors.extend(_check_type(export["dpi"], (int, float), "export.dpi"))
                if isinstance(export["dpi"], (int, float)) and export["dpi"] <= 0:
                    errors.append("'export.dpi' must be positive.")
            if "transparent" in export:
                errors.extend(_check_type(export["transparent"], bool, "export.transparent"))
            if "metadata" in export:
                errors.extend(_check_type(export["metadata"], dict, "export.metadata"))

    # --- style ---
    if "style" in raw:
        style = raw["style"]
        if not isinstance(style, dict):
            errors.append("'style' must be a mapping.")
        else:
            errors.extend(_check_unknown_keys(style, _VALID_STYLE_KEYS, "style"))
            if "font_size" in style:
                errors.extend(_check_type(style["font_size"], (int, float), "style.font_size"))
                if isinstance(style["font_size"], (int, float)) and style["font_size"] <= 0:
                    errors.append("'style.font_size' must be positive.")
            if "figure_size" in style:
                fs = style["figure_size"]
                if not isinstance(fs, (list, tuple)) or len(fs) != 2:
                    errors.append("'style.figure_size' must be a list of two numbers [w, h].")
                elif not all(isinstance(v, (int, float)) for v in fs):
                    errors.append("'style.figure_size' values must be numbers.")

    # --- registry_file ---
    if "registry_file" in raw:
        errors.extend(_check_type(raw["registry_file"], str, "registry_file"))

    return errors


def validate_figure_spec(raw: dict[str, Any]) -> list[str]:
    """Validate a raw figure specification dictionary.

    Parameters
    ----------
    raw : dict
        Dictionary loaded from a figure spec YAML file.

    Returns
    -------
    list[str]
        Validation error messages.  Empty list means valid.
    """
    errors: list[str] = []

    if not isinstance(raw, dict):
        return ["Figure specification must be a YAML mapping (dict)."]

    # --- schema version ---
    if "spec_version" in raw:
        ver = raw["spec_version"]
        if not isinstance(ver, int):
            errors.append("'spec_version' must be an integer.")
        elif ver > CURRENT_SPEC_VERSION:
            errors.append(
                f"'spec_version' {ver} is newer than supported "
                f"({CURRENT_SPEC_VERSION}). Please upgrade eikon."
            )

    if "name" not in raw:
        errors.append("'name' is required.")
    elif not isinstance(raw["name"], str) or not raw["name"].strip():
        errors.append("'name' must be a non-empty string.")

    if "panels" in raw:
        panels = raw["panels"]
        if not isinstance(panels, list):
            errors.append("'panels' must be a list.")
        else:
            for i, panel in enumerate(panels):
                if not isinstance(panel, dict):
                    errors.append(f"panels[{i}] must be a mapping.")
                    continue
                if "name" not in panel:
                    errors.append(f"panels[{i}]: 'name' is required.")
                if "plot_type" not in panel:
                    errors.append(f"panels[{i}]: 'plot_type' is required.")

    if "layout" in raw:
        layout = raw["layout"]
        if not isinstance(layout, dict):
            errors.append("'layout' must be a mapping.")
        else:
            for dim in ("rows", "cols"):
                if dim in layout:
                    val = layout[dim]
                    if not isinstance(val, int) or val < 1:
                        errors.append(f"'layout.{dim}' must be a positive integer.")

    # --- margin_labels ---
    if "margin_labels" in raw:
        ml = raw["margin_labels"]
        if not isinstance(ml, dict):
            errors.append("'margin_labels' must be a mapping.")
        else:
            valid_edges = {"top", "bottom", "left", "right"}
            for edge_key, edge_val in ml.items():
                if edge_key not in valid_edges:
                    errors.append(
                        f"'margin_labels' key {edge_key!r} is invalid; "
                        f"expected one of {sorted(valid_edges)}."
                    )
                if not isinstance(edge_val, dict):
                    errors.append(f"margin_labels[{edge_key!r}] must be a mapping.")
                    continue
                if "labels" not in edge_val:
                    errors.append(f"margin_labels[{edge_key!r}]: 'labels' is required.")
                else:
                    labels = edge_val["labels"]
                    if not isinstance(labels, (list, dict)):
                        errors.append(
                            f"margin_labels[{edge_key!r}].labels must be a list or mapping."
                        )
                if "target" in edge_val:
                    tgt = edge_val["target"]
                    if isinstance(tgt, dict):
                        kind = tgt.get("kind", "layout")
                        if kind == "virtual":
                            if "axes" not in tgt:
                                errors.append(
                                    f"margin_labels[{edge_key!r}].target: "
                                    "'axes' is required for virtual targets."
                                )
                            if "grid" not in tgt:
                                errors.append(
                                    f"margin_labels[{edge_key!r}].target: "
                                    "'grid' is required for virtual targets."
                                )
                if "label_styles" in edge_val:
                    ls = edge_val["label_styles"]
                    if not isinstance(ls, dict):
                        errors.append(
                            f"margin_labels[{edge_key!r}].label_styles must be a mapping."
                        )
                if "cell_range" in edge_val:
                    cr = edge_val["cell_range"]
                    if not isinstance(cr, (list, tuple)) or len(cr) != 2:
                        errors.append(
                            f"margin_labels[{edge_key!r}].cell_range must be "
                            "a list of two integers [start, end]."
                        )
                    elif not all(isinstance(v, int) for v in cr):
                        errors.append(
                            f"margin_labels[{edge_key!r}].cell_range values "
                            "must be integers."
                        )
                    elif cr[0] < 0 or cr[1] <= cr[0]:
                        errors.append(
                            f"margin_labels[{edge_key!r}].cell_range must "
                            "satisfy 0 <= start < end."
                        )

    return errors
