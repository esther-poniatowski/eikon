"""Export configuration dataclasses.

:class:`ExportSpec` holds per-figure export overrides.
:class:`ResolvedExportConfig` is the fully resolved configuration with no
``None`` values, produced by merging ``ExportSpec`` on top of
``ExportDefaults`` from the project configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Literal

from eikon._types import ExportFormat
from eikon.config._schema import ExportDefaults

__all__ = ["ExportSpec", "ResolvedExportConfig", "resolve_export_config"]


@dataclass(frozen=True, kw_only=True, slots=True)
class ExportSpec:
    """Per-figure export overrides.

    Any ``None`` field inherits the project-level default.

    Attributes
    ----------
    formats : tuple[str, ...] | None
        Format names (e.g. ``("pdf", "svg")``).
    dpi : int | None
        Resolution in dots per inch.
    transparent : bool | None
        Export with transparent background.
    filename_template : str | None
        Template for output filename.  Variables: ``{name}``, ``{group}``,
        ``{date}``, ``{format}``.
    subdirectory : str | None
        Subdirectory under the output dir (e.g. a group folder).
    collision : Literal["overwrite", "increment", "fail"] | None
        How to handle existing files at the export path.
    metadata : dict[str, str] | None
        Additional metadata to inject into exported files.
    """

    formats: tuple[str, ...] | None = None
    dpi: int | None = None
    transparent: bool | None = None
    filename_template: str | None = None
    subdirectory: str | None = None
    collision: Literal["overwrite", "increment", "fail"] | None = None
    metadata: dict[str, str] | None = None


@dataclass(frozen=True, kw_only=True, slots=True)
class ResolvedExportConfig:
    """Fully resolved export configuration — no optional fields.

    Attributes
    ----------
    formats : tuple[ExportFormat, ...]
        Export file formats.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        Transparent background flag.
    bbox_inches : str
        Bounding box setting for ``savefig``.
    pad_inches : float
        Padding around the figure.
    filename_template : str
        Template for output filenames.
    subdirectory : str
        Subdirectory under the output dir.
    collision : str
        Collision strategy: ``"overwrite"``, ``"increment"``, or ``"fail"``.
    metadata : dict[str, str]
        Metadata injected into exported files.
    """

    formats: tuple[ExportFormat, ...]
    dpi: int
    transparent: bool
    bbox_inches: str
    pad_inches: float
    filename_template: str
    subdirectory: str
    collision: str
    metadata: dict[str, str] = field(default_factory=dict)


def resolve_export_config(
    defaults: ExportDefaults,
    spec_export: ExportSpec | None = None,
    cli_formats: tuple[str, ...] = (),
) -> ResolvedExportConfig:
    """Merge per-figure overrides on top of project defaults.

    Parameters
    ----------
    defaults : ExportDefaults
        Project-level export settings.
    spec_export : ExportSpec, optional
        Per-figure overrides.
    cli_formats : tuple[str, ...]
        Format names from CLI flags (highest priority).

    Returns
    -------
    ResolvedExportConfig
        Fully resolved configuration.
    """
    override = spec_export or ExportSpec()

    # Format resolution: CLI > spec > project default
    if cli_formats:
        formats = tuple(ExportFormat.from_string(f) for f in cli_formats)
    elif override.formats is not None:
        formats = tuple(ExportFormat.from_string(f) for f in override.formats)
    else:
        formats = defaults.formats

    return ResolvedExportConfig(
        formats=formats,
        dpi=override.dpi if override.dpi is not None else defaults.dpi,
        transparent=(
            override.transparent
            if override.transparent is not None
            else defaults.transparent
        ),
        bbox_inches=defaults.bbox_inches,
        pad_inches=defaults.pad_inches,
        filename_template=override.filename_template or "{name}",
        subdirectory=override.subdirectory or "",
        collision=override.collision or "overwrite",
        metadata={**defaults.metadata, **(override.metadata or {})},
    )
