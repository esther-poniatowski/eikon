"""Example 2: Multi-panel figure with a shared legend.

Demonstrates a 2x2 grid layout with per-panel styles, hidden spines,
and a single shared legend.

Usage::

    python examples/02_multi_panel.py
"""

import eikon

spec = eikon.FigureSpec(
    name="multi-panel",
    title="Multi-Panel Demo",
    title_kwargs={"fontsize": 14, "y": 0.95},
    shared_legend={"loc": "upper right"},
    panels=(
        eikon.PanelSpec(
            name="A",
            plot_type="line",
            row=0,
            col=0,
            label="(a) Line",
            hide_spines=("top", "right"),
        ),
        eikon.PanelSpec(
            name="B",
            plot_type="scatter",
            row=0,
            col=1,
            label="(b) Scatter",
            hide_spines=("top", "right"),
        ),
        eikon.PanelSpec(
            name="C",
            plot_type="bar",
            row=1,
            col=0,
            label="(c) Bar",
            hide_spines=("top", "right"),
        ),
        eikon.PanelSpec(
            name="D",
            plot_type="line",
            row=1,
            col=1,
            label="(d) Line 2",
            hide_spines=("top", "right"),
        ),
    ),
    layout={"rows": 2, "cols": 2, "hspace": 0.35, "wspace": 0.3},
    style="publication",
)

handle = eikon.render(spec)
handle.show()
