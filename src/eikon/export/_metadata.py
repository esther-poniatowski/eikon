"""Post-export metadata injection.

Provides functions to inject metadata into already-exported files.
PDF metadata is handled natively by matplotlib's ``savefig``, but this
module offers a post-hoc injection path for workflows that need to add
metadata after the initial save (e.g. batch annotation).

PNG metadata uses matplotlib's built-in text chunk support.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

__all__ = ["inject_pdf_metadata", "inject_png_metadata"]


def inject_pdf_metadata(path: Path, metadata: dict[str, str]) -> None:
    """Inject metadata into an existing PDF file.

    Uses matplotlib's PdfPages as a lightweight re-write.  If the file
    does not exist or metadata is empty, this is a no-op.

    Parameters
    ----------
    path : Path
        Path to the PDF file.
    metadata : dict[str, str]
        Key-value metadata pairs (e.g. ``{"Author": "Name"}``).
    """
    if not path.exists() or not metadata:
        return

    from matplotlib.backends.backend_pdf import PdfPages

    info: dict[str, Any] = {}
    for key, value in metadata.items():
        info[f"/{key}"] = value

    with PdfPages(path) as pdf:
        pdf.infodict().update(info)


def inject_png_metadata(path: Path, metadata: dict[str, str]) -> None:
    """Inject text metadata into an existing PNG file.

    Re-saves the PNG with updated text chunks.  If the file does not exist
    or metadata is empty, this is a no-op.

    Parameters
    ----------
    path : Path
        Path to the PNG file.
    metadata : dict[str, str]
        Key-value metadata pairs.

    Notes
    -----
    Requires Pillow for PNG text chunk manipulation.  Falls back to a no-op
    if Pillow is not installed.
    """
    if not path.exists() or not metadata:
        return

    try:
        from PIL import Image
        from PIL.PngImagePlugin import PngInfo
    except ImportError:
        return

    img = Image.open(path)
    png_info = PngInfo()
    for key, value in metadata.items():
        png_info.add_text(key, value)
    img.save(path, pnginfo=png_info)
