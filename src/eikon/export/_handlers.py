"""Format-specific export handlers.

Each handler wraps ``Figure.savefig()`` with format-appropriate options.
Custom handlers can be registered via :func:`register_format_handler`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from eikon._types import ExportFormat
from eikon.export._config import ResolvedExportConfig

__all__ = ["export_figure", "get_handler", "register_format_handler"]

type _HandlerFn = Any  # Callable[[Figure, Path, ResolvedExportConfig], None]

_HANDLER_REGISTRY: dict[ExportFormat, _HandlerFn] = {}


def register_format_handler(fmt: ExportFormat, handler: _HandlerFn) -> None:
    """Register a custom export handler for a format.

    This allows overriding built-in handlers or adding support for new
    formats (after adding the format to :class:`ExportFormat`).

    Parameters
    ----------
    fmt : ExportFormat
        The export format to register the handler for.
    handler : Callable
        A callable with signature ``(figure, path, config) -> None``.
    """
    _HANDLER_REGISTRY[fmt] = handler


def export_figure(
    figure: Any,
    path: Path,
    fmt: ExportFormat,
    config: ResolvedExportConfig,
) -> None:
    """Export a figure to a file using the appropriate handler.

    Parameters
    ----------
    figure : Figure
        The matplotlib Figure to export.
    path : Path
        Output file path.
    fmt : ExportFormat
        Export format.
    config : ResolvedExportConfig
        Resolved export settings.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    handler = get_handler(fmt)
    handler(figure, path, config)


def get_handler(fmt: ExportFormat) -> _HandlerFn:
    """Return the handler function for a given format.

    Looks up custom-registered handlers first, then falls back to
    built-in defaults.

    Parameters
    ----------
    fmt : ExportFormat
        Export format.

    Returns
    -------
    Callable
        A handler function ``(figure, path, config) -> None``.

    Raises
    ------
    KeyError
        If no handler is registered for the format.
    """
    if fmt in _HANDLER_REGISTRY:
        return _HANDLER_REGISTRY[fmt]

    def _make_handler(format_str: str, *, use_dpi: bool = True) -> _HandlerFn:
        def handler(figure: Any, path: Path, config: ResolvedExportConfig) -> None:
            _save_default(figure, path, config, fmt=format_str, use_dpi=use_dpi)
        return handler

    _builtins: dict[ExportFormat, _HandlerFn] = {
        ExportFormat.PDF: _make_handler("pdf"),
        ExportFormat.SVG: _make_handler("svg", use_dpi=False),
        ExportFormat.PNG: _make_handler("png"),
    }
    return _builtins[fmt]


def _save_default(
    figure: Any,
    path: Path,
    config: ResolvedExportConfig,
    *,
    fmt: str,
    use_dpi: bool = True,
) -> None:
    """Save figure in the given format with standard savefig options."""
    kwargs: dict[str, Any] = {
        "format": fmt,
        "transparent": config.transparent,
        "bbox_inches": config.bbox_inches,
        "pad_inches": config.pad_inches,
    }
    if use_dpi:
        kwargs["dpi"] = config.dpi
    if config.metadata:
        kwargs["metadata"] = config.metadata
    figure.savefig(path, **kwargs)
