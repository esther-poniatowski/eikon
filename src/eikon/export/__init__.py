"""Export pipeline for eikon figures.

Handles saving rendered figures to various file formats (PDF, SVG, PNG)
with configurable paths, metadata injection, and filename sanitization.

Public API
----------
ExportSpec
    Per-figure export overrides.
ResolvedExportConfig
    Fully resolved export configuration.
resolve_export_config
    Merge per-figure overrides with project defaults.
batch_export
    Export a figure to all configured formats.
build_export_path
    Build the output path for a single format.
sanitize_filename
    Ensure filenames are cross-platform safe.
"""

from eikon.export._batch import batch_export, parse_export_spec
from eikon.export._config import ExportSpec, ResolvedExportConfig, resolve_export_config
from eikon.export._handlers import export_figure
from eikon.export._paths import build_export_path
from eikon.export._sanitize import sanitize_filename

__all__ = [
    "ExportSpec",
    "ResolvedExportConfig",
    "batch_export",
    "build_export_path",
    "export_figure",
    "parse_export_spec",
    "resolve_export_config",
    "sanitize_filename",
]
