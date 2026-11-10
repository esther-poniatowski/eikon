from pathlib import Path

import typer

from eikon.cli._context import USAGE_ERROR
from eikon.config._defaults import CONFIG_FILENAME
from eikon.config._resolver import locate_config
from eikon.exceptions import ConfigConflictError


def cli_init(
    path: str = typer.Argument(".", help="Project directory to initialize."),
    force: bool = typer.Option(
        False, "--force", help="Overwrite the settings file and the example specs if they exist."
    ),
) -> None:
    """Initialize an eikon project."""
    project_dir = Path(path).resolve()
    try:
        config_path = locate_config(project_dir) or project_dir / CONFIG_FILENAME
    except ConfigConflictError as exc:
        typer.echo(f"Error: {exc}", err=True)
        raise typer.Exit(code=USAGE_ERROR) from exc
    example_spec_path = project_dir / "specs" / "example.yaml"
    multi_spec_path = project_dir / "specs" / "multi-panel-example.yaml"

    # The scaffolded files may hold edits of the researcher, which eikon cannot regenerate.
    existing = [p for p in (config_path, example_spec_path, multi_spec_path) if p.exists()]
    if existing and not force:
        names = ", ".join(str(p) for p in existing)
        typer.echo(f"Error: refusing to overwrite {names}; pass --force to overwrite.", err=True)
        raise typer.Exit(code=USAGE_ERROR)

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

    example_spec = """\
# Example figure specification — single panel
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

    multi_spec = """\
# Example figure specification — multi-panel layout
spec_version: 1
name: multi-panel-example
title: "Multi-Panel Figure"
title_kwargs:
  fontsize: 14
  y: 0.95
tags: [example]
panels:
  - name: A
    plot_type: line
    row: 0
    col: 0
    label: "(a)"
    hide_spines: [top, right]
  - name: B
    plot_type: scatter
    row: 0
    col: 1
    label: "(b)"
    hide_spines: [top, right]
  - name: C
    plot_type: bar
    row: 1
    col: [0, 1]
    label: "(c)"
    hide_spines: [top, right]
layout:
  rows: 2
  cols: 2
  height_ratios: [1.0, 0.8]
  hspace: 0.3
  wspace: 0.25
shared_legend:
  loc: upper right
style: publication
export:
  formats: [pdf, png]
  dpi: 300
"""
    multi_spec_path.write_text(multi_spec, encoding="utf-8")

    typer.echo(f"Initialized eikon project in {project_dir}")
    for dirname in dirs:
        typer.echo(f"  Created {dirname}/")
    typer.echo(f"  Created {config_path.relative_to(project_dir).as_posix()}")
    typer.echo("  Created specs/example.yaml")
    typer.echo("  Created specs/multi-panel-example.yaml")
