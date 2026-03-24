# Eikon

[![Conda](https://img.shields.io/badge/conda-eresthanaconda--channel-blue)](#installation)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)]()
[![Last Commit](https://img.shields.io/github/last-commit/esther-poniatowski/eikon)](https://github.com/esther-poniatowski/eikon/commits/main)
[![Python](https://img.shields.io/badge/python-%3E%3D3.12-blue)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

Figure management library for declarative, reproducible scientific visualizations.

---

## Overview

### Motivations

Scientific workflows require reproducible, publication-quality figures with consistent styling across
analyses. Managing figures manually becomes error-prone as the number of panels, conditions, and
output formats grows. Coordinating layout, aesthetics, and export settings across a project demands
a structured approach.

### Advantages

Eikon manages scientific figures built on Matplotlib: define figures declaratively in YAML, apply
composable styles, and export to multiple formats with a single command.

---

## Features

- [x] **Declarative figure specifications**: Define figures as structured objects with layout,
  styling, and export settings in YAML or Python.
- [x] **Data binding**: Specify data sources, column mappings, and reusable transforms for each panel.
- [x] **Consistent styling**: Apply composable style sheets with built-in presets
  (publication, presentation, poster) and custom YAML styles.
- [x] **Layout management**: Compose multi-panel figures with flexible grid specifications,
  shared axes, colorbars, and insets.
- [x] **Export pipeline**: Batch export figures to PDF, SVG, and PNG with configurable
  resolution, injected metadata, and filename templates.
- [x] **Figure registry**: Track and organize figures across analyses with tags, groups, and
  a registry manifest backed by YAML.
- [x] **Extensibility**: Register custom plot types via decorators, add data transforms,
  and hook into the render/export lifecycle. Plugin discovery via entry points.

---

## Installation

### Using pip

```bash
pip install git+https://github.com/esther-poniatowski/eikon.git
```

### From source

```bash
git clone https://github.com/esther-poniatowski/eikon.git
cd eikon
pip install -e .
```

For development tools:

```bash
pip install -e ".[dev]"
```

---

## Quick Start

### Initialize a project

```bash
eikon init
```

The `init` command creates `eikon.yaml`, `specs/`, `styles/`, `figures/`, and `data/` directories.

### Write a figure spec

Create `specs/example.yaml`:

```yaml
name: example
title: "Example Figure"
panels:
  - name: A
    plot_type: line
    params:
      color: blue
layout:
  rows: 1
  cols: 1
style: publication
export:
  formats: [pdf, svg]
  dpi: 300
```

### Render from the CLI

```bash
eikon render specs/example.yaml --format pdf --format svg
```

### Render from Python

```python
import eikon

handle = eikon.render("example", formats=("pdf", "svg"))
print(handle.export_paths)
handle.close()
```

---

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `EIKON_PROJECT_ROOT` | Explicit project root directory | Auto-discovered | No |

### Configuration File

Project settings are specified in `eikon.yaml` at the project root:

```yaml
paths:
  output_dir: figures
  styles_dir: styles
  specs_dir: specs
  data_dir: data

export:
  formats: [pdf]
  dpi: 300
  transparent: false
  metadata:
    author: "Author Name"

style:
  base_style: default
  font_family: serif
  font_size: 10.0
  figure_size: [6.4, 4.8]

registry_file: eikon-registry.yaml
```

---

## Documentation

- [User Guide](docs/guide/) — Getting started, configuration, specifications, styles, layouts,
  rendering, export, registry, CLI, and extensions.
- [API Reference](docs/api/) — Complete reference for all public classes, functions, and protocols.

To build the docs locally:

```bash
pip install -e ".[docs]"
cd docs && make html
open _build/html/index.html
```

### Data transform registry

Register reusable data-processing steps and reference them by name in YAML specs:

- `eikon.ext.register_transform(name, fn)` — add a transform callable.
- `eikon.ext.list_transforms()` — list registered transforms.
- `eikon.ext.clear_transforms()` — clear all transforms (useful for tests or long-running sessions).

---

## Support

**Issues**: [GitHub Issues](https://github.com/esther-poniatowski/eikon/issues)

---

## Acknowledgments

### Authors & Contributors

**Author**: @esther-poniatowski

For academic use, please cite using the GitHub "Cite this repository" feature to
generate a citation in various formats.

### Third-Party Dependencies

- **[Matplotlib](https://matplotlib.org/)** — Plotting library
- **[NumPy](https://numpy.org/)** — Array operations
- **[PyYAML](https://pyyaml.org/)** — YAML parsing
- **[Typer](https://typer.tiangolo.com/)** — CLI framework
- **[Rich](https://rich.readthedocs.io/)** — Terminal formatting

---

## License

This project is licensed under the terms of the [GNU General Public License v3.0](LICENSE).
