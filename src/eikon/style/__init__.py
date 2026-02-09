"""Style management for eikon figures.

This subpackage provides composable style sheets that bridge high-level
properties (font family, palette, line width) to matplotlib ``rcParams``.

Public API
----------
StyleSheet
    Composable style definition dataclass.
compose_styles
    Merge multiple style sheets.
resolve_style_chain
    Resolve ``extends`` inheritance chains.
style_context
    Context manager for temporary style application.
to_rcparams
    Convert a StyleSheet to a matplotlib rcParams dict.
load_style
    Load a style from a preset name, file path, or dict.
PRESETS
    Built-in style presets.
"""

from eikon.style._composer import compose_styles, resolve_style_chain
from eikon.style._loader import load_style
from eikon.style._presets import PRESETS
from eikon.style._rcparams import style_context, to_rcparams
from eikon.style._sheet import StyleSheet

__all__ = [
    "PRESETS",
    "StyleSheet",
    "compose_styles",
    "load_style",
    "resolve_style_chain",
    "style_context",
    "to_rcparams",
]
