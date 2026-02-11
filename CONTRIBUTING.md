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

## License

By contributing, you agree that your contributions will be licensed under the GPL-3.0-or-later license.
