from __future__ import annotations

from pathlib import Path

import typer

from eikon.cli.commands import (
    batch,
    info,
    init,
    registry,
    render,
    render_registry,
    validate,
)

__all__ = [
    "info",
    "init",
    "validate",
    "render",
    "batch",
    "registry",
    "render_registry",
    "get_project_root",
]


def get_project_root(ctx: typer.Context) -> Path | None:
    """Extract the ``--project-root`` value from the CLI context, if set."""
    obj = ctx.find_root().obj
    if isinstance(obj, dict):
        return obj.get("project_root")
    return None
