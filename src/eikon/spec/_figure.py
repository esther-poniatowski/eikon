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

    Attributes
    ----------
    fontsize : float | None
        Font size in points.
    fontweight : str | None
        Font weight (e.g. ``"bold"``).
    y : float | None
        Vertical position in figure coordinates.
    x : float | None
        Horizontal position in figure coordinates.
    ha : str | None
        Horizontal alignment.
    extra : dict[str, Any]
        Additional keyword arguments forwarded verbatim.
    """

    fontsize: float | None = None
    fontweight: str | None = None
    y: float | None = None
    x: float | None = None
    ha: str | None = None
    extra: dict[str, Any] = field(default_factory=dict)

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

    Attributes
    ----------
    loc : str | None
        Legend location (e.g. ``"upper right"``).
    ncol : int | None
        Number of legend columns.
    fontsize : float | str | None
        Font size for legend text.
    frameon : bool | None
        Whether to draw the legend frame.
    extra : dict[str, Any]
        Additional keyword arguments forwarded verbatim.
    """

    loc: str | None = None
    ncol: int | None = None
    fontsize: float | str | None = None
    frameon: bool | None = None
    extra: dict[str, Any] = field(default_factory=dict)

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
    layout : LayoutSpec | None
        Layout specification (rows, cols, ratios). ``None`` implies a
        single-panel figure.
    style : StyleRef | None
        Figure-level style override.
    export : ExportSpec | None
        Per-figure export settings override.
    title_kwargs : TitleConfig | None
        Extra keyword arguments forwarded to
        :meth:`matplotlib.figure.Figure.suptitle`.  ``None`` uses
        matplotlib defaults.
    shared_legend : SharedLegendConfig | None
        If set, collect legend handles from the first panel that has them
        and render a single figure-level legend.
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
    layout: LayoutSpec | None = None
    style: StyleRef | None = None
    export: ExportSpec | None = None
    title_kwargs: TitleConfig | None = None
    shared_legend: SharedLegendConfig | None = None
    margin_labels: dict[str, MarginLabelSpec] | None = None
    metadata: dict[str, str] = field(default_factory=dict)
