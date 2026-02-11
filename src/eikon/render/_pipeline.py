"""Rendering pipeline orchestrator.

Chains the rendering stages: config → style → layout → draw → post-process → export.
Each stage is a small function with a clear input/output contract.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

from eikon.config._loader import load_config
from eikon.config._resolver import ResolvedPaths, resolve_paths
from eikon.config._schema import ProjectConfig
from eikon.exceptions import ConfigNotFoundError, RenderError
from eikon.ext import discover_plugins
from eikon.ext._hooks import HookName, fire_hook
from eikon.layout._builder import build_layout
from eikon.layout._constraints import validate_layout_strict
from eikon.layout._placement import resolve_placements
from eikon.render._context import RenderContext
from eikon.render._drawing import draw_panel
from eikon.render._handle import FigureHandle
from eikon.spec._figure import FigureSpec
from eikon.spec._parse import parse_layout_spec
from eikon.style._composer import resolve_style_chain
from eikon.style._loader import load_style
from eikon.style._presets import PRESETS
from eikon.style._rcparams import style_context
from eikon.style._sheet import StyleSheet

__all__ = ["render_figure"]


def render_figure(
    spec: FigureSpec,
    *,
    config: ProjectConfig | None = None,
    resolved_paths: ResolvedPaths | None = None,
    formats: tuple[str, ...] = (),
    show: bool = False,
    overrides: dict[str, Any] | None = None,
) -> FigureHandle:
    """Render a figure from its specification — the main pipeline entry point.

    Parameters
    ----------
    spec : FigureSpec
        The figure specification to render.
    config : ProjectConfig, optional
        Project configuration.  Defaults to built-in defaults.
    formats : tuple[str, ...]
        Export format names (e.g. ``("pdf", "svg")``).  Empty = no export.
    show : bool
        Whether to display the figure interactively after rendering.
    overrides : dict[str, Any], optional
        Per-call keyword overrides forwarded to the pipeline.

    Returns
    -------
    FigureHandle
        A handle to the rendered figure.

    Raises
    ------
    RenderError
        If any stage of the pipeline fails.
    """
    import eikon.contrib  # noqa: F401  — register built-in plot types lazily
    discover_plugins()

    if config is not None:
        cfg = config
    else:
        try:
            cfg = load_config()
        except ConfigNotFoundError:
            cfg = ProjectConfig()
    if resolved_paths is not None:
        paths = resolved_paths
    else:
        try:
            paths = resolve_paths(cfg.paths)
        except ConfigNotFoundError:
            paths = ResolvedPaths(
                project_root=Path.cwd(),
                output_dir=Path.cwd() / cfg.paths.output_dir,
                styles_dir=Path.cwd() / cfg.paths.styles_dir,
                specs_dir=Path.cwd() / cfg.paths.specs_dir,
                data_dir=Path.cwd() / cfg.paths.data_dir,
            )

    ctx = RenderContext(
        spec=spec,
        config=cfg,
        paths=paths,
        export_formats=formats,
        show=show,
        overrides=overrides or {},
    )

    try:
        _resolve_style(ctx)
        fire_hook(HookName.PRE_RENDER, spec=ctx.spec, config=ctx.config)
        _build_layout(ctx)
        _draw_panels(ctx)
        _post_process(ctx)
        fire_hook(HookName.POST_RENDER, spec=ctx.spec, layout=ctx.layout)
    except Exception as exc:
        if not isinstance(exc, RenderError):
            msg = f"Rendering failed for {spec.name!r}: {exc}"
            raise RenderError(msg) from exc
        raise

    handle = FigureHandle(
        spec=ctx.spec,
        figure=ctx.layout.figure if ctx.layout else None,
        axes=dict(ctx.layout.axes) if ctx.layout else {},
    )

    # Export stage (after rendering, before show)
    if ctx.export_formats and handle.figure is not None:
        try:
            export_paths = _export_figure(ctx, handle.figure)
            handle.export_paths = export_paths
        except Exception as exc:
            if not isinstance(exc, RenderError):
                msg = f"Export failed for {spec.name!r}: {exc}"
                raise RenderError(msg) from exc
            raise

    if show:
        handle.show()

    return handle


def _resolve_style(ctx: RenderContext) -> None:
    """Resolve the figure's style to a StyleSheet."""
    style_ref = ctx.spec.style or ctx.config.style.base_style

    if style_ref is None or style_ref == "" or style_ref == "default":
        ctx.style = StyleSheet(name="default")
        return

    search_dirs = (ctx.paths.styles_dir,)
    sheet = load_style(style_ref, search_dirs=search_dirs)
    if sheet.extends:
        registry = _build_style_registry(search_dirs)
        sheet = resolve_style_chain(sheet, registry)
    ctx.style = sheet


