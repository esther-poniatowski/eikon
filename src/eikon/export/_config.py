"""Export configuration dataclasses.

:class:`ExportSpec` holds per-figure export overrides.
:class:`ResolvedExportConfig` is the fully resolved configuration with no
``None`` values, produced by merging ``ExportSpec`` on top of
``ExportDefaults`` from the project configuration.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import StrEnum

from eikon._types import ExportFormat
from eikon.config._schema import ExportDefaults

__all__ = [
    "CollisionMode",
    "ExportSpec",
    "ResolvedExportConfig",
    "parse_collision_mode",
    "resolve_export_config",
]


class CollisionMode(StrEnum):
    """Closed set of export collision policies."""

    OVERWRITE = "overwrite"
    INCREMENT = "increment"
    FAIL = "fail"


def parse_collision_mode(value: str | CollisionMode) -> CollisionMode:
    """Normalize and validate a collision policy value."""
    if isinstance(value, CollisionMode):
        return value
    normalized = str(value).strip().lower()
    try:
        return CollisionMode(normalized)
    except ValueError as exc:
        valid = ", ".join(mode.value for mode in CollisionMode)
        raise ValueError(f"Unknown collision mode {value!r}. Expected one of: {valid}.") from exc


@dataclass(frozen=True, kw_only=True, slots=True)
class ExportSpec:
    """Per-figure export overrides.

    Any ``None`` field inherits the project-level default.
    """

    formats: tuple[str, ...] | None = None
    """Format names (e.g. ``("pdf", "svg")``)."""
    dpi: int | None = None
    """Resolution in dots per inch."""
    transparent: bool | None = None
    """Export with transparent background."""
    filename_template: str | None = None
    """Template for output filename using ``{name}``, ``{group}``,
    ``{date}``, ``{format}``.
    """
    subdirectory: str | None = None
    """Subdirectory under the output dir (e.g. a group folder)."""
    collision: CollisionMode | None = None
    """How to handle existing files at the export path."""
    metadata: dict[str, str] | None = None
    """Additional metadata to inject into exported files."""


@dataclass(frozen=True, kw_only=True, slots=True)
class ResolvedExportConfig:
    """Fully resolved export configuration — no optional fields.
    """

    formats: tuple[ExportFormat, ...]
    """Export file formats."""
    dpi: int
    """Resolution in dots per inch."""
    transparent: bool
    """Transparent background flag."""
    bbox_inches: str
    """Bounding box setting for ``savefig``."""
    pad_inches: float
    """Padding around the figure."""
    filename_template: str
    """Template for output filenames."""
    subdirectory: str
    """Subdirectory under the output dir."""
    collision: CollisionMode
    """Collision policy, either ``"overwrite"``, ``"increment"``, or ``"fail"``."""
    metadata: dict[str, str] = field(default_factory=dict)
    """Metadata injected into exported files."""


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
        collision=parse_collision_mode(override.collision or CollisionMode.OVERWRITE),
        metadata={**defaults.metadata, **(override.metadata or {})},
    )
