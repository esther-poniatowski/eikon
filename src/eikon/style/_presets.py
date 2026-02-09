"""Built-in style presets for common use cases.

Three presets are provided out of the box:

- **publication** — compact, serif fonts, suitable for journal figures.
- **presentation** — larger fonts, sans-serif, readable on slides.
- **poster** — extra-large fonts and line widths for poster figures.
"""

from eikon.style._sheet import StyleSheet

__all__ = ["PRESETS", "get_preset"]

PRESETS: dict[str, StyleSheet] = {
    "publication": StyleSheet(
        name="publication",
        font_family="serif",
        font_size=8.0,
        line_width=0.8,
        figure_size=(7.0, 5.0),
        rc_overrides={
            "axes.linewidth": 0.5,
            "xtick.major.width": 0.5,
            "ytick.major.width": 0.5,
            "xtick.direction": "in",
            "ytick.direction": "in",
        },
    ),
    "presentation": StyleSheet(
        name="presentation",
        font_family="sans-serif",
        font_size=14.0,
        line_width=1.5,
        figure_size=(10.0, 7.0),
        rc_overrides={
            "axes.linewidth": 1.0,
            "xtick.major.width": 1.0,
            "ytick.major.width": 1.0,
        },
    ),
    "poster": StyleSheet(
        name="poster",
        font_family="sans-serif",
        font_size=20.0,
        line_width=2.5,
        figure_size=(14.0, 10.0),
        rc_overrides={
            "axes.linewidth": 1.5,
            "xtick.major.width": 1.5,
            "ytick.major.width": 1.5,
            "xtick.major.size": 6.0,
            "ytick.major.size": 6.0,
        },
    ),
}


def get_preset(name: str) -> StyleSheet | None:
    """Return a built-in preset by name, or ``None`` if not found."""
    return PRESETS.get(name)