def _build_style_registry(
    search_dirs: tuple[Path, ...],
) -> dict[str, StyleSheet]:
    """Build a style registry from presets and user style files.

    Scans the given directories for ``.yaml``, ``.yml``, and ``.mplstyle``
    files so that user styles can ``extends`` other user styles, not only
    built-in presets.
    """
    registry: dict[str, StyleSheet] = dict(PRESETS)
    for directory in search_dirs:
        if not directory.is_dir():
            continue
        for path in directory.iterdir():
            if path.suffix in (".yaml", ".yml", ".mplstyle"):
                try:
                    user_sheet = load_style(path)
                    registry[user_sheet.name] = user_sheet
                except Exception:  # noqa: BLE001
                    continue
    return registry


def _build_layout(ctx: RenderContext) -> None:
    """Build the matplotlib Figure and Axes from the spec's layout."""
    layout_dict = ctx.spec.layout or {}
    layout = parse_layout_spec(layout_dict)

    placements = resolve_placements(ctx.spec.panels, layout)
    validate_layout_strict(placements, layout)

    figure_size = (
        ctx.style.figure_size
        if ctx.style and ctx.style.figure_size
        else ctx.config.style.figure_size
    )
    dpi = ctx.config.export.dpi

    # Apply style context around layout building and drawing
    assert ctx.style is not None
    with style_context(ctx.style):
        ctx.layout = build_layout(
            layout, placements, figure_size=figure_size, dpi=dpi,
        )


def _draw_panels(ctx: RenderContext) -> None:
    """Draw all panels into their axes, applying per-panel styles."""
    assert ctx.layout is not None
    assert ctx.style is not None
    with style_context(ctx.style):
        for panel in ctx.spec.panels:
            if panel.name not in ctx.layout.axes:
                continue
            ax = ctx.layout.axes[panel.name]
            if panel.style is not None:
                search_dirs = (ctx.paths.styles_dir,)
                panel_sheet = load_style(panel.style, search_dirs=search_dirs)
                with style_context(panel_sheet):
                    draw_panel(ax, panel, data_dir=ctx.paths.data_dir)
            else:
                draw_panel(ax, panel, data_dir=ctx.paths.data_dir)


def _post_process(ctx: RenderContext) -> None:
    """Apply titles, labels, and other figure-level post-processing."""
    assert ctx.layout is not None
    fig = ctx.layout.figure

    if ctx.spec.title:
        title_kw = ctx.spec.title_kwargs or {}
        fig.suptitle(ctx.spec.title, **title_kw)

    # Apply panel labels
    for panel in ctx.spec.panels:
        if panel.label and panel.name in ctx.layout.axes:
            ax = ctx.layout.axes[panel.name]
            ax.set_title(panel.label)

    # Hide spines per panel
    for panel in ctx.spec.panels:
        if panel.hide_spines and panel.name in ctx.layout.axes:
            ax = ctx.layout.axes[panel.name]
            for spine_name in panel.hide_spines:
                ax.spines[spine_name].set_visible(False)
            # Remove ticks on hidden spines
            if "top" in panel.hide_spines or "bottom" in panel.hide_spines:
                if "top" in panel.hide_spines:
                    ax.tick_params(top=False)
                if "bottom" in panel.hide_spines:
                    ax.tick_params(bottom=False)
            if "left" in panel.hide_spines or "right" in panel.hide_spines:
                if "right" in panel.hide_spines:
                    ax.tick_params(right=False)
                if "left" in panel.hide_spines:
                    ax.tick_params(left=False)

    # Margin labels
    if ctx.spec.margin_labels:
        from eikon.render._margin_labels import draw_margin_labels

        draw_margin_labels(fig, ctx.layout, ctx.spec.margin_labels)

    # Shared legend: collect handles from the first panel that has them,
    # remove per-panel legends, and place a single figure-level legend.
    if ctx.spec.shared_legend is not None:
        handles: list[Any] = []
        labels: list[str] = []
        for panel in ctx.spec.panels:
            if panel.name in ctx.layout.axes:
                ax = ctx.layout.axes[panel.name]
                h, lab = ax.get_legend_handles_labels()
                if h and not handles:
                    handles, labels = h, lab
                legend = ax.get_legend()
                if legend is not None:
                    legend.remove()
        if handles:
            fig.legend(handles, labels, **ctx.spec.shared_legend)


def _export_figure(ctx: RenderContext, figure: Any) -> dict[str, Path]:
    """Run the export pipeline for the rendered figure."""
    from eikon.export._batch import batch_export, parse_export_spec

    export_spec = parse_export_spec(ctx.spec.export)

    return batch_export(
        figure=figure,
        name=ctx.spec.name,
        group=ctx.spec.group,
        output_dir=ctx.paths.output_dir,
        export_defaults=ctx.config.export,
        export_spec=export_spec,
        cli_formats=ctx.export_formats,
    )


