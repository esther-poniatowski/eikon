"""Example 4: Register and use a custom plot type.

Shows how to extend eikon with a custom plot function using the
``@plot_type`` decorator and render it via the standard pipeline.

Usage::

    python examples/04_custom_plot_type.py
"""

import numpy as np

import eikon
from eikon.ext import plot_type


@plot_type("sine_wave")
def sine_wave(ax, periods=2, color="steelblue", **kwargs):
    """Plot a sine wave with configurable periods."""
    x = np.linspace(0, 2 * np.pi * periods, 500)
    y = np.sin(x)
    ax.plot(x, y, color=color, linewidth=1.5, label=f"{periods} periods")
    ax.set_xlabel("x")
    ax.set_ylabel("sin(x)")
    ax.legend()


spec = eikon.FigureSpec(
    name="custom-plot",
    title="Custom Plot Type: Sine Wave",
    panels=(
        eikon.PanelSpec(
            name="A",
            plot_type="sine_wave",
            params={"periods": 3, "color": "coral"},
            hide_spines=("top", "right"),
        ),
    ),
    style="publication",
)

handle = eikon.render(spec)
handle.show()
