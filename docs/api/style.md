# eikon.style

Style management: composable style sheets, presets, and matplotlib integration.

For usage examples, see the {doc}`Styles guide </guide/styles>`.

## Classes

### StyleSheet

```
eikon.style.StyleSheet(*, name, font_family=None, font_size=None,
                       line_width=None, palette=None, figure_size=None,
                       rc_overrides={}, extends=())
```

Composable style definition. Frozen dataclass. `None` fields inherit from parent styles.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | *(required)* | Style identifier |
| `font_family` | `str \| None` | `None` | Font family |
| `font_size` | `float \| None` | `None` | Base font size (pt) |
| `line_width` | `float \| None` | `None` | Default line width (pt) |
| `palette` | `tuple[str, ...] \| None` | `None` | Color palette |
| `figure_size` | `tuple[float, float] \| None` | `None` | Width x height (inches) |
| `rc_overrides` | `dict[str, object]` | `{}` | Raw matplotlib rcParams |
| `extends` | `tuple[str, ...]` | `()` | Parent style names |

## Constants

### PRESETS

```
eikon.style.PRESETS: dict[str, StyleSheet]
```

Built-in style presets:

| Name | Font | Size | Line width | Figure size |
|------|------|------|------------|-------------|
| `"publication"` | serif | 8pt | 0.8pt | 7.0 x 5.0" |
| `"presentation"` | sans-serif | 14pt | 1.5pt | 10.0 x 7.0" |
| `"poster"` | sans-serif | 20pt | 2.5pt | 14.0 x 10.0" |

## Functions

### load_style

```
eikon.style.load_style(ref: str | Path | dict[str, object],
                       search_dirs: tuple[Path, ...] = ()) -> StyleSheet
```

Load a style from a preset name, a `.yaml`/`.mplstyle` file path, or a raw dict.

**Raises:** `StyleNotFoundError` if the reference cannot be resolved.

---

### compose_styles

```
eikon.style.compose_styles(*sheets: StyleSheet) -> StyleSheet
```

Merge multiple style sheets. Later sheets override earlier ones. `None` fields are skipped (inherited from earlier sheets).

---

### resolve_style_chain

```
eikon.style.resolve_style_chain(sheet: StyleSheet,
                                registry: Mapping[str, StyleSheet],
                                *, _seen=None) -> StyleSheet
```

Recursively resolve the `extends` chain of a style sheet using a name registry.

---

### to_rcparams

```
eikon.style.to_rcparams(sheet: StyleSheet) -> dict[str, Any]
```

Convert a `StyleSheet` to a matplotlib `rcParams` dict.

---

### style_context

```
eikon.style.style_context(sheet: StyleSheet, *, debug: bool = False)
```

Context manager that temporarily applies a `StyleSheet` to matplotlib. All drawing calls within the block use the style's `rcParams`.

```python
with style_context(sheet):
    fig, ax = plt.subplots()
    ax.plot(x, y)
```
