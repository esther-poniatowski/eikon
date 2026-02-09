"""Built-in matplotlib plot type wrappers.

Each function is registered via ``@plot_type("name")`` and delegates to
the corresponding matplotlib ``Axes`` method.  The ``params`` dict from
``PanelSpec`` is forwarded as keyword arguments.
"""

from __future__ import annotations

from typing import Any

from eikon.ext import plot_type

__all__: list[str] = []


@plot_type("line")
def _line(ax: Any, /, **kwargs: Any) -> None:
    """Line plot via ``ax.plot()``."""
    x = kwargs.pop("x", None)
    y = kwargs.pop("y", None)
    if x is not None and y is not None:
        ax.plot(x, y, **kwargs)
    elif y is not None:
        ax.plot(y, **kwargs)
    else:
        ax.plot(**kwargs)


@plot_type("scatter")
def _scatter(ax: Any, /, **kwargs: Any) -> None:
    """Scatter plot via ``ax.scatter()``."""
    x = kwargs.pop("x", None)
    y = kwargs.pop("y", None)
    if x is not None and y is not None:
        ax.scatter(x, y, **kwargs)


@plot_type("bar")
def _bar(ax: Any, /, **kwargs: Any) -> None:
    """Bar chart via ``ax.bar()``."""
    x = kwargs.pop("x", None)
    height = kwargs.pop("height", kwargs.pop("y", None))
    if x is not None and height is not None:
        ax.bar(x, height, **kwargs)


@plot_type("barh")
def _barh(ax: Any, /, **kwargs: Any) -> None:
    """Horizontal bar chart via ``ax.barh()``."""
    y = kwargs.pop("y", None)
    width = kwargs.pop("width", kwargs.pop("x", None))
    if y is not None and width is not None:
        ax.barh(y, width, **kwargs)


@plot_type("hist")
def _hist(ax: Any, /, **kwargs: Any) -> None:
    """Histogram via ``ax.hist()``."""
    x = kwargs.pop("x", None)
    if x is not None:
        ax.hist(x, **kwargs)


@plot_type("heatmap")
def _heatmap(ax: Any, /, **kwargs: Any) -> None:
    """Heatmap via ``ax.imshow()``."""
    data = kwargs.pop("data", None)
    if data is not None:
        ax.imshow(data, **kwargs)


@plot_type("contour")
def _contour(ax: Any, /, **kwargs: Any) -> None:
    """Contour plot via ``ax.contour()``."""
    x = kwargs.pop("x", None)
    y = kwargs.pop("y", None)
    z = kwargs.pop("z", None)
    if z is not None:
        if x is not None and y is not None:
            ax.contour(x, y, z, **kwargs)
        else:
            ax.contour(z, **kwargs)


@plot_type("errorbar")
def _errorbar(ax: Any, /, **kwargs: Any) -> None:
    """Error bar plot via ``ax.errorbar()``."""
    x = kwargs.pop("x", None)
    y = kwargs.pop("y", None)
    if x is not None and y is not None:
        ax.errorbar(x, y, **kwargs)
