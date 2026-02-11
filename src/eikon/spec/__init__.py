"""Declarative figure specifications.

Provides dataclasses for defining figures, panels, and data bindings,
plus a parser for constructing specifications from YAML dictionaries.
"""

from eikon.spec._data import DataBinding
from eikon.spec._figure import FigureSpec
from eikon.spec._margin_labels import MarginLabelSpec, MarginLabelStyle, MarginTarget
from eikon.spec._override import merge_spec_override
from eikon.spec._panel import PanelSpec
from eikon.spec._parse import parse_figure_file, parse_figure_spec

__all__ = [
    "DataBinding",
    "FigureSpec",
    "MarginLabelSpec",
    "MarginLabelStyle",
    "MarginTarget",
    "PanelSpec",
    "merge_spec_override",
    "parse_figure_file",
    "parse_figure_spec",
]
