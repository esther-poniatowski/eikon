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
    replaced outright.

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
        elif key == "layout" and isinstance(value, dict) and base.layout is not None:
            kwargs["layout"] = {**base.layout, **value}
        elif key == "export" and isinstance(value, dict) and base.export is not None:
            kwargs["export"] = {**base.export, **value}
        elif key == "margin_labels" and isinstance(value, dict) and base.margin_labels is not None:
            kwargs["margin_labels"] = {**base.margin_labels, **value}
        elif key == "tags" and isinstance(value, (list, tuple)):
            kwargs["tags"] = tuple(value)
        elif key == "panels":
            # Panels are not merged — they are replaced entirely.
            # Merging individual panels would require matching by name,
            # which is deferred to a future enhancement.
            continue
        else:
            kwargs[key] = value

    return replace(base, **kwargs)
