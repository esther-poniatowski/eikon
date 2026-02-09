"""Path resolution for eikon projects.

Resolves relative paths from :class:`PathsConfig` against a discovered
or explicit project root directory.

Project root resolution uses a three-tier strategy:

1. Explicit ``project_root`` parameter (or ``--project-root`` CLI flag).
2. ``EIKON_PROJECT_ROOT`` environment variable.
3. Auto-discovery: walk upward from cwd until ``eikon.yaml`` is found.
"""

import os
from dataclasses import dataclass
from pathlib import Path

from eikon.config._defaults import CONFIG_FILENAME
from eikon.config._schema import PathsConfig
from eikon.exceptions import ConfigNotFoundError

__all__ = ["ResolvedPaths", "resolve_paths", "discover_project_root"]

EIKON_PROJECT_ROOT_ENV = "EIKON_PROJECT_ROOT"
"""Environment variable name for explicit project root override."""


@dataclass(frozen=True, slots=True)
class ResolvedPaths:
    """Fully resolved, absolute paths for a project.

    Once constructed, the resolved root is cached on this object and
    never re-computed — preventing cross-project bleed when the working
    directory changes during execution.

    Attributes
    ----------
    project_root : Path
        Absolute path to the project root directory.
    output_dir : Path
        Absolute path to the figure output directory.
    styles_dir : Path
        Absolute path to the styles directory.
    specs_dir : Path
        Absolute path to the figure specs directory.
    data_dir : Path
        Absolute path to the data directory.
    """

    project_root: Path
    output_dir: Path
    styles_dir: Path
    specs_dir: Path
    data_dir: Path


def discover_project_root(start: Path | None = None) -> Path:
    """Resolve the project root using the three-tier strategy.

    Resolution order:

    1. ``EIKON_PROJECT_ROOT`` environment variable (if set and non-empty).
    2. Walk upward from *start* (defaults to cwd) until ``eikon.yaml`` is
       found.

    Use the *start* parameter or the env var for environments where the
    working directory is unreliable (CI runners, notebook kernels).

    Parameters
    ----------
    start : Path, optional
        Starting directory for upward walk.  Defaults to the current
        working directory.  Ignored when ``EIKON_PROJECT_ROOT`` is set.

    Returns
    -------
    Path
        Absolute path to the project root.

    Raises
    ------
    ConfigNotFoundError
        If no ``eikon.yaml`` is found via any method.
    """
    # Tier 2: environment variable
    env_root = os.environ.get(EIKON_PROJECT_ROOT_ENV, "").strip()
    if env_root:
        root = Path(env_root).resolve()
        if (root / CONFIG_FILENAME).is_file():
            return root
        raise ConfigNotFoundError(str(root))

    # Tier 3: upward walk
    current = (start or Path.cwd()).resolve()
    for directory in (current, *current.parents):
        if (directory / CONFIG_FILENAME).is_file():
            return directory
    raise ConfigNotFoundError(str(current))


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
        falls back to the env var / auto-discovery tiers via
        :func:`discover_project_root`.

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
