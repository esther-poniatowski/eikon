"""Path resolution for eikon projects.

Resolves relative paths from :class:`PathsConfig` against a discovered
or explicit project root directory.

Project root resolution follows the command-line conventions of the workspace tools, and stops at
the first answer:

1. Explicit ``project_root`` parameter (or ``--root`` CLI option).
2. ``EIKON_ROOT`` environment variable.
3. The nearest ancestor of the current folder that holds ``eikon.yml``, in its ``config/tools/``
   or at its own level.
4. The current folder.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from eikon.config._defaults import CONFIG_LOCATIONS
from eikon.config._schema import PathsConfig
from eikon.exceptions import ConfigConflictError

__all__ = ["ResolvedPaths", "resolve_paths", "discover_project_root", "locate_config"]

EIKON_ROOT_ENV = "EIKON_ROOT"
"""Environment variable name for explicit project root override."""


@dataclass(frozen=True, slots=True)
class ResolvedPaths:
    """Fully resolved, absolute paths for a project.

    Once constructed, the resolved root is cached on this object and
    never re-computed — preventing cross-project bleed when the working
    directory changes during execution.
    """

    project_root: Path
    """Absolute path to the project root directory."""
    output_dir: Path
    """Absolute path to the figure output directory."""
    styles_dir: Path
    """Absolute path to the styles directory."""
    specs_dir: Path
    """Absolute path to the figure specs directory."""
    data_dir: Path
    """Absolute path to the data directory."""


def locate_config(root: Path) -> Path | None:
    """Return the configuration file of a project root, or ``None`` when it holds none.

    The file sits in ``config/tools/eikon.yml`` or at the root itself, ``eikon.yml``.

    Raises
    ------
    ConfigConflictError
        If the root holds both files, so that neither silently wins.

    Examples
    --------
    >>> import tempfile
    >>> root = Path(tempfile.mkdtemp())
    >>> locate_config(root) is None
    True
    >>> (root / "config" / "tools").mkdir(parents=True)
    >>> _ = (root / "config" / "tools" / "eikon.yml").write_text("{}")
    >>> locate_config(root).relative_to(root).as_posix()
    'config/tools/eikon.yml'
    >>> _ = (root / "eikon.yml").write_text("{}")
    >>> locate_config(root)
    Traceback (most recent call last):
    ...
    eikon.exceptions.ConfigConflictError: Two configuration files compete: ...
    """
    found = [root / location for location in CONFIG_LOCATIONS if (root / location).is_file()]
    if len(found) > 1:
        raise ConfigConflictError([str(path) for path in found])
    return found[0] if found else None


def _holds_config(directory: Path) -> bool:
    """Return whether *directory* holds a configuration file at one of its places."""
    return any((directory / location).is_file() for location in CONFIG_LOCATIONS)


def discover_project_root(start: Path | None = None) -> Path:
    """Resolve the project root when no explicit root is given.

    Resolution order:

    1. ``EIKON_ROOT`` environment variable (if set and non-empty).
    2. The nearest ancestor of *start*, *start* included, that holds
       ``config/tools/eikon.yml`` or ``eikon.yml``.
    3. *start* itself, where eikon then runs on its built-in defaults.

    Use the *start* parameter or the env var for environments where the
    working directory is unreliable (CI runners, notebook kernels).

    Parameters
    ----------
    start : Path, optional
        Starting directory for upward walk.  Defaults to the current
        working directory.  Ignored when ``EIKON_ROOT`` is set.

    Returns
    -------
    Path
        Absolute path to the project root.
    """
    env_root = os.environ.get(EIKON_ROOT_ENV, "").strip()
    if env_root:
        return Path(env_root).resolve()

    current = (start or Path.cwd()).resolve()
    for directory in (current, *current.parents):
        if _holds_config(directory):
            return directory
    return current


def resolve_paths(
    config: PathsConfig,
    project_root: Path | None = None,
) -> ResolvedPaths:
    """Resolve all relative paths against the project root.

    Parameters
    ----------
    config : PathsConfig
        Path configuration with relative paths.
    project_root : Path, optional
        Explicit project root (tier 1 — highest priority).  If ``None``,
        falls back to the environment variable, the upward search and the
        current folder via :func:`discover_project_root`.

    Returns
    -------
    ResolvedPaths
        Fully resolved, absolute paths.
    """
    root = (project_root or discover_project_root()).resolve()
    return ResolvedPaths(
        project_root=root,
        output_dir=(root / config.output_dir).resolve(),
        styles_dir=(root / config.styles_dir).resolve(),
        specs_dir=(root / config.specs_dir).resolve(),
        data_dir=(root / config.data_dir).resolve(),
    )
