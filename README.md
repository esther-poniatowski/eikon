# Eikon

[![Conda](https://img.shields.io/badge/conda-eresthanaconda--channel-blue)](docs/guide/installation.md)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)]()
[![Last Commit](https://img.shields.io/github/last-commit/esther-poniatowski/eikon)](https://github.com/esther-poniatowski/eikon/commits/main)
[![Python](https://img.shields.io/badge/python-%E2%89%A53.12-blue)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL--3.0-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

Defines and exports Matplotlib figures declaratively for reproducible scientific
visualizations.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Documentation](#documentation)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Overview

### Motivation

Scientific workflows require reproducible, publication-quality figures with consistent
styling across analyses. Managing figures manually becomes error-prone as the number of
panels, conditions, and output formats grows.

### Advantages

- **Declarative specifications** — figures, panels, and export settings are defined as
  structured YAML objects.
- **Composable styling** — built-in presets (publication, presentation, poster) and
  custom YAML style sheets compose freely.
- **Batch export** — render to PDF, SVG, and PNG with configurable resolution, metadata
  injection, and filename templates.
- **Extensibility** — custom plot types register via decorators; data transforms and
  lifecycle hooks extend the pipeline through entry points.

---

## Features

- [x] **Declarative figure specifications**: Define figures with layout, styling, and
  export settings in YAML or Python.
- [x] **Data binding**: Specify data sources, column mappings, and reusable transforms
  for each panel.
- [x] **Consistent styling**: Apply composable style sheets with built-in presets and
  custom YAML styles.
- [x] **Layout management**: Compose multi-panel figures with flexible grids, shared
  axes, colorbars, and insets.
- [x] **Export pipeline**: Batch export to PDF, SVG, and PNG with configurable
  resolution, metadata, and filename templates.
- [x] **Figure registry**: Track and organize figures across analyses with tags, groups,
  and a YAML registry manifest.
- [x] **Extensibility**: Register custom plot types via decorators, add data transforms,
  and hook into the render/export lifecycle.

---

## Quick Start

Initialize a project:

```sh
eikon init
```

Render a figure:

```sh
eikon render specs/example.yaml --format pdf --format svg
```

---

## Documentation

| Guide | Content |
| ----- | ------- |
| [Installation](docs/guide/installation.md) | Prerequisites, pip/source setup |
| [Usage](docs/guide/usage.md) | Project setup, figure specs, rendering, export, registry |
| [Configuration](docs/guide/configuration.md) | `eikon.yaml` settings, paths, export defaults |
| [Specifications](docs/guide/specifications.md) | Figure and panel spec reference |
| [Styles](docs/guide/styles.md) | Style sheets, presets, composition |
| [Layouts](docs/guide/layouts.md) | Grid layouts, shared axes, colorbars, insets |
| [Rendering](docs/guide/rendering.md) | Render pipeline and Python API |
| [Export](docs/guide/export.md) | Formats, resolution, metadata |
| [Registry](docs/guide/registry.md) | Figure tracking and organization |
| [CLI Reference](docs/guide/cli.md) | Full command registry and options |
| [Extensions](docs/guide/extensions.md) | Custom plot types, transforms, hooks |

Full API documentation and rendered guides are also available at
[esther-poniatowski.github.io/eikon](https://esther-poniatowski.github.io/eikon/).

---

## Contributing

Contribution guidelines are described in [CONTRIBUTING.md](CONTRIBUTING.md).

---

## Acknowledgments

### Authors

**Author**: @esther-poniatowski

For academic use, the GitHub "Cite this repository" feature generates citations in
various formats. The [citation metadata](CITATION.cff) file is also available.

### Third-Party Dependencies

- **[Matplotlib](https://matplotlib.org/)** — Plotting library.
- **[NumPy](https://numpy.org/)** — Array operations.
- **[PyYAML](https://pyyaml.org/)** — YAML parsing.
- **[Typer](https://typer.tiangolo.com/)** — CLI framework.
- **[Rich](https://rich.readthedocs.io/)** — Terminal formatting.

---

## License

This project is licensed under the terms of the
[GNU General Public License v3.0](LICENSE).
