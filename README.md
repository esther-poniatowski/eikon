# Eikon

[![Conda](https://img.shields.io/badge/conda-eresthanaconda--channel-blue)](#installation)
[![Maintenance](https://img.shields.io/maintenance/yes/2026)]()
[![Last Commit](https://img.shields.io/github/last-commit/esther-poniatowski/eikon)](https://github.com/esther-poniatowski/eikon/commits/main)
[![Python](https://img.shields.io/badge/python-supported-blue)](https://www.python.org/)
[![License: GPL](https://img.shields.io/badge/License-GPL-yellow.svg)](https://opensource.org/licenses/GPL-3.0)

Figure management library for programmatic creation, styling, and export of scientific visualizations.

---

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [Documentation](#documentation)
- [Support](#support)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Overview

### Motivations

Scientific workflows require reproducible, publication-quality figures with consistent styling across
analyses. Manual figure management becomes error-prone as the number of panels, conditions, and
output formats grows. Coordinating layout, aesthetics, and export settings across a project demands
a structured approach.

### Advantages

Eikon provides a figure management framework for programmatic creation, styling, and export of
scientific visualizations built on top of matplotlib.

---

## Features

- [ ] **Declarative figure specifications**: Define figures as structured objects with layout,
  styling, and export settings.
- [ ] **Consistent styling**: Apply and manage style sheets for uniform aesthetics across figures.
- [ ] **Layout management**: Compose multi-panel figures with flexible grid specifications.
- [ ] **Export pipelines**: Batch export figures to multiple formats (PDF, SVG, PNG) with
  configurable resolution and metadata.
- [ ] **Figure registry**: Track and organize figures across analyses and manuscripts.

---

## Installation

To install the package and its dependencies, use one of the following methods:

### Using Pip Installs Packages

Install the package from the GitHub repository URL via `pip`:

```bash
pip install git+https://github.com/esther-poniatowski/eikon.git
```

### Using Conda

Install the package from the private channel eresthanaconda:

```bash
conda install eikon -c eresthanaconda
```

### From Source

1. Clone the repository:

      ```bash
      git clone https://github.com/esther-poniatowski/eikon.git
      ```

2. Create a dedicated virtual environment:

      ```bash
      cd eikon
      conda env create -f environment.yml
      ```

---

## Usage

### Command Line Interface (CLI)

To display the list of available commands and options:

```sh
eikon --help
```

### Programmatic Usage

To use the package programmatically in Python:

```python
import eikon
```

---

## Configuration

### Environment Variables

|Variable|Description|Default|Required|
|---|---|---|---|
|`VAR_1`|Description 1|None|Yes|
|`VAR_2`|Description 2|`false`|No|

### Configuration File

Configuration options are specified in YAML files located in the `config/` directory.

The canonical configuration schema is provided in [`config/default.yaml`](config/default.yaml).

```yaml
var_1: value1
var_2: value2
```

---

## Documentation

- [User Guide](https://esther-poniatowski.github.io/eikon/guide/)
- [API Documentation](https://esther-poniatowski.github.io/eikon/api/)

> [!NOTE]
> Documentation can also be browsed locally from the [`docs/`](docs/) directory.

## Support

**Issues**: [GitHub Issues](https://github.com/esther-poniatowski/eikon/issues)

**Email**: `{{ contact@example.com }}`

---

## Contributing

Please refer to the [contribution guidelines](CONTRIBUTING.md).

---

## Acknowledgments

### Authors & Contributors

**Author**: @esther-poniatowski

**Contact**: `{{ contact@example.com }}`

For academic use, please cite using the GitHub "Cite this repository" feature to
generate a citation in various formats.

Alternatively, refer to the [citation metadata](CITATION.cff).

### Third-Party Dependencies

- **[Matplotlib](https://matplotlib.org/)** - Plotting library
- **[NumPy](https://numpy.org/)** - Array operations

---

## License

This project is licensed under the terms of the [GNU General Public License v3.0](LICENSE).
