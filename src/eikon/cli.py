"""Command-line interface for the `eikon` package.

Defines commands available via ``python -m eikon`` or ``eikon`` if installed as a script.

Commands
--------
info : Display diagnostic information.
init : Initialize an eikon project with configuration and directories.
validate : Validate a configuration or figure specification YAML file.
render : Render and export a figure from a YAML specification.
batch : Batch render multiple figures with progress tracking.
registry : Manage the figure registry (list, add, remove, show).

See Also
--------
typer.Typer
    Library for building CLI applications: https://typer.tiangolo.com/
"""

from pathlib import Path

import typer

from . import __version__, info

app = typer.Typer(add_completion=False)


@app.command("info")
def cli_info() -> None:
    """Display version and platform diagnostics."""
    typer.echo(info())


@app.command("init")
def cli_init(
    path: str = typer.Argument(".", help="Project directory to initialize."),
) -> None:
    """Initialize an eikon project with configuration and directory structure."""
    project_dir = Path(path).resolve()
    config_path = project_dir / "eikon.yaml"

    if config_path.exists():
        typer.echo(f"eikon.yaml already exists in {project_dir}")
        raise typer.Exit(code=1)

    # Create directory structure
    dirs = ["figures", "styles", "specs", "data"]
    for dirname in dirs:
        (project_dir / dirname).mkdir(parents=True, exist_ok=True)

    # Write default configuration
    default_yaml = """\
# Eikon project configuration
# See: https://github.com/esther-poniatowski/eikon
config_version: 1

paths:
  output_dir: figures
  styles_dir: styles
  specs_dir: specs
  data_dir: data

export:
  formats: [pdf]
  dpi: 300
  transparent: false
  metadata: {}

style:
  base_style: default
  font_family: serif
  font_size: 10.0
  figure_size: [6.4, 4.8]

registry_file: eikon-registry.yaml
"""
    config_path.write_text(default_yaml, encoding="utf-8")

    # Write example figure spec
    example_spec_path = project_dir / "specs" / "example.yaml"
    example_spec = """\
# Example figure specification
spec_version: 1
name: example
title: "Example Figure"
tags: [example]
group: ""
panels:
  - name: A
    plot_type: line
    row: 0
    col: 0
    params: {}
    label: "(a)"
layout:
  rows: 1
  cols: 1
style: publication
export:
  formats: [pdf]
  dpi: 300
"""
    example_spec_path.write_text(example_spec, encoding="utf-8")

    typer.echo(f"Initialized eikon project in {project_dir}")
    for dirname in dirs:
        typer.echo(f"  Created {dirname}/")
    typer.echo("  Created eikon.yaml")
    typer.echo("  Created specs/example.yaml")


