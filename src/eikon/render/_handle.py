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

    def save(
        self,
        path: str | Path,
        *,
        dpi: int = 300,
        bbox_inches: str = "tight",
        close: bool = True,
        **kwargs: Any,
    ) -> Path:
        """Save the figure to a file and optionally close it.

        Parameters
        ----------
        path : str | Path
            Destination file path (e.g. ``"output/fig.pdf"``).
            Parent directories are created automatically.
        dpi : int
            Resolution in dots per inch.
        bbox_inches : str
            Bounding-box option forwarded to
            :meth:`matplotlib.figure.Figure.savefig`.
        close : bool
            Whether to close the figure after saving (default ``True``).
        **kwargs
            Extra keyword arguments forwarded to ``savefig``.

        Returns
        -------
        Path
            The resolved output path.
        """
        path = Path(path)
        path.parent.mkdir(parents=True, exist_ok=True)
        self.figure.savefig(path, dpi=dpi, bbox_inches=bbox_inches, **kwargs)
        if close:
            self.close()
        return path

    def close(self) -> None:
        """Close the matplotlib Figure to free memory."""
        import matplotlib.pyplot as plt

        plt.close(self.figure)
