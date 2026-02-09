"""Render context — mutable state carried through the rendering pipeline.

The :class:`RenderContext` is an internal object that accumulates state
as the pipeline progresses through its stages.  It is not part of the
public API.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from eikon.config._schema import ProjectConfig
from eikon.layout._builder import BuiltLayout
from eikon.spec._figure import FigureSpec
from eikon.style._sheet import StyleSheet

__all__ = ["RenderContext"]


@dataclass(kw_only=True, slots=True)
class RenderContext:
    """Mutable state for a single render pass.

    Attributes
    ----------
    spec : FigureSpec
        The figure specification being rendered.
    config : ProjectConfig
        The resolved project configuration.
    style : StyleSheet | None
        The resolved style sheet (set during style resolution).
    layout : BuiltLayout | None
        The built layout (set during layout building).
    export_formats : tuple[str, ...]
        Formats to export (empty = no export).
    show : bool
        Whether to display the figure interactively after rendering.
    overrides : dict[str, Any]
        Per-call keyword overrides.
    """

    spec: FigureSpec
    config: ProjectConfig
    style: StyleSheet | None = None
    layout: BuiltLayout | None = None
    export_formats: tuple[str, ...] = ()
    show: bool = False
    overrides: dict[str, Any] = field(default_factory=dict)