@app.command("validate")
def cli_validate(
    target: str = typer.Argument(..., help="Path to eikon.yaml or a figure spec YAML file."),
) -> None:
    """Validate a configuration or figure specification YAML file."""
    import yaml

    from .config._validation import validate_config, validate_figure_spec

    target_path = Path(target).resolve()
    if not target_path.is_file():
        typer.echo(f"File not found: {target_path}", err=True)
        raise typer.Exit(code=1)

    try:
        raw = yaml.safe_load(target_path.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        typer.echo(f"YAML parse error: {exc}", err=True)
        raise typer.Exit(code=1)

    if not isinstance(raw, dict):
        typer.echo(f"Expected a YAML mapping, got {type(raw).__name__}.", err=True)
        raise typer.Exit(code=1)

    # Determine whether this is a project config or a figure spec
    if target_path.name == "eikon.yaml" or "paths" in raw or "export" in raw:
        errors = validate_config(raw)
        kind = "Configuration"
    else:
        errors = validate_figure_spec(raw)
        kind = "Figure specification"

    if errors:
        from rich.console import Console
        from rich.panel import Panel

        console = Console(stderr=True)
        body = "\n".join(f"[red]\u2717[/red] {e}" for e in errors)
        console.print(Panel(body, title=f"{kind} validation failed", border_style="red"))
        raise typer.Exit(code=1)

    typer.echo(f"{kind} is valid: {target_path.name}")


@app.command("render")
def cli_render(
    spec_path: str = typer.Argument(..., help="Path to a figure spec YAML file."),
    formats: list[str] = typer.Option(  # noqa: B006
        [], "--format", "-f", help="Export format(s): pdf, svg, png."
    ),
    show: bool = typer.Option(False, "--show", help="Display figure interactively."),
) -> None:
    """Render and export a figure from a YAML specification."""
    from eikon.config._defaults import DEFAULT_CONFIG
    from eikon.render._pipeline import render_figure
    from eikon.spec._parse import parse_figure_file

    target_path = Path(spec_path).resolve()
    if not target_path.is_file():
        typer.echo(f"Spec file not found: {target_path}", err=True)
        raise typer.Exit(code=1)

    try:
        figure_spec = parse_figure_file(target_path)
    except Exception as exc:
        typer.echo(f"Failed to parse spec: {exc}", err=True)
        raise typer.Exit(code=1)

    fmt_tuple = tuple(formats) if formats else ()

    try:
        handle = render_figure(
            figure_spec,
            config=DEFAULT_CONFIG,
            formats=fmt_tuple,
            show=show,
        )
    except Exception as exc:
        typer.echo(f"Render failed: {exc}", err=True)
        raise typer.Exit(code=1)

    if handle.export_paths:
        typer.echo(f"Rendered {figure_spec.name!r}:")
        for fmt_name, path in sorted(handle.export_paths.items()):
            typer.echo(f"  {fmt_name}: {path}")
    else:
        typer.echo(f"Rendered {figure_spec.name!r} (no export formats specified).")

    handle.close()


@app.command("batch")
def cli_batch(
    specs: list[str] = typer.Argument(  # noqa: B006
        None, help="Spec files to render.  If omitted, scans the specs directory."
    ),
    tags: list[str] = typer.Option(  # noqa: B006
        [], "--tag", "-t", help="Filter by tag (repeatable)."
    ),
    group: str = typer.Option("", "--group", "-g", help="Filter by group."),
    match_all: bool = typer.Option(
        False, "--match-all", help="Require all tags to match."
    ),
    formats: list[str] = typer.Option(  # noqa: B006
        [], "--format", "-f", help="Export format(s): pdf, svg, png."
    ),
    continue_on_error: bool = typer.Option(
        True, "--continue-on-error/--fail-fast", help="Continue after errors."
    ),
) -> None:
    """Batch render multiple figures with progress tracking."""
    from rich.console import Console
    from rich.progress import Progress

    from eikon.config._defaults import DEFAULT_CONFIG
    from eikon.render._pipeline import render_figure
    from eikon.spec._parse import parse_figure_file

    console = Console(stderr=True)
    fmt_tuple = tuple(formats) if formats else ()

    # Discover spec files
    if specs:
        spec_paths = [Path(s).resolve() for s in specs]
    else:
        specs_dir = Path.cwd() / DEFAULT_CONFIG.paths.specs_dir
        if not specs_dir.is_dir():
            typer.echo(f"Specs directory not found: {specs_dir}", err=True)
            raise typer.Exit(code=1)
        spec_paths = sorted(specs_dir.glob("*.yaml"))
        if not spec_paths:
            typer.echo(f"No YAML spec files found in {specs_dir}", err=True)
            raise typer.Exit(code=1)

    # Parse specs and apply tag/group filters
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

    # Render with progress
    rendered = 0
    failed = 0
    all_paths: dict[str, dict[str, Path]] = {}

    with Progress(console=console) as progress:
        task = progress.add_task("Rendering figures", total=len(figure_specs))
        for fs in figure_specs:
            progress.update(task, description=f"Rendering {fs.name!r}")
            try:
                handle = render_figure(
                    fs, config=DEFAULT_CONFIG, formats=fmt_tuple,
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

    # Summary
    typer.echo(f"Batch complete: {rendered} rendered, {failed} failed.")
    for name, paths in sorted(all_paths.items()):
        typer.echo(f"  {name}:")
        for fmt_name, fpath in sorted(paths.items()):
            typer.echo(f"    {fmt_name}: {fpath}")

    if failed > 0:
        raise typer.Exit(code=1)


registry_app = typer.Typer(add_completion=False, help="Manage the figure registry.")
app.add_typer(registry_app, name="registry")


@registry_app.command("list")
def registry_list(
    tags: list[str] = typer.Option(  # noqa: B006
        [], "--tag", "-t", help="Filter by tag (repeatable)."
    ),
    group: str = typer.Option("", "--group", "-g", help="Filter by group."),
    match_all: bool = typer.Option(
        False, "--match-all", help="Require all tags to match."
    ),
) -> None:
    """List registered figures, with optional tag/group filters."""
    from eikon import load_registry

    reg = load_registry()

    if tags or group:
        entries = reg.query(
            tags=tuple(tags), group=group, match_all_tags=match_all
        )
    else:
        entries = {name: reg.get(name) for name in reg.list_all()}

    if not entries:
        typer.echo("No figures found.")
        raise typer.Exit()

    for name in sorted(entries):
        entry = entries[name]
        parts = [name]
        if entry.get("group"):
            parts.append(f"[{entry['group']}]")
        if entry.get("tags"):
            parts.append(", ".join(entry["tags"]))
        typer.echo("  ".join(parts))


@registry_app.command("add")
def registry_add(
    name: str = typer.Argument(..., help="Figure name to register."),
    tags: list[str] = typer.Option(  # noqa: B006
        [], "--tag", "-t", help="Tag (repeatable)."
    ),
    group: str = typer.Option("", "--group", "-g", help="Group key."),
    on_conflict: str = typer.Option(
        "update", "--on-conflict", help="Conflict strategy: update, fail, skip."
    ),
) -> None:
    """Register a figure in the registry."""
    from eikon import load_registry
    from eikon.exceptions import RegistryError

    reg = load_registry()

    try:
        reg.register(
            name,
            tags=tuple(tags),
            group=group,
            on_conflict=on_conflict,  # type: ignore[arg-type]
        )
        reg.save()
    except RegistryError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Registered {name!r}.")


@registry_app.command("remove")
def registry_remove(
    name: str = typer.Argument(..., help="Figure name to remove."),
) -> None:
    """Remove a figure from the registry."""
    from eikon import load_registry
    from eikon.exceptions import RegistryError

    reg = load_registry()

    try:
        reg.remove(name)
        reg.save()
    except RegistryError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Removed {name!r}.")


@registry_app.command("show")
def registry_show(
    name: str = typer.Argument(..., help="Figure name to show."),
) -> None:
    """Show details for a registered figure."""
    import json

    from eikon import load_registry
    from eikon.exceptions import RegistryError

    reg = load_registry()

    try:
        entry = reg.get(name)
    except RegistryError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    typer.echo(f"{name}:")
    typer.echo(json.dumps(entry, indent=2, default=str))


@app.callback(invoke_without_command=True)
def main_callback(
    ctx: typer.Context,
    version: bool = typer.Option(
        False, "--version", "-v", help="Show the package version and exit."
    ),
    project_root: str = typer.Option(
        "",
        "--project-root",
        help="Explicit project root directory, overriding auto-discovery.",
    ),
) -> None:
    """Root command for the package command-line interface."""
    if version:
        typer.echo(__version__)
        raise typer.Exit()
    if project_root:
        import os

        os.environ["EIKON_PROJECT_ROOT"] = str(Path(project_root).resolve())
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())
