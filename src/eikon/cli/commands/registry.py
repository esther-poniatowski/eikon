import json
from pathlib import Path

import typer

from eikon import load_registry
from eikon.cli.commands import get_project_root
from eikon.config._session import ProjectSession
from eikon.exceptions import RegistryError
from eikon.registry import Registry

app = typer.Typer(add_completion=False, help="Manage the figure registry")


def _load_reg(project_root: Path | None = None) -> Registry:
    session = ProjectSession.from_config(project_root=project_root)
    reg = load_registry(config=session.config)
    reg.path = session.paths.project_root / session.config.registry_file
    return reg


@app.command("list")
def registry_list(
    ctx: typer.Context,
    tags: list[str] = typer.Option(
        [], "--tag", "-t", help="Filter by tag (repeatable)."
    ),
    group: str = typer.Option("", "--group", "-g", help="Filter by group."),
    match_all: bool = typer.Option(
        False, "--match-all", help="Require all tags to match."
    ),
) -> None:
    reg = _load_reg(get_project_root(ctx))

    if tags or group:
        entries = reg.query(tags=tuple(tags), group=group, match_all_tags=match_all)
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


@app.command("add")
def registry_add(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Figure name to register."),
    tags: list[str] = typer.Option(
        [], "--tag", "-t", help="Tag (repeatable)."
    ),
    group: str = typer.Option("", "--group", "-g", help="Group key."),
    on_conflict: str = typer.Option(
        "update", "--on-conflict", help="Conflict strategy: update, fail, skip."
    ),
    spec_path: str = typer.Option(
        "",
        "--spec-path",
        help="Path to the figure spec YAML file (stored in registry metadata).",
    ),
) -> None:
    reg = _load_reg(get_project_root(ctx))

    try:
        reg.register(
            name,
            tags=tuple(tags),
            group=group,
            on_conflict=on_conflict,  # type: ignore[arg-type]
            spec_path=spec_path or None,
        )
        reg.save()
    except RegistryError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Registered {name!r}.")


@app.command("remove")
def registry_remove(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Figure name to remove."),
) -> None:
    reg = _load_reg(get_project_root(ctx))

    try:
        reg.remove(name)
        reg.save()
    except RegistryError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Removed {name!r}.")


@app.command("show")
def registry_show(
    ctx: typer.Context,
    name: str = typer.Argument(..., help="Figure name to show."),
) -> None:
    reg = _load_reg(get_project_root(ctx))

    try:
        entry = reg.get(name)
    except RegistryError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    typer.echo(f"{name}:")
    typer.echo(json.dumps(entry, indent=2, default=str))
