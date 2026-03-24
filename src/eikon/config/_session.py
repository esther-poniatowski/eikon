"""Project session — single entry point for config + path resolution.

A :class:`ProjectSession` bundles a :class:`ProjectConfig` with its
:class:`ResolvedPaths`, eliminating the duplicated load+resolve ceremony
across call sites.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from eikon.config._loader import load_config
from eikon.config._resolver import ResolvedPaths, resolve_paths
from eikon.config._schema import ProjectConfig
from eikon.exceptions import ConfigNotFoundError

__all__ = ["ProjectSession"]


@dataclass(frozen=True, slots=True)
class ProjectSession:
    """Bundled project configuration and resolved paths.

    Attributes
    ----------
    config : ProjectConfig
        The validated project configuration.
    paths : ResolvedPaths
        Fully resolved, absolute paths for the project.
    """

    config: ProjectConfig
    paths: ResolvedPaths

    @classmethod
    def from_config(
        cls,
        config: ProjectConfig | None = None,
        project_root: Path | None = None,
        *,
        strict: bool = True,
    ) -> ProjectSession:
        """Create a session by loading config and resolving paths.

        Parameters
        ----------
        config : ProjectConfig, optional
            Pre-loaded configuration.  If ``None``, loads from disk.
        project_root : Path, optional
            Explicit project root directory.  Passed through to
            :func:`resolve_paths` as tier-1 override.
        strict : bool
            If ``True`` (default), let :class:`ConfigNotFoundError`
            propagate when no config file or project root is found.
            If ``False``, fall back to built-in defaults and
            cwd-based paths.

        Returns
        -------
        ProjectSession
            A fully resolved session.

        Raises
        ------
        ConfigNotFoundError
            If *strict* is ``True`` and no configuration is found.
        """
        if config is not None:
            cfg = config
        else:
            try:
                config_path = (
                    (project_root.resolve() / "eikon.yaml")
                    if project_root is not None
                    else None
                )
                cfg = load_config(path=config_path)
            except ConfigNotFoundError:
                if strict:
                    raise
                cfg = ProjectConfig()

        try:
            paths = resolve_paths(cfg.paths, project_root=project_root)
        except ConfigNotFoundError:
            if strict:
                raise
            root = (project_root or Path.cwd()).resolve()
            paths = ResolvedPaths(
                project_root=root,
                output_dir=root / cfg.paths.output_dir,
                styles_dir=root / cfg.paths.styles_dir,
                specs_dir=root / cfg.paths.specs_dir,
                data_dir=root / cfg.paths.data_dir,
            )

        return cls(config=cfg, paths=paths)
