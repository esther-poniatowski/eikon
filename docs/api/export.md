<a id="export"></a>

# Export

Export configuration, batch export, handlers, metadata, paths, and filename sanitization.

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

Template for output filename using `{name}`, `{group}`,
`{date}`, `{format}`.

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

<a id="eikon.export._config.ResolvedExportConfig.formats"></a>

#### formats *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[ExportFormat](types.md#eikon._types.ExportFormat), ...]*

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

Collision policy, either `"overwrite"`, `"increment"`, or `"fail"`.

<a id="eikon.export._config.ResolvedExportConfig.metadata"></a>

#### metadata *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

Metadata injected into exported files.

<a id="eikon.export._config.parse_collision_mode"></a>

### eikon.export._config.parse_collision_mode(value)

Normalize and validate a collision policy value.

<a id="eikon.export._config.resolve_export_config"></a>

### eikon.export._config.resolve_export_config(defaults, spec_export=None, cli_formats=())

Merge per-figure overrides on top of project defaults.

* **Parameters:**
  * **defaults** ([*ExportDefaults*](config.md#eikon.config._schema.ExportDefaults)) – Project-level export settings.
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
  * **export_defaults** ([*ExportDefaults*](config.md#eikon.config._schema.ExportDefaults)) – Project-level export settings.
  * **export_spec** ([*ExportSpec*](#eikon.export._config.ExportSpec) *,* *optional*) – Per-figure export overrides.
  * **cli_formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Format names from CLI flags (highest priority).
* **Returns:**
  Mapping of format name (lowercase) to exported file path.
* **Return type:**
  [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), Path]
* **Raises:**
  [**ExportError**](types.md#eikon.exceptions.ExportError) – If any export operation fails.

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
  * **fmt** ([*ExportFormat*](types.md#eikon._types.ExportFormat)) – Export format.
  * **config** ([*ResolvedExportConfig*](#eikon.export._config.ResolvedExportConfig)) – Resolved export settings.

<a id="eikon.export._handlers.get_handler"></a>

### eikon.export._handlers.get_handler(fmt)

Return the handler function for a given format.

Looks up custom-registered handlers first, then falls back to
built-in defaults.

* **Parameters:**
  **fmt** ([*ExportFormat*](types.md#eikon._types.ExportFormat)) – Export format.
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
  * **fmt** ([*ExportFormat*](types.md#eikon._types.ExportFormat)) – The export format to register the handler for.
  * **handler** (*Callable*) – A callable with signature `(figure, path, config) -> None`.

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

<a id="eikon.export._metadata.inject_png_metadata"></a>

### eikon.export._metadata.inject_png_metadata(path, metadata)

Inject text metadata into an existing PNG file.

Re-saves the PNG with updated text chunks.  If the file does not exist
or metadata is empty, this is a no-op.

* **Parameters:**
  * **path** (*Path*) – Path to the PNG file.
  * **metadata** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Key-value metadata pairs.

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
  * **fmt** ([*ExportFormat*](types.md#eikon._types.ExportFormat)) – Export format.
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
  [**ExportError**](types.md#eikon.exceptions.ExportError) – If `collision="fail"` and the target path already exists.

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
