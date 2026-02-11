"""Example 3: Render a figure from a YAML spec file.

Demonstrates loading a figure specification from YAML and rendering it.
Creates a temporary spec file for the demo.

Usage::

    python examples/03_yaml_spec.py
"""

import tempfile
from pathlib import Path

from eikon.render._pipeline import render_figure
from eikon.spec._parse import parse_figure_file

# Create a temporary YAML spec
yaml_content = """\
name: yaml-demo
title: "Figure from YAML"
panels:
  - name: A
    plot_type: line
    row: 0
    col: 0
    label: "(a)"
    hide_spines: [top, right]
  - name: B
    plot_type: scatter
    row: 0
    col: 1
    label: "(b)"
    hide_spines: [top, right]
layout:
  rows: 1
  cols: 2
  width_ratios: [2.0, 1.0]
style: publication
"""

with tempfile.TemporaryDirectory() as tmpdir:
    spec_path = Path(tmpdir) / "demo.yaml"
    spec_path.write_text(yaml_content, encoding="utf-8")

    spec = parse_figure_file(spec_path)
    handle = render_figure(spec)
    handle.show()
