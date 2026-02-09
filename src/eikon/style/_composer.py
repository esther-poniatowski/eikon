"""Style composition — merging and flattening style inheritance chains.

The composer resolves :attr:`StyleSheet.extends` chains depth-first, then
overlays the leaf sheet's explicitly set fields.  ``rc_overrides`` dicts
are deep-merged; all other fields use rightmost-wins semantics.
"""

from __future__ import annotations

from dataclasses import replace
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections.abc import Mapping

from eikon.style._sheet import StyleSheet

__all__ = ["compose_styles", "resolve_style_chain"]


def compose_styles(*sheets: StyleSheet) -> StyleSheet:
    """Merge multiple style sheets left-to-right (rightmost wins).

    Parameters
    ----------
    *sheets : StyleSheet
        Style sheets to compose, in increasing priority order.

    Returns
    -------
    StyleSheet
        A new sheet with all fields resolved.

    Raises
    ------
    ValueError
        If no sheets are provided.
    """
    if not sheets:
        msg = "compose_styles requires at least one StyleSheet"
        raise ValueError(msg)

    result = sheets[0]
    for sheet in sheets[1:]:
        result = _overlay(result, sheet)
    return result


def resolve_style_chain(
    sheet: StyleSheet,
    registry: Mapping[str, StyleSheet],
    *,
    _seen: frozenset[str] | None = None,
) -> StyleSheet:
    """Resolve the ``extends`` chain of a style sheet recursively.

    Parents are resolved depth-first, left-to-right.  Circular references
    are detected and raise :class:`ValueError`.

    Parameters
    ----------
    sheet : StyleSheet
        The leaf style sheet whose chain to resolve.
    registry : Mapping[str, StyleSheet]
        Name-to-sheet mapping (presets + user-loaded styles).
    _seen : frozenset[str] | None
        Internal parameter for cycle detection.

    Returns
    -------
    StyleSheet
        Fully resolved style sheet with no remaining ``extends``.
    """
    seen = _seen or frozenset()
    if sheet.name in seen:
        msg = f"Circular style reference detected: {sheet.name!r}"
        raise ValueError(msg)
    seen = seen | {sheet.name}

    if not sheet.extends:
        return sheet

    # Resolve each parent recursively, then compose them
    resolved_parents: list[StyleSheet] = []
    for parent_name in sheet.extends:
        parent = registry.get(parent_name)
        if parent is None:
            from eikon.exceptions import StyleNotFoundError

            raise StyleNotFoundError(parent_name)
        resolved_parents.append(
            resolve_style_chain(parent, registry, _seen=seen)
        )

    # Compose all parents left-to-right, then overlay the leaf
    base = compose_styles(*resolved_parents)
    return _overlay(base, sheet)


def _overlay(base: StyleSheet, top: StyleSheet) -> StyleSheet:
    """Overlay *top* onto *base*, keeping non-None values from *top*.

    ``rc_overrides`` are deep-merged; all other fields use top's value
    when it is not ``None``, otherwise fall back to base.
    """
    merged_rc = {**base.rc_overrides, **top.rc_overrides}
    return replace(
        base,
        name=top.name,
        font_family=(
            top.font_family if top.font_family is not None
            else base.font_family
        ),
        font_size=(
            top.font_size if top.font_size is not None
            else base.font_size
        ),
        line_width=(
            top.line_width if top.line_width is not None
            else base.line_width
        ),
        palette=(
            top.palette if top.palette is not None
            else base.palette
        ),
        figure_size=(
            top.figure_size if top.figure_size is not None
            else base.figure_size
        ),
        rc_overrides=merged_rc,
        extends=(),  # Fully resolved; no further parents
    )
