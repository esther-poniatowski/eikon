# CLI Reference

Eikon provides a command-line interface built on [Typer](https://typer.tiangolo.com/). All commands are accessed via the `eikon` entry point.

## Global options

```bash
eikon -v, --version      # Show version and exit
eikon -r, --root DIR     # Set explicit project root
eikon -c, --config PATH  # Read another settings file
eikon --help             # Show available commands
```

The `--root` option overrides auto-discovery and the `EIKON_ROOT` environment variable. The `--config` option names a settings file relative to the current folder, in place of `config/tools/eikon.yml` or `eikon.yml` below the root. As global options, both precede the command: `eikon --root DIR render specs/fig1.yaml`. The [configuration guide](configuration.md#project-root-discovery) states the full resolution.

A usage or configuration error, such as an absent `--config` file or two competing settings files, exits with status 2; a validation that finds a problem exits with status 1.

## Commands

### `eikon init`

Create a new eikon project with default configuration and directory structure.

```bash
eikon init
eikon init /path/to/project
```

Accepts an optional positional `path` argument (defaults to `.`).

Options:
- `--force` — Overwrite the settings file and the example specs if they exist. Without it, `eikon init` stops with an error that names each existing file, since the researcher may have edited them.

Creates:
- `eikon.yml` — Project configuration file, or the existing `config/tools/eikon.yml` when `--force` overwrites it
- `specs/` — Directory for figure specifications (with two example specs)
- `styles/` — Directory for custom style files
- `figures/` — Output directory for exported figures
- `data/` — Directory for data sources

### `eikon validate`

Validate a configuration or figure spec YAML file.

```bash
eikon validate eikon.yml
eikon validate specs/fig1.yaml
eikon validate specs/fig1.yaml --kind figure
```

Options:

- `--kind` — Validation target kind: `auto` (default), `config`, or `figure`. In `auto` mode, files named `eikon.yml` are validated as config; all others are validated as figure specs.

Outputs validation results with Rich formatting. Returns exit code 1 on validation errors, and 2 when the file does not exist.

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
eikon registry list --tag neural --tag overview --match-all
```

Options:

- `--tag`, `-t` — Filter by tag (repeatable)
- `--group`, `-g` — Filter by group
- `--match-all` — Require all tags to match (default: any)

#### `eikon registry add`

```bash
eikon registry add fig1 --tag neural --tag overview --group manuscript-1
eikon registry add fig1 --spec-path specs/fig1.yaml
```

Options:
- `--tag`, `-t` — Tags (repeatable)
- `--group`, `-g` — Group name
- `--on-conflict` — Conflict strategy: `update` (default), `fail`, or `skip`
- `--spec-path` — Path to the figure spec file, relative to the current folder; the registry stores it relative to the project root

#### `eikon registry remove`

```bash
eikon registry remove fig1
```

#### `eikon registry show`

```bash
eikon registry show fig1
```

Displays the full registry entry as formatted JSON.
