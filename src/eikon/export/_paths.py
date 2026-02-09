"""Export path construction with template variable substitution.

Builds the output file path for each exported figure by combining the
output directory, optional subdirectory, sanitized filename, and format
extension.  Handles filename collision via configurable strategies.
"""

from __future__ import annotations

import datetime
from pathlib import Path

from eikon._types import ExportFormat
from eikon.exceptions import ExportError
from eikon.export._sanitize import sanitize_filename

__all__ = ["build_export_path"]


def build_export_path(
    *,
    name: str,
    fmt: ExportFormat,
    output_dir: Path,
    filename_template: str = "{name}",
    subdirectory: str = "",
    group: str = "",
    collision: str = "overwrite",
) -> Path:
    """Build the export file path for a single format.

    Template variables:
    - ``{name}`` — figure name (sanitized)
    - ``{group}`` — figure group (sanitized, empty string if unset)
    - ``{date}`` — current date as ``YYYY-MM-DD``
    - ``{format}`` — export format extension (e.g. ``pdf``)

    Parameters
    ----------
    name : str
        Figure name from the specification.
    fmt : ExportFormat
        Export format.
    output_dir : Path
        Base output directory.
    filename_template : str
        Template string for the filename (without extension).
    subdirectory : str
        Subdirectory under ``output_dir``.
    group : str
        Figure group name.
    collision : str
        Collision strategy: ``"overwrite"``, ``"increment"``, or ``"fail"``.

    Returns
    -------
    Path
        Fully resolved output file path.

    Raises
    ------
    ExportError
        If ``collision="fail"`` and the target path already exists.
    """
    extension = fmt.value

    stem = filename_template.format(
        name=sanitize_filename(name),
        group=sanitize_filename(group) if group else "",
        date=datetime.date.today().isoformat(),
        format=extension,
    )
    stem = sanitize_filename(stem)

    directory = output_dir
    if subdirectory:
        directory = directory / sanitize_filename(subdirectory)

    path = directory / f"{stem}.{extension}"

    if collision == "fail" and path.exists():
        msg = f"Export path already exists and collision='fail': {path}"
        raise ExportError(msg)

    if collision == "increment" and path.exists():
        path = _increment_path(path)

    return path


def _increment_path(path: Path) -> Path:
    """Append a numeric suffix to avoid collision.

    ``file.pdf`` → ``file_1.pdf`` → ``file_2.pdf`` → …
    """
    stem = path.stem
    suffix = path.suffix
    parent = path.parent
    counter = 1
    while True:
        candidate = parent / f"{stem}_{counter}{suffix}"
        if not candidate.exists():
            return candidate
        counter += 1
