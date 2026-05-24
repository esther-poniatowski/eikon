<a id="eikon-package"></a>

# Eikon Package

Declarative figure specifications, rendering, export, registry, and extension APIs.

<a id="top-level-entry-points"></a>

## Top-Level Entry Points

`eikon` re-exports the public objects documented in the sections below. The
top-level convenience functions are documented here to avoid duplicate API
targets for re-exported classes.

<a id="eikon.info"></a>

### eikon.info()

Format diagnostic information on package and platform.

* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="eikon.render"></a>

### eikon.render(name_or_spec, \*, config=None, resolved_paths=None, session=None, formats=(), overrides=None, show=False, strict=True, extensions=None)

Convenience function: render a figure by name or spec.

This is the primary high-level entry point.  It accepts either a
`FigureSpec` object or a string name (resolved as a YAML
file path via the project config’s specs directory).

* **Parameters:**
  * **name_or_spec** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*FigureSpec*](#eikon.spec._figure.FigureSpec)) – A `FigureSpec` instance, or a string name / path to a YAML
    spec file.
  * **config** ([*ProjectConfig*](#eikon.config._schema.ProjectConfig) *,* *optional*) – Project configuration.  If `None`, uses built-in defaults.
  * **resolved_paths** ([*ResolvedPaths*](#eikon.config._resolver.ResolvedPaths) *,* *optional*) – Pre-resolved paths.  Prefer passing a *session* instead.
  * **session** ([*ProjectSession*](#eikon.config._session.ProjectSession) *,* *optional*) – A pre-built session.  Takes precedence over *config* and
    *resolved_paths* when provided.
  * **formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Export format names (e.g. `("pdf", "svg")`).
  * **overrides** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*object*](https://docs.python.org/3/library/functions.html#object) *]* *,* *optional*) – Per-call overrides forwarded to the pipeline.
  * **show** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether to display the figure interactively.
  * **strict** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If `True` (default), let config/path errors propagate.
    If `False`, fall back to built-in defaults.
  * **extensions** ([*ExtensionRegistry*](#eikon.ext._registry.ExtensionRegistry) *|* *None*)
* **Returns:**
  A handle to the rendered figure.
* **Return type:**
  [FigureHandle](#eikon.render._handle.FigureHandle)

<a id="module-eikon._types"></a>

<a id="shared-types"></a>

## Shared Types

Shared type aliases and enumerations used across the eikon package.

<a id="eikon._types.ExportFormat"></a>

### *class* eikon._types.ExportFormat(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Supported export file formats.

<a id="eikon._types.ExportFormat.PDF"></a>

#### PDF *= 'pdf'*

<a id="eikon._types.ExportFormat.SVG"></a>

#### SVG *= 'svg'*

<a id="eikon._types.ExportFormat.PNG"></a>

#### PNG *= 'png'*

<a id="eikon._types.ExportFormat.from_string"></a>

#### *classmethod* from_string(value)

Parse a format string (case-insensitive) into an ExportFormat.

* **Parameters:**
  **value** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Format name, e.g. `"pdf"`, `"PNG"`.
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If the string does not match any known format.
* **Return type:**
  [*ExportFormat*](#eikon._types.ExportFormat)

<a id="module-eikon.exceptions"></a>

<a id="exceptions"></a>

## Exceptions

Exception hierarchy for the eikon package.

All eikon exceptions inherit from [`EikonError`](#eikon.exceptions.EikonError), allowing users to catch
the entire family with a single `except EikonError` clause.

<a id="eikon.exceptions.EikonError"></a>

### *exception* eikon.exceptions.EikonError

Bases: [`Exception`](https://docs.python.org/3/library/exceptions.html#Exception)

Base exception for all eikon errors.

<a id="eikon.exceptions.ConfigError"></a>

### *exception* eikon.exceptions.ConfigError

Bases: [`EikonError`](#eikon.exceptions.EikonError)

Configuration loading or validation error.

<a id="eikon.exceptions.ConfigNotFoundError"></a>

### *exception* eikon.exceptions.ConfigNotFoundError(search_root='.')

Bases: [`ConfigError`](#eikon.exceptions.ConfigError)

No `eikon.yaml` found in the project hierarchy.

* **Parameters:**
  **search_root** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
* **Return type:**
  None

<a id="eikon.exceptions.ConfigValidationError"></a>

### *exception* eikon.exceptions.ConfigValidationError(errors)

Bases: [`ConfigError`](#eikon.exceptions.ConfigError)

Schema validation failure with detailed messages.

* **Parameters:**
  **errors** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Individual validation error messages.
* **Return type:**
  None

<a id="eikon.exceptions.SpecError"></a>

### *exception* eikon.exceptions.SpecError

Bases: [`EikonError`](#eikon.exceptions.EikonError)

Figure specification error.

<a id="eikon.exceptions.SpecValidationError"></a>

### *exception* eikon.exceptions.SpecValidationError(errors)

Bases: [`SpecError`](#eikon.exceptions.SpecError)

Invalid figure specification.

* **Parameters:**
  **errors** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Individual validation error messages.
* **Return type:**
  None

<a id="eikon.exceptions.StyleError"></a>

### *exception* eikon.exceptions.StyleError

Bases: [`EikonError`](#eikon.exceptions.EikonError)

Style loading or composition error.

<a id="eikon.exceptions.StyleNotFoundError"></a>

### *exception* eikon.exceptions.StyleNotFoundError(name)

Bases: [`StyleError`](#eikon.exceptions.StyleError)

Referenced style could not be found.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The style name or path that was not found.
* **Return type:**
  None

<a id="eikon.exceptions.LayoutError"></a>

### *exception* eikon.exceptions.LayoutError

Bases: [`EikonError`](#eikon.exceptions.EikonError)

Layout building or validation error.

<a id="eikon.exceptions.PanelOverlapError"></a>

### *exception* eikon.exceptions.PanelOverlapError(panel_a, panel_b)

Bases: [`LayoutError`](#eikon.exceptions.LayoutError)

Two panels occupy the same grid cells.

* **Parameters:**
  * **panel_a** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the first overlapping panel.
  * **panel_b** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the second overlapping panel.
* **Return type:**
  None

<a id="eikon.exceptions.RenderError"></a>

### *exception* eikon.exceptions.RenderError

Bases: [`EikonError`](#eikon.exceptions.EikonError)

Error during rendering.

<a id="eikon.exceptions.UnknownPlotTypeError"></a>

### *exception* eikon.exceptions.UnknownPlotTypeError(name, available)

Bases: [`RenderError`](#eikon.exceptions.RenderError)

Referenced plot type is not registered.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The unrecognized plot type name.
  * **available** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Currently registered plot type names.
* **Return type:**
  None

<a id="eikon.exceptions.ExportError"></a>

### *exception* eikon.exceptions.ExportError

Bases: [`EikonError`](#eikon.exceptions.EikonError)

Error during figure export.

<a id="eikon.exceptions.RegistryError"></a>

### *exception* eikon.exceptions.RegistryError

Bases: [`EikonError`](#eikon.exceptions.EikonError)

Error in the figure registry.

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

* **Parameters:**
  * **output_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **styles_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **specs_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **data_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

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

* **Parameters:**
  * **formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*ExportFormat*](#eikon._types.ExportFormat) *,*  *...* *]*)
  * **dpi** ([*int*](https://docs.python.org/3/library/functions.html#int))
  * **transparent** ([*bool*](https://docs.python.org/3/library/functions.html#bool))
  * **bbox_inches** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **pad_inches** ([*float*](https://docs.python.org/3/library/functions.html#float))
  * **metadata** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*)

<a id="eikon.config._schema.ExportDefaults.formats"></a>

#### formats *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[ExportFormat](#eikon._types.ExportFormat), ...]*

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

* **Parameters:**
  * **base_style** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **font_family** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **font_size** ([*float*](https://docs.python.org/3/library/functions.html#float))
  * **figure_size** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*float*](https://docs.python.org/3/library/functions.html#float) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *]*)

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

* **Parameters:**
  * **paths** ([*PathsConfig*](#eikon.config._schema.PathsConfig))
  * **export** ([*ExportDefaults*](#eikon.config._schema.ExportDefaults))
  * **style** ([*StyleDefaults*](#eikon.config._schema.StyleDefaults))
  * **registry_file** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

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
  * [**ConfigNotFoundError**](#eikon.exceptions.ConfigNotFoundError) – If no configuration file is found.
  * [**ConfigValidationError**](#eikon.exceptions.ConfigValidationError) – If the configuration fails schema validation.
  * [**ConfigError**](#eikon.exceptions.ConfigError) – If the YAML file cannot be parsed.

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

* **Parameters:**
  * **project_root** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **output_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **styles_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **specs_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **data_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))

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
  [**ConfigNotFoundError**](#eikon.exceptions.ConfigNotFoundError) – If no `eikon.yaml` is found via any method.

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

* **Parameters:**
  * **config** ([*ProjectConfig*](#eikon.config._schema.ProjectConfig))
  * **paths** ([*ResolvedPaths*](#eikon.config._resolver.ResolvedPaths))

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
  [**ConfigNotFoundError**](#eikon.exceptions.ConfigNotFoundError) – If *strict* is `True` and no configuration is found.

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

<a id="module-eikon.spec._figure"></a>

<a id="figure-specifications"></a>

## Figure Specifications

Figure specification — the central declarative abstraction.

A [`FigureSpec`](#eikon.spec._figure.FigureSpec) fully describes a figure: its panels, layout,
style, export settings, and organizational metadata.

<a id="eikon.spec._figure.FigureSpec"></a>

### *class* eikon.spec._figure.FigureSpec(\*, name, title='', tags=(), group='', panels=(), layout=None, style=None, export=None, title_kwargs=None, shared_legend=None, margin_labels=None, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Declarative specification for a single figure.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **title** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **tags** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[**Tag* *,*  *...* *]*)
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **panels** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*PanelSpec*](#eikon.spec._panel.PanelSpec) *,*  *...* *]*)
  * **layout** ([*LayoutSpec*](#eikon.layout._grid.LayoutSpec) *|* *None*)
  * **style** (*StyleRef* *|* *None*)
  * **export** ([*ExportSpec*](#eikon.export._config.ExportSpec) *|* *None*)
  * **title_kwargs** ([*TitleConfig*](#eikon.spec._figure.TitleConfig) *|* *None*)
  * **shared_legend** ([*SharedLegendConfig*](#eikon.spec._figure.SharedLegendConfig) *|* *None*)
  * **margin_labels** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*MarginLabelSpec*](#eikon.spec._margin_labels.MarginLabelSpec) *]*  *|* *None*)
  * **metadata** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*)

<a id="eikon.spec._figure.FigureSpec.name"></a>

#### name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Unique identifier for this figure within the project.

<a id="eikon.spec._figure.FigureSpec.title"></a>

#### title *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Display title rendered on the figure.

<a id="eikon.spec._figure.FigureSpec.tags"></a>

#### tags *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[Tag, ...]*

Organizational tags for filtering and grouping.

<a id="eikon.spec._figure.FigureSpec.group"></a>

#### group *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Grouping key (e.g. `"manuscript-1"`).

<a id="eikon.spec._figure.FigureSpec.panels"></a>

#### panels *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[PanelSpec](#eikon.spec._panel.PanelSpec), ...]*

Ordered panel definitions composing this figure.

<a id="eikon.spec._figure.FigureSpec.layout"></a>

#### layout *: [LayoutSpec](#eikon.layout._grid.LayoutSpec) | [None](https://docs.python.org/3/library/constants.html#None)*

Layout specification (rows, cols, ratios). `None` implies a
single-panel figure.

<a id="eikon.spec._figure.FigureSpec.style"></a>

#### style *: StyleRef | [None](https://docs.python.org/3/library/constants.html#None)*

Figure-level style override.

<a id="eikon.spec._figure.FigureSpec.export"></a>

#### export *: [ExportSpec](#eikon.export._config.ExportSpec) | [None](https://docs.python.org/3/library/constants.html#None)*

Per-figure export settings override.

<a id="eikon.spec._figure.FigureSpec.title_kwargs"></a>

#### title_kwargs *: [TitleConfig](#eikon.spec._figure.TitleConfig) | [None](https://docs.python.org/3/library/constants.html#None)*

Extra keyword arguments forwarded to
`matplotlib.figure.Figure.suptitle()`.  `None` uses
matplotlib defaults.

<a id="eikon.spec._figure.FigureSpec.shared_legend"></a>

#### shared_legend *: [SharedLegendConfig](#eikon.spec._figure.SharedLegendConfig) | [None](https://docs.python.org/3/library/constants.html#None)*

If set, collect legend handles from the first panel that has them
and render a single figure-level legend.

<a id="eikon.spec._figure.FigureSpec.margin_labels"></a>

#### margin_labels *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [MarginLabelSpec](#eikon.spec._margin_labels.MarginLabelSpec)] | [None](https://docs.python.org/3/library/constants.html#None)*

Edge labels for annotating rows or columns.  Keys are edge
names (`"top"`, `"bottom"`, `"left"`, `"right"`).

<a id="eikon.spec._figure.FigureSpec.metadata"></a>

#### metadata *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

Arbitrary metadata fields (e.g. author, project).

<a id="eikon.spec._figure.TitleConfig"></a>

### *class* eikon.spec._figure.TitleConfig(\*, fontsize=None, fontweight=None, y=None, x=None, ha=None, extra=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Keyword arguments forwarded to `matplotlib.figure.Figure.suptitle()`.

* **Parameters:**
  * **fontsize** ([*float*](https://docs.python.org/3/library/functions.html#float) *|* *None*)
  * **fontweight** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*)
  * **y** ([*float*](https://docs.python.org/3/library/functions.html#float) *|* *None*)
  * **x** ([*float*](https://docs.python.org/3/library/functions.html#float) *|* *None*)
  * **ha** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*)
  * **extra** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)

<a id="eikon.spec._figure.TitleConfig.fontsize"></a>

#### fontsize *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Font size in points.

<a id="eikon.spec._figure.TitleConfig.fontweight"></a>

#### fontweight *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Font weight (e.g. `"bold"`).

<a id="eikon.spec._figure.TitleConfig.y"></a>

#### y *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Vertical position in figure coordinates.

<a id="eikon.spec._figure.TitleConfig.x"></a>

#### x *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Horizontal position in figure coordinates.

<a id="eikon.spec._figure.TitleConfig.ha"></a>

#### ha *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Horizontal alignment.

<a id="eikon.spec._figure.TitleConfig.extra"></a>

#### extra *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Additional keyword arguments forwarded verbatim.

<a id="eikon.spec._figure.TitleConfig.to_kwargs"></a>

#### to_kwargs()

Return a dict suitable for `fig.suptitle(**kwargs)`.

* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [*Any*](https://docs.python.org/3/library/typing.html#typing.Any)]

<a id="eikon.spec._figure.SharedLegendConfig"></a>

### *class* eikon.spec._figure.SharedLegendConfig(\*, loc=None, ncol=None, fontsize=None, frameon=None, extra=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Configuration for a shared figure-level legend.

* **Parameters:**
  * **loc** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*)
  * **ncol** ([*int*](https://docs.python.org/3/library/functions.html#int) *|* *None*)
  * **fontsize** ([*float*](https://docs.python.org/3/library/functions.html#float) *|* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*)
  * **frameon** ([*bool*](https://docs.python.org/3/library/functions.html#bool) *|* *None*)
  * **extra** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)

<a id="eikon.spec._figure.SharedLegendConfig.loc"></a>

#### loc *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Legend location (e.g. `"upper right"`).

<a id="eikon.spec._figure.SharedLegendConfig.ncol"></a>

#### ncol *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)*

Number of legend columns.

<a id="eikon.spec._figure.SharedLegendConfig.fontsize"></a>

#### fontsize *: [float](https://docs.python.org/3/library/functions.html#float) | [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Font size for legend text.

<a id="eikon.spec._figure.SharedLegendConfig.frameon"></a>

#### frameon *: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None)*

Whether to draw the legend frame.

<a id="eikon.spec._figure.SharedLegendConfig.extra"></a>

#### extra *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Additional keyword arguments forwarded verbatim.

<a id="eikon.spec._figure.SharedLegendConfig.to_kwargs"></a>

#### to_kwargs()

Return a dict suitable for `fig.legend(**kwargs)`.

* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [*Any*](https://docs.python.org/3/library/typing.html#typing.Any)]

<a id="module-eikon.spec._panel"></a>

<a id="panel-specifications"></a>

## Panel Specifications

Panel specification for a single axes region within a figure.

A [`PanelSpec`](#eikon.spec._panel.PanelSpec) describes one axes panel: its plot type, position
in the grid layout, data binding, and per-panel style overrides.

<a id="eikon.spec._panel.PanelSpec"></a>

### *class* eikon.spec._panel.PanelSpec(\*, name, plot_type, data=None, row=0, col=0, style=None, params=<factory>, label='', auto_size=False, hide_spines=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Specification for one axes panel within a figure.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **plot_type** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **data** ([*DataBinding*](#eikon.spec._data.DataBinding) *|* *None*)
  * **row** ([*int*](https://docs.python.org/3/library/functions.html#int) *|* [*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*int*](https://docs.python.org/3/library/functions.html#int) *,* [*int*](https://docs.python.org/3/library/functions.html#int) *]*)
  * **col** ([*int*](https://docs.python.org/3/library/functions.html#int) *|* [*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*int*](https://docs.python.org/3/library/functions.html#int) *,* [*int*](https://docs.python.org/3/library/functions.html#int) *]*)
  * **style** (*StyleRef* *|* *None*)
  * **params** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)
  * **label** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **auto_size** ([*bool*](https://docs.python.org/3/library/functions.html#bool))
  * **hide_spines** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*  *|* *None*)

<a id="eikon.spec._panel.PanelSpec.name"></a>

#### name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Panel identifier (e.g. `"A"`, `"top-left"`).

<a id="eikon.spec._panel.PanelSpec.plot_type"></a>

#### plot_type *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Registry key for the plot function to invoke.

<a id="eikon.spec._panel.PanelSpec.data"></a>

#### data *: [DataBinding](#eikon.spec._data.DataBinding) | [None](https://docs.python.org/3/library/constants.html#None)*

Data source reference. `None` if data is passed via `params`.

<a id="eikon.spec._panel.PanelSpec.row"></a>

#### row *: [int](https://docs.python.org/3/library/functions.html#int) | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int), [int](https://docs.python.org/3/library/functions.html#int)]*

Row index (zero-based) or `(start, end)` span in the grid.

<a id="eikon.spec._panel.PanelSpec.col"></a>

#### col *: [int](https://docs.python.org/3/library/functions.html#int) | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int), [int](https://docs.python.org/3/library/functions.html#int)]*

Column index (zero-based) or `(start, end)` span in the grid.

<a id="eikon.spec._panel.PanelSpec.style"></a>

#### style *: StyleRef | [None](https://docs.python.org/3/library/constants.html#None)*

Per-panel style override.

<a id="eikon.spec._panel.PanelSpec.params"></a>

#### params *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Keyword arguments forwarded to the plot function.

<a id="eikon.spec._panel.PanelSpec.label"></a>

#### label *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Panel label rendered on the axes (e.g. `"(a)"`, `"(b)"`).

<a id="eikon.spec._panel.PanelSpec.auto_size"></a>

#### auto_size *: [bool](https://docs.python.org/3/library/functions.html#bool)*

When `True`, defer figure size to the constrained-layout solver
rather than using the explicit `figure_size`.

<a id="eikon.spec._panel.PanelSpec.hide_spines"></a>

#### hide_spines *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Spine names to hide on this panel’s axes.  Common values are
`("top", "right")` for a cleaner look.  Valid names:
`"top"`, `"bottom"`, `"left"`, `"right"`.
`None` (default) keeps all spines visible.

<a id="module-eikon.spec._data"></a>

<a id="data-bindings"></a>

## Data Bindings

Data binding specification for figure panels.

A [`DataBinding`](#eikon.spec._data.DataBinding) describes how data is sourced and prepared
before being passed to a plot function.

<a id="eikon.spec._data.DataBinding"></a>

### *class* eikon.spec._data.DataBinding(\*, source='', x='', y='', hue='', transforms=(), params=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Reference to data for a panel.

* **Parameters:**
  * **source** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **x** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **y** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **hue** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **transforms** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*)
  * **params** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)

<a id="eikon.spec._data.DataBinding.source"></a>

#### source *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Path to a data file or a named data source identifier.

<a id="eikon.spec._data.DataBinding.x"></a>

#### x *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Column or field name for the x-axis variable.

<a id="eikon.spec._data.DataBinding.y"></a>

#### y *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Column or field name for the y-axis variable.

<a id="eikon.spec._data.DataBinding.hue"></a>

#### hue *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Grouping variable name for color coding.

<a id="eikon.spec._data.DataBinding.transforms"></a>

#### transforms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

Named transforms to apply in order before plotting.

<a id="eikon.spec._data.DataBinding.params"></a>

#### params *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Additional parameters passed to data loading or transforms.

<a id="module-eikon.spec._margin_labels"></a>

<a id="margin-labels"></a>

## Margin Labels

Margin label specification dataclasses.

Declarative types for figure-edge labels that annotate rows or columns
of a panel grid (or a virtual inset grid within a single panel).

<a id="eikon.spec._margin_labels.MarginLabelSpec"></a>

### *class* eikon.spec._margin_labels.MarginLabelSpec(\*, labels, style=MarginLabelStyle(bg_color=None, text_color='black', fontsize=8.0, fontweight='normal', rotation=None), level_styles=None, target=MarginTarget(kind='layout', axes=None, grid=None), strip_size=0.04, pad=6.0, gap=2.0, zorder=2.1, label_styles=None, cell_range=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Specification for labels on one edge of the figure.

* **Parameters:**
  * **labels** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*  *|* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)
  * **style** ([*MarginLabelStyle*](#eikon.spec._margin_labels.MarginLabelStyle))
  * **level_styles** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*MarginLabelStyle*](#eikon.spec._margin_labels.MarginLabelStyle) *,*  *...* *]*  *|* *None*)
  * **target** ([*MarginTarget*](#eikon.spec._margin_labels.MarginTarget))
  * **strip_size** ([*float*](https://docs.python.org/3/library/functions.html#float))
  * **pad** ([*float*](https://docs.python.org/3/library/functions.html#float))
  * **gap** ([*float*](https://docs.python.org/3/library/functions.html#float))
  * **zorder** ([*float*](https://docs.python.org/3/library/functions.html#float))
  * **label_styles** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*MarginLabelStyle*](#eikon.spec._margin_labels.MarginLabelStyle) *]*  *|* *None*)
  * **cell_range** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*int*](https://docs.python.org/3/library/functions.html#int) *,* [*int*](https://docs.python.org/3/library/functions.html#int) *]*  *|* *None*)

<a id="eikon.spec._margin_labels.MarginLabelSpec.labels"></a>

#### labels *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...] | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Label content.  A flat tuple gives one label per grid cell.
A nested dict expresses hierarchy — keys are group labels,
values are sub-dicts (recursive) or `None` / tuples of
leaf labels.

<a id="eikon.spec._margin_labels.MarginLabelSpec.style"></a>

#### style *: [MarginLabelStyle](#eikon.spec._margin_labels.MarginLabelStyle)*

Default style applied to all labels on this edge.

<a id="eikon.spec._margin_labels.MarginLabelSpec.level_styles"></a>

#### level_styles *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[MarginLabelStyle](#eikon.spec._margin_labels.MarginLabelStyle), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Per-level style overrides (outermost level first).  Falls
back to `style` for any level without an override.

<a id="eikon.spec._margin_labels.MarginLabelSpec.target"></a>

#### target *: [MarginTarget](#eikon.spec._margin_labels.MarginTarget)*

Which grid the labels align to.

<a id="eikon.spec._margin_labels.MarginLabelSpec.strip_size"></a>

#### strip_size *: [float](https://docs.python.org/3/library/functions.html#float)*

Height (for top/bottom) or width (for left/right) of each
label band, in figure-fraction units.

<a id="eikon.spec._margin_labels.MarginLabelSpec.pad"></a>

#### pad *: [float](https://docs.python.org/3/library/functions.html#float)*

Gap between the axes edge and the first label level, in points.

<a id="eikon.spec._margin_labels.MarginLabelSpec.gap"></a>

#### gap *: [float](https://docs.python.org/3/library/functions.html#float)*

Gap between stacked label levels, in points.

<a id="eikon.spec._margin_labels.MarginLabelSpec.zorder"></a>

#### zorder *: [float](https://docs.python.org/3/library/functions.html#float)*

Drawing order for label text and background patches.

<a id="eikon.spec._margin_labels.MarginLabelSpec.label_styles"></a>

#### label_styles *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [MarginLabelStyle](#eikon.spec._margin_labels.MarginLabelStyle)] | [None](https://docs.python.org/3/library/constants.html#None)*

Per-label style overrides keyed by label text.  When a label’s
text matches a key here, this style is used instead of the
level/edge default.

<a id="eikon.spec._margin_labels.MarginLabelSpec.cell_range"></a>

#### cell_range *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int), [int](https://docs.python.org/3/library/functions.html#int)] | [None](https://docs.python.org/3/library/constants.html#None)*

`(start, end)` restricting which cells of the grid the labels
cover (0-indexed, end-exclusive).  `None` = all cells along
the relevant axis.

<a id="eikon.spec._margin_labels.MarginLabelStyle"></a>

### *class* eikon.spec._margin_labels.MarginLabelStyle(\*, bg_color=None, text_color='black', fontsize=8.0, fontweight='normal', rotation=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Visual style for margin label text and optional background strip.

* **Parameters:**
  * **bg_color** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*)
  * **text_color** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **fontsize** ([*float*](https://docs.python.org/3/library/functions.html#float))
  * **fontweight** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **rotation** ([*float*](https://docs.python.org/3/library/functions.html#float) *|* *None*)

<a id="eikon.spec._margin_labels.MarginLabelStyle.bg_color"></a>

#### bg_color *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Background color for the label strip.  `None` = transparent.

<a id="eikon.spec._margin_labels.MarginLabelStyle.text_color"></a>

#### text_color *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Text color.

<a id="eikon.spec._margin_labels.MarginLabelStyle.fontsize"></a>

#### fontsize *: [float](https://docs.python.org/3/library/functions.html#float)*

Font size in points.

<a id="eikon.spec._margin_labels.MarginLabelStyle.fontweight"></a>

#### fontweight *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Font weight (`"normal"`, `"bold"`, etc.).

<a id="eikon.spec._margin_labels.MarginLabelStyle.rotation"></a>

#### rotation *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Text rotation in degrees.  `None` = edge default
(0 for top/bottom, 90 for left, 270 for right).

<a id="eikon.spec._margin_labels.MarginTarget"></a>

### *class* eikon.spec._margin_labels.MarginTarget(\*, kind='layout', axes=None, grid=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Which axes grid the margin labels align to.

For `kind="layout"` (the default), labels align to the figure’s
GridSpec cells.  For `kind="virtual"`, labels subdivide a single
panel’s axes evenly — useful for inset grids drawn inside plot
functions.

* **Parameters:**
  * **kind** ([*Literal*](https://docs.python.org/3/library/typing.html#typing.Literal) *[* *'layout'* *,*  *'virtual'* *]*)
  * **axes** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*)
  * **grid** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*int*](https://docs.python.org/3/library/functions.html#int) *,* [*int*](https://docs.python.org/3/library/functions.html#int) *]*  *|* *None*)

<a id="eikon.spec._margin_labels.MarginTarget.kind"></a>

#### kind *: [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['layout', 'virtual']*

Targeting mode.

<a id="eikon.spec._margin_labels.MarginTarget.axes"></a>

#### axes *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Panel name whose axes to subdivide (required for `"virtual"`).

<a id="eikon.spec._margin_labels.MarginTarget.grid"></a>

#### grid *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int), [int](https://docs.python.org/3/library/functions.html#int)] | [None](https://docs.python.org/3/library/constants.html#None)*

`(rows, cols)` of the virtual grid (required for `"virtual"`).

<a id="module-eikon.spec._override"></a>

<a id="specification-overrides"></a>

## Specification Overrides

Override and merge logic for figure specifications.

Provides utilities to apply partial overrides to `FigureSpec`
instances, producing new immutable specs with the overrides applied.

<a id="eikon.spec._override.merge_spec_override"></a>

### eikon.spec._override.merge_spec_override(base, override)

Apply a dictionary of overrides to a figure specification.

Only fields present in *override* are changed.  Nested dictionaries
(`layout`, `export`, `metadata`) are shallow-merged rather than
replaced outright; typed dataclass fields are re-parsed from raw
dicts when provided.

* **Parameters:**
  * **base** ([*FigureSpec*](#eikon.spec._figure.FigureSpec)) – The base specification.
  * **override** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]*) – Fields to override.
* **Returns:**
  A new specification with overrides applied.
* **Return type:**
  [FigureSpec](#eikon.spec._figure.FigureSpec)

<a id="module-eikon.spec._parse"></a>

<a id="specification-parsing"></a>

## Specification Parsing

Parse figure specifications from YAML files or dictionaries.

Converts raw dictionaries (typically loaded from YAML) into validated
`FigureSpec` instances.

<a id="eikon.spec._parse.parse_figure_file"></a>

### eikon.spec._parse.parse_figure_file(path)

Load and parse a figure specification from a YAML file.

* **Parameters:**
  **path** (*Path*) – Path to the YAML file.
* **Returns:**
  Parsed and validated figure specification.
* **Return type:**
  [FigureSpec](#eikon.spec._figure.FigureSpec)
* **Raises:**
  * [**ConfigError**](#eikon.exceptions.ConfigError) – If the file cannot be read or parsed.
  * [**SpecValidationError**](#eikon.exceptions.SpecValidationError) – If the specification fails validation.

<a id="eikon.spec._parse.parse_figure_spec"></a>

### eikon.spec._parse.parse_figure_spec(raw)

Parse a figure specification from a dictionary.

* **Parameters:**
  **raw** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) – Dictionary representation of a figure specification.
* **Returns:**
  Parsed and validated figure specification.
* **Return type:**
  [FigureSpec](#eikon.spec._figure.FigureSpec)
* **Raises:**
  [**SpecValidationError**](#eikon.exceptions.SpecValidationError) – If the specification fails validation.

<a id="eikon.spec._parse.parse_layout_spec"></a>

### eikon.spec._parse.parse_layout_spec(raw)

Convert a raw layout dictionary to a `LayoutSpec`.

* **Parameters:**
  **raw** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) – Dictionary representation of a layout specification, typically
  from the `layout` key of a figure YAML file.
* **Returns:**
  Parsed layout specification.
* **Return type:**
  [LayoutSpec](#eikon.layout._grid.LayoutSpec)

<a id="module-eikon.style._sheet"></a>

<a id="style-sheets"></a>

## Style Sheets

StyleSheet dataclass — the composable unit of visual styling.

A [`StyleSheet`](#eikon.style._sheet.StyleSheet) captures high-level style properties (font, palette,
line width) that are later translated to matplotlib `rcParams`.  Sheets
can extend other sheets via `extends`, enabling inheritance chains.

<a id="eikon.style._sheet.StyleSheet"></a>

### *class* eikon.style._sheet.StyleSheet(\*, name, font_family=None, font_size=None, line_width=None, palette=None, figure_size=None, rc_overrides=<factory>, extends=())

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Composable style definition for figures.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **font_family** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*)
  * **font_size** ([*float*](https://docs.python.org/3/library/functions.html#float) *|* *None*)
  * **line_width** ([*float*](https://docs.python.org/3/library/functions.html#float) *|* *None*)
  * **palette** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*  *|* *None*)
  * **figure_size** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*float*](https://docs.python.org/3/library/functions.html#float) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *]*  *|* *None*)
  * **rc_overrides** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*object*](https://docs.python.org/3/library/functions.html#object) *]*)
  * **extends** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*)

<a id="eikon.style._sheet.StyleSheet.name"></a>

#### name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Identifier for this style (e.g. `"publication"`).

<a id="eikon.style._sheet.StyleSheet.font_family"></a>

#### font_family *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Font family name.  `None` means “inherit from parent”.

<a id="eikon.style._sheet.StyleSheet.font_size"></a>

#### font_size *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Base font size in points.

<a id="eikon.style._sheet.StyleSheet.line_width"></a>

#### line_width *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Default line width in points.

<a id="eikon.style._sheet.StyleSheet.palette"></a>

#### palette *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Ordered colour palette (hex strings or named colours).

<a id="eikon.style._sheet.StyleSheet.figure_size"></a>

#### figure_size *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[float](https://docs.python.org/3/library/functions.html#float), [float](https://docs.python.org/3/library/functions.html#float)] | [None](https://docs.python.org/3/library/constants.html#None)*

Default `(width, height)` in inches.

<a id="eikon.style._sheet.StyleSheet.rc_overrides"></a>

#### rc_overrides *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [object](https://docs.python.org/3/library/functions.html#object)]*

Raw matplotlib `rcParams` overrides.  Deep-merged during
composition; leaf values win.

<a id="eikon.style._sheet.StyleSheet.extends"></a>

#### extends *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

Ordered parent style names.  Resolved left-to-right, with this
sheet’s values overlaying the merged parents.

<a id="module-eikon.style._loader"></a>

<a id="style-loading"></a>

## Style Loading

Load a `StyleSheet` from any `StyleRef`.

A `StyleRef` can be:

- A **preset name** (e.g. `"publication"`) — looked up in built-in presets.
- A **matplotlib style name** (e.g. `"seaborn-v0_8-paper"`) — converted to a
  minimal `StyleSheet` wrapping the matplotlib style.
- A **file path** (`Path` or string ending in `.yaml` / `.mplstyle`) —
  loaded from disk.
- A **raw dict** — parsed directly into a `StyleSheet`.

<a id="eikon.style._loader.load_style"></a>

### eikon.style._loader.load_style(ref, search_dirs=())

Resolve a `StyleRef` to a `StyleSheet`.

* **Parameters:**
  * **ref** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *Path* *|* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*object*](https://docs.python.org/3/library/functions.html#object) *]*) – Style reference to resolve.
  * **search_dirs** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[**Path* *,*  *...* *]*) – Additional directories to search for style files.
* **Returns:**
  The loaded style sheet.
* **Return type:**
  [StyleSheet](#eikon.style._sheet.StyleSheet)
* **Raises:**
  * [**StyleNotFoundError**](#eikon.exceptions.StyleNotFoundError) – If the reference cannot be resolved.
  * [**StyleError**](#eikon.exceptions.StyleError) – If a style file is malformed.

<a id="module-eikon.style._composer"></a>

<a id="style-composition"></a>

## Style Composition

Style composition — merging and flattening style inheritance chains.

The composer resolves `StyleSheet.extends` chains depth-first, then
overlays the leaf sheet’s explicitly set fields.  `rc_overrides` dicts
are deep-merged; all other fields use rightmost-wins semantics.

<a id="eikon.style._composer.compose_styles"></a>

### eikon.style._composer.compose_styles(\*sheets)

Merge multiple style sheets left-to-right (rightmost wins).

* **Parameters:**
  **\*sheets** ([*StyleSheet*](#eikon.style._sheet.StyleSheet)) – Style sheets to compose, in increasing priority order.
* **Returns:**
  A new sheet with all fields resolved.
* **Return type:**
  [StyleSheet](#eikon.style._sheet.StyleSheet)
* **Raises:**
  [**ValueError**](https://docs.python.org/3/library/exceptions.html#ValueError) – If no sheets are provided.

<a id="eikon.style._composer.resolve_style_chain"></a>

### eikon.style._composer.resolve_style_chain(sheet, registry, \*, \_seen=None)

Resolve the `extends` chain of a style sheet recursively.

Parents are resolved depth-first, left-to-right.  Circular references
are detected and raise [`ValueError`](https://docs.python.org/3/library/exceptions.html#ValueError).

* **Parameters:**
  * **sheet** ([*StyleSheet*](#eikon.style._sheet.StyleSheet)) – The leaf style sheet whose chain to resolve.
  * **registry** (*Mapping* *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*StyleSheet*](#eikon.style._sheet.StyleSheet) *]*) – Name-to-sheet mapping (presets + user-loaded styles).
  * **\_seen** ([*frozenset*](https://docs.python.org/3/library/stdtypes.html#frozenset) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*  *|* *None*) – Internal parameter for cycle detection.
* **Returns:**
  Fully resolved style sheet with no remaining `extends`.
* **Return type:**
  [StyleSheet](#eikon.style._sheet.StyleSheet)

<a id="module-eikon.style._presets"></a>

<a id="style-presets"></a>

## Style Presets

Built-in style presets for common use cases.

Three presets are provided out of the box:

- **publication** — compact, sans-serif fonts, suitable for journal figures.
- **presentation** — larger fonts, sans-serif, readable on slides.
- **poster** — extra-large fonts and line widths for poster figures.

<a id="eikon.style._presets.get_preset"></a>

### eikon.style._presets.get_preset(name)

Return a built-in preset by name, or `None` if not found.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
* **Return type:**
  [*StyleSheet*](#eikon.style._sheet.StyleSheet) | None

<a id="module-eikon.style._rcparams"></a>

<a id="matplotlib-parameters"></a>

## Matplotlib Parameters

Bridge between `StyleSheet` and matplotlib `rcParams`.

Converts high-level style properties to the `rcParams` dict that
matplotlib consumes, and provides a context manager for temporary
application.

<a id="eikon.style._rcparams.to_rcparams"></a>

### eikon.style._rcparams.to_rcparams(sheet)

Convert a `StyleSheet` into a matplotlib `rcParams` dict.

Only fields that are not `None` are included.  The `rc_overrides`
dict is merged last, allowing raw escape-hatch overrides.

* **Parameters:**
  **sheet** ([*StyleSheet*](#eikon.style._sheet.StyleSheet)) – The style sheet to convert.
* **Returns:**
  Dictionary suitable for `matplotlib.rc_context()`.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]

<a id="eikon.style._rcparams.style_context"></a>

### eikon.style._rcparams.style_context(sheet, \*, debug=False)

Temporarily apply a `StyleSheet` as matplotlib `rcParams`.

Uses `matplotlib.rc_context()` to scope changes; all parameters
are reverted when the context manager exits.  Fully re-entrant: nested
calls correctly restore the outer state.

* **Parameters:**
  * **sheet** ([*StyleSheet*](#eikon.style._sheet.StyleSheet)) – The style sheet to apply.
  * **debug** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – When `True`, capture modified keys on entry and assert they are
    restored on exit — useful for detecting plot functions that mutate
    `rcParams` directly outside the context manager.
* **Yields:**
  *None*
* **Return type:**
  Generator[None]

<a id="module-eikon.layout._grid"></a>

<a id="layout-grid"></a>

## Layout Grid

Grid layout specification dataclass.

A [`LayoutSpec`](#eikon.layout._grid.LayoutSpec) declaratively describes the grid structure of a
multi-panel figure: number of rows/columns, size ratios, and spacing.

<a id="eikon.layout._grid.LayoutSpec"></a>

### *class* eikon.layout._grid.LayoutSpec(\*, rows=1, cols=1, width_ratios=None, height_ratios=None, wspace=None, hspace=None, constrained_layout=True)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Declarative specification for a figure’s grid layout.

* **Parameters:**
  * **rows** ([*int*](https://docs.python.org/3/library/functions.html#int))
  * **cols** ([*int*](https://docs.python.org/3/library/functions.html#int))
  * **width_ratios** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*float*](https://docs.python.org/3/library/functions.html#float) *,*  *...* *]*  *|* *None*)
  * **height_ratios** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*float*](https://docs.python.org/3/library/functions.html#float) *,*  *...* *]*  *|* *None*)
  * **wspace** ([*float*](https://docs.python.org/3/library/functions.html#float) *|* *None*)
  * **hspace** ([*float*](https://docs.python.org/3/library/functions.html#float) *|* *None*)
  * **constrained_layout** ([*bool*](https://docs.python.org/3/library/functions.html#bool))

<a id="eikon.layout._grid.LayoutSpec.rows"></a>

#### rows *: [int](https://docs.python.org/3/library/functions.html#int)*

Number of grid rows (>= 1).

<a id="eikon.layout._grid.LayoutSpec.cols"></a>

#### cols *: [int](https://docs.python.org/3/library/functions.html#int)*

Number of grid columns (>= 1).

<a id="eikon.layout._grid.LayoutSpec.width_ratios"></a>

#### width_ratios *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[float](https://docs.python.org/3/library/functions.html#float), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Relative column widths.  Length must equal `cols` when set.

<a id="eikon.layout._grid.LayoutSpec.height_ratios"></a>

#### height_ratios *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[float](https://docs.python.org/3/library/functions.html#float), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Relative row heights.  Length must equal `rows` when set.

<a id="eikon.layout._grid.LayoutSpec.wspace"></a>

#### wspace *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Horizontal spacing between panels (fraction of average axis width).

<a id="eikon.layout._grid.LayoutSpec.hspace"></a>

#### hspace *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Vertical spacing between panels (fraction of average axis height).

<a id="eikon.layout._grid.LayoutSpec.constrained_layout"></a>

#### constrained_layout *: [bool](https://docs.python.org/3/library/functions.html#bool)*

Whether to use matplotlib’s constrained layout engine.

<a id="module-eikon.layout._placement"></a>

<a id="panel-placement"></a>

## Panel Placement

Resolve panel positions to grid slices.

Converts the `row` / `col` fields of `PanelSpec` (which accept
either a single `int` or a `(start, end)` tuple) into `slice` objects
suitable for subscripting a matplotlib `GridSpec`.

<a id="eikon.layout._placement.PanelPlacement"></a>

### *class* eikon.layout._placement.PanelPlacement(\*, panel_name, row_slice, col_slice)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Resolved position of a panel within the grid.

* **Parameters:**
  * **panel_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **row_slice** ([*slice*](https://docs.python.org/3/library/functions.html#slice))
  * **col_slice** ([*slice*](https://docs.python.org/3/library/functions.html#slice))

<a id="eikon.layout._placement.PanelPlacement.panel_name"></a>

#### panel_name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Name of the panel this placement belongs to.

<a id="eikon.layout._placement.PanelPlacement.row_slice"></a>

#### row_slice *: [slice](https://docs.python.org/3/library/functions.html#slice)*

Row span as a `slice` for `GridSpec` subscripting.

<a id="eikon.layout._placement.PanelPlacement.col_slice"></a>

#### col_slice *: [slice](https://docs.python.org/3/library/functions.html#slice)*

Column span as a `slice` for `GridSpec` subscripting.

<a id="eikon.layout._placement.resolve_placements"></a>

### eikon.layout._placement.resolve_placements(panels, layout)

Convert panel row/col fields to grid slice placements.

* **Parameters:**
  * **panels** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*PanelSpec*](#eikon.spec._panel.PanelSpec) *,*  *...* *]*) – Panel specifications with `row` and `col` fields.
  * **layout** ([*LayoutSpec*](#eikon.layout._grid.LayoutSpec)) – The grid layout to place panels within.
* **Returns:**
  One placement per panel, in the same order.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[PanelPlacement](#eikon.layout._placement.PanelPlacement), …]

<a id="module-eikon.layout._builder"></a>

<a id="layout-building"></a>

## Layout Building

Build a matplotlib Figure with positioned Axes from layout specs.

The builder is the final step of the layout pipeline: it takes a
validated `LayoutSpec` and resolved `PanelPlacement` objects
and produces a real `matplotlib.figure.Figure` with one `Axes` per
panel.

<a id="eikon.layout._builder.BuiltLayout"></a>

### *class* eikon.layout._builder.BuiltLayout(\*, figure, axes, grid_spec)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Result of building a layout: a Figure and its named Axes.

* **Parameters:**
  * **figure** (*Figure*)
  * **axes** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)
  * **grid_spec** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any))

<a id="eikon.layout._builder.BuiltLayout.figure"></a>

#### figure *: Figure*

The matplotlib Figure object.

<a id="eikon.layout._builder.BuiltLayout.axes"></a>

#### axes *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Mapping from panel names to their Axes objects.

<a id="eikon.layout._builder.BuiltLayout.grid_spec"></a>

#### grid_spec *: [Any](https://docs.python.org/3/library/typing.html#typing.Any)*

<a id="eikon.layout._builder.build_layout"></a>

### eikon.layout._builder.build_layout(layout, placements, \*, figure_size=(6.4, 4.8), dpi=100)

Create a matplotlib Figure with positioned Axes.

* **Parameters:**
  * **layout** ([*LayoutSpec*](#eikon.layout._grid.LayoutSpec)) – Grid layout specification.
  * **placements** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*PanelPlacement*](#eikon.layout._placement.PanelPlacement) *,*  *...* *]*) – Resolved panel placements (from `resolve_placements()`).
  * **figure_size** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*float*](https://docs.python.org/3/library/functions.html#float) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *]*) – Figure dimensions `(width, height)` in inches.
  * **dpi** ([*int*](https://docs.python.org/3/library/functions.html#int) *|* [*float*](https://docs.python.org/3/library/functions.html#float)) – Resolution in dots per inch.
* **Returns:**
  The Figure and a `dict[str, Axes]` mapping panel names.
* **Return type:**
  [BuiltLayout](#eikon.layout._builder.BuiltLayout)

<a id="module-eikon.layout._constraints"></a>

<a id="layout-constraints"></a>

## Layout Constraints

Layout validation — bounds checking and overlap detection.

Validates that panel placements fit within the grid and that no two
panels occupy intersecting cells.

<a id="eikon.layout._constraints.validate_layout"></a>

### eikon.layout._constraints.validate_layout(placements, layout)

Validate layout constraints and return a list of error messages.

Checks performed:

1. Grid dimensions are positive.
2. Ratio lengths match grid dimensions (when provided).
3. Panels occupy at least one cell.
4. No two panels overlap.

* **Parameters:**
  * **placements** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*PanelPlacement*](#eikon.layout._placement.PanelPlacement) *,*  *...* *]*) – Resolved panel placements.
  * **layout** ([*LayoutSpec*](#eikon.layout._grid.LayoutSpec)) – The grid layout specification.
* **Returns:**
  Validation error messages (empty if valid).
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)]
* **Raises:**
  [**PanelOverlapError**](#eikon.exceptions.PanelOverlapError) – If two panels occupy intersecting grid cells.

<a id="module-eikon.layout._shared_axes"></a>

<a id="shared-axes"></a>

## Shared Axes

Shared-axis linking across panels.

Provides a helper to create shared-x or shared-y axis groups across
named panels after layout build.  This is a thin wrapper around
matplotlib’s `Axes.sharex` / `Axes.sharey`.

<a id="eikon.layout._shared_axes.link_axes"></a>

### eikon.layout._shared_axes.link_axes(built, groups, axis='both')

Link axes across panels so they share scales.

Within each group, the first panel becomes the reference and all
subsequent panels share its x-axis, y-axis, or both.

* **Parameters:**
  * **built** ([*BuiltLayout*](#eikon.layout._builder.BuiltLayout)) – A built layout containing the axes dict.
  * **groups** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]* *,*  *...* *]*) – Groups of panel names to link.  Each inner tuple is one group.
  * **axis** (`"x"` | `"y"` | `"both"`) – Which axis to share.
* **Raises:**
  [**LayoutError**](#eikon.exceptions.LayoutError) – If a panel name is not found in the built layout.
* **Return type:**
  None

<a id="module-eikon.layout._colorbars"></a>

<a id="colorbars"></a>

## Colorbars

Colorbar attachment for layout panels.

Provides a constrained-layout-aware helper to attach a colorbar to a
specific panel in a built layout.

<a id="eikon.layout._colorbars.add_colorbar"></a>

### eikon.layout._colorbars.add_colorbar(built, panel_name, mappable, \*, position='right', size='5%', pad=0.05, \*\*kwargs)

Attach a colorbar to a panel in the built layout.

Uses `fig.colorbar` which is compatible with constrained layout.

* **Parameters:**
  * **built** ([*BuiltLayout*](#eikon.layout._builder.BuiltLayout)) – A built layout containing the figure and axes dict.
  * **panel_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the panel to attach the colorbar to.
  * **mappable** (*ScalarMappable*) – The matplotlib mappable (e.g. `AxesImage`) to draw the colorbar for.
  * **position** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Location: `"right"`, `"left"`, `"top"`, or `"bottom"`.
  * **size** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Colorbar width as a percentage string (e.g. `"5%"`).
  * **pad** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Padding between the axes and colorbar.
  * **\*\*kwargs** – Additional keyword arguments passed to `fig.colorbar`.
* **Returns:**
  The created matplotlib colorbar.
* **Return type:**
  Colorbar
* **Raises:**
  [**LayoutError**](#eikon.exceptions.LayoutError) – If *panel_name* is not found in the built layout.

<a id="module-eikon.layout._insets"></a>

<a id="insets"></a>

## Insets

Inset axes creation and registration.

Provides a helper to create an inset axes within an existing panel and
register it in the `BuiltLayout.axes` dict for downstream use.

<a id="eikon.layout._insets.add_inset"></a>

### eikon.layout._insets.add_inset(built, parent_panel, name, bounds)

Create an inset axes and register it in the layout.

* **Parameters:**
  * **built** ([*BuiltLayout*](#eikon.layout._builder.BuiltLayout)) – A built layout containing the figure and axes dict.
  * **parent_panel** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the panel to create the inset within.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name for the new inset axes.
  * **bounds** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*float*](https://docs.python.org/3/library/functions.html#float) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *]*) – `(x, y, width, height)` in axes-relative coordinates (0–1).
* **Returns:**
  A new `BuiltLayout` with the inset axes added to the `axes` dict.
* **Return type:**
  [BuiltLayout](#eikon.layout._builder.BuiltLayout)
* **Raises:**
  [**LayoutError**](#eikon.exceptions.LayoutError) – If *parent_panel* is not found or *name* already exists.

<a id="module-eikon.render._protocols"></a>

<a id="render-protocols"></a>

## Render Protocols

Protocol definitions for rendering extensibility.

All rendering extension points are defined as [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)
classes — any callable matching the signature works, with no base-class
registration required.

<a id="eikon.render._protocols.PlotFunction"></a>

### *class* eikon.render._protocols.PlotFunction(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Protocol for a function that draws into a matplotlib Axes.

* **Parameters:**
  * **ax** (*Axes*) – The matplotlib Axes to draw into.
  * **\*\*kwargs** (*Any*) – Keyword arguments from `PanelSpec.params` and resolved data.

<a id="eikon.render._protocols.FigurePostProcessor"></a>

### *class* eikon.render._protocols.FigurePostProcessor(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Protocol for a post-processing step applied after all panels are drawn.

* **Parameters:**
  * **figure** (*Figure*) – The matplotlib Figure.
  * **axes** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Axes* *]*) – Panel-name-to-Axes mapping.

<a id="eikon.render._protocols.DataTransform"></a>

### *class* eikon.render._protocols.DataTransform(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Protocol for a data transformation applied before drawing.

* **Parameters:**
  **data** (*Any*) – Raw data from the data binding.
* **Returns:**
  Transformed data passed to the plot function.
* **Return type:**
  Any

<a id="module-eikon.render._handle"></a>

<a id="render-handles"></a>

## Render Handles

FigureHandle — lightweight wrapper around a rendered figure.

A [`FigureHandle`](#eikon.render._handle.FigureHandle) is the primary return type of
`render_figure()` and the convenience `eikon.render()` function.
It provides access to the figure, spec, layout, and export paths
without requiring the user to manage matplotlib or filesystem details.

<a id="eikon.render._handle.FigureHandle"></a>

### *class* eikon.render._handle.FigureHandle(\*, spec, figure, axes=<factory>, export_paths=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Result of rendering a figure.

* **Parameters:**
  * **spec** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any))
  * **figure** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any))
  * **axes** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)
  * **export_paths** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path) *]*)

<a id="eikon.render._handle.FigureHandle.spec"></a>

#### spec *: [Any](https://docs.python.org/3/library/typing.html#typing.Any)*

The `FigureSpec` that was rendered.

<a id="eikon.render._handle.FigureHandle.figure"></a>

#### figure *: [Any](https://docs.python.org/3/library/typing.html#typing.Any)*

The matplotlib `Figure` object.

<a id="eikon.render._handle.FigureHandle.axes"></a>

#### axes *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Panel-name-to-`Axes` mapping.

<a id="eikon.render._handle.FigureHandle.export_paths"></a>

#### export_paths *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]*

Format-to-path mapping of exported files (empty if not exported).

<a id="eikon.render._handle.FigureHandle.show"></a>

#### show()

Display the figure interactively via `plt.show()`.

* **Return type:**
  None

<a id="eikon.render._handle.FigureHandle.path"></a>

#### path(fmt)

Return the export path for a given format, or `None`.

* **Parameters:**
  **fmt** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Export format key (e.g. `"pdf"`, `"svg"`).
* **Return type:**
  [*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path) | None

<a id="eikon.render._handle.FigureHandle.save"></a>

#### save(path, \*, dpi=300, bbox_inches='tight', close=True, \*\*kwargs)

Save the figure to a file and optionally close it.

* **Parameters:**
  * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *Path*) – Destination file path (e.g. `"output/fig.pdf"`).
    Parent directories are created automatically.
  * **dpi** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Resolution in dots per inch.
  * **bbox_inches** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Bounding-box option forwarded to
    `matplotlib.figure.Figure.savefig()`.
  * **close** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether to close the figure after saving (default `True`).
  * **\*\*kwargs** – Extra keyword arguments forwarded to `savefig`.
* **Returns:**
  The resolved output path.
* **Return type:**
  Path

<a id="eikon.render._handle.FigureHandle.close"></a>

#### close()

Close the matplotlib Figure to free memory.

* **Return type:**
  None

<a id="module-eikon.render._context"></a>

<a id="render-contexts"></a>

## Render Contexts

Render context — mutable state carried through the rendering pipeline.

The [`RenderContext`](#eikon.render._context.RenderContext) is an internal object that accumulates state
as the pipeline progresses through its stages.  It is not part of the
public API.

<a id="eikon.render._context.RenderContext"></a>

### *class* eikon.render._context.RenderContext(\*, spec, config, paths, style=None, layout=None, export_formats=(), show=False, overrides=<factory>, data=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Mutable state for a single render pass.

* **Parameters:**
  * **spec** ([*FigureSpec*](#eikon.spec._figure.FigureSpec))
  * **config** ([*ProjectConfig*](#eikon.config._schema.ProjectConfig))
  * **paths** ([*ResolvedPaths*](#eikon.config._resolver.ResolvedPaths))
  * **style** ([*StyleSheet*](#eikon.style._sheet.StyleSheet) *|* *None*)
  * **layout** ([*BuiltLayout*](#eikon.layout._builder.BuiltLayout) *|* *None*)
  * **export_formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*)
  * **show** ([*bool*](https://docs.python.org/3/library/functions.html#bool))
  * **overrides** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)
  * **data** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]* *]*)

<a id="eikon.render._context.RenderContext.spec"></a>

#### spec *: [FigureSpec](#eikon.spec._figure.FigureSpec)*

The figure specification being rendered.

<a id="eikon.render._context.RenderContext.config"></a>

#### config *: [ProjectConfig](#eikon.config._schema.ProjectConfig)*

The resolved project configuration.

<a id="eikon.render._context.RenderContext.paths"></a>

#### paths *: [ResolvedPaths](#eikon.config._resolver.ResolvedPaths)*

<a id="eikon.render._context.RenderContext.style"></a>

#### style *: [StyleSheet](#eikon.style._sheet.StyleSheet) | [None](https://docs.python.org/3/library/constants.html#None)*

The resolved style sheet (set during style resolution).

<a id="eikon.render._context.RenderContext.layout"></a>

#### layout *: [BuiltLayout](#eikon.layout._builder.BuiltLayout) | [None](https://docs.python.org/3/library/constants.html#None)*

The built layout (set during layout building).

<a id="eikon.render._context.RenderContext.export_formats"></a>

#### export_formats *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

Formats to export (empty = no export).

<a id="eikon.render._context.RenderContext.show"></a>

#### show *: [bool](https://docs.python.org/3/library/functions.html#bool)*

Whether to display the figure interactively after rendering.

<a id="eikon.render._context.RenderContext.overrides"></a>

#### overrides *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Per-call keyword overrides.

<a id="eikon.render._context.RenderContext.data"></a>

#### data *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]]*

<a id="module-eikon.render._data"></a>

<a id="render-data-loading"></a>

## Render Data Loading

Data resolution utilities for the rendering pipeline.

Resolves [`DataBinding`](#eikon.spec._data.DataBinding) instances into concrete
keyword arguments that are forwarded to plot functions. Data files are
resolved relative to the project’s configured `data_dir` and loaded
using lightweight, dependency-tolerant logic (pandas if available,
fallback to the stdlib CSV reader).

<a id="eikon.render._data.resolve_data_binding"></a>

### eikon.render._data.resolve_data_binding(binding, data_dir, \*, extensions=None)

Load data for a panel and return kwargs for the plot function.

Returns a dict containing at least `data` (the loaded table-like
object) plus `x`/`y`/`hue` keys when the binding specifies
corresponding columns.

* **Parameters:**
  * **binding** ([*DataBinding*](#eikon.spec._data.DataBinding))
  * **data_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **extensions** ([*ExtensionRegistry*](#eikon.ext._registry.ExtensionRegistry) *|* *None*)
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [*Any*](https://docs.python.org/3/library/typing.html#typing.Any)]

<a id="module-eikon.render._drawing"></a>

<a id="drawing"></a>

## Drawing

Panel drawing dispatch — route draw calls to registered plot functions.

This module connects the rendering pipeline to the extension registry:
for each panel, it looks up the registered plot function by
`PanelSpec.plot_type` and invokes it on the corresponding `Axes`.

<a id="eikon.render._drawing.draw_panel"></a>

### eikon.render._drawing.draw_panel(ax, panel, \*, data_dir, extensions=None)

Draw a single panel using its registered plot function.

* **Parameters:**
  * **ax** (*Axes*) – The matplotlib Axes to draw into.
  * **panel** ([*PanelSpec*](#eikon.spec._panel.PanelSpec)) – The panel specification containing plot_type and params.
  * **data_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **extensions** ([*ExtensionRegistry*](#eikon.ext._registry.ExtensionRegistry) *|* *None*)
* **Raises:**
  [**UnknownPlotTypeError**](#eikon.exceptions.UnknownPlotTypeError) – If the panel’s `plot_type` is not registered.
* **Return type:**
  None

<a id="eikon.render._drawing.draw_all_panels"></a>

### eikon.render._drawing.draw_all_panels(axes, panels, \*, data_dir, extensions=None)

Draw all panels into their corresponding axes.

* **Parameters:**
  * **axes** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Axes* *]*) – Panel-name-to-Axes mapping from `BuiltLayout`.
  * **panels** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*PanelSpec*](#eikon.spec._panel.PanelSpec) *,*  *...* *]*) – Panel specifications to draw.
  * **data_dir** ([*Path*](https://docs.python.org/3/library/pathlib.html#pathlib.Path))
  * **extensions** ([*ExtensionRegistry*](#eikon.ext._registry.ExtensionRegistry) *|* *None*)
* **Return type:**
  None

<a id="module-eikon.render._pipeline"></a>

<a id="render-pipeline"></a>

## Render Pipeline

Rendering pipeline orchestrator.

Chains the rendering stages: config -> style -> layout -> draw -> post-process -> export.
Each stage is a pure function with explicit typed inputs and outputs.
The orchestrator composes stages without mutable shared state.

<a id="eikon.render._pipeline.render_figure"></a>

### eikon.render._pipeline.render_figure(spec, \*, session=None, config=None, resolved_paths=None, formats=(), show=False, overrides=None, extensions=None)

Render a figure from its specification — the main pipeline entry point.

* **Parameters:**
  * **spec** ([*FigureSpec*](#eikon.spec._figure.FigureSpec)) – The figure specification to render.
  * **session** ([*ProjectSession*](#eikon.config._session.ProjectSession) *,* *optional*) – A pre-built project session.  Takes precedence over *config*
    and *resolved_paths*.
  * **config** ([*ProjectConfig*](#eikon.config._schema.ProjectConfig) *,* *optional*) – Project configuration.  Defaults to built-in defaults.
  * **resolved_paths** ([*ResolvedPaths*](#eikon.config._resolver.ResolvedPaths) *,* *optional*) – Pre-resolved paths.
  * **formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Export format names (e.g. `("pdf", "svg")`).  Empty = no export.
  * **show** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether to display the figure interactively after rendering.
  * **overrides** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]* *,* *optional*) – Per-call keyword overrides forwarded to the pipeline.
  * **extensions** ([*ExtensionRegistry*](#eikon.ext._registry.ExtensionRegistry) *|* *None*)
* **Returns:**
  A handle to the rendered figure.
* **Return type:**
  [FigureHandle](#eikon.render._handle.FigureHandle)
* **Raises:**
  [**RenderError**](#eikon.exceptions.RenderError) – If any stage of the pipeline fails.

<a id="module-eikon.render._margin_labels"></a>

<a id="render-margin-labels"></a>

## Render Margin Labels

Margin label rendering — hierarchy resolution, geometry, and drawing.

Converts declarative `MarginLabelSpec` definitions into positioned
text and optional background patches on a matplotlib Figure.

<a id="eikon.render._margin_labels.draw_margin_labels"></a>

### eikon.render._margin_labels.draw_margin_labels(fig, built, margin_labels)

Render margin labels on the figure.

* **Parameters:**
  * **fig** (*Figure*) – The matplotlib figure to draw on.
  * **built** ([*BuiltLayout*](#eikon.layout._builder.BuiltLayout)) – The built layout (provides `grid_spec` and `axes`).
  * **margin_labels** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*MarginLabelSpec*](#eikon.spec._margin_labels.MarginLabelSpec) *]*) – Mapping from edge name to label spec.
* **Return type:**
  None

<a id="module-eikon.export._config"></a>

<a id="export-configuration"></a>

## Export Configuration

Export configuration dataclasses.

[`ExportSpec`](#eikon.export._config.ExportSpec) holds per-figure export overrides.
[`ResolvedExportConfig`](#eikon.export._config.ResolvedExportConfig) is the fully resolved configuration with no
`None` values, produced by merging `ExportSpec` on top of
`ExportDefaults` from the project configuration.

<a id="eikon.export._config.CollisionMode"></a>

### *class* eikon.export._config.CollisionMode(\*values)

Bases: [`StrEnum`](https://docs.python.org/3/library/enum.html#enum.StrEnum)

Closed set of export collision policies.

<a id="eikon.export._config.CollisionMode.OVERWRITE"></a>

#### OVERWRITE *= 'overwrite'*

<a id="eikon.export._config.CollisionMode.INCREMENT"></a>

#### INCREMENT *= 'increment'*

<a id="eikon.export._config.CollisionMode.FAIL"></a>

#### FAIL *= 'fail'*

<a id="eikon.export._config.ExportSpec"></a>

### *class* eikon.export._config.ExportSpec(\*, formats=None, dpi=None, transparent=None, filename_template=None, subdirectory=None, collision=None, metadata=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Per-figure export overrides.

Any `None` field inherits the project-level default.

* **Parameters:**
  * **formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*  *|* *None*)
  * **dpi** ([*int*](https://docs.python.org/3/library/functions.html#int) *|* *None*)
  * **transparent** ([*bool*](https://docs.python.org/3/library/functions.html#bool) *|* *None*)
  * **filename_template** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*)
  * **subdirectory** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *None*)
  * **collision** ([*CollisionMode*](#eikon.export._config.CollisionMode) *|* *None*)
  * **metadata** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*  *|* *None*)

<a id="eikon.export._config.ExportSpec.formats"></a>

#### formats *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Format names (e.g. `("pdf", "svg")`).

<a id="eikon.export._config.ExportSpec.dpi"></a>

#### dpi *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)*

Resolution in dots per inch.

<a id="eikon.export._config.ExportSpec.transparent"></a>

#### transparent *: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None)*

Export with transparent background.

<a id="eikon.export._config.ExportSpec.filename_template"></a>

#### filename_template *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

`{name}`, `{group}`,
`{date}`, `{format}`.

* **Type:**
  Template for output filename.  Variables

<a id="eikon.export._config.ExportSpec.subdirectory"></a>

#### subdirectory *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Subdirectory under the output dir (e.g. a group folder).

<a id="eikon.export._config.ExportSpec.collision"></a>

#### collision *: [CollisionMode](#eikon.export._config.CollisionMode) | [None](https://docs.python.org/3/library/constants.html#None)*

How to handle existing files at the export path.

<a id="eikon.export._config.ExportSpec.metadata"></a>

#### metadata *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)] | [None](https://docs.python.org/3/library/constants.html#None)*

Additional metadata to inject into exported files.

<a id="eikon.export._config.ResolvedExportConfig"></a>

### *class* eikon.export._config.ResolvedExportConfig(\*, formats, dpi, transparent, bbox_inches, pad_inches, filename_template, subdirectory, collision, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Fully resolved export configuration — no optional fields.

* **Parameters:**
  * **formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*ExportFormat*](#eikon._types.ExportFormat) *,*  *...* *]*)
  * **dpi** ([*int*](https://docs.python.org/3/library/functions.html#int))
  * **transparent** ([*bool*](https://docs.python.org/3/library/functions.html#bool))
  * **bbox_inches** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **pad_inches** ([*float*](https://docs.python.org/3/library/functions.html#float))
  * **filename_template** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **subdirectory** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **collision** ([*CollisionMode*](#eikon.export._config.CollisionMode))
  * **metadata** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*)

<a id="eikon.export._config.ResolvedExportConfig.formats"></a>

#### formats *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[ExportFormat](#eikon._types.ExportFormat), ...]*

Export file formats.

<a id="eikon.export._config.ResolvedExportConfig.dpi"></a>

#### dpi *: [int](https://docs.python.org/3/library/functions.html#int)*

Resolution in dots per inch.

<a id="eikon.export._config.ResolvedExportConfig.transparent"></a>

#### transparent *: [bool](https://docs.python.org/3/library/functions.html#bool)*

Transparent background flag.

<a id="eikon.export._config.ResolvedExportConfig.bbox_inches"></a>

#### bbox_inches *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Bounding box setting for `savefig`.

<a id="eikon.export._config.ResolvedExportConfig.pad_inches"></a>

#### pad_inches *: [float](https://docs.python.org/3/library/functions.html#float)*

Padding around the figure.

<a id="eikon.export._config.ResolvedExportConfig.filename_template"></a>

#### filename_template *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Template for output filenames.

<a id="eikon.export._config.ResolvedExportConfig.subdirectory"></a>

#### subdirectory *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Subdirectory under the output dir.

<a id="eikon.export._config.ResolvedExportConfig.collision"></a>

#### collision *: [CollisionMode](#eikon.export._config.CollisionMode)*

`"overwrite"`, `"increment"`, or `"fail"`.

* **Type:**
  Collision strategy

<a id="eikon.export._config.ResolvedExportConfig.metadata"></a>

#### metadata *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

Metadata injected into exported files.

<a id="eikon.export._config.parse_collision_mode"></a>

### eikon.export._config.parse_collision_mode(value)

Normalize and validate a collision policy value.

* **Parameters:**
  **value** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*CollisionMode*](#eikon.export._config.CollisionMode))
* **Return type:**
  [*CollisionMode*](#eikon.export._config.CollisionMode)

<a id="eikon.export._config.resolve_export_config"></a>

### eikon.export._config.resolve_export_config(defaults, spec_export=None, cli_formats=())

Merge per-figure overrides on top of project defaults.

* **Parameters:**
  * **defaults** ([*ExportDefaults*](#eikon.config._schema.ExportDefaults)) – Project-level export settings.
  * **spec_export** ([*ExportSpec*](#eikon.export._config.ExportSpec) *,* *optional*) – Per-figure overrides.
  * **cli_formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Format names from CLI flags (highest priority).
* **Returns:**
  Fully resolved configuration.
* **Return type:**
  [ResolvedExportConfig](#eikon.export._config.ResolvedExportConfig)

<a id="module-eikon.export._batch"></a>

<a id="export-batch"></a>

## Export Batch

Batch export across multiple figures and formats.

The [`batch_export()`](#eikon.export._batch.batch_export) function exports a rendered figure to all
configured formats, returning a mapping of format names to file paths.

<a id="eikon.export._batch.batch_export"></a>

### eikon.export._batch.batch_export(\*, figure, name, group='', output_dir, export_defaults, export_spec=None, cli_formats=(), extensions=None)

Export a rendered figure to all configured formats.

* **Parameters:**
  * **figure** (*Figure*) – The matplotlib Figure to export.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Figure name (used for filename construction).
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Figure group name.
  * **output_dir** (*Path*) – Base output directory.
  * **export_defaults** ([*ExportDefaults*](#eikon.config._schema.ExportDefaults)) – Project-level export settings.
  * **export_spec** ([*ExportSpec*](#eikon.export._config.ExportSpec) *,* *optional*) – Per-figure export overrides.
  * **cli_formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Format names from CLI flags (highest priority).
  * **extensions** ([*ExtensionRegistry*](#eikon.ext._registry.ExtensionRegistry) *|* *None*)
* **Returns:**
  Mapping of format name (lowercase) to exported file path.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Path]
* **Raises:**
  [**ExportError**](#eikon.exceptions.ExportError) – If any export operation fails.

<a id="module-eikon.export._handlers"></a>

<a id="export-handlers"></a>

## Export Handlers

Format-specific export handlers.

Each handler wraps `Figure.savefig()` with format-appropriate options.
Custom handlers can be registered via [`register_format_handler()`](#eikon.export._handlers.register_format_handler).

<a id="eikon.export._handlers.export_figure"></a>

### eikon.export._handlers.export_figure(figure, path, fmt, config)

Export a figure to a file using the appropriate handler.

* **Parameters:**
  * **figure** (*Figure*) – The matplotlib Figure to export.
  * **path** (*Path*) – Output file path.
  * **fmt** ([*ExportFormat*](#eikon._types.ExportFormat)) – Export format.
  * **config** ([*ResolvedExportConfig*](#eikon.export._config.ResolvedExportConfig)) – Resolved export settings.
* **Return type:**
  None

<a id="eikon.export._handlers.get_handler"></a>

### eikon.export._handlers.get_handler(fmt)

Return the handler function for a given format.

Looks up custom-registered handlers first, then falls back to
built-in defaults.

* **Parameters:**
  **fmt** ([*ExportFormat*](#eikon._types.ExportFormat)) – Export format.
* **Returns:**
  A handler function `(figure, path, config) -> None`.
* **Return type:**
  Callable
* **Raises:**
  [**KeyError**](https://docs.python.org/3/library/exceptions.html#KeyError) – If no handler is registered for the format.

<a id="eikon.export._handlers.register_format_handler"></a>

### eikon.export._handlers.register_format_handler(fmt, handler)

Register a custom export handler for a format.

This allows overriding built-in handlers or adding support for new
formats (after adding the format to `ExportFormat`).

* **Parameters:**
  * **fmt** ([*ExportFormat*](#eikon._types.ExportFormat)) – The export format to register the handler for.
  * **handler** (*Callable*) – A callable with signature `(figure, path, config) -> None`.
* **Return type:**
  None

<a id="module-eikon.export._metadata"></a>

<a id="export-metadata"></a>

## Export Metadata

Post-export metadata injection.

Provides functions to inject metadata into already-exported files.
PDF metadata is handled natively by matplotlib’s `savefig`, but this
module offers a post-hoc injection path for workflows that need to add
metadata after the initial save (e.g. batch annotation).

PNG metadata uses matplotlib’s built-in text chunk support.

<a id="eikon.export._metadata.inject_pdf_metadata"></a>

### eikon.export._metadata.inject_pdf_metadata(path, metadata)

Inject metadata into an existing PDF file.

Uses `pypdf` to read, annotate, and re-write the PDF.  If `pypdf`
is not installed, emits a warning and returns without modifying the
file.  If the file does not exist or metadata is empty, this is a no-op.

* **Parameters:**
  * **path** (*Path*) – Path to the PDF file.
  * **metadata** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Key-value metadata pairs (e.g. `{"Author": "Name"}`).
* **Return type:**
  None

<a id="eikon.export._metadata.inject_png_metadata"></a>

### eikon.export._metadata.inject_png_metadata(path, metadata)

Inject text metadata into an existing PNG file.

Re-saves the PNG with updated text chunks.  If the file does not exist
or metadata is empty, this is a no-op.

* **Parameters:**
  * **path** (*Path*) – Path to the PNG file.
  * **metadata** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Key-value metadata pairs.
* **Return type:**
  None

### Notes

Requires Pillow for PNG text chunk manipulation.  Falls back to a no-op
if Pillow is not installed.

<a id="module-eikon.export._paths"></a>

<a id="export-paths"></a>

## Export Paths

Export path construction with template variable substitution.

Builds the output file path for each exported figure by combining the
output directory, optional subdirectory, sanitized filename, and format
extension.  Handles filename collision via configurable strategies.

<a id="eikon.export._paths.build_export_path"></a>

### eikon.export._paths.build_export_path(\*, name, fmt, output_dir, filename_template='{name}', subdirectory='', group='', collision=CollisionMode.OVERWRITE)

Build the export file path for a single format.

Template variables:
- `{name}` — figure name (sanitized)
- `{group}` — figure group (sanitized, empty string if unset)
- `{date}` — current date as `YYYY-MM-DD`
- `{format}` — export format extension (e.g. `pdf`)

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Figure name from the specification.
  * **fmt** ([*ExportFormat*](#eikon._types.ExportFormat)) – Export format.
  * **output_dir** (*Path*) – Base output directory.
  * **filename_template** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Template string for the filename (without extension).
  * **subdirectory** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Subdirectory under `output_dir`.
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Figure group name.
  * **collision** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Collision strategy: `"overwrite"`, `"increment"`, or `"fail"`.
* **Returns:**
  Fully resolved output file path.
* **Return type:**
  Path
* **Raises:**
  [**ExportError**](#eikon.exceptions.ExportError) – If `collision="fail"` and the target path already exists.

<a id="module-eikon.export._sanitize"></a>

<a id="filename-sanitization"></a>

## Filename Sanitization

Filename sanitization for cross-platform safety.

Ensures exported filenames are safe on Windows, macOS, and Linux by
stripping or replacing problematic characters and enforcing length limits.

<a id="eikon.export._sanitize.sanitize_filename"></a>

### eikon.export._sanitize.sanitize_filename(name)

Sanitize a string for use as a filename.

- Strips leading/trailing whitespace.
- Replaces illegal characters with underscores.
- Collapses consecutive underscores.
- Truncates to 200 characters.
- Returns `"unnamed"` for empty inputs.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Raw filename (without extension).
* **Returns:**
  Sanitized filename safe for all major operating systems.
* **Return type:**
  [str](https://docs.python.org/3/library/stdtypes.html#str)

<a id="module-eikon.registry._registry"></a>

<a id="registry"></a>

## Registry

Registry class — CRUD operations on the figure registry.

The [`Registry`](#eikon.registry._registry.Registry) provides a high-level API for managing figure
entries: registering, querying, removing, and persisting to YAML.

<a id="eikon.registry._registry.Registry"></a>

### *class* eikon.registry._registry.Registry(path)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

In-memory figure registry backed by a YAML manifest.

* **Parameters:**
  **path** (*Path*) – Path to the YAML manifest file.

<a id="eikon.registry._registry.Registry.load"></a>

#### load()

Load entries from the manifest file.

If the file does not exist, the registry starts empty.

* **Return type:**
  None

<a id="eikon.registry._registry.Registry.save"></a>

#### save()

Persist current entries to the manifest file.

* **Return type:**
  None

<a id="eikon.registry._registry.Registry.register"></a>

#### register(name, \*, tags=(), group='', metadata=None, on_conflict='update', spec_path=None)

Register a figure in the registry.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Figure name (unique identifier).
  * **tags** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Organizational tags.
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Grouping key (e.g. `"manuscript-1"`).
  * **metadata** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]* *,* *optional*) – Arbitrary metadata fields.
  * **on_conflict** ( *{"update"* *,*  *"fail"* *,*  *"skip"}*) – How to handle duplicate names. `"update"` replaces the existing
    entry, `"fail"` raises `RegistryError`, and `"skip"` keeps
    the existing entry.
  * **spec_path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *optional*) – Path to the figure specification YAML file.
* **Raises:**
  [**RegistryError**](#eikon.exceptions.RegistryError) – If `on_conflict="fail"` and the name already exists.
* **Return type:**
  None

<a id="eikon.registry._registry.Registry.get"></a>

#### get(name)

Get a registry entry by name.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Figure name.
* **Returns:**
  The entry data.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]
* **Raises:**
  [**RegistryError**](#eikon.exceptions.RegistryError) – If the name is not registered.

<a id="eikon.registry._registry.Registry.remove"></a>

#### remove(name)

Remove a figure from the registry.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Figure name.
* **Raises:**
  [**RegistryError**](#eikon.exceptions.RegistryError) – If the name is not registered.
* **Return type:**
  None

<a id="eikon.registry._registry.Registry.list_all"></a>

#### list_all()

Return a sorted list of all registered figure names.

* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="eikon.registry._registry.Registry.query"></a>

#### query(\*, tags=(), group='', match_all_tags=False)

Query the registry with optional tag and group filters.

* **Parameters:**
  * **tags** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Tags to match.  Empty = no tag filter.
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Group to match.  Empty = no group filter.
  * **match_all_tags** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If `True`, entries must have **all** tags.
* **Returns:**
  Matching entries.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]]

<a id="module-eikon.registry._index"></a>

<a id="registry-index"></a>

## Registry Index

YAML manifest I/O for the figure registry.

The manifest is a YAML file (default `eikon-registry.yaml`) that
persists registry entries across sessions.  Each entry stores the
figure name, tags, group, and the timestamp of last registration.

<a id="eikon.registry._index.load_manifest"></a>

### eikon.registry._index.load_manifest(path)

Load the registry manifest from a YAML file.

* **Parameters:**
  **path** (*Path*) – Path to the manifest file.
* **Returns:**
  Mapping of figure names to their registry entries.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]]
* **Raises:**
  [**RegistryError**](#eikon.exceptions.RegistryError) – If the file exists but is not a valid YAML mapping.

<a id="eikon.registry._index.save_manifest"></a>

### eikon.registry._index.save_manifest(path, entries)

Save the registry manifest to a YAML file.

* **Parameters:**
  * **path** (*Path*) – Path to the manifest file.
  * **entries** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]* *]*) – Mapping of figure names to their registry entries.
* **Return type:**
  None

<a id="module-eikon.registry._query"></a>

<a id="registry-queries"></a>

## Registry Queries

Query and filter logic for registry entries.

Provides functions to filter registry entries by tags, group,
or arbitrary predicates.

<a id="eikon.registry._query.filter_by_tags"></a>

### eikon.registry._query.filter_by_tags(entries, tags, \*, match_all=False)

Filter entries that have any (or all) of the given tags.

* **Parameters:**
  * **entries** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]* *]*) – Registry entries to filter.
  * **tags** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Tags to match against.
  * **match_all** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If `True`, an entry must have **all** tags.
    If `False` (default), an entry must have **any** tag.
* **Returns:**
  Filtered entries.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]]

<a id="eikon.registry._query.filter_by_group"></a>

### eikon.registry._query.filter_by_group(entries, group)

Filter entries belonging to a specific group.

* **Parameters:**
  * **entries** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]* *]*) – Registry entries to filter.
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Group name to match.
* **Returns:**
  Filtered entries.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]]

<a id="eikon.registry._query.filter_entries"></a>

### eikon.registry._query.filter_entries(entries, \*, tags=(), group='', match_all_tags=False)

Apply tag and group filters in sequence.

* **Parameters:**
  * **entries** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]* *]*) – Registry entries to filter.
  * **tags** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Tags to match.  Empty = no tag filter.
  * **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Group name.  Empty = no group filter.
  * **match_all_tags** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether tag matching requires all tags.
* **Returns:**
  Filtered entries.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Any]]

<a id="module-eikon.registry._locking"></a>

<a id="registry-locking"></a>

## Registry Locking

Advisory file locking for concurrent registry access.

Provides a context manager that acquires an exclusive lock on the
registry manifest file, preventing partial reads or lost writes when
multiple processes access the same manifest concurrently.

Uses `fcntl.flock` (Unix/macOS) when available, with a no-op
fallback on platforms that lack `fcntl` (e.g. Windows).

<a id="eikon.registry._locking.registry_lock"></a>

### eikon.registry._locking.registry_lock(path, \*, timeout=5.0)

Acquire an exclusive advisory lock on a file.

* **Parameters:**
  * **path** (*Path*) – Path to the file to lock.  A `.lock` sibling file is used.
  * **timeout** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Maximum seconds to wait for the lock.  Defaults to 5.
* **Yields:**
  *None* – Control while the lock is held.
* **Raises:**
  [**RegistryError**](#eikon.exceptions.RegistryError) – If the lock cannot be acquired within *timeout*.
* **Return type:**
  [*Generator*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Generator)[None]

<a id="module-eikon.ext._registry"></a>

<a id="extension-registry"></a>

## Extension Registry

Explicit extension registry and runtime bootstrap helpers.

<a id="eikon.ext._registry.ExtensionRegistry"></a>

### *class* eikon.ext._registry.ExtensionRegistry(\*, plot_types=None, hooks=None, transforms=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Container for plot types, hooks, and transforms.

* **Parameters:**
  * **plot_types** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Callable* *[* *...* *,* *None* *]* *]*  *|* *None*)
  * **hooks** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[**Any* *,* [*list*](https://docs.python.org/3/library/stdtypes.html#list) *[**Callable* *[* *...* *,* *Any* *]* *]* *]*  *|* *None*)
  * **transforms** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Callable* *[* *[**Any* *]* *,* *Any* *]* *]*  *|* *None*)

<a id="eikon.ext._registry.ExtensionRegistry.clone"></a>

#### clone()

* **Return type:**
  [*ExtensionRegistry*](#eikon.ext._registry.ExtensionRegistry)

<a id="eikon.ext._registry.ExtensionRegistry.register_plot_type"></a>

#### register_plot_type(name, fn)

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **fn** ([*Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable) *[* *[* *...* *]* *,* *None* *]*)
* **Return type:**
  None

<a id="eikon.ext._registry.ExtensionRegistry.get_plot_type"></a>

#### get_plot_type(name)

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
* **Return type:**
  [*Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable)[[…], None]

<a id="eikon.ext._registry.ExtensionRegistry.list_plot_types"></a>

#### list_plot_types()

* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="eikon.ext._registry.ExtensionRegistry.clear_plot_types"></a>

#### clear_plot_types()

* **Return type:**
  None

<a id="eikon.ext._registry.ExtensionRegistry.register_hook"></a>

#### register_hook(hook, fn)

* **Parameters:**
  * **hook** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any))
  * **fn** ([*Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable) *[* *[* *...* *]* *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)
* **Return type:**
  None

<a id="eikon.ext._registry.ExtensionRegistry.fire_hook"></a>

#### fire_hook(hook, \*\*kwargs)

* **Parameters:**
  * **hook** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any))
  * **kwargs** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any))
* **Return type:**
  None

<a id="eikon.ext._registry.ExtensionRegistry.clear_hooks"></a>

#### clear_hooks()

* **Return type:**
  None

<a id="eikon.ext._registry.ExtensionRegistry.register_transform"></a>

#### register_transform(name, fn)

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **fn** ([*Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable) *[* *[*[*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]* *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)
* **Return type:**
  None

<a id="eikon.ext._registry.ExtensionRegistry.list_transforms"></a>

#### list_transforms()

* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="eikon.ext._registry.ExtensionRegistry.clear_transforms"></a>

#### clear_transforms()

* **Return type:**
  None

<a id="eikon.ext._registry.ExtensionRegistry.apply_transforms"></a>

#### apply_transforms(data, names)

* **Parameters:**
  * **data** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any))
  * **names** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*)
* **Return type:**
  [*Any*](https://docs.python.org/3/library/typing.html#typing.Any)

<a id="eikon.ext._registry.build_runtime_registry"></a>

### eikon.ext._registry.build_runtime_registry()

Return a bootstrapped snapshot for one render/runtime session.

* **Return type:**
  [*ExtensionRegistry*](#eikon.ext._registry.ExtensionRegistry)

<a id="eikon.ext._registry.get_default_registry"></a>

### eikon.ext._registry.get_default_registry()

Return the mutable process-local default registry.

* **Return type:**
  [*ExtensionRegistry*](#eikon.ext._registry.ExtensionRegistry)

<a id="module-eikon.ext._plot_types"></a>

<a id="plot-types"></a>

## Plot Types

Plot type registry — string-keyed dictionary of plot functions.

Provides a global registry of plot functions, a `@plot_type` decorator
for registration, and a lookup function used by the drawing module.

<a id="eikon.ext._plot_types.register_plot_type"></a>

### eikon.ext._plot_types.register_plot_type(name, fn)

Register a plot function under a string key.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The plot type name (e.g. `"line"`, `"scatter"`).
  * **fn** ([*PlotFunction*](#eikon.render._protocols.PlotFunction)) – A callable matching the `PlotFunction` protocol.
* **Return type:**
  None

<a id="eikon.ext._plot_types.get_plot_type"></a>

### eikon.ext._plot_types.get_plot_type(name)

Look up a registered plot function by name.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The plot type name.
* **Returns:**
  The registered plot function.
* **Return type:**
  [PlotFunction](#eikon.render._protocols.PlotFunction)
* **Raises:**
  [**UnknownPlotTypeError**](#eikon.exceptions.UnknownPlotTypeError) – If no plot type is registered under *name*.

<a id="eikon.ext._plot_types.plot_type"></a>

### eikon.ext._plot_types.plot_type(name)

Decorator to register a function as a named plot type.

Usage:

```default
@plot_type("line")
def draw_line(ax, /, **kwargs):
    ax.plot(kwargs.get("x", []), kwargs.get("y", []))
```

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The plot type name to register under.
* **Returns:**
  The original function, unmodified.
* **Return type:**
  Callable

<a id="eikon.ext._plot_types.list_plot_types"></a>

### eikon.ext._plot_types.list_plot_types()

Return a sorted list of all registered plot type names.

* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="module-eikon.ext._transforms"></a>

<a id="data-transforms"></a>

## Data Transforms

Registry and application of data transforms.

Transforms are simple callables that accept a data object and return a
transformed data object. They are addressed by string name to keep the
declarative YAML surface stable.

<a id="eikon.ext._transforms.register_transform"></a>

### eikon.ext._transforms.register_transform(name, fn)

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str))
  * **fn** ([*Callable*](https://docs.python.org/3/library/collections.abc.html#collections.abc.Callable) *[* *[*[*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]* *,* [*Any*](https://docs.python.org/3/library/typing.html#typing.Any) *]*)
* **Return type:**
  None

<a id="eikon.ext._transforms.apply_transforms"></a>

### eikon.ext._transforms.apply_transforms(data, names)

* **Parameters:**
  * **data** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any))
  * **names** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*)
* **Return type:**
  [*Any*](https://docs.python.org/3/library/typing.html#typing.Any)

<a id="eikon.ext._transforms.list_transforms"></a>

### eikon.ext._transforms.list_transforms()

* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)]

<a id="module-eikon.ext._hooks"></a>

<a id="lifecycle-hooks"></a>

## Lifecycle Hooks

Lifecycle hook system for rendering and export events.

Hooks allow users to inject custom logic at well-defined points in the
render/export pipeline without modifying eikon source.

<a id="eikon.ext._hooks.HookName"></a>

### *class* eikon.ext._hooks.HookName(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Well-defined hook points in the figure lifecycle.

<a id="eikon.ext._hooks.HookName.PRE_RENDER"></a>

#### PRE_RENDER *= 'pre_render'*

<a id="eikon.ext._hooks.HookName.POST_RENDER"></a>

#### POST_RENDER *= 'post_render'*

<a id="eikon.ext._hooks.HookName.PRE_EXPORT"></a>

#### PRE_EXPORT *= 'pre_export'*

<a id="eikon.ext._hooks.HookName.POST_EXPORT"></a>

#### POST_EXPORT *= 'post_export'*

<a id="eikon.ext._hooks.register_hook"></a>

### eikon.ext._hooks.register_hook(hook, fn)

Register a callback for a lifecycle hook.

* **Parameters:**
  * **hook** ([*HookName*](#eikon.ext._hooks.HookName)) – The hook point to attach to.
  * **fn** (*HookFunction*) – A callable invoked when the hook fires.
* **Return type:**
  None

<a id="eikon.ext._hooks.fire_hook"></a>

### eikon.ext._hooks.fire_hook(hook, \*\*kwargs)

Fire all callbacks registered for a hook.

* **Parameters:**
  * **hook** ([*HookName*](#eikon.ext._hooks.HookName)) – The hook point to fire.
  * **\*\*kwargs** (*Any*) – Context passed to each callback.
* **Return type:**
  None

<a id="eikon.ext._hooks.clear_hooks"></a>

### eikon.ext._hooks.clear_hooks()

Remove all registered hooks.  For testing only.

* **Return type:**
  None

<a id="module-eikon.ext._discovery"></a>

<a id="plugin-discovery"></a>

## Plugin Discovery

Entry-point based plugin discovery.

Discovers and loads third-party plot types and hooks registered via
the `eikon.plot_types` entry-point group in `pyproject.toml`.

<a id="eikon.ext._discovery.discover_plugins"></a>

### eikon.ext._discovery.discover_plugins(group='eikon.plot_types')

Load all entry points in the given group.

Each entry point should be a module that, when imported, registers
its plot types via `@plot_type("name")` or
`register_plot_type(name, fn)`.

* **Parameters:**
  **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Entry-point group name to discover.
* **Returns:**
  Number of entry points successfully loaded.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)

<a id="module-eikon.contrib._matplotlib"></a>

<a id="matplotlib-contributions"></a>

## Matplotlib Contributions

Built-in matplotlib plot type wrappers.

Each function is registered via `@plot_type("name")` and delegates to
the corresponding matplotlib `Axes` method.  The `params` dict from
`PanelSpec` is forwarded as keyword arguments.

<a id="module-eikon.contrib._seaborn"></a>

<a id="seaborn-contributions"></a>

## Seaborn Contributions

Built-in seaborn plot type wrappers (lazy import).

Seaborn is imported only when one of its plot types is first invoked,
keeping it an optional dependency.
