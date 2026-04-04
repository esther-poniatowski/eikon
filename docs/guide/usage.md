# Usage

Eikon manages scientific figures through a declarative workflow: define figure
specifications in YAML, apply composable styles, and export to multiple formats.
Both a CLI and a Python API expose the same functionality.

For the full command registry, refer to [CLI Reference](cli.md). For project
settings and export defaults, refer to [Configuration](configuration.md).

## Setting Up a Project

The `init` command scaffolds a new project with the standard directory layout:

```sh
mkdir my-figures && cd my-figures
eikon init
```

The command creates:

```
my-figures/
    eikon.yaml          # Project configuration
    specs/              # Figure specification YAML files
    styles/             # Custom style files
    figures/            # Exported figures (output)
    data/               # Data sources
```

## Registering a Plot Type

Every panel requires a plot function. Custom plot types register via the
`@plot_type` decorator:

```python
from eikon.ext import plot_type

@plot_type("my_line")
def draw_line(ax, /, **kwargs):
    x = kwargs.get("x", [0, 1, 2])
    y = kwargs.get("y", [0, 1, 4])
    ax.plot(x, y)
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
```

Eikon ships built-in wrappers for common matplotlib and seaborn plot types (see
[Extensions](extensions.md)).

## Writing a Figure Specification

Create `specs/first-figure.yaml`:

```yaml
name: first-figure
title: "My First Figure"
panels:
  - name: A
    plot_type: my_line
```

The specification defines the figure declaratively: panel layout, plot types,
data bindings, styling, and export settings all reside in the YAML file.

## Rendering a Figure

**From the command line:**

```sh
eikon render specs/first-figure.yaml --format pdf --format png
```

**From Python:**

```python
import eikon

handle = eikon.render("first-figure", formats=("pdf", "png"))
print(handle.export_paths)
handle.close()
```

The exported files appear in the `figures/` directory (configurable via
`eikon.yaml`).

## Composing Multi-Panel Figures

A 1x2 grid with two panels:

```yaml
name: two-panels
panels:
  - name: A
    plot_type: my_line
    row: 0
    col: 0
  - name: B
    plot_type: scatter
    row: 0
    col: 1
    params:
      color: red
layout:
  rows: 1
  cols: 2
  width_ratios: [2, 1]
```

## Applying Consistent Styling

Composable style sheets control how figures look:

```yaml
style: publication
```

Built-in presets include `publication`, `presentation`, and `poster`. Custom
styles are defined as YAML files in the `styles/` directory. See
[Styles](styles.md) for the full reference.

## Batch Export

The export pipeline supports multiple formats, resolution settings, and embedded
metadata in a single invocation:

```sh
eikon render specs/ --format pdf --format svg --format png
```

## Managing a Figure Registry

Track and organize figures across analyses with tags and groups:

```sh
eikon registry list
eikon registry add specs/first-figure.yaml --tags analysis,main
```

The registry manifest (`eikon-registry.yaml`) provides a structured index of all
figures in the project. See [Registry](registry.md) for the full reference.

## Next Steps

- [Configuration](configuration.md) — Project settings, paths, export defaults.
- [Specifications](specifications.md) — Full reference for figure and panel specs.
- [Styles](styles.md) — Style sheets, presets, composition.
- [Layouts](layouts.md) — Grids, shared axes, colorbars, insets.
- [Extensions](extensions.md) — Custom plot types, transforms, hooks.
- [CLI Reference](cli.md) — Full command registry and options.
