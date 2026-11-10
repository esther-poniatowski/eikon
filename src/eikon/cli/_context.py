"""Project session built from the global options of the command line.

The root callback stores ``--root`` and ``--config`` in the context object; each command that works
on a project builds its session here, so that every command resolves the root and the settings file
in one way and reports a configuration error with the same exit status.
"""

from pathlib import Path

import typer

from eikon.config._session import ProjectSession
from eikon.exceptions import ConfigError

__all__ = ["USAGE_ERROR", "session_from_context"]

USAGE_ERROR = 2
"""Exit status of a usage or configuration error."""


def session_from_context(ctx: typer.Context) -> ProjectSession:
    """Build the project session from the ``--root`` and ``--config`` global options.

    Parameters
    ----------
    ctx : typer.Context
        Context of the running command.

    Returns
    -------
    ProjectSession
        Session of the project root, with the settings file named by ``--config``, the settings
        file found below the root, or the built-in defaults.

    Raises
    ------
    typer.Exit
        With status :data:`USAGE_ERROR` when the settings file is absent, conflicting or invalid.
    """
    obj = ctx.find_root().obj
    options: dict[str, Path] = obj if isinstance(obj, dict) else {}
    try:
        return ProjectSession.from_config(
            project_root=options.get("root"),
            config_path=options.get("config"),
        )
    except ConfigError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=USAGE_ERROR) from exc
