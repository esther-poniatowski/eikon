"""Built-in seaborn plot type wrappers (lazy import).

Seaborn is imported only when one of its plot types is first invoked,
keeping it an optional dependency.
"""

from __future__ import annotations

from typing import Any

from eikon.ext import plot_type

__all__: list[str] = []


def _lazy_import_seaborn() -> Any:
    """Import seaborn, raising ImportError with a helpful message."""
    try:
        import seaborn as sns  # type: ignore[import-untyped]
    except ImportError:
        msg = (
            "seaborn is required for sns.* plot types. "
            "Install it with: pip install seaborn"
        )
        raise ImportError(msg) from None
    return sns


@plot_type("sns.lineplot")
def _lineplot(ax: Any, /, **kwargs: Any) -> None:
    """Seaborn line plot."""
    sns = _lazy_import_seaborn()
    sns.lineplot(ax=ax, **kwargs)


@plot_type("sns.scatterplot")
def _scatterplot(ax: Any, /, **kwargs: Any) -> None:
    """Seaborn scatter plot."""
    sns = _lazy_import_seaborn()
    sns.scatterplot(ax=ax, **kwargs)


@plot_type("sns.heatmap")
def _heatmap(ax: Any, /, **kwargs: Any) -> None:
    """Seaborn heatmap."""
    sns = _lazy_import_seaborn()
    sns.heatmap(ax=ax, **kwargs)


@plot_type("sns.boxplot")
def _boxplot(ax: Any, /, **kwargs: Any) -> None:
    """Seaborn box plot."""
    sns = _lazy_import_seaborn()
    sns.boxplot(ax=ax, **kwargs)


@plot_type("sns.violinplot")
def _violinplot(ax: Any, /, **kwargs: Any) -> None:
    """Seaborn violin plot."""
    sns = _lazy_import_seaborn()
    sns.violinplot(ax=ax, **kwargs)
