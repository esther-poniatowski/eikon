"""Shared type aliases and enumerations used across the eikon package."""

from enum import Enum
from pathlib import Path

__all__ = ["ExportFormat", "Tag", "DPI", "StyleRef"]


class ExportFormat(Enum):
    """Supported export file formats."""

    PDF = "pdf"
    SVG = "svg"
    PNG = "png"

    @classmethod
    def from_string(cls, value: str) -> "ExportFormat":
        """Parse a format string (case-insensitive) into an ExportFormat.

        Parameters
        ----------
        value : str
            Format name, e.g. ``"pdf"``, ``"PNG"``.

        Raises
        ------
        ValueError
            If the string does not match any known format.
        """
        try:
            return cls(value.lower())
        except ValueError:
            valid = ", ".join(f.value for f in cls)
            msg = f"Unknown export format {value!r}. Valid formats: {valid}"
            raise ValueError(msg) from None


type Tag = str
"""A tag is a simple string label for organizing figures."""

type DPI = int | float
"""Normalized DPI value for export resolution."""

type StyleRef = str | Path | dict[str, object]
"""A style reference: a built-in preset name, a path to a style file, or a raw dict."""
