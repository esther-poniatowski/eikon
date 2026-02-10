# Export

The export pipeline saves rendered figures to files in multiple formats with configurable resolution, metadata, and filename patterns.

## Supported formats

| Format | Extension | Description |
|--------|-----------|-------------|
| PDF | `.pdf` | Vector format, ideal for publications |
| SVG | `.svg` | Scalable vector, for web and presentations |
| PNG | `.png` | Raster format with configurable DPI |

## Export settings

Export settings follow the configuration hierarchy:

```
Project defaults (eikon.yaml) → Per-figure overrides (spec YAML) → CLI flags
```

### Project-level defaults

In `eikon.yaml`:

```yaml
export:
  formats: [pdf, svg]
  dpi: 300
  transparent: false
  metadata:
    author: "E. Poniatowski"
```

### Per-figure overrides

In a figure spec YAML:

```yaml
export:
  formats: [pdf, svg, png]
  dpi: 600
  transparent: true
  filename_template: "{name}_{date}"
  subdirectory: "high-res"
  collision: increment
  metadata:
    project: "Manuscript 1"
```

### ExportSpec fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `formats` | `tuple[str, ...]` | inherited | Export format names |
| `dpi` | `int` | inherited | Resolution (dots per inch) |
| `transparent` | `bool` | inherited | Transparent background |
| `filename_template` | `str` | `"{name}"` | Output filename pattern |
| `subdirectory` | `str` | `""` | Subfolder under output_dir |
| `collision` | `str` | `"overwrite"` | `"overwrite"`, `"increment"`, or `"fail"` |
| `metadata` | `dict[str, str]` | inherited | Metadata injected into files |

### Filename templates

Templates support these variables:

- `{name}` — Figure name
- `{group}` — Figure group
- `{date}` — Current date (ISO format)
- `{format}` — Export format extension

Example: `"{group}/{name}_{date}"` produces `manuscript-1/fig1_2026-02-10.pdf`.

### Collision handling

When an output file already exists:

- `"overwrite"` (default) — Replace the file
- `"increment"` — Append a number suffix (`fig1_1.pdf`, `fig1_2.pdf`)
- `"fail"` — Raise an `ExportError`

## Exporting from the CLI

```bash
# Single figure
eikon render specs/fig1.yaml --format pdf --format svg

# Batch export
eikon batch --format pdf --format png
```

## Exporting from Python

### Via render()

```python
import eikon

handle = eikon.render("my-figure", formats=("pdf", "svg"))
print(handle.export_paths)
# {"pdf": PosixPath("figures/my-figure.pdf"),
#  "svg": PosixPath("figures/my-figure.svg")}
handle.close()
```

### Direct batch export

For lower-level control:

```python
from eikon.export import batch_export
from eikon.config import load_config, resolve_paths

config = load_config()
paths = resolve_paths(config.paths)

exported = batch_export(
    figure=fig,                       # matplotlib Figure
    name="my-figure",
    output_dir=paths.output_dir,
    export_defaults=config.export,
    cli_formats=("pdf", "png"),
)
# {"pdf": Path(...), "png": Path(...)}
```

See the {doc}`/api/export` for the complete API reference.
