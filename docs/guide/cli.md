# CLI Reference

Eikon provides a command-line interface built on [Typer](https://typer.tiangolo.com/). All commands are accessed via the `eikon` entry point.

## Global options

```bash
eikon --version          # Show version and exit
eikon --project-root DIR # Set explicit project root
eikon --help             # Show available commands
```

The `--project-root` flag overrides auto-discovery and the `EIKON_PROJECT_ROOT` environment variable.

## Commands

### `eikon init`

Create a new eikon project with default configuration and directory structure.

```bash
eikon init
eikon init --project-root /path/to/project
```

Creates:
- `eikon.yaml` — Project configuration file
- `specs/` — Directory for figure specifications (with an example spec)
- `styles/` — Directory for custom style files
- `figures/` — Output directory for exported figures
- `data/` — Directory for data sources

### `eikon validate`

Validate a configuration or figure spec YAML file.

```bash
eikon validate eikon.yaml
eikon validate specs/fig1.yaml
```

Outputs validation results with Rich formatting. Returns exit code 1 on validation errors.

### `eikon info`

Display version and platform diagnostics.

```bash
eikon info
# eikon 0.1.0 | Platform: Darwin Python 3.12.0
```

### `eikon render`

Render a single figure from a spec file.

```bash
eikon render specs/fig1.yaml
eikon render specs/fig1.yaml --format pdf --format svg
eikon render specs/fig1.yaml --show              # Display interactively
```

Options:
- `--format`, `-f` — Export format(s), repeatable
- `--show` — Display the figure in a matplotlib window

### `eikon render-registry`

Render a figure by its registry name.

```bash
eikon render-registry fig1
eikon render-registry fig1 --format pdf --show
```

Looks up the spec path from the registry manifest. If no `spec_path` is stored, falls back to `specs/<name>.yaml`.

### `eikon batch`

Batch render multiple figures with filtering and progress bars.

```bash
# Render all specs in the specs/ directory
eikon batch

# Render specific files
eikon batch specs/fig1.yaml specs/fig2.yaml

# Filter by tags
eikon batch --tag neural --tag overview

# Filter by group
eikon batch --group manuscript-1

# Require all tags to match
eikon batch --tag neural --tag overview --match-all

# Export formats
eikon batch --format pdf --format svg

# Stop on first error (default: continue)
eikon batch --fail-fast
```

Options:
- `--tag`, `-t` — Filter by tag (repeatable)
- `--group`, `-g` — Filter by group
- `--match-all` — Require all tags to match (default: any)
- `--format`, `-f` — Export format(s), repeatable
- `--continue-on-error` / `--fail-fast` — Error handling (default: continue)

Progress is displayed with Rich progress bars on stderr.

### `eikon registry`

Manage the figure registry. This is a command group with subcommands.

#### `eikon registry list`

```bash
eikon registry list
eikon registry list --tag neural
eikon registry list --group manuscript-1
```

#### `eikon registry add`

```bash
eikon registry add fig1 --tag neural --tag overview --group manuscript-1
eikon registry add fig1 --spec-path specs/fig1.yaml
```

Options:
- `--tag`, `-t` — Tags (repeatable)
- `--group`, `-g` — Group name
- `--spec-path` — Path to the figure spec file

#### `eikon registry remove`

```bash
eikon registry remove fig1
```

#### `eikon registry show`

```bash
eikon registry show fig1
```

Displays the full registry entry as formatted YAML.
