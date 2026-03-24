from pathlib import Path

import typer
from rich.console import Console
from rich.progress import Progress

from eikon.cli.commands import get_project_root
from eikon.config._session import ProjectSession
from eikon.render._pipeline import render_figure
from eikon.spec._parse import parse_figure_file


def cli_batch(
    ctx: typer.Context,
    specs: list[str] = typer.Argument(
        None, help="Spec files to render. If omitted, scans the specs directory."
    ),
    tags: list[str] = typer.Option(
        [], "--tag", "-t", help="Filter by tag (repeatable)."
    ),
    group: str = typer.Option("", "--group", "-g", help="Filter by group."),
    match_all: bool = typer.Option(
        False, "--match-all", help="Require all tags to match."
    ),
    formats: list[str] = typer.Option(
        [], "--format", "-f", help="Export format(s): pdf, svg, png."
    ),
    continue_on_error: bool = typer.Option(
        True, "--continue-on-error/--fail-fast", help="Continue after errors."
    ),
) -> None:
    """Batch render figures."""
    console = Console(stderr=True)
    fmt_tuple = tuple(formats) if formats else ()

    session = ProjectSession.from_config(project_root=get_project_root(ctx))

    if specs:
        spec_paths = [Path(s).resolve() for s in specs]
    else:
        specs_dir = session.paths.specs_dir
        if not specs_dir.is_dir():
            typer.echo(f"Specs directory not found: {specs_dir}", err=True)
            raise typer.Exit(code=1)
        spec_paths = sorted(specs_dir.glob("*.yaml"))
        if not spec_paths:
            typer.echo(f"No YAML spec files found in {specs_dir}", err=True)
            raise typer.Exit(code=1)

    figure_specs = []
    for sp in spec_paths:
        if not sp.is_file():
            console.print(f"[yellow]Skipping missing file: {sp}[/yellow]")
            continue
        try:
            fs = parse_figure_file(sp)
        except Exception as exc:
            console.print(f"[yellow]Skipping {sp.name}: {exc}[/yellow]")
            continue
        if tags:
            spec_tags = set(fs.tags)
            tag_set = set(tags)
            if match_all and not (tag_set <= spec_tags):
                continue
            if not match_all and not (tag_set & spec_tags):
                continue
        if group and fs.group != group:
            continue
        figure_specs.append(fs)

    if not figure_specs:
        typer.echo("No matching figures found.")
        raise typer.Exit()

    rendered = 0
    failed = 0
    all_paths: dict[str, dict[str, Path]] = {}

    with Progress(console=console) as progress:
        task = progress.add_task("Rendering figures", total=len(figure_specs))
        for fs in figure_specs:
            progress.update(task, description=f"Rendering {fs.name!r}")
            try:
                handle = render_figure(
                    fs,
                    session=session,
                    formats=fmt_tuple,
                )
                if handle.export_paths:
                    all_paths[fs.name] = dict(handle.export_paths)
                handle.close()
                rendered += 1
            except Exception as exc:
                failed += 1
                console.print(f"[red]Failed {fs.name!r}: {exc}[/red]")
                if not continue_on_error:
                    progress.stop()
                    typer.echo(
                        f"Aborted: {rendered} rendered, {failed} failed.",
                        err=True,
                    )
                    raise typer.Exit(code=1)
            progress.advance(task)

    typer.echo(f"Batch complete: {rendered} rendered, {failed} failed.")
    for name, paths_map in sorted(all_paths.items()):
        typer.echo(f"  {name}:")
        for fmt_name, fpath in sorted(paths_map.items()):
            typer.echo(f"    {fmt_name}: {fpath}")

    if failed > 0:
        raise typer.Exit(code=1)
