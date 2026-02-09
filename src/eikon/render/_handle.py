"""FigureHandle — lightweight wrapper around a rendered figure.

A :class:`FigureHandle` is the primary return type of
:func:`render_figure` and the convenience ``eikon.render()`` function.
It provides access to the figure, spec, layout, and export paths
without requiring the user to manage matplotlib or filesystem details.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

__all__ = ["FigureHandle"]


@dataclass(kw_only=True, slots=True)
class FigureHandle:
    """Result of rendering a figure.

    Attributes
    ----------
    spec : Any
        The :class:`FigureSpec` that was rendered.
    figure : Any
        The matplotlib ``Figure`` object.
    axes : dict[str, Any]
        Panel-name-to-``Axes`` mapping.
    export_paths : dict[str, Path]
        Format-to-path mapping of exported files (empty if not exported).
    """

    spec: Any
    figure: Any
    axes: dict[str, Any] = field(default_factory=dict)
    export_paths: dict[str, Path] = field(default_factory=dict)

    def show(self) -> None:
        """Display the figure interactively via ``plt.show()``."""
        import matplotlib.pyplot as plt

        plt.show()

    def path(self, fmt: str) -> Path | None:
        """Return the export path for a given format, or ``None``.

        Parameters
        ----------
        fmt : str
            Export format key (e.g. ``"pdf"``, ``"svg"``).
        """
        return self.export_paths.get(fmt.lower())

    def close(self) -> None:
        """Close the matplotlib Figure to free memory."""
        import matplotlib.pyplot as plt

        plt.close(self.figure)
