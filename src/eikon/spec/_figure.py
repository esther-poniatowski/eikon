"""Figure specification — the central declarative abstraction.

A :class:`FigureSpec` fully describes a figure: its panels, layout,
style, export settings, and organizational metadata.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any

from eikon._types import StyleRef, Tag

if TYPE_CHECKING:
    from eikon.export._config import ExportSpec
    from eikon.layout._grid import LayoutSpec
    from eikon.spec._margin_labels import MarginLabelSpec
    from eikon.spec._panel import PanelSpec

__all__ = ["FigureSpec", "TitleConfig", "SharedLegendConfig"]


@dataclass(frozen=True, kw_only=True, slots=True)
class TitleConfig:
    """Keyword arguments forwarded to :meth:`matplotlib.figure.Figure.suptitle`.
    """

    fontsize: float | None = None
    """Font size in points."""
    fontweight: str | None = None
    """Font weight (e.g. ``"bold"``)."""
    y: float | None = None
    """Vertical position in figure coordinates."""
    x: float | None = None
    """Horizontal position in figure coordinates."""
    ha: str | None = None
    """Horizontal alignment."""
    extra: dict[str, Any] = field(default_factory=dict)
    """Additional keyword arguments forwarded verbatim."""

    def to_kwargs(self) -> dict[str, Any]:
        """Return a dict suitable for ``fig.suptitle(**kwargs)``."""
        kw: dict[str, Any] = {}
        if self.fontsize is not None:
            kw["fontsize"] = self.fontsize
        if self.fontweight is not None:
            kw["fontweight"] = self.fontweight
        if self.y is not None:
            kw["y"] = self.y
        if self.x is not None:
            kw["x"] = self.x
        if self.ha is not None:
            kw["ha"] = self.ha
        kw.update(self.extra)
        return kw


@dataclass(frozen=True, kw_only=True, slots=True)
class SharedLegendConfig:
    """Configuration for a shared figure-level legend.
    """

    loc: str | None = None
    """Legend location (e.g. ``"upper right"``)."""
    ncol: int | None = None
    """Number of legend columns."""
    fontsize: float | str | None = None
    """Font size for legend text."""
    frameon: bool | None = None
    """Whether to draw the legend frame."""
    extra: dict[str, Any] = field(default_factory=dict)
    """Additional keyword arguments forwarded verbatim."""

    def to_kwargs(self) -> dict[str, Any]:
        """Return a dict suitable for ``fig.legend(**kwargs)``."""
        kw: dict[str, Any] = {}
        if self.loc is not None:
            kw["loc"] = self.loc
        if self.ncol is not None:
            kw["ncol"] = self.ncol
        if self.fontsize is not None:
            kw["fontsize"] = self.fontsize
        if self.frameon is not None:
            kw["frameon"] = self.frameon
        kw.update(self.extra)
        return kw


@dataclass(frozen=True, kw_only=True, slots=True)
class FigureSpec:
    """Declarative specification for a single figure.
    """

    name: str
    """Unique identifier for this figure within the project."""
    title: str = ""
    """Display title rendered on the figure."""
    tags: tuple[Tag, ...] = ()
    """Organizational tags for filtering and grouping."""
    group: str = ""
    """Grouping key (e.g. ``"manuscript-1"``)."""
    panels: tuple[PanelSpec, ...] = ()
    """Ordered panel definitions composing this figure."""
    layout: LayoutSpec | None = None
    """Layout specification (rows, cols, ratios). ``None`` implies a
    single-panel figure.
    """
    style: StyleRef | None = None
    """Figure-level style override."""
    export: ExportSpec | None = None
    """Per-figure export settings override."""
    title_kwargs: TitleConfig | None = None
    """Extra keyword arguments forwarded to
    :meth:`matplotlib.figure.Figure.suptitle`.  ``None`` uses
    matplotlib defaults.
    """
    shared_legend: SharedLegendConfig | None = None
    """If set, collect legend handles from the first panel that has them
    and render a single figure-level legend.
    """
    margin_labels: dict[str, MarginLabelSpec] | None = None
    """Edge labels for annotating rows or columns.  Keys are edge
    names (``"top"``, ``"bottom"``, ``"left"``, ``"right"``).
    """
    metadata: dict[str, str] = field(default_factory=dict)
    """Arbitrary metadata fields (e.g. author, project)."""
