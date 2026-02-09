"""Declarative figure specifications.

Provides dataclasses for defining figures, panels, and data bindings,
plus a parser for constructing specifications from YAML dictionaries.
"""

from eikon.spec._data import DataBinding
from eikon.spec._figure import FigureSpec
from eikon.spec._override import merge_spec_override
from eikon.spec._panel import PanelSpec
from eikon.spec._parse import parse_figure_file, parse_figure_spec

__all__ = [
    "DataBinding",
    "FigureSpec",
    "PanelSpec",
    "parse_figure_spec",
    "parse_figure_file",
    "merge_spec_override",
]
