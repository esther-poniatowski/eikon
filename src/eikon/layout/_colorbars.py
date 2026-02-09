"""Colorbar attachment for layout panels.

Provides a constrained-layout-aware helper to attach a colorbar to a
specific panel in a built layout.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from matplotlib.cm import ScalarMappable

    from eikon.layout._builder import BuiltLayout

from eikon.exceptions import LayoutError

__all__ = ["add_colorbar"]


def add_colorbar(
    built: BuiltLayout,
    panel_name: str,
    mappable: ScalarMappable,
    *,
    position: str = "right",
    size: str = "5%",
    pad: float = 0.05,
    **kwargs: Any,
) -> Any:
    """Attach a colorbar to a panel in the built layout.

    Uses ``fig.colorbar`` which is compatible with constrained layout.

    Parameters
    ----------
    built : BuiltLayout
        A built layout containing the figure and axes dict.
    panel_name : str
        Name of the panel to attach the colorbar to.
    mappable : ScalarMappable
        The matplotlib mappable (e.g. ``AxesImage``) to draw the colorbar for.
    position : str
        Location: ``"right"``, ``"left"``, ``"top"``, or ``"bottom"``.
    size : str
        Colorbar width as a percentage string (e.g. ``"5%"``).
    pad : float
        Padding between the axes and colorbar.
    **kwargs
        Additional keyword arguments passed to ``fig.colorbar``.

    Returns
    -------
    Colorbar
        The created matplotlib colorbar.

    Raises
    ------
    LayoutError
        If *panel_name* is not found in the built layout.
    """
    if panel_name not in built.axes:
        raise LayoutError(f"Panel {panel_name!r} not found in built layout.")

    ax = built.axes[panel_name]
    return built.figure.colorbar(
        mappable,
        ax=ax,
        location=position,
        fraction=_parse_fraction(size),
        pad=pad,
        **kwargs,
    )


def _parse_fraction(size: str) -> float:
    """Convert a percentage string like ``"5%"`` to a fraction."""
    if size.endswith("%"):
        return float(size[:-1]) / 100.0
    return float(size)
