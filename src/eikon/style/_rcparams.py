"""Bridge between :class:`StyleSheet` and matplotlib ``rcParams``.

Converts high-level style properties to the ``rcParams`` dict that
matplotlib consumes, and provides a context manager for temporary
application.
"""

from __future__ import annotations

from contextlib import contextmanager
from typing import TYPE_CHECKING, Any

import matplotlib as mpl
from cycler import cycler

from eikon.style._sheet import StyleSheet

if TYPE_CHECKING:
    from collections.abc import Generator

__all__ = ["to_rcparams", "style_context"]


def to_rcparams(sheet: StyleSheet) -> dict[str, Any]:
    """Convert a :class:`StyleSheet` into a matplotlib ``rcParams`` dict.

    Only fields that are not ``None`` are included.  The ``rc_overrides``
    dict is merged last, allowing raw escape-hatch overrides.

    Parameters
    ----------
    sheet : StyleSheet
        The style sheet to convert.

    Returns
    -------
    dict[str, Any]
        Dictionary suitable for :func:`matplotlib.rc_context`.
    """
    params: dict[str, Any] = {}

    if sheet.font_family is not None:
        params["font.family"] = sheet.font_family
    if sheet.font_size is not None:
        params["font.size"] = sheet.font_size
    if sheet.line_width is not None:
        params["lines.linewidth"] = sheet.line_width
    if sheet.palette is not None and len(sheet.palette) > 0:
        params["axes.prop_cycle"] = cycler(color=list(sheet.palette))
    if sheet.figure_size is not None:
        params["figure.figsize"] = list(sheet.figure_size)

    # rc_overrides merge last — they are the user's escape hatch
    params.update(sheet.rc_overrides)

    return params


@contextmanager
def style_context(
    sheet: StyleSheet,
    *,
    debug: bool = False,
) -> Generator[None]:
    """Temporarily apply a :class:`StyleSheet` as matplotlib ``rcParams``.

    Uses :func:`matplotlib.rc_context` to scope changes; all parameters
    are reverted when the context manager exits.  Fully re-entrant: nested
    calls correctly restore the outer state.

    Parameters
    ----------
    sheet : StyleSheet
        The style sheet to apply.
    debug : bool
        When ``True``, capture modified keys on entry and assert they are
        restored on exit — useful for detecting plot functions that mutate
        ``rcParams`` directly outside the context manager.

    Yields
    ------
    None
    """
    params = to_rcparams(sheet)

    snapshot: dict[str, Any] = {}
    if debug:
        snapshot = {k: mpl.rcParams[k] for k in params if k in mpl.rcParams}

    with mpl.rc_context(rc=params):
        yield

    if debug:
        for key, original in snapshot.items():
            current = mpl.rcParams[key]
            if current != original:
                import warnings

                warnings.warn(
                    f"rcParams[{key!r}] was not restored after "
                    f"style_context: expected {original!r}, got {current!r}",
                    RuntimeWarning,
                    stacklevel=2,
                )
