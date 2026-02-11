from pathlib import Path

import typer


def cli_init(
    path: str = typer.Argument(".", help="Project directory to initialize."),
) -> None:
    """Initialize an eikon project."""
    project_dir = Path(path).resolve()
    config_path = project_dir / "eikon.yaml"

    if config_path.exists():
        typer.echo(f"eikon.yaml already exists in {project_dir}")
        raise typer.Exit(code=1)

    dirs = ["figures", "styles", "specs", "data"]
    for dirname in dirs:
        (project_dir / dirname).mkdir(parents=True, exist_ok=True)

    default_yaml = """\
# Eikon project configuration
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
  font_family: sans-serif
  font_size: 10.0
  figure_size: [6.4, 4.8]

registry_file: eikon-registry.yaml
"""
    config_path.write_text(default_yaml, encoding="utf-8")

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
