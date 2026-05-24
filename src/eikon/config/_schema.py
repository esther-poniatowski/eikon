"""Dataclass schemas for project configuration.

All configuration sections are modeled as frozen, keyword-only dataclasses
with sensible defaults.  They are composed into :class:`ProjectConfig`,
the top-level configuration object.
"""

from dataclasses import dataclass, field
from pathlib import Path

from eikon._types import ExportFormat

__all__ = [
    "PathsConfig",
    "ExportDefaults",
    "StyleDefaults",
    "ProjectConfig",
]


@dataclass(frozen=True, kw_only=True, slots=True)
class PathsConfig:
    """Configurable directory paths, stored relative to the project root.
    """

    output_dir: Path = Path("figures")
    """Directory where exported figures are written."""
    styles_dir: Path = Path("styles")
    """Directory containing user-defined style files."""
    specs_dir: Path = Path("specs")
    """Directory containing YAML figure specifications."""
    data_dir: Path = Path("data")
    """Directory containing data sources for figures."""


@dataclass(frozen=True, kw_only=True, slots=True)
class ExportDefaults:
    """Default export settings applied to all figures unless overridden.
    """

    formats: tuple[ExportFormat, ...] = (ExportFormat.PDF,)
    """File formats to export."""
    dpi: int = 300
    """Resolution in dots per inch."""
    transparent: bool = False
    """Whether to export with a transparent background."""
    bbox_inches: str = "tight"
    """Bounding box setting passed to ``matplotlib.figure.Figure.savefig``."""
    pad_inches: float = 0.1
    """Padding around the figure when using ``bbox_inches='tight'``."""
    metadata: dict[str, str] = field(default_factory=dict)
    """Metadata fields injected into exported files."""


@dataclass(frozen=True, kw_only=True, slots=True)
class StyleDefaults:
    """Default style settings applied to all figures unless overridden.
    """

    base_style: str = "default"
    """Name of the base matplotlib or eikon style preset."""
    font_family: str = "sans-serif"
    """Font family name."""
    font_size: float = 10.0
    """Base font size in points."""
    figure_size: tuple[float, float] = (6.4, 4.8)
    """Default figure dimensions ``(width, height)`` in inches."""


@dataclass(frozen=True, kw_only=True, slots=True)
class ProjectConfig:
    """Top-level project configuration, composed from section dataclasses.
    """

    paths: PathsConfig = field(default_factory=PathsConfig)
    """Directory layout for the project."""
    export: ExportDefaults = field(default_factory=ExportDefaults)
    """Default export settings."""
    style: StyleDefaults = field(default_factory=StyleDefaults)
    """Default style settings."""
    registry_file: Path = Path("eikon-registry.yaml")
    """Path to the figure registry manifest, relative to project root."""
