"""Project session — single entry point for config + path resolution.

A :class:`ProjectSession` bundles a :class:`ProjectConfig` with its
:class:`ResolvedPaths`, eliminating the duplicated load+resolve ceremony
across call sites.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from eikon.config._loader import load_config
from eikon.config._resolver import ResolvedPaths, discover_project_root, resolve_paths
from eikon.config._schema import ProjectConfig
from eikon.exceptions import ConfigNotFoundError

__all__ = ["ProjectSession"]


@dataclass(frozen=True, slots=True)
class ProjectSession:
    """Bundled project configuration and resolved paths.
    """

    config: ProjectConfig
    """The validated project configuration."""
    paths: ResolvedPaths
    """Fully resolved, absolute paths for the project."""

    @classmethod
    def from_config(
        cls,
        config: ProjectConfig | None = None,
        project_root: Path | None = None,
        *,
        config_path: Path | None = None,
        strict: bool = True,
    ) -> ProjectSession:
        """Create a session by loading config and resolving paths.

        Parameters
        ----------
        config : ProjectConfig, optional
            Pre-loaded configuration.  If ``None``, loads from disk.
        project_root : Path, optional
            Explicit project root directory.  Passed through to
            :func:`resolve_paths` as tier-1 override.  If ``None``, the root
            is resolved by :func:`discover_project_root`.
        config_path : Path, optional
            Explicit settings file, as given by ``--config``, read relative
            to the current folder.  If ``None``, the settings file is located
            below the root; a root without one yields the built-in defaults.
        strict : bool
            If ``True`` (default), let :class:`ConfigNotFoundError`
            propagate when the file named by *config_path* is absent.
            If ``False``, fall back to built-in defaults.

        Returns
        -------
        ProjectSession
            A fully resolved session.

        Raises
        ------
        ConfigNotFoundError
            If *strict* is ``True`` and *config_path* names an absent file.
        ConfigConflictError
            If the root holds both ``config/tools/eikon.yml`` and ``eikon.yml``.
        """
        root = project_root.resolve() if project_root is not None else discover_project_root()
        if config is not None:
            cfg = config
        else:
            try:
                cfg = load_config(config_path, root=root)
            except ConfigNotFoundError:
                if strict:
                    raise
                cfg = ProjectConfig()

        return cls(config=cfg, paths=resolve_paths(cfg.paths, project_root=root))
