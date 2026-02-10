# eikon.export

Export pipeline: format handlers, path construction, and batch export.

For usage examples, see the {doc}`Export guide </guide/export>`.

## Classes

### ExportSpec

```
eikon.export.ExportSpec(*, formats=None, dpi=None, transparent=None,
                        filename_template=None, subdirectory=None,
                        collision=None, metadata=None)
```

Per-figure export overrides. `None` fields inherit project defaults. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `formats` | `tuple[str, ...] \| None` | `None` | Format names |
| `dpi` | `int \| None` | `None` | Resolution |
| `transparent` | `bool \| None` | `None` | Transparent background |
| `filename_template` | `str \| None` | `None` | Filename pattern (`{name}`, `{group}`, `{date}`, `{format}`) |
| `subdirectory` | `str \| None` | `None` | Subfolder under output_dir |
| `collision` | `"overwrite" \| "increment" \| "fail" \| None` | `None` | File collision strategy |
| `metadata` | `dict[str, str] \| None` | `None` | Extra metadata |

---

### ResolvedExportConfig

```
eikon.export.ResolvedExportConfig(*, formats, dpi, transparent, bbox_inches,
                                  pad_inches, filename_template, subdirectory,
                                  collision, metadata={})
```

Fully resolved export configuration — no optional fields. Frozen dataclass.

| Field | Type | Description |
|-------|------|-------------|
| `formats` | `tuple[ExportFormat, ...]` | Export formats |
| `dpi` | `int` | Resolution |
| `transparent` | `bool` | Transparent background |
| `bbox_inches` | `str` | Bounding box mode |
| `pad_inches` | `float` | Padding (inches) |
| `filename_template` | `str` | Filename pattern |
| `subdirectory` | `str` | Subfolder |
| `collision` | `str` | Collision strategy |
| `metadata` | `dict[str, str]` | Metadata |

## Functions

### resolve_export_config

```
eikon.export.resolve_export_config(defaults: ExportDefaults,
                                   spec_export: ExportSpec | None = None,
                                   cli_formats: tuple[str, ...] = ()
                                   ) -> ResolvedExportConfig
```

Merge per-figure overrides onto project defaults. Resolution priority: CLI formats > spec formats > project defaults.

---

### parse_export_spec

```
eikon.export.parse_export_spec(raw: dict[str, Any] | None) -> ExportSpec | None
```

Parse a raw dict (from YAML) into an `ExportSpec`. Returns `None` if input is `None`.

---

### batch_export

```
eikon.export.batch_export(*, figure, name, group="", output_dir,
                          export_defaults, export_spec=None,
                          cli_formats=()) -> dict[str, Path]
```

Export a figure to all configured formats. Returns a dict mapping format names to output paths.

---

### export_figure

```
eikon.export.export_figure(figure: Figure, path: Path,
                           fmt: ExportFormat,
                           config: ResolvedExportConfig) -> None
```

Export a single figure to one format at the given path.

---

### build_export_path

```
eikon.export.build_export_path(*, name, fmt, output_dir,
                               filename_template="{name}",
                               subdirectory="", group="",
                               collision="overwrite") -> Path
```

Construct the output file path from a template and parameters.

---

### sanitize_filename

```
eikon.export.sanitize_filename(name: str) -> str
```

Sanitize a string for use as a filename (remove unsafe characters).
