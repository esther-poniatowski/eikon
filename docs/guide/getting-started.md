# Getting Started

## Installation

### From PyPI (pip)

```bash
pip install eikon
```

### From source

```bash
git clone https://github.com/esther-poniatowski/eikon.git
cd eikon
pip install -e .
```

For development tools (pytest, mypy, ruff):

```bash
pip install -e ".[dev]"
```

### Requirements

- Python >= 3.12
- matplotlib >= 3.8
- numpy >= 1.26
- PyYAML >= 6.0
- Typer, Rich (installed automatically)

## Initializing a project

Run `eikon init` to scaffold a new project:

```bash
mkdir my-figures && cd my-figures
eikon init
```

This creates:

```
my-figures/
    eikon.yaml          # Project configuration
    specs/              # Figure specification YAML files
    styles/             # Custom style files
    figures/            # Exported figures (output)
    data/               # Data sources
```

See the {doc}`CLI reference </guide/cli>` for all `eikon init` options.

## Your first figure

### 1. Register a plot type

Every panel needs a plot function. Register one in your Python code:

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

Eikon ships with built-in wrappers for common matplotlib and seaborn plot types (see {doc}`/guide/extensions`).

### 2. Write a figure spec

Create `specs/first-figure.yaml`:

```yaml
name: first-figure
title: "My First Figure"
panels:
  - name: A
    plot_type: my_line
```

### 3. Render the figure

**From Python:**

```python
import eikon

handle = eikon.render("first-figure", formats=("pdf", "png"))
print(handle.export_paths)  # {"pdf": Path(...), "png": Path(...)}
handle.close()
```

**From the command line:**

```bash
eikon render specs/first-figure.yaml --format pdf --format png
```

The exported files appear in the `figures/` directory (configurable via `eikon.yaml`).

### 4. Multi-panel figures

Create a 1x2 grid with two panels:

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

## Next steps

- {doc}`configuration` — Customize paths, export defaults, and styles
- {doc}`specifications` — Full reference for figure and panel specs
- {doc}`styles` — Apply consistent styling across figures
- {doc}`cli` — Complete CLI command reference
