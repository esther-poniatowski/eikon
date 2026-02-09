"""Figure specification — the central declarative abstraction.

A :class:`FigureSpec` fully describes a figure: its panels, layout,
style, export settings, and organizational metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from eikon._types import StyleRef, Tag

if TYPE_CHECKING:
    from eikon.spec._panel import PanelSpec

__all__ = ["FigureSpec"]


@dataclass(frozen=True, kw_only=True, slots=True)
class FigureSpec:
    """Declarative specification for a single figure.

    Attributes
    ----------
    name : str
        Unique identifier for this figure within the project.
    title : str
        Display title rendered on the figure.
    tags : tuple[Tag, ...]
        Organizational tags for filtering and grouping.
    group : str
        Grouping key (e.g. ``"manuscript-1"``).
    panels : tuple[PanelSpec, ...]
        Ordered panel definitions composing this figure.
    layout : dict[str, Any] | None
        Layout specification (rows, cols, ratios). Interpreted by the
        layout engine.  ``None`` implies a single-panel figure.
    style : StyleRef | None
        Figure-level style override.
    export : dict[str, Any] | None
        Per-figure export settings override.
    metadata : dict[str, str]
        Arbitrary metadata fields (e.g. author, project).
    """

    name: str
    title: str = ""
    tags: tuple[Tag, ...] = ()
    group: str = ""
    panels: tuple[PanelSpec, ...] = ()
    layout: dict[str, Any] | None = None
    style: StyleRef | None = None
    export: dict[str, Any] | None = None
    metadata: dict[str, str] = field(default_factory=dict)
