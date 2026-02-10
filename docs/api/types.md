# eikon types and exceptions

Shared type aliases, enumerations, and the exception hierarchy.

## Types (`eikon._types`)

### ExportFormat

```
eikon._types.ExportFormat
```

Enum of supported export file formats.

| Member | Value |
|--------|-------|
| `PDF` | `"pdf"` |
| `SVG` | `"svg"` |
| `PNG` | `"png"` |

**Class method:**

```
ExportFormat.from_string(value: str) -> ExportFormat
```

Parse a format string (case-insensitive). **Raises** `ValueError` for unknown formats.

---

### Type Aliases

```python
type Tag = str
```
A string label for organizing figures.

```python
type DPI = int | float
```
Export resolution in dots per inch.

```python
type StyleRef = str | Path | dict[str, object]
```
A style reference: preset name, file path, or raw dict of rcParams.

## Exceptions (`eikon.exceptions`)

All eikon exceptions inherit from `EikonError`, allowing a single catch-all:

```python
try:
    eikon.render("fig1")
except eikon.exceptions.EikonError as e:
    print(f"Eikon error: {e}")
```

### Hierarchy

```
EikonError
├── ConfigError
│   ├── ConfigNotFoundError
│   └── ConfigValidationError
├── SpecError
│   └── SpecValidationError
├── StyleError
│   └── StyleNotFoundError
├── LayoutError
│   └── PanelOverlapError
├── RenderError
│   └── UnknownPlotTypeError
├── ExportError
└── RegistryError
```

### Exception details

#### ConfigNotFoundError

```
ConfigNotFoundError(search_root: str = ".")
```

Raised when no `eikon.yaml` is found. Message includes the search starting point and suggests running `eikon init`.

---

#### ConfigValidationError

```
ConfigValidationError(errors: list[str])
```

Schema validation failure. The `errors` attribute contains individual error messages.

---

#### SpecValidationError

```
SpecValidationError(errors: list[str])
```

Figure spec validation failure. The `errors` attribute contains individual error messages.

---

#### StyleNotFoundError

```
StyleNotFoundError(name: str)
```

A referenced style preset, file, or name was not found. The `name` attribute contains the reference.

---

#### PanelOverlapError

```
PanelOverlapError(panel_a: str, panel_b: str)
```

Two panels occupy the same grid cells. Attributes: `panel_a`, `panel_b`.

---

#### UnknownPlotTypeError

```
UnknownPlotTypeError(name: str, available: list[str])
```

A plot type name is not registered. Attributes: `name` (the unknown type), `available` (registered types).

---

#### ExportError

Generic error during figure export.

---

#### RegistryError

Error in the figure registry (duplicate name, missing entry, etc.).
