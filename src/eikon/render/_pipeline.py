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
from eikon.exceptions import RenderError
from eikon.ext import discover_plugins
from eikon.ext._hooks import HookName, fire_hook
from eikon.layout._builder import build_layout
from eikon.layout._constraints import validate_layout_strict
from eikon.layout._grid import LayoutSpec
from eikon.layout._placement import resolve_placements
from eikon.render._context import RenderContext
from eikon.render._drawing import draw_all_panels
from eikon.render._handle import FigureHandle
from eikon.spec._figure import FigureSpec
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

    cfg = config or load_config()
    paths = resolved_paths or resolve_paths(cfg.paths)

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

    sheet = load_style(style_ref, search_dirs=(ctx.paths.styles_dir,))
    if sheet.extends:
        registry = dict(PRESETS)
        sheet = resolve_style_chain(sheet, registry)
    ctx.style = sheet


def _build_layout(ctx: RenderContext) -> None:
    """Build the matplotlib Figure and Axes from the spec's layout."""
    layout_dict = ctx.spec.layout or {}
    layout = _parse_layout_spec(layout_dict)

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
    """Draw all panels into their axes."""
    assert ctx.layout is not None
    assert ctx.style is not None
    with style_context(ctx.style):
        draw_all_panels(
            ctx.layout.axes,
            ctx.spec.panels,
            data_dir=ctx.paths.data_dir,
        )


def _post_process(ctx: RenderContext) -> None:
    """Apply titles, labels, and other figure-level post-processing."""
    assert ctx.layout is not None
    fig = ctx.layout.figure

    if ctx.spec.title:
        fig.suptitle(ctx.spec.title)

    # Apply panel labels
    for panel in ctx.spec.panels:
        if panel.label and panel.name in ctx.layout.axes:
            ax = ctx.layout.axes[panel.name]
            ax.set_title(panel.label)


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


def _parse_layout_spec(raw: dict[str, Any]) -> LayoutSpec:
    """Convert a raw layout dict to a LayoutSpec."""
    kwargs: dict[str, Any] = {}
    if "rows" in raw:
        kwargs["rows"] = int(raw["rows"])
    if "cols" in raw:
        kwargs["cols"] = int(raw["cols"])
    if "width_ratios" in raw:
        kwargs["width_ratios"] = tuple(float(r) for r in raw["width_ratios"])
    if "height_ratios" in raw:
        kwargs["height_ratios"] = tuple(float(r) for r in raw["height_ratios"])
    if "wspace" in raw:
        kwargs["wspace"] = float(raw["wspace"])
    if "hspace" in raw:
        kwargs["hspace"] = float(raw["hspace"])
    if "constrained_layout" in raw:
        kwargs["constrained_layout"] = bool(raw["constrained_layout"])
    return LayoutSpec(**kwargs)
