"""StyleSheet dataclass — the composable unit of visual styling.

A :class:`StyleSheet` captures high-level style properties (font, palette,
line width) that are later translated to matplotlib ``rcParams``.  Sheets
can extend other sheets via :attr:`extends`, enabling inheritance chains.
"""

from dataclasses import dataclass, field

__all__ = ["StyleSheet"]


@dataclass(frozen=True, kw_only=True, slots=True)
class StyleSheet:
    """Composable style definition for figures.

    Attributes
    ----------
    name : str
        Identifier for this style (e.g. ``"publication"``).
    font_family : str | None
        Font family name.  ``None`` means "inherit from parent".
    font_size : float | None
        Base font size in points.
    line_width : float | None
        Default line width in points.
    palette : tuple[str, ...] | None
        Ordered colour palette (hex strings or named colours).
    figure_size : tuple[float, float] | None
        Default ``(width, height)`` in inches.
    rc_overrides : dict[str, object]
        Raw matplotlib ``rcParams`` overrides.  Deep-merged during
        composition; leaf values win.
    extends : tuple[str, ...]
        Ordered parent style names.  Resolved left-to-right, with this
        sheet's values overlaying the merged parents.
    """

    name: str
    font_family: str | None = None
    font_size: float | None = None
    line_width: float | None = None
    palette: tuple[str, ...] | None = None
    figure_size: tuple[float, float] | None = None
    rc_overrides: dict[str, object] = field(default_factory=dict)
    extends: tuple[str, ...] = ()
