"""Rendering pipeline orchestrator.

Chains the rendering stages: config -> style -> layout -> draw -> post-process -> export.
Each stage is a pure function with explicit typed inputs and outputs.
The orchestrator composes stages without mutable shared state.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any

from eikon.config._resolver import ResolvedPaths
from eikon.config._schema import ProjectConfig
from eikon.config._session import ProjectSession
from eikon.exceptions import RenderError
from eikon.ext import discover_plugins
from eikon.ext._hooks import HookName, fire_hook
from eikon.layout._builder import BuiltLayout, build_layout
from eikon.layout._constraints import validate_layout_strict
from eikon.layout._grid import LayoutSpec
from eikon.layout._placement import resolve_placements
from eikon.render._drawing import draw_panel
from eikon.render._handle import FigureHandle
from eikon.spec._figure import FigureSpec, SharedLegendConfig
from eikon.spec._panel import PanelSpec
from eikon.style._composer import resolve_style_chain
from eikon.style._loader import load_style
from eikon.style._presets import PRESETS
from eikon.style._rcparams import style_context
from eikon.style._sheet import StyleSheet

__all__ = ["render_figure"]


# ---------------------------------------------------------------------------
# Stage result types
# ---------------------------------------------------------------------------


@dataclass(frozen=True, slots=True)
class ResolvedStyle:
    """Output of the style resolution stage."""

    sheet: StyleSheet


@dataclass(frozen=True, slots=True)
class ResolvedLayout:
    """Output of the layout building stage."""

    built: BuiltLayout


# ---------------------------------------------------------------------------
# Stage functions — each takes explicit parameters, returns explicit results
# ---------------------------------------------------------------------------


def stage_resolve_style(
    *,
    style_ref: str | None,
    base_style: str,
    styles_dir: Path,
) -> ResolvedStyle:
    """Resolve a style reference to a :class:`StyleSheet`."""
    ref = style_ref or base_style

    if ref is None or ref == "" or ref == "default":
        return ResolvedStyle(sheet=StyleSheet(name="default"))

    search_dirs = (styles_dir,)
    sheet = load_style(ref, search_dirs=search_dirs)
    if sheet.extends:
        registry = _build_style_registry(search_dirs)
        sheet = resolve_style_chain(sheet, registry)
    return ResolvedStyle(sheet=sheet)


def stage_build_layout(
    *,
    layout_spec: LayoutSpec,
    panels: tuple[PanelSpec, ...],
    style: StyleSheet,
    figure_size: tuple[float, float],
    dpi: int,
) -> ResolvedLayout:
    """Build the matplotlib Figure and Axes from layout and panel specs."""
    placements = resolve_placements(panels, layout_spec)
    validate_layout_strict(placements, layout_spec)

    with style_context(style):
        built = build_layout(
            layout_spec, placements, figure_size=figure_size, dpi=dpi,
        )
    return ResolvedLayout(built=built)


def stage_draw_panels(
    *,
    panels: tuple[PanelSpec, ...],
    built: BuiltLayout,
    style: StyleSheet,
    styles_dir: Path,
    data_dir: Path,
) -> None:
    """Draw all panels into their axes, applying per-panel styles."""
    with style_context(style):
        for panel in panels:
            if panel.name not in built.axes:
                continue
            ax = built.axes[panel.name]
            if panel.style is not None:
                panel_sheet = load_style(panel.style, search_dirs=(styles_dir,))
                with style_context(panel_sheet):
                    draw_panel(ax, panel, data_dir=data_dir)
            else:
                draw_panel(ax, panel, data_dir=data_dir)


def stage_post_process(
    *,
    built: BuiltLayout,
    spec: FigureSpec,
) -> None:
    """Apply titles, labels, and other figure-level post-processing."""
    fig = built.figure

    if spec.title:
        title_kw = spec.title_kwargs.to_kwargs() if spec.title_kwargs else {}
        fig.suptitle(spec.title, **title_kw)

    for panel in spec.panels:
        if panel.label and panel.name in built.axes:
            ax = built.axes[panel.name]
            ax.set_title(panel.label)

    for panel in spec.panels:
        if panel.hide_spines and panel.name in built.axes:
            ax = built.axes[panel.name]
            for spine_name in panel.hide_spines:
                ax.spines[spine_name].set_visible(False)
            if "top" in panel.hide_spines:
                ax.tick_params(top=False)
            if "bottom" in panel.hide_spines:
                ax.tick_params(bottom=False)
            if "right" in panel.hide_spines:
                ax.tick_params(right=False)
            if "left" in panel.hide_spines:
                ax.tick_params(left=False)

    if spec.margin_labels:
        from eikon.render._margin_labels import draw_margin_labels

        draw_margin_labels(fig, built, spec.margin_labels)

    if spec.shared_legend is not None:
        _apply_shared_legend(fig, spec.panels, built, spec.shared_legend)


def stage_export(
    *,
    figure: Any,
    spec: FigureSpec,
    output_dir: Path,
    export_defaults: Any,
    cli_formats: tuple[str, ...],
) -> dict[str, Path]:
    """Run the export pipeline for the rendered figure."""
    from eikon.export._batch import batch_export

    return batch_export(
        figure=figure,
        name=spec.name,
        group=spec.group,
        output_dir=output_dir,
        export_defaults=export_defaults,
        export_spec=spec.export,
        cli_formats=cli_formats,
    )


# ---------------------------------------------------------------------------
# Orchestrator — thin composition of stages
# ---------------------------------------------------------------------------


def render_figure(
    spec: FigureSpec,
    *,
    session: ProjectSession | None = None,
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
    session : ProjectSession, optional
        A pre-built project session.  Takes precedence over *config*
        and *resolved_paths*.
    config : ProjectConfig, optional
        Project configuration.  Defaults to built-in defaults.
    resolved_paths : ResolvedPaths, optional
        Pre-resolved paths.
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

    if session is not None:
        sess = session
    elif config is not None or resolved_paths is not None:
        sess = ProjectSession.from_config(config=config, strict=False)
        if resolved_paths is not None:
            sess = ProjectSession(config=sess.config, paths=resolved_paths)
    else:
        sess = ProjectSession.from_config(strict=False)

    cfg = sess.config
    paths = sess.paths

    try:
        # Stage 1: Style resolution
        resolved_style = stage_resolve_style(
            style_ref=spec.style,
            base_style=cfg.style.base_style,
            styles_dir=paths.styles_dir,
        )

        fire_hook(HookName.PRE_RENDER, spec=spec, config=cfg)

        # Stage 2: Layout building
        figure_size = (
            resolved_style.sheet.figure_size
            if resolved_style.sheet.figure_size
            else cfg.style.figure_size
        )
        resolved_layout = stage_build_layout(
            layout_spec=spec.layout or LayoutSpec(),
            panels=spec.panels,
            style=resolved_style.sheet,
            figure_size=figure_size,
            dpi=cfg.export.dpi,
        )

        # Stage 3: Panel drawing
        stage_draw_panels(
            panels=spec.panels,
            built=resolved_layout.built,
            style=resolved_style.sheet,
            styles_dir=paths.styles_dir,
            data_dir=paths.data_dir,
        )

        # Stage 4: Post-processing
        stage_post_process(built=resolved_layout.built, spec=spec)

        fire_hook(HookName.POST_RENDER, spec=spec, layout=resolved_layout.built)
    except Exception as exc:
        if not isinstance(exc, RenderError):
            msg = f"Rendering failed for {spec.name!r}: {exc}"
            raise RenderError(msg) from exc
        raise

    handle = FigureHandle(
        spec=spec,
        figure=resolved_layout.built.figure,
        axes=dict(resolved_layout.built.axes),
    )

    # Stage 5: Export (after rendering, before show)
    if formats and handle.figure is not None:
        try:
            export_paths = stage_export(
                figure=handle.figure,
                spec=spec,
                output_dir=paths.output_dir,
                export_defaults=cfg.export,
                cli_formats=formats,
            )
            handle.export_paths = export_paths
        except Exception as exc:
            if not isinstance(exc, RenderError):
                msg = f"Export failed for {spec.name!r}: {exc}"
                raise RenderError(msg) from exc
            raise

    if show:
        handle.show()

    return handle


# ---------------------------------------------------------------------------
# Internal helpers
# ---------------------------------------------------------------------------


def _build_style_registry(
    search_dirs: tuple[Path, ...],
) -> dict[str, StyleSheet]:
    """Build a style registry from presets and user style files."""
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


def _apply_shared_legend(
    fig: Any,
    panels: tuple[PanelSpec, ...],
    built: BuiltLayout,
    legend_config: SharedLegendConfig,
) -> None:
    """Collect handles from the first panel and place a figure-level legend."""
    handles: list[Any] = []
    labels: list[str] = []
    for panel in panels:
        if panel.name in built.axes:
            ax = built.axes[panel.name]
            h, lab = ax.get_legend_handles_labels()
            if h and not handles:
                handles, labels = h, lab
            legend = ax.get_legend()
            if legend is not None:
                legend.remove()
    if handles:
        fig.legend(handles, labels, **legend_config.to_kwargs())
