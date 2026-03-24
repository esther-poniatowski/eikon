from pathlib import Path

import typer

from eikon.cli.commands import get_project_root
from eikon.config._session import ProjectSession
from eikon.render._pipeline import render_figure
from eikon.spec._parse import parse_figure_file


def cli_render(
    ctx: typer.Context,
    spec_path: str = typer.Argument(..., help="Path to a figure spec YAML file."),
    formats: list[str] = typer.Option(  # noqa: B006
        [], "--format", "-f", help="Export format(s): pdf, svg, png."
    ),
    show: bool = typer.Option(False, "--show", help="Display figure interactively."),
) -> None:
    """Render and export a figure."""
    target_path = Path(spec_path).resolve()
    if not target_path.is_file():
        typer.echo(f"Spec file not found: {target_path}", err=True)
        raise typer.Exit(code=1)

    try:
        figure_spec = parse_figure_file(target_path)
    except Exception as exc:  # pragma: no cover - CLI surface
        typer.echo(f"Failed to parse spec: {exc}", err=True)
        raise typer.Exit(code=1)

    fmt_tuple = tuple(formats) if formats else ()

    try:
        session = ProjectSession.from_config(project_root=get_project_root(ctx))
        handle = render_figure(
            figure_spec,
            session=session,
            formats=fmt_tuple,
            show=show,
        )
    except Exception as exc:  # pragma: no cover - CLI surface
        typer.echo(f"Render failed: {exc}", err=True)
        raise typer.Exit(code=1)

    if handle.export_paths:
        typer.echo(f"Rendered {figure_spec.name!r}:")
        for fmt_name, path in sorted(handle.export_paths.items()):
            typer.echo(f"  {fmt_name}: {path}")
    else:
        typer.echo(f"Rendered {figure_spec.name!r} (no export formats specified).")

    handle.close()
