"""Override and merge logic for figure specifications.

Provides utilities to apply partial overrides to :class:`FigureSpec`
instances, producing new immutable specs with the overrides applied.
"""

from dataclasses import replace
from typing import Any

from eikon.spec._figure import FigureSpec

__all__ = ["merge_spec_override"]


def merge_spec_override(
    base: FigureSpec,
    override: dict[str, Any],
) -> FigureSpec:
    """Apply a dictionary of overrides to a figure specification.

    Only fields present in *override* are changed.  Nested dictionaries
    (``layout``, ``export``, ``metadata``) are shallow-merged rather than
    replaced outright; typed dataclass fields are re-parsed from raw
    dicts when provided.

    Parameters
    ----------
    base : FigureSpec
        The base specification.
    override : dict[str, Any]
        Fields to override.

    Returns
    -------
    FigureSpec
        A new specification with overrides applied.
    """
    kwargs: dict[str, Any] = {}

    for key, value in override.items():
        if key == "metadata" and isinstance(value, dict):
            kwargs["metadata"] = {**base.metadata, **value}
        elif key == "layout" and isinstance(value, dict):
            from eikon.spec._parse import parse_layout_spec

            if base.layout is not None:
                from dataclasses import asdict

                merged = {**asdict(base.layout), **value}
            else:
                merged = value
            kwargs["layout"] = parse_layout_spec(merged)
        elif key == "export" and isinstance(value, dict):
            from eikon.spec._parse import _build_export_spec

            if base.export is not None:
                from dataclasses import asdict

                merged = {**asdict(base.export), **value}
            else:
                merged = value
            kwargs["export"] = _build_export_spec(merged)
        elif key == "title_kwargs" and isinstance(value, dict):
            from eikon.spec._parse import _build_title_config

            kwargs["title_kwargs"] = _build_title_config(value)
        elif key == "shared_legend" and isinstance(value, dict):
            from eikon.spec._parse import _build_shared_legend_config

            kwargs["shared_legend"] = _build_shared_legend_config(value)
        elif key == "margin_labels" and isinstance(value, dict) and base.margin_labels is not None:
            kwargs["margin_labels"] = {**base.margin_labels, **value}
        elif key == "tags" and isinstance(value, (list, tuple)):
            kwargs["tags"] = tuple(value)
        elif key == "panels" and isinstance(value, (list, tuple)):
            from eikon.spec._parse import _build_panel

            kwargs["panels"] = tuple(
                _build_panel(p) if isinstance(p, dict) else p for p in value
            )
        else:
            kwargs[key] = value

    return replace(base, **kwargs)
