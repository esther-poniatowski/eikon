"""Panel drawing dispatch — route draw calls to registered plot functions.

This module connects the rendering pipeline to the extension registry:
for each panel, it looks up the registered plot function by
``PanelSpec.plot_type`` and invokes it on the corresponding ``Axes``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from eikon.ext._plot_types import get_plot_type
from eikon.ext._registry import ExtensionRegistry
from eikon.render._data import resolve_data_binding
from eikon.spec._panel import PanelSpec

__all__ = ["draw_panel", "draw_all_panels"]


def draw_panel(
    ax: Any,
    panel: PanelSpec,
    *,
    data_dir: Path,
    extensions: ExtensionRegistry | None = None,
) -> None:
    """Draw a single panel using its registered plot function.

    Parameters
    ----------
    ax : Axes
        The matplotlib Axes to draw into.
    panel : PanelSpec
        The panel specification containing plot_type and params.

    Raises
    ------
    UnknownPlotTypeError
        If the panel's ``plot_type`` is not registered.
    """
    plot_fn = extensions.get_plot_type(panel.plot_type) if extensions else get_plot_type(panel.plot_type)

    data_kwargs = {}
    if panel.data is not None:
        data_kwargs = resolve_data_binding(panel.data, data_dir, extensions=extensions)

    plot_fn(ax, **data_kwargs, **panel.params)


def draw_all_panels(
    axes: dict[str, Any],
    panels: tuple[PanelSpec, ...],
    *,
    data_dir: Path,
    extensions: ExtensionRegistry | None = None,
) -> None:
    """Draw all panels into their corresponding axes.

    Parameters
    ----------
    axes : dict[str, Axes]
        Panel-name-to-Axes mapping from :class:`BuiltLayout`.
    panels : tuple[PanelSpec, ...]
        Panel specifications to draw.
    """
    for panel in panels:
        if panel.name in axes:
            draw_panel(axes[panel.name], panel, data_dir=data_dir, extensions=extensions)
