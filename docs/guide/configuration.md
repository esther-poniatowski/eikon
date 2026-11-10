# Configuration

Eikon uses a layered configuration system. Settings are resolved in this order (later layers override earlier ones):

```
Built-in defaults → eikon.yml → Figure-level overrides → Runtime kwargs
```

## Project configuration file

The main configuration file is `eikon.yml`, placed in the `config/tools/` folder of the project root or at the root itself. A project that keeps the settings of its tools off its root uses `config/tools/eikon.yml`. When both files exist, Eikon stops with an error that names both. Without any settings file, Eikon runs on its built-in defaults. Run `eikon init` to generate a template.

The global option `-c`, `--config PATH` names another settings file, relative to the current folder; a file named by `--config` and absent is an error. The paths written in the settings file are relative to the project root, wherever the file lies, so that the file moves between the root and `config/tools/` without an edit.

### Full schema

```yaml
config_version: 1

# Directory paths (relative to the project root)
paths:
  output_dir: figures       # Where exported figures are saved
  styles_dir: styles        # Custom style files
  specs_dir: specs          # Figure specification YAML files
  data_dir: data            # Data sources

# Default export settings
export:
  formats: [pdf]            # Default formats: pdf, svg, png
  dpi: 300                  # Resolution in dots per inch
  transparent: false        # Transparent background
  bbox_inches: tight        # Bounding box setting for savefig
  pad_inches: 0.1           # Padding when bbox_inches is tight
  metadata:                 # Metadata embedded in exported files
    author: "Author Name"

# Default style settings
style:
  base_style: default       # Matplotlib style or eikon preset
  font_family: sans-serif
  font_size: 10.0
  figure_size: [6.4, 4.8]  # Width x height in inches

# Path to the figure registry manifest
registry_file: eikon-registry.yaml
```

All fields are optional. Omitted fields use built-in defaults.

## Project root discovery

Eikon resolves the project root in this order, and stops at the first answer:

1. **`-r`, `--root` CLI option** (highest priority)
2. **`EIKON_ROOT` environment variable**
3. **Upward search**: the nearest ancestor of the current folder that holds `config/tools/eikon.yml` or `eikon.yml`
4. **The current folder**

Eikon commands can therefore run from any subdirectory of the project.

```bash
# Explicit root
eikon --root /path/to/project render specs/fig.yaml

# Via environment variable
export EIKON_ROOT=/path/to/project
eikon render specs/fig.yaml

# Another settings file, relative to the current folder
eikon --config settings/figures.yml render specs/fig.yaml
```

## Configuration in Python

Load and inspect the configuration programmatically:

```python
from eikon import load_config, resolve_paths

config = load_config()                          # Loads eikon.yml, or the defaults
paths = resolve_paths(config.paths)             # Resolve to absolute paths

print(paths.project_root)  # /absolute/path/to/project
print(paths.output_dir)    # /absolute/path/to/project/figures
print(paths.specs_dir)     # /absolute/path/to/project/specs
```

Pass an explicit path to load a specific config file:

```python
from pathlib import Path
config = load_config(Path("other-config.yaml"))
```

## Configuration dataclasses

All configuration sections are frozen, keyword-only dataclasses:

| Class | Fields | Description |
|-------|--------|-------------|
| `ProjectConfig` | `paths`, `export`, `style`, `registry_file` | Top-level container |
| `PathsConfig` | `output_dir`, `styles_dir`, `specs_dir`, `data_dir` | Directory layout |
| `ExportDefaults` | `formats`, `dpi`, `transparent`, `bbox_inches`, `pad_inches`, `metadata` | Export settings |
| `StyleDefaults` | `base_style`, `font_family`, `font_size`, `figure_size` | Style settings |
| `ProjectSession` | `config`, `paths` | Bundled config + resolved paths |
| `ResolvedPaths` | `project_root`, `output_dir`, `styles_dir`, `specs_dir`, `data_dir` | Absolute paths |

See [the generated configuration API](../api/config.md#module-eikon.config._schema) for complete field documentation.

## Validation

Validate a configuration file from the CLI:

```bash
eikon validate eikon.yml
```

Or programmatically:

```python
from eikon.config import validate_config
import yaml

with open("eikon.yml") as f:
    raw = yaml.safe_load(f)

errors = validate_config(raw)
if errors:
    for e in errors:
        print(f"  - {e}")
```
