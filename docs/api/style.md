<a id="style"></a>

# Style

Style sheet definitions, loading, composition, presets, and Matplotlib parameter conversion.

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
  * [**StyleNotFoundError**](types.md#eikon.exceptions.StyleNotFoundError) – If the reference cannot be resolved.
  * [**StyleError**](types.md#eikon.exceptions.StyleError) – If a style file is malformed.

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
