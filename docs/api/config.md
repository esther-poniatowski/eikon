<a id="configuration"></a>

# Configuration

Project configuration schema, loading, resolution, sessions, and validation.

<a id="module-eikon.config._schema"></a>

<a id="configuration-schema"></a>

## Configuration Schema

Dataclass schemas for project configuration.

All configuration sections are modeled as frozen, keyword-only dataclasses
with sensible defaults.  They are composed into [`ProjectConfig`](#eikon.config._schema.ProjectConfig),
the top-level configuration object.

<a id="eikon.config._schema.PathsConfig"></a>

### *class* eikon.config._schema.PathsConfig(\*, output_dir=PosixPath('figures'), styles_dir=PosixPath('styles'), specs_dir=PosixPath('specs'), data_dir=PosixPath('data'))

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Configurable directory paths, stored relative to the project root.

<a id="eikon.config._schema.PathsConfig.output_dir"></a>

#### output_dir *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Directory where exported figures are written.

<a id="eikon.config._schema.PathsConfig.styles_dir"></a>

#### styles_dir *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Directory containing user-defined style files.

<a id="eikon.config._schema.PathsConfig.specs_dir"></a>

#### specs_dir *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Directory containing YAML figure specifications.

<a id="eikon.config._schema.PathsConfig.data_dir"></a>

#### data_dir *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Directory containing data sources for figures.

<a id="eikon.config._schema.ExportDefaults"></a>

### *class* eikon.config._schema.ExportDefaults(\*, formats=(ExportFormat.PDF, ), dpi=300, transparent=False, bbox_inches='tight', pad_inches=0.1, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Default export settings applied to all figures unless overridden.

<a id="eikon.config._schema.ExportDefaults.formats"></a>

#### formats *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[ExportFormat](types.md#eikon._types.ExportFormat), ...]*

File formats to export.

<a id="eikon.config._schema.ExportDefaults.dpi"></a>

#### dpi *: [int](https://docs.python.org/3/library/functions.html#int)*

Resolution in dots per inch.

<a id="eikon.config._schema.ExportDefaults.transparent"></a>

#### transparent *: [bool](https://docs.python.org/3/library/functions.html#bool)*

Whether to export with a transparent background.

<a id="eikon.config._schema.ExportDefaults.bbox_inches"></a>

#### bbox_inches *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Bounding box setting passed to `matplotlib.figure.Figure.savefig`.

<a id="eikon.config._schema.ExportDefaults.pad_inches"></a>

#### pad_inches *: [float](https://docs.python.org/3/library/functions.html#float)*

Padding around the figure when using `bbox_inches='tight'`.

<a id="eikon.config._schema.ExportDefaults.metadata"></a>

#### metadata *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

Metadata fields injected into exported files.

<a id="eikon.config._schema.StyleDefaults"></a>

### *class* eikon.config._schema.StyleDefaults(\*, base_style='default', font_family='sans-serif', font_size=10.0, figure_size=(6.4, 4.8))

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Default style settings applied to all figures unless overridden.

<a id="eikon.config._schema.StyleDefaults.base_style"></a>

#### base_style *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Name of the base matplotlib or eikon style preset.

<a id="eikon.config._schema.StyleDefaults.font_family"></a>

#### font_family *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Font family name.

<a id="eikon.config._schema.StyleDefaults.font_size"></a>

#### font_size *: [float](https://docs.python.org/3/library/functions.html#float)*

Base font size in points.

<a id="eikon.config._schema.StyleDefaults.figure_size"></a>

#### figure_size *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[float](https://docs.python.org/3/library/functions.html#float), [float](https://docs.python.org/3/library/functions.html#float)]*

Default figure dimensions `(width, height)` in inches.

<a id="eikon.config._schema.ProjectConfig"></a>

### *class* eikon.config._schema.ProjectConfig(\*, paths=<factory>, export=<factory>, style=<factory>, registry_file=PosixPath('eikon-registry.yaml'))

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Top-level project configuration, composed from section dataclasses.

<a id="eikon.config._schema.ProjectConfig.paths"></a>

#### paths *: [PathsConfig](#eikon.config._schema.PathsConfig)*

Directory layout for the project.

<a id="eikon.config._schema.ProjectConfig.export"></a>

#### export *: [ExportDefaults](#eikon.config._schema.ExportDefaults)*

Default export settings.

<a id="eikon.config._schema.ProjectConfig.style"></a>

#### style *: [StyleDefaults](#eikon.config._schema.StyleDefaults)*

Default style settings.

<a id="eikon.config._schema.ProjectConfig.registry_file"></a>

#### registry_file *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Path to the figure registry manifest, relative to project root.

<a id="module-eikon.config._loader"></a>

<a id="configuration-loading"></a>

## Configuration Loading

YAML configuration loading and deep merging.

Loads `eikon.yaml` from disk, validates the content, and constructs a
`ProjectConfig` with proper layered merging of defaults.

<a id="eikon.config._loader.load_config"></a>

### eikon.config._loader.load_config(path=None)

Load and validate the project configuration.

* **Parameters:**
  **path** (*Path* *,* *optional*) – Explicit path to an `eikon.yaml` file.  If `None`, the file is
  discovered by walking upward from the current working directory.
* **Returns:**
  Validated project configuration.
* **Return type:**
  [ProjectConfig](#eikon.config._schema.ProjectConfig)
* **Raises:**
  * [**ConfigNotFoundError**](types.md#eikon.exceptions.ConfigNotFoundError) – If no configuration file is found.
  * [**ConfigValidationError**](types.md#eikon.exceptions.ConfigValidationError) – If the configuration fails schema validation.
  * [**ConfigError**](types.md#eikon.exceptions.ConfigError) – If the YAML file cannot be parsed.

<a id="eikon.config._loader.merge_configs"></a>

### eikon.config._loader.merge_configs(base, override)

Deep-merge an override dictionary into an existing configuration.

* **Parameters:**
  * **base** ([*ProjectConfig*](#eikon.config._schema.ProjectConfig)) – The base configuration to merge onto.
  * **override** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) – A dictionary of overrides (same structure as `eikon.yaml`).
* **Returns:**
  A new configuration with overrides applied.
* **Return type:**
  [ProjectConfig](#eikon.config._schema.ProjectConfig)

<a id="module-eikon.config._resolver"></a>

<a id="configuration-resolution"></a>

## Configuration Resolution

Path resolution for eikon projects.

Resolves relative paths from `PathsConfig` against a discovered
or explicit project root directory.

Project root resolution uses a three-tier strategy:

1. Explicit `project_root` parameter (or `--project-root` CLI flag).
2. `EIKON_PROJECT_ROOT` environment variable.
3. Auto-discovery: walk upward from cwd until `eikon.yaml` is found.

<a id="eikon.config._resolver.ResolvedPaths"></a>

### *class* eikon.config._resolver.ResolvedPaths(project_root, output_dir, styles_dir, specs_dir, data_dir)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Fully resolved, absolute paths for a project.

Once constructed, the resolved root is cached on this object and
never re-computed — preventing cross-project bleed when the working
directory changes during execution.

<a id="eikon.config._resolver.ResolvedPaths.project_root"></a>

#### project_root *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Absolute path to the project root directory.

<a id="eikon.config._resolver.ResolvedPaths.output_dir"></a>

#### output_dir *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Absolute path to the figure output directory.

<a id="eikon.config._resolver.ResolvedPaths.styles_dir"></a>

#### styles_dir *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Absolute path to the styles directory.

<a id="eikon.config._resolver.ResolvedPaths.specs_dir"></a>

#### specs_dir *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Absolute path to the figure specs directory.

<a id="eikon.config._resolver.ResolvedPaths.data_dir"></a>

#### data_dir *: [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Absolute path to the data directory.

<a id="eikon.config._resolver.resolve_paths"></a>

### eikon.config._resolver.resolve_paths(config, project_root=None)

Resolve all relative paths against the project root.

* **Parameters:**
  * **config** ([*PathsConfig*](#eikon.config._schema.PathsConfig)) – Path configuration with relative paths.
  * **project_root** (*Path* *,* *optional*) – Explicit project root (tier 1 — highest priority).  If `None`,
    falls back to the env var / auto-discovery tiers via
    [`discover_project_root()`](#eikon.config._resolver.discover_project_root).
* **Returns:**
  Fully resolved, absolute paths.
* **Return type:**
  [ResolvedPaths](#eikon.config._resolver.ResolvedPaths)

<a id="eikon.config._resolver.discover_project_root"></a>

### eikon.config._resolver.discover_project_root(start=None)

Resolve the project root using the three-tier strategy.

Resolution order:

1. `EIKON_PROJECT_ROOT` environment variable (if set and non-empty).
2. Walk upward from *start* (defaults to cwd) until `eikon.yaml` is
   found.

Use the *start* parameter or the env var for environments where the
working directory is unreliable (CI runners, notebook kernels).

* **Parameters:**
  **start** (*Path* *,* *optional*) – Starting directory for upward walk.  Defaults to the current
  working directory.  Ignored when `EIKON_PROJECT_ROOT` is set.
* **Returns:**
  Absolute path to the project root.
* **Return type:**
  Path
* **Raises:**
  [**ConfigNotFoundError**](types.md#eikon.exceptions.ConfigNotFoundError) – If no `eikon.yaml` is found via any method.

<a id="module-eikon.config._session"></a>

<a id="project-sessions"></a>

## Project Sessions

Project session — single entry point for config + path resolution.

A [`ProjectSession`](#eikon.config._session.ProjectSession) bundles a `ProjectConfig` with its
`ResolvedPaths`, eliminating the duplicated load+resolve ceremony
across call sites.

<a id="eikon.config._session.ProjectSession"></a>

### *class* eikon.config._session.ProjectSession(config, paths)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Bundled project configuration and resolved paths.

<a id="eikon.config._session.ProjectSession.config"></a>

#### config *: [ProjectConfig](#eikon.config._schema.ProjectConfig)*

The validated project configuration.

<a id="eikon.config._session.ProjectSession.paths"></a>

#### paths *: [ResolvedPaths](#eikon.config._resolver.ResolvedPaths)*

Fully resolved, absolute paths for the project.

<a id="eikon.config._session.ProjectSession.from_config"></a>

#### *classmethod* from_config(config=None, project_root=None, \*, strict=True)

Create a session by loading config and resolving paths.

* **Parameters:**
  * **config** ([*ProjectConfig*](#eikon.config._schema.ProjectConfig) *,* *optional*) – Pre-loaded configuration.  If `None`, loads from disk.
  * **project_root** (*Path* *,* *optional*) – Explicit project root directory.  Passed through to
    `resolve_paths()` as tier-1 override.
  * **strict** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If `True` (default), let `ConfigNotFoundError`
    propagate when no config file or project root is found.
    If `False`, fall back to built-in defaults and
    cwd-based paths.
* **Returns:**
  A fully resolved session.
* **Return type:**
  [ProjectSession](#eikon.config._session.ProjectSession)
* **Raises:**
  [**ConfigNotFoundError**](types.md#eikon.exceptions.ConfigNotFoundError) – If *strict* is `True` and no configuration is found.

<a id="module-eikon.config._validation"></a>

<a id="configuration-validation"></a>

## Configuration Validation

Schema validation for raw configuration dictionaries.

Validates YAML-loaded dicts before they are converted into typed
dataclasses, producing descriptive error messages.

<a id="eikon.config._validation.validate_config"></a>

### eikon.config._validation.validate_config(raw)

Validate a raw project configuration dictionary.

* **Parameters:**
  **raw** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) – Dictionary loaded from `eikon.yaml`.
* **Returns:**
  Validation error messages.  Empty list means valid.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="eikon.config._validation.validate_figure_spec"></a>

### eikon.config._validation.validate_figure_spec(raw)

Validate a raw figure specification dictionary.

* **Parameters:**
  **raw** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) – Dictionary loaded from a figure spec YAML file.
* **Returns:**
  Validation error messages.  Empty list means valid.
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)]
