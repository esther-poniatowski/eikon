# Installation

## Prerequisites

- Python >= 3.12
- matplotlib >= 3.8
- numpy >= 1.26
- PyYAML >= 6.0
- Typer, Rich (installed automatically)

## Using pip

```sh
pip install git+https://github.com/esther-poniatowski/eikon.git
```

## From Source

1. Clone the repository:

   ```sh
   git clone https://github.com/esther-poniatowski/eikon.git
   ```

2. Install in editable mode:

   ```sh
   cd eikon
   pip install -e .
   ```

For development tools (pytest, mypy, ruff):

```sh
pip install -e ".[dev]"
```
