"""Initialization logic and public interface for the ``eikon`` package.

Provides a curated API surface re-exporting the most commonly used
classes and functions from subpackages.

Variables
---------
__version__ : str, default "0.0.0+unknown"
    Version of the package. If the package metadata is unavailable (e.g. in editable or source-only
    environments), a fallback value is provided (PEP 440 compliant).

Functions
---------
info() -> str
    Format diagnostic information about the package and platform.

Examples
--------
To programmatically retrieve the package version:

    >>> import eikon
    >>> eikon.__version__
    '0.1.0'

See Also
--------
importlib.metadata.version
    Function to retrieve the version of a package.
PackageNotFoundError
    Exception raised when the package is not found in the environment.
"""

import platform
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

try:
    if __package__ is None:  # erroneous script execution
        raise PackageNotFoundError
    __version__ = version(__package__)
except PackageNotFoundError:
    __version__ = "0.0.0+unknown"

from eikon.config import ProjectConfig, ProjectSession, load_config, resolve_paths  # noqa: E402
from eikon.config._resolver import ResolvedPaths  # noqa: E402
from eikon.ext import ExtensionRegistry  # noqa: E402
from eikon.export import ExportSpec, batch_export  # noqa: E402
from eikon.layout import BuiltLayout, LayoutSpec, build_layout  # noqa: E402
from eikon.registry import Registry  # noqa: E402
from eikon.render import FigureHandle, render_figure  # noqa: E402
from eikon.spec import (  # noqa: E402
    DataBinding,
    FigureSpec,
    MarginLabelSpec,
    MarginLabelStyle,
    MarginTarget,
    PanelSpec,
    SharedLegendConfig,
    TitleConfig,
    parse_figure_spec,
)
from eikon.style import StyleSheet, load_style, style_context  # noqa: E402

__all__ = [
    # Version & diagnostics
    "__version__",
    "info",
    # Configuration
    "ProjectConfig",
    "ProjectSession",
    "ResolvedPaths",
    "load_config",
    "resolve_paths",
    # Specifications
    "DataBinding",
    "FigureSpec",
    "MarginLabelSpec",
    "MarginLabelStyle",
    "MarginTarget",
    "PanelSpec",
    "SharedLegendConfig",
    "TitleConfig",
    "parse_figure_spec",
    # Style
    "StyleSheet",
    "load_style",
    "style_context",
    # Layout
    "LayoutSpec",
    "BuiltLayout",
    "build_layout",
    # Export
    "ExportSpec",
    "batch_export",
    # Registry
    "Registry",
    "load_registry",
    # Render
    "FigureHandle",
    "render_figure",
    "render",
]


def info() -> str:
    """Format diagnostic information on package and platform."""
    return (
        f"{__package__} {__version__} | "
        f"Platform: {platform.system()} Python {platform.python_version()}"
    )


def render(
    name_or_spec: str | FigureSpec,
    *,
    config: ProjectConfig | None = None,
    resolved_paths: ResolvedPaths | None = None,
    session: ProjectSession | None = None,
    formats: tuple[str, ...] = (),
    overrides: dict[str, object] | None = None,
    show: bool = False,
    strict: bool = True,
    extensions: ExtensionRegistry | None = None,
) -> FigureHandle:
    """Convenience function: render a figure by name or spec.

    This is the primary high-level entry point.  It accepts either a
    :class:`FigureSpec` object or a string name (resolved as a YAML
    file path via the project config's specs directory).

    Parameters
    ----------
    name_or_spec : str | FigureSpec
        A ``FigureSpec`` instance, or a string name / path to a YAML
        spec file.
    config : ProjectConfig, optional
        Project configuration.  If ``None``, uses built-in defaults.
    resolved_paths : ResolvedPaths, optional
        Pre-resolved paths.  Prefer passing a *session* instead.
    session : ProjectSession, optional
        A pre-built session.  Takes precedence over *config* and
        *resolved_paths* when provided.
    formats : tuple[str, ...]
        Export format names (e.g. ``("pdf", "svg")``).
    overrides : dict[str, object], optional
        Per-call overrides forwarded to the pipeline.
    show : bool
        Whether to display the figure interactively.
    strict : bool
        If ``True`` (default), let config/path errors propagate.
        If ``False``, fall back to built-in defaults.

    Returns
    -------
    FigureHandle
        A handle to the rendered figure.
    """
    if session is not None:
        sess = session
    elif config is not None or resolved_paths is not None:
        cfg = config or ProjectSession.from_config(strict=strict).config
        if resolved_paths is not None:
            paths = resolved_paths
        else:
            paths = ProjectSession.from_config(config=cfg, strict=strict).paths
        sess = ProjectSession(config=cfg, paths=paths)
    else:
        sess = ProjectSession.from_config(strict=strict)

    if isinstance(name_or_spec, str):
        from eikon.spec import parse_figure_file

        spec_entry = None
        try:
            reg = load_registry(config=sess.config, resolved_paths=sess.paths)
            spec_entry = reg.get(name_or_spec)
        except Exception:
            spec_entry = None

        spec_path = Path(name_or_spec)
        if spec_entry and spec_entry.get("spec_path"):
            spec_path = Path(spec_entry["spec_path"])
            if not spec_path.is_absolute():
                spec_path = sess.paths.project_root / spec_path
        else:
            if not spec_entry:
                import warnings

                warnings.warn(
                    f"Figure '{name_or_spec}' not found in registry; falling back to specs_dir.",
                    UserWarning,
                    stacklevel=2,
                )
            if not spec_path.suffix:
                spec_path = sess.paths.specs_dir / f"{spec_path.name}.yaml"

        spec = parse_figure_file(spec_path)
    else:
        spec = name_or_spec

    return render_figure(
        spec,
        session=sess,
        formats=formats,
        show=show,
        overrides=dict(overrides) if overrides else {},
        extensions=extensions,
    )


def load_registry(
    *,
    config: ProjectConfig | None = None,
    resolved_paths: ResolvedPaths | None = None,
    project_root: Path | None = None,
) -> Registry:
    """Load the project figure registry.

    Parameters
    ----------
    config : ProjectConfig, optional
        Project configuration.  If ``None``, uses built-in defaults.

    Returns
    -------
    Registry
        A loaded registry instance.
    """
    cfg = config or load_config(path=(project_root / "eikon.yaml") if project_root is not None else None)
    paths = resolved_paths or resolve_paths(cfg.paths, project_root=project_root)

    registry_path = cfg.registry_file
    if not Path(registry_path).is_absolute():
        registry_path = paths.project_root / registry_path

    reg = Registry(Path(registry_path))
    reg.load()
    return reg
