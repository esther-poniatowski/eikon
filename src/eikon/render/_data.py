"""Data resolution utilities for the rendering pipeline.

Resolves :class:`~eikon.spec._data.DataBinding` instances into concrete
keyword arguments that are forwarded to plot functions. Data files are
resolved relative to the project's configured ``data_dir`` and loaded
using lightweight, dependency-tolerant logic (pandas if available,
fallback to the stdlib CSV reader).
"""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Any

from eikon.exceptions import RenderError
from eikon.ext._transforms import apply_transforms
from eikon.spec._data import DataBinding

__all__ = ["resolve_data_binding"]


def resolve_data_binding(binding: DataBinding, data_dir: Path) -> dict[str, Any]:
    """Load data for a panel and return kwargs for the plot function.

    Returns a dict containing at least ``data`` (the loaded table-like
    object) plus ``x``/``y``/``hue`` keys when the binding specifies
    corresponding columns.
    """

    if not binding.source:
        return {}

    source_path = Path(binding.source)
    if not source_path.is_absolute():
        source_path = (data_dir / source_path).resolve()

    if not source_path.exists():
        raise RenderError(f"Data source not found: {source_path}")

    data_obj = _load_table(source_path)
    data_obj = apply_transforms(data_obj, binding.transforms)

    kwargs: dict[str, Any] = {"data": data_obj}

    for key, column in ("x", binding.x), ("y", binding.y), ("hue", binding.hue):
        if column:
            kwargs[key] = _extract_column(data_obj, column)

    # Merge any loader params
    kwargs.update(binding.params)
    return kwargs


def _load_table(path: Path) -> Any:
    suffix = path.suffix.lower()

    if suffix in {".csv", ".tsv", ".txt"}:
        delimiter = "\t" if suffix == ".tsv" else ","
        try:
            import pandas as pd  # type: ignore[import-untyped]

            return pd.read_csv(path, sep=delimiter)
        except ImportError:
            return _read_csv_fallback(path, delimiter)

    raise RenderError(f"Unsupported data source format: {path.name}")


def _read_csv_fallback(path: Path, delimiter: str) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=delimiter)
        return [dict(row) for row in reader]


def _extract_column(data: Any, column: str) -> Any:
    # list of dicts (check before __getitem__ since lists have __getitem__)
    if isinstance(data, list) and data and isinstance(data[0], dict):
        return [row.get(column) for row in data]

    # pandas DataFrame / other subscriptable objects
    if hasattr(data, "__getitem__"):
        try:
            return data[column]
        except Exception as exc:
            raise RenderError(f"Column '{column}' not found in data source") from exc

    raise RenderError("Unable to extract columns from data source")
