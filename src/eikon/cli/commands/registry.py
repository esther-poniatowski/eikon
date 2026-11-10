import json
from pathlib import Path

import typer

from eikon import load_registry
from eikon.cli._context import session_from_context
from eikon.exceptions import RegistryError
from eikon.registry import Registry

app = typer.Typer(add_completion=False, help="Manage the figure registry")


def _load_reg(ctx: typer.Context) -> Registry:
    session = session_from_context(ctx)
    return load_registry(config=session.config, resolved_paths=session.paths)


def _stored_spec_path(spec_path: str, root: Path) -> str | None:
    """Return the spec path to store in the registry, relative to *root* when it lies below it.

    The command line gives the path relative to the current folder, and the registry keeps it
    relative to the project root, which ``render-registry`` reads it against.
    """
    if not spec_path:
        return None
    resolved = Path(spec_path).resolve()
    try:
        return resolved.relative_to(root).as_posix()
    except ValueError:
        return str(resolved)


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
    reg = _load_reg(ctx)

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
        help=(
            "Path to the figure spec YAML file, relative to the current folder; "
            "the registry stores it relative to the project root."
        ),
    ),
) -> None:
    session = session_from_context(ctx)
    reg = load_registry(config=session.config, resolved_paths=session.paths)

    try:
        reg.register(
            name,
            tags=tuple(tags),
            group=group,
            on_conflict=on_conflict,  # type: ignore[arg-type]
            spec_path=_stored_spec_path(spec_path, session.paths.project_root),
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
    reg = _load_reg(ctx)

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
    reg = _load_reg(ctx)

    try:
        entry = reg.get(name)
    except RegistryError as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(code=1)

    typer.echo(f"{name}:")
    typer.echo(json.dumps(entry, indent=2, default=str))
