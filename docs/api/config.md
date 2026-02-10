# eikon.config

Configuration system for eikon projects.

For usage examples, see the {doc}`Configuration guide </guide/configuration>`.

## Classes

### ProjectConfig

```
eikon.config.ProjectConfig(*, paths=PathsConfig(), export=ExportDefaults(),
                           style=StyleDefaults(), registry_file=Path("eikon-registry.yaml"))
```

Top-level project configuration. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `paths` | `PathsConfig` | `PathsConfig()` | Directory layout |
| `export` | `ExportDefaults` | `ExportDefaults()` | Export settings |
| `style` | `StyleDefaults` | `StyleDefaults()` | Style settings |
| `registry_file` | `Path` | `Path("eikon-registry.yaml")` | Registry manifest path |

---

### PathsConfig

```
eikon.config.PathsConfig(*, output_dir=Path("figures"), styles_dir=Path("styles"),
                         specs_dir=Path("specs"), data_dir=Path("data"))
```

Directory paths, stored relative to the project root. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `output_dir` | `Path` | `Path("figures")` | Exported figures directory |
| `styles_dir` | `Path` | `Path("styles")` | Custom style files directory |
| `specs_dir` | `Path` | `Path("specs")` | Figure spec YAML directory |
| `data_dir` | `Path` | `Path("data")` | Data sources directory |

---

### ExportDefaults

```
eikon.config.ExportDefaults(*, formats=(ExportFormat.PDF,), dpi=300,
                            transparent=False, bbox_inches="tight",
                            pad_inches=0.1, metadata={})
```

Default export settings. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `formats` | `tuple[ExportFormat, ...]` | `(ExportFormat.PDF,)` | Export formats |
| `dpi` | `int` | `300` | Resolution in DPI |
| `transparent` | `bool` | `False` | Transparent background |
| `bbox_inches` | `str` | `"tight"` | Bounding box mode |
| `pad_inches` | `float` | `0.1` | Padding (inches) |
| `metadata` | `dict[str, str]` | `{}` | Metadata for exports |

---

### StyleDefaults

```
eikon.config.StyleDefaults(*, base_style="default", font_family="serif",
                           font_size=10.0, figure_size=(6.4, 4.8))
```

Default style settings. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `base_style` | `str` | `"default"` | Base matplotlib style |
| `font_family` | `str` | `"serif"` | Font family |
| `font_size` | `float` | `10.0` | Base font size (pt) |
| `figure_size` | `tuple[float, float]` | `(6.4, 4.8)` | Width x height (inches) |

---

### ResolvedPaths

```
eikon.config.ResolvedPaths(project_root, output_dir, styles_dir, specs_dir, data_dir)
```

Fully resolved absolute paths. Frozen dataclass. Once constructed, the project root is cached and never recomputed.

| Field | Type | Description |
|-------|------|-------------|
| `project_root` | `Path` | Absolute project root |
| `output_dir` | `Path` | Absolute output directory |
| `styles_dir` | `Path` | Absolute styles directory |
| `specs_dir` | `Path` | Absolute specs directory |
| `data_dir` | `Path` | Absolute data directory |

## Functions

### load_config

```
eikon.config.load_config(path: Path | None = None) -> ProjectConfig
```

Load project configuration from a YAML file. If `path` is `None`, discovers `eikon.yaml` by walking upward from the current directory.

**Raises:** `ConfigNotFoundError` if no config file is found.

---

### resolve_paths

```
eikon.config.resolve_paths(config: PathsConfig, project_root: Path | None = None) -> ResolvedPaths
```

Resolve relative paths against the project root.

Resolution priority:
1. Explicit `project_root` parameter
2. `EIKON_PROJECT_ROOT` environment variable
3. Auto-discovery (walk upward for `eikon.yaml`)

---

### merge_configs

```
eikon.config.merge_configs(base: ProjectConfig, override: dict[str, Any]) -> ProjectConfig
```

Deep-merge a raw dict of overrides onto a base configuration.

---

### validate_config

```
eikon.config.validate_config(raw: dict[str, Any]) -> list[str]
```

Validate a raw config dict. Returns a list of error messages (empty if valid).

---

### discover_project_root

```
eikon.config.discover_project_root(start: Path | None = None) -> Path
```

Find the project root using the three-tier strategy.

**Raises:** `ConfigNotFoundError` if no `eikon.yaml` is found.
