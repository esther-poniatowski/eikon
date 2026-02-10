"""CLI entry that re-exports the Typer app from subcommands."""

from eikon.cli._app import app

__all__ = ["app"]
