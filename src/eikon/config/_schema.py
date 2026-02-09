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

    Attributes
    ----------
    output_dir : Path
        Directory where exported figures are written.
    styles_dir : Path
        Directory containing user-defined style files.
    specs_dir : Path
        Directory containing YAML figure specifications.
    data_dir : Path
        Directory containing data sources for figures.
    """

    output_dir: Path = Path("figures")
    styles_dir: Path = Path("styles")
    specs_dir: Path = Path("specs")
    data_dir: Path = Path("data")


@dataclass(frozen=True, kw_only=True, slots=True)
class ExportDefaults:
    """Default export settings applied to all figures unless overridden.

    Attributes
    ----------
    formats : tuple[ExportFormat, ...]
        File formats to export.
    dpi : int
        Resolution in dots per inch.
    transparent : bool
        Whether to export with a transparent background.
    bbox_inches : str
        Bounding box setting passed to ``matplotlib.figure.Figure.savefig``.
    pad_inches : float
        Padding around the figure when using ``bbox_inches='tight'``.
    metadata : dict[str, str]
        Metadata fields injected into exported files.
    """

    formats: tuple[ExportFormat, ...] = (ExportFormat.PDF,)
    dpi: int = 300
    transparent: bool = False
    bbox_inches: str = "tight"
    pad_inches: float = 0.1
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, kw_only=True, slots=True)
class StyleDefaults:
    """Default style settings applied to all figures unless overridden.

    Attributes
    ----------
    base_style : str
        Name of the base matplotlib or eikon style preset.
    font_family : str
        Font family name.
    font_size : float
        Base font size in points.
    figure_size : tuple[float, float]
        Default figure dimensions ``(width, height)`` in inches.
    """

    base_style: str = "default"
    font_family: str = "serif"
    font_size: float = 10.0
    figure_size: tuple[float, float] = (6.4, 4.8)


@dataclass(frozen=True, kw_only=True, slots=True)
class ProjectConfig:
    """Top-level project configuration, composed from section dataclasses.

    Attributes
    ----------
    paths : PathsConfig
        Directory layout for the project.
    export : ExportDefaults
        Default export settings.
    style : StyleDefaults
        Default style settings.
    registry_file : Path
        Path to the figure registry manifest, relative to project root.
    """

    paths: PathsConfig = field(default_factory=PathsConfig)
    export: ExportDefaults = field(default_factory=ExportDefaults)
    style: StyleDefaults = field(default_factory=StyleDefaults)
    registry_file: Path = Path("eikon-registry.yaml")
