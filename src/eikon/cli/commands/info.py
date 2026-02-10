import typer

from eikon import info as info_fn


def cli_info() -> None:
    """Display version and platform info."""
    typer.echo(info_fn())
