from pathlib import Path

import typer
import yaml

from eikon.config._validation import validate_config, validate_figure_spec


def cli_validate(
    target: str = typer.Argument(..., help="Path to eikon.yaml or a figure spec YAML file."),
    kind: str = typer.Option(
        "auto",
        "--kind",
        help="Validation target kind: auto, config, or figure.",
    ),
) -> None:
    """Validate config or figure spec YAML."""
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

    normalized_kind = kind.strip().lower()
    if normalized_kind not in {"auto", "config", "figure"}:
        typer.echo(f"Invalid validation kind: {kind}", err=True)
        raise typer.Exit(code=1)

    if normalized_kind == "config" or (
        normalized_kind == "auto" and target_path.name == "eikon.yaml"
    ):
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
