# Contributing to Eikon

Thank you for your interest in contributing to Eikon! This document provides guidelines for setting up the development environment, running tests, and submitting changes.

## Development Setup

### Prerequisites

- Python >= 3.12
- [Conda](https://docs.conda.io/) (recommended) or virtualenv

### Environment

```bash
# Clone the repository
git clone https://github.com/esther-poniatowski/eikon.git
cd eikon

# Create and activate the conda environment
conda create -n eikon python=3.12
conda activate eikon

# Install in editable mode with dev dependencies
pip install -e ".[dev]"
```

## Running Tests

```bash
# Run the full test suite
python -m pytest tests/ -v

# Run with coverage
python -m pytest tests/ --cov=eikon --cov-report=term-missing

# Run a specific test module
python -m pytest tests/test_eikon/test_render/test_pipeline.py -v
```

## Code Quality

All code must pass three checks before merging:

```bash
# Linting (ruff)
ruff check src/eikon/

# Type checking (mypy strict mode)
mypy src/eikon/ --strict

# Tests (all must pass)
python -m pytest tests/ -v
```

## Code Style

- **Dataclasses**: Use `frozen=True, kw_only=True, slots=True`.
- **Type aliases**: Use Python 3.12 `type` keyword (not `TypeAlias`).
- **Private modules**: Name `_*.py` and expose via `__init__.py` with `__all__`.
- **Protocols over ABCs**: Use `typing.Protocol` for extensibility interfaces.
- **Import ordering**: Enforced by ruff (I001) — stdlib, third-party, local.
- **Docstrings**: NumPy-style with Parameters, Returns, and Raises sections.

## Project Structure

```
src/eikon/
  _types.py          # Type aliases
  exceptions.py      # Exception hierarchy
  config/            # Configuration loading and validation
  spec/              # Figure and panel specifications
  style/             # Style sheets, presets, and composition
  layout/            # Grid layout, placement, and constraints
  render/            # Pipeline orchestrator, drawing, handles
  export/            # Format handlers and metadata injection
  ext/               # Plugin discovery, hooks, plot types
  contrib/           # Built-in plot type implementations
  registry/          # Figure registry with YAML persistence
  cli/               # Typer-based CLI commands
```

## Submitting Changes

1. Fork the repository and create a feature branch from `main`.
2. Make your changes, ensuring all three checks pass (ruff, mypy, pytest).
3. Add tests for new functionality or bug fixes.
4. Open a pull request with a clear description of the changes.

## Configuration File Organization

This project separates configuration concerns between two locations:

### `pyproject.toml` — Project Management

Contains only build system, package metadata, dependencies, entry points, and tool configurations
that **must** reside in `pyproject.toml` (because the tool does not support external config paths):

- `[build-system]` — Build backend (setuptools)
- `[project]` — Name, version, authors, license, description, keywords, classifiers, URLs
- `[project.dependencies]` — Runtime dependencies
- `[project.optional-dependencies]` — Optional dependency groups
- `[project.scripts]` — CLI entry points
- `[tool.setuptools]` — Package discovery and source layout
- `[tool.pytest.ini_options]` — Pytest settings (pytest does not support custom config paths)

### `config/tools/` — Tool-Specific Settings

Contains dedicated configuration files for each development tool. This achieves modular,
tool-specific settings that are decoupled from the main project file:

| File                  | Tool                   | Purpose                           |
|-----------------------|------------------------|-----------------------------------|
| `black.toml`          | Black                  | Code formatting rules             |
| `mypy.ini`            | MyPy                   | Static type checking rules        |
| `pylintrc.ini`        | Pylint                 | Linting rules (main code)         |
| `pylintrc_tests.ini`  | Pylint                 | Linting rules (test code)         |
| `pyrightconfig.json`  | Pyright                | Static type analysis overrides    |
| `releaserc.toml`      | Python Semantic Release| Versioning and changelog           |

### `config/dictionaries/` — Spell Checking

Custom word lists for CSpell (VS Code spell checker):

| File          | Contents                    |
|---------------|-----------------------------|
| `project.txt` | Project-specific terms      |
| `python.txt`  | Python language terms       |
| `tools.txt`   | Development tool names      |

### Rationale

- **Modularity**: Each tool's configuration is self-contained and independently editable.
- **Clarity**: `pyproject.toml` stays concise and focused on project identity.
- **Discoverability**: Tool configs are grouped in a single directory, easy to locate.
- **Flexibility**: Tools with complex configs (Pylint, MyPy) benefit from dedicated files
  with inline comments explaining each setting.

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0-or-later license.
