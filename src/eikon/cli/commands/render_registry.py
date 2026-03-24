from pathlib import Path

import typer

from eikon import load_registry
from eikon.cli.commands import get_project_root
from eikon.config._session import ProjectSession
from eikon.render._pipeline import render_figure
from eikon.spec._parse import parse_figure_file


def cli_render_by_name(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Registered figure name"),
    formats: list[str] = typer.Option([], "--format", "-f", help="Export formats"),
    show: bool = typer.Option(False, "--show", help="Display figure interactively."),
) -> None:
    """Render a figure by registry name."""
    session = ProjectSession.from_config(project_root=get_project_root(ctx))
    reg = load_registry(config=session.config)

    entry = reg.get(name)
    raw_path = entry.get("spec_path", "") if isinstance(entry, dict) else ""
    if raw_path:
        spec_path = Path(raw_path)
    else:
        spec_path = session.paths.specs_dir / f"{name}.yaml"

    if not spec_path.is_file():
        typer.echo(
            f"Spec file not found for registered figure {name!r}: {spec_path}", err=True
        )
        raise typer.Exit(code=1)

    figure_spec = parse_figure_file(spec_path)
    fmt_tuple = tuple(formats) if formats else ()

    handle = render_figure(
        figure_spec,
        session=session,
        formats=fmt_tuple,
        show=show,
    )

    if handle.export_paths:
        typer.echo(f"Rendered {figure_spec.name!r}:")
        for fmt_name, path in sorted(handle.export_paths.items()):
            typer.echo(f"  {fmt_name}: {path}")
    else:
        typer.echo(f"Rendered {figure_spec.name!r} (no export formats specified).")

    handle.close()
