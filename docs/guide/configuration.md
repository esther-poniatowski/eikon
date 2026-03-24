# Configuration

Eikon uses a layered configuration system. Settings are resolved in this order (later layers override earlier ones):

```
Built-in defaults → eikon.yaml → Figure-level overrides → Runtime kwargs
```

## Project configuration file

The main configuration file is `eikon.yaml`, placed at the project root. Run `eikon init` to generate a template.

### Full schema

```yaml
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
  metadata:                 # Metadata injected into exported files
    author: "Author Name"

# Default style settings
style:
  base_style: default       # Matplotlib style or eikon preset
  font_family: serif
  font_size: 10.0
  figure_size: [6.4, 4.8]  # Width x height in inches

# Path to the figure registry manifest
registry_file: eikon-registry.yaml
```

All fields are optional. Omitted fields use built-in defaults.

## Project root discovery

Eikon locates the project root using a three-tier strategy:

1. **`--project-root` CLI flag** (highest priority)
2. **`EIKON_PROJECT_ROOT` environment variable**
3. **Auto-discovery**: walk upward from the current working directory until `eikon.yaml` is found

Eikon commands can therefore run from any subdirectory of the project.

```bash
# Explicit root
eikon render specs/fig.yaml --project-root /path/to/project

# Via environment variable
export EIKON_PROJECT_ROOT=/path/to/project
eikon render specs/fig.yaml
```

## Configuration in Python

Load and inspect the configuration programmatically:

```python
from eikon import load_config, resolve_paths

config = load_config()                          # Loads eikon.yaml
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
| `ResolvedPaths` | `project_root`, `output_dir`, `styles_dir`, `specs_dir`, `data_dir` | Absolute paths |

See the {doc}`/api/config` for complete field documentation.

## Validation

Validate a configuration file from the CLI:

```bash
eikon validate eikon.yaml
```

Or programmatically:

```python
from eikon.config import validate_config
import yaml

with open("eikon.yaml") as f:
    raw = yaml.safe_load(f)

errors = validate_config(raw)
if errors:
    for e in errors:
        print(f"  - {e}")
```
