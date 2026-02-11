"""Example 1: Single-panel figure rendered programmatically.

This script demonstrates the simplest use case — creating a single-panel
figure using eikon's Python API.

Usage::

    python examples/01_single_panel.py
"""

import eikon

spec = eikon.FigureSpec(
    name="single-panel",
    title="Simple Line Plot",
    panels=(
        eikon.PanelSpec(name="main", plot_type="line"),
    ),
    style="publication",
)

handle = eikon.render(spec)
handle.show()
