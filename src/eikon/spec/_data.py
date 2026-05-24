"""Data binding specification for figure panels.

A :class:`DataBinding` describes how data is sourced and prepared
before being passed to a plot function.
"""

from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

__all__ = ["DataBinding"]


@dataclass(frozen=True, kw_only=True, slots=True)
class DataBinding:
    """Reference to data for a panel.
    """

    source: str | Path = ""
    """Path to a data file or a named data source identifier."""
    x: str = ""
    """Column or field name for the x-axis variable."""
    y: str = ""
    """Column or field name for the y-axis variable."""
    hue: str = ""
    """Grouping variable name for color coding."""
    transforms: tuple[str, ...] = ()
    """Named transforms to apply in order before plotting."""
    params: dict[str, Any] = field(default_factory=dict)
    """Additional parameters passed to data loading or transforms."""
