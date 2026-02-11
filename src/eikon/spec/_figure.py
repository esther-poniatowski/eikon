"""Figure specification — the central declarative abstraction.

A :class:`FigureSpec` fully describes a figure: its panels, layout,
style, export settings, and organizational metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from eikon._types import StyleRef, Tag

if TYPE_CHECKING:
    from eikon.spec._margin_labels import MarginLabelSpec
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
    title_kwargs : dict[str, Any] | None
        Extra keyword arguments forwarded to
        :meth:`matplotlib.figure.Figure.suptitle` (e.g. ``y``,
        ``fontsize``, ``fontweight``).  ``None`` uses matplotlib defaults.
    shared_legend : dict[str, Any] | None
        If set, collect legend handles from the first panel that has them
        and render a single figure-level legend.  Accepted keys are any
        keyword arguments to :meth:`matplotlib.figure.Figure.legend`
        (e.g. ``loc``, ``ncol``, ``fontsize``, ``frameon``).  Pass an
        empty dict ``{}`` for default placement.
    margin_labels : dict[str, MarginLabelSpec] | None
        Edge labels for annotating rows or columns.  Keys are edge
        names (``"top"``, ``"bottom"``, ``"left"``, ``"right"``).
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
    title_kwargs: dict[str, Any] | None = None
    shared_legend: dict[str, Any] | None = None
    margin_labels: dict[str, MarginLabelSpec] | None = None
    metadata: dict[str, str] = field(default_factory=dict)
