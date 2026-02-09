"""Protocol definitions for rendering extensibility.

All rendering extension points are defined as :class:`~typing.Protocol`
classes — any callable matching the signature works, with no base-class
registration required.
"""

from __future__ import annotations

from typing import Any, Protocol, runtime_checkable

__all__ = ["PlotFunction", "FigurePostProcessor", "DataTransform"]


@runtime_checkable
class PlotFunction(Protocol):
    """Protocol for a function that draws into a matplotlib Axes.

    Parameters
    ----------
    ax : Axes
        The matplotlib Axes to draw into.
    **kwargs : Any
        Keyword arguments from ``PanelSpec.params`` and resolved data.
    """

    def __call__(self, ax: Any, /, **kwargs: Any) -> None: ...


@runtime_checkable
class FigurePostProcessor(Protocol):
    """Protocol for a post-processing step applied after all panels are drawn.

    Parameters
    ----------
    figure : Figure
        The matplotlib Figure.
    axes : dict[str, Axes]
        Panel-name-to-Axes mapping.
    """

    def __call__(self, figure: Any, axes: dict[str, Any], /) -> None: ...


@runtime_checkable
class DataTransform(Protocol):
    """Protocol for a data transformation applied before drawing.

    Parameters
    ----------
    data : Any
        Raw data from the data binding.

    Returns
    -------
    Any
        Transformed data passed to the plot function.
    """

    def __call__(self, data: Any, /) -> Any: ...
