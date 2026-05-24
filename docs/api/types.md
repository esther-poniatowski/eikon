<a id="types-and-exceptions"></a>

# Types and Exceptions

Shared type aliases, enums, and exception classes.

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

<a id="eikon.exceptions.ConfigValidationError"></a>

### *exception* eikon.exceptions.ConfigValidationError(errors)

Bases: [`ConfigError`](#eikon.exceptions.ConfigError)

Schema validation failure with detailed messages.

* **Parameters:**
  **errors** ([*list*](https://docs.python.org/3/library/stdtypes.html#list) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *]*) – Individual validation error messages.

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

<a id="eikon.exceptions.ExportError"></a>

### *exception* eikon.exceptions.ExportError

Bases: [`EikonError`](#eikon.exceptions.EikonError)

Error during figure export.

<a id="eikon.exceptions.RegistryError"></a>

### *exception* eikon.exceptions.RegistryError

Bases: [`EikonError`](#eikon.exceptions.EikonError)

Error in the figure registry.
