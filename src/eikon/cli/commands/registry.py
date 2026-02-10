import json

import typer

from eikon import load_registry
from eikon.config._loader import load_config
from eikon.config._resolver import resolve_paths
from eikon.exceptions import RegistryError
from eikon.registry import Registry

app = typer.Typer(add_completion=False, help="Manage the figure registry")


def _load_reg() -> Registry:
    config = load_config()
    paths = resolve_paths(config.paths)
    reg = load_registry(config=config)
    reg.path = paths.project_root / config.registry_file
    return reg


@app.command("list")
def registry_list(
    tags: list[str] = typer.Option(
        [], "--tag", "-t", help="Filter by tag (repeatable)."
    ),
    group: str = typer.Option("", "--group", "-g", help="Filter by group."),
    match_all: bool = typer.Option(
        False, "--match-all", help="Require all tags to match."
    ),
) -> None:
    reg = _load_reg()

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
    reg = _load_reg()

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
    name: str = typer.Argument(..., help="Figure name to remove."),
) -> None:
    reg = _load_reg()

    try:
        reg.remove(name)
        reg.save()
    except RegistryError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    typer.echo(f"Removed {name!r}.")


@app.command("show")
def registry_show(
    name: str = typer.Argument(..., help="Figure name to show."),
) -> None:
    reg = _load_reg()

    try:
        entry = reg.get(name)
    except RegistryError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    typer.echo(f"{name}:")
    typer.echo(json.dumps(entry, indent=2, default=str))
