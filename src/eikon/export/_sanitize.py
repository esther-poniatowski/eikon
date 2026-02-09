"""Filename sanitization for cross-platform safety.

Ensures exported filenames are safe on Windows, macOS, and Linux by
stripping or replacing problematic characters and enforcing length limits.
"""

from __future__ import annotations

import re

__all__ = ["sanitize_filename"]

# Characters illegal on Windows (and generally problematic elsewhere).
_ILLEGAL_RE = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
_MAX_LENGTH = 200


def sanitize_filename(name: str) -> str:
    """Sanitize a string for use as a filename.

    - Strips leading/trailing whitespace.
    - Replaces illegal characters with underscores.
    - Collapses consecutive underscores.
    - Truncates to 200 characters.
    - Returns ``"unnamed"`` for empty inputs.

    Parameters
    ----------
    name : str
        Raw filename (without extension).

    Returns
    -------
    str
        Sanitized filename safe for all major operating systems.
    """
    name = name.strip()
    if not name:
        return "unnamed"

    name = _ILLEGAL_RE.sub("_", name)
    name = re.sub(r"_+", "_", name)
    name = name.strip("_")

    if not name:
        return "unnamed"

    return name[:_MAX_LENGTH]
