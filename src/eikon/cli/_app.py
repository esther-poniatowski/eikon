"""Top-level Typer app wiring subcommands together."""

import typer

from eikon import __version__
from eikon.cli import commands

app = typer.Typer(add_completion=False)


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
    """Root command for the package CLI."""
    from pathlib import Path

    if version:
        typer.echo(__version__)
        raise typer.Exit()
    ctx.ensure_object(dict)
    if project_root:
        ctx.obj["project_root"] = Path(project_root).resolve()
    if ctx.invoked_subcommand is None:
        typer.echo(ctx.get_help())


# Standalone commands registered directly on the root app
app.command("info")(commands.info.cli_info)
app.command("init")(commands.init.cli_init)
app.command("validate")(commands.validate.cli_validate)
app.command("render")(commands.render.cli_render)
app.command("batch")(commands.batch.cli_batch)
app.command("render-registry")(commands.render_registry.cli_render_by_name)

# Registry has real subcommands — wire as a Typer sub-app
app.add_typer(commands.registry.app, name="registry")
