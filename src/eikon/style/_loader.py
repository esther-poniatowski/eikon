"""Load a :class:`StyleSheet` from any :type:`StyleRef`.

A ``StyleRef`` can be:

- A **preset name** (e.g. ``"publication"``) — looked up in built-in presets.
- A **matplotlib style name** (e.g. ``"seaborn-v0_8-paper"``) — converted to a
  minimal ``StyleSheet`` wrapping the matplotlib style.
- A **file path** (``Path`` or string ending in ``.yaml`` / ``.mplstyle``) —
  loaded from disk.
- A **raw dict** — parsed directly into a ``StyleSheet``.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from eikon.exceptions import StyleError, StyleNotFoundError
from eikon.style._presets import PRESETS
from eikon.style._sheet import StyleSheet

__all__ = ["load_style"]

CURRENT_STYLE_VERSION = 1
"""Maximum supported style schema version."""


def load_style(
    ref: str | Path | dict[str, object],
    search_dirs: tuple[Path, ...] = (),
) -> StyleSheet:
    """Resolve a :type:`StyleRef` to a :class:`StyleSheet`.

    Parameters
    ----------
    ref : str | Path | dict[str, object]
        Style reference to resolve.
    search_dirs : tuple[Path, ...]
        Additional directories to search for style files.

    Returns
    -------
    StyleSheet
        The loaded style sheet.

    Raises
    ------
    StyleNotFoundError
        If the reference cannot be resolved.
    StyleError
        If a style file is malformed.
    """
    if isinstance(ref, dict):
        return _from_dict(ref)
    if isinstance(ref, Path):
        return _from_file(ref)
    # str — could be preset, matplotlib style, or file path
    return _from_string(ref, search_dirs)


def _from_string(
    name: str,
    search_dirs: tuple[Path, ...],
) -> StyleSheet:
    """Resolve a string reference: preset → file search → matplotlib style."""
    # 1. Check built-in presets
    if name in PRESETS:
        return PRESETS[name]

    # 2. Check if it looks like a file path
    if name.endswith((".yaml", ".yml", ".mplstyle")):
        path = _find_file(name, search_dirs)
        if path is not None:
            return _from_file(path)
        raise StyleNotFoundError(name)

    # 3. Search directories for name.yaml
    for suffix in (".yaml", ".yml"):
        path = _find_file(name + suffix, search_dirs)
        if path is not None:
            return _from_file(path)

    # 4. Try as a matplotlib built-in style
    return _from_matplotlib_style(name)


def _find_file(
    name: str,
    search_dirs: tuple[Path, ...],
) -> Path | None:
    """Search for a style file in the given directories."""
    target = Path(name)
    if target.is_absolute() and target.is_file():
        return target
    for directory in search_dirs:
        candidate = directory / name
        if candidate.is_file():
            return candidate
    return None


def _from_file(path: Path) -> StyleSheet:
    """Load a StyleSheet from a YAML or .mplstyle file."""
    if not path.is_file():
        raise StyleNotFoundError(str(path))

    if path.suffix == ".mplstyle":
        return _from_mplstyle_file(path)
    return _from_yaml_file(path)


def _from_yaml_file(path: Path) -> StyleSheet:
    """Parse a YAML style file into a StyleSheet."""
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        msg = f"Failed to parse style file {path}: {exc}"
        raise StyleError(msg) from exc

    if not isinstance(raw, dict):
        msg = f"Style file {path} must contain a YAML mapping"
        raise StyleError(msg)

    # Use filename stem as fallback name
    if "name" not in raw:
        raw["name"] = path.stem

    return _from_dict(raw)


def _from_mplstyle_file(path: Path) -> StyleSheet:
    """Wrap a .mplstyle file as a StyleSheet with rc_overrides."""
    import matplotlib.style as mpl_style

    try:
        rc: dict[str, Any] = dict(mpl_style.library[path.stem])
    except KeyError:
        # Not in the library — read it manually
        rc = _parse_mplstyle(path)

    return StyleSheet(
        name=path.stem,
        rc_overrides=rc,
    )


def _parse_mplstyle(path: Path) -> dict[str, Any]:
    """Parse a .mplstyle file into a dict of rcParams."""
    import matplotlib as mpl

    params: dict[str, Any] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        key = key.strip()
        value = value.strip()
        if value.startswith("#"):
            continue
        try:
            validate = getattr(mpl.rcParams, "validate", {})
            params[key] = validate[key](value)
        except (KeyError, ValueError, TypeError):
            params[key] = value
    return params


def _from_matplotlib_style(name: str) -> StyleSheet:
    """Wrap a matplotlib built-in style as a StyleSheet."""
    import matplotlib.style as mpl_style

    if name not in mpl_style.library:
        raise StyleNotFoundError(name)

    return StyleSheet(
        name=name,
        rc_overrides=dict(mpl_style.library[name]),
    )


def _from_dict(raw: dict[str, object]) -> StyleSheet:
    """Build a StyleSheet from a raw dictionary."""
    # Check schema version
    ver = raw.get("style_version")
    if ver is not None:
        if not isinstance(ver, int):
            msg = "'style_version' must be an integer"
            raise StyleError(msg)
        if ver > CURRENT_STYLE_VERSION:
            msg = (
                f"'style_version' {ver} is newer than supported "
                f"({CURRENT_STYLE_VERSION}). Please upgrade eikon."
            )
            raise StyleError(msg)

    name = str(raw.get("name", "unnamed"))
    extends_raw = raw.get("extends", ())
    extends: tuple[str, ...]
    if isinstance(extends_raw, str):
        extends = (extends_raw,)
    elif isinstance(extends_raw, list):
        extends = tuple(str(e) for e in extends_raw)
    else:
        extends = ()

    palette_raw = raw.get("palette")
    palette: tuple[str, ...] | None = None
    if isinstance(palette_raw, (list, tuple)):
        palette = tuple(str(c) for c in palette_raw)

    figure_size_raw = raw.get("figure_size")
    figure_size: tuple[float, float] | None = None
    if isinstance(figure_size_raw, (list, tuple)) and len(figure_size_raw) == 2:
        figure_size = (float(figure_size_raw[0]), float(figure_size_raw[1]))

    rc_overrides_raw = raw.get("rc_overrides", {})
    rc_overrides: dict[str, object] = {}
    if isinstance(rc_overrides_raw, dict):
        rc_overrides = dict(rc_overrides_raw)

    return StyleSheet(
        name=name,
        font_family=_opt_str(raw.get("font_family")),
        font_size=_opt_float(raw.get("font_size")),
        line_width=_opt_float(raw.get("line_width")),
        palette=palette,
        figure_size=figure_size,
        rc_overrides=rc_overrides,
        extends=extends,
    )


def _opt_str(value: object) -> str | None:
    """Convert to str if not None."""
    return str(value) if value is not None else None


def _opt_float(value: object) -> float | None:
    """Convert to float if not None."""
    return float(value) if value is not None else None  # type: ignore[arg-type]
