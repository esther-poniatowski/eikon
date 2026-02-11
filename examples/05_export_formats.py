"""Example 5: Export a figure to multiple formats.

Demonstrates rendering a figure and exporting it to PDF, PNG, and SVG
formats in a temporary directory.

Usage::

    python examples/05_export_formats.py
"""

import tempfile
from pathlib import Path

from eikon.config._defaults import DEFAULT_CONFIG
from eikon.config._resolver import resolve_paths
from eikon.render._pipeline import render_figure
from eikon.spec._figure import FigureSpec
from eikon.spec._panel import PanelSpec

spec = FigureSpec(
    name="exported-figure",
    title="Multi-Format Export",
    panels=(
        PanelSpec(
            name="A",
            plot_type="line",
            label="(a)",
            hide_spines=("top", "right"),
        ),
    ),
    style="publication",
)

with tempfile.TemporaryDirectory() as tmpdir:
    root = Path(tmpdir)
    paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=root)
    paths.output_dir.mkdir(parents=True, exist_ok=True)

    handle = render_figure(
        spec,
        config=DEFAULT_CONFIG,
        resolved_paths=paths,
        formats=("pdf", "png", "svg"),
    )

    print("Exported files:")
    for fmt, path in handle.export_paths.items():
        size = Path(path).stat().st_size
        print(f"  {fmt}: {path} ({size:,} bytes)")
