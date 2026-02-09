"""Batch export across multiple figures and formats.

The :func:`batch_export` function exports a rendered figure to all
configured formats, returning a mapping of format names to file paths.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from eikon.config._schema import ExportDefaults
from eikon.exceptions import ExportError
from eikon.export._config import ExportSpec, resolve_export_config
from eikon.export._handlers import export_figure
from eikon.export._paths import build_export_path
from eikon.ext._hooks import HookName, fire_hook

__all__ = ["batch_export"]


def batch_export(
    *,
    figure: Any,
    name: str,
    group: str = "",
    output_dir: Path,
    export_defaults: ExportDefaults,
    export_spec: ExportSpec | None = None,
    cli_formats: tuple[str, ...] = (),
) -> dict[str, Path]:
    """Export a rendered figure to all configured formats.

    Parameters
    ----------
    figure : Figure
        The matplotlib Figure to export.
    name : str
        Figure name (used for filename construction).
    group : str
        Figure group name.
    output_dir : Path
        Base output directory.
    export_defaults : ExportDefaults
        Project-level export settings.
    export_spec : ExportSpec, optional
        Per-figure export overrides.
    cli_formats : tuple[str, ...]
        Format names from CLI flags (highest priority).

    Returns
    -------
    dict[str, Path]
        Mapping of format name (lowercase) to exported file path.

    Raises
    ------
    ExportError
        If any export operation fails.
    """
    resolved = resolve_export_config(export_defaults, export_spec, cli_formats)

    if not resolved.formats:
        return {}

    paths: dict[str, Path] = {}

    for fmt in resolved.formats:
        try:
            path = build_export_path(
                name=name,
                fmt=fmt,
                output_dir=output_dir,
                filename_template=resolved.filename_template,
                subdirectory=resolved.subdirectory,
                group=group,
                collision=resolved.collision,
            )

            fire_hook(HookName.PRE_EXPORT, figure=figure, path=path, format=fmt)
            export_figure(figure, path, fmt, resolved)
            fire_hook(HookName.POST_EXPORT, figure=figure, path=path, format=fmt)

            paths[fmt.value] = path
        except ExportError:
            raise
        except Exception as exc:
            msg = f"Export to {fmt.value} failed for {name!r}: {exc}"
            raise ExportError(msg) from exc

    return paths


def parse_export_spec(raw: dict[str, Any] | None) -> ExportSpec | None:
    """Parse an export spec from a raw dict (e.g. from YAML).

    Parameters
    ----------
    raw : dict or None
        Raw export dict from a figure specification.

    Returns
    -------
    ExportSpec or None
        Parsed spec, or ``None`` if input is empty.
    """
    if not raw:
        return None

    kwargs: dict[str, Any] = {}
    if "formats" in raw:
        kwargs["formats"] = tuple(str(f) for f in raw["formats"])
    if "dpi" in raw:
        kwargs["dpi"] = int(raw["dpi"])
    if "transparent" in raw:
        kwargs["transparent"] = bool(raw["transparent"])
    if "filename_template" in raw:
        kwargs["filename_template"] = str(raw["filename_template"])
    if "subdirectory" in raw:
        kwargs["subdirectory"] = str(raw["subdirectory"])
    if "collision" in raw:
        kwargs["collision"] = str(raw["collision"])
    if "metadata" in raw:
        kwargs["metadata"] = dict(raw["metadata"])

    return ExportSpec(**kwargs) if kwargs else None
