# Styles

Eikon's style system provides composable, reusable visual configurations that translate to matplotlib `rcParams`. Styles can be applied per-figure, per-panel, or globally.

## StyleSheet

A `StyleSheet` captures high-level style properties:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | *(required)* | Style identifier |
| `font_family` | `str` or `None` | `None` | Font family name |
| `font_size` | `float` or `None` | `None` | Base font size (pt) |
| `line_width` | `float` or `None` | `None` | Default line width (pt) |
| `palette` | `tuple[str, ...]` or `None` | `None` | Color palette |
| `figure_size` | `(float, float)` or `None` | `None` | Width x height (inches) |
| `rc_overrides` | `dict[str, object]` | `{}` | Raw matplotlib rcParams |
| `extends` | `tuple[str, ...]` | `()` | Parent styles to inherit from |

`None` fields inherit from parent styles or project defaults.

## Built-in presets

Three presets are available out of the box:

### `publication`

Compact serif fonts, thin lines. Suitable for journal figures.

- Font: serif, 8pt
- Line width: 0.8pt
- Figure size: 7.0 x 5.0 inches
- Tick direction: inward

### `presentation`

Larger sans-serif fonts. Readable on slides.

- Font: sans-serif, 14pt
- Line width: 1.5pt
- Figure size: 10.0 x 7.0 inches

### `poster`

Extra-large fonts and thick lines for poster figures.

- Font: sans-serif, 20pt
- Line width: 2.5pt
- Figure size: 14.0 x 10.0 inches

Use a preset by name in a figure spec:

```yaml
style: publication
```

Or in Python:

```python
from eikon.style import PRESETS

sheet = PRESETS["publication"]
```

## Custom styles

### YAML style files

Place custom style files in the `styles/` directory:

```yaml
# styles/my-style.yaml
name: my-style
font_family: "Helvetica"
font_size: 9.0
line_width: 1.0
palette: ["#1f77b4", "#ff7f0e", "#2ca02c"]
figure_size: [7.5, 5.0]
rc_overrides:
  axes.linewidth: 0.6
  xtick.direction: in
  ytick.direction: in
```

Reference it in a figure spec:

```yaml
style: my-style
```

### Python construction

```python
from eikon import StyleSheet

sheet = StyleSheet(
    name="custom",
    font_family="Helvetica",
    font_size=9.0,
    palette=("#1f77b4", "#ff7f0e"),
)
```

## Style composition and inheritance

Styles can extend other styles. Child values override parent values:

```yaml
# styles/manuscript.yaml
name: manuscript
extends: [publication]
font_family: "Times New Roman"
rc_overrides:
  figure.facecolor: white
```

The inheritance chain is resolved left-to-right: if `extends: [A, B]`, then B's values overlay A's, and the current sheet's values overlay both.

```python
from eikon.style import compose_styles, resolve_style_chain

# Manual composition
merged = compose_styles(base_sheet, overlay_sheet)

# Automatic chain resolution (resolves `extends` references)
resolved = resolve_style_chain(sheet, registry={"publication": pub_sheet})
```

## Applying styles

### Context manager

The `style_context()` context manager temporarily applies a stylesheet:

```python
from eikon import style_context, StyleSheet

sheet = StyleSheet(name="temp", font_size=12.0)
with style_context(sheet):
    # All matplotlib calls inside this block use the style
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])
```

### In the render pipeline

Styles are applied automatically when specified in a figure spec. The render pipeline resolves the style, converts it to `rcParams`, and wraps the drawing phase in a context manager.

## Converting to rcParams

For direct matplotlib integration:

```python
from eikon.style import to_rcparams

params = to_rcparams(sheet)
# {'font.family': 'serif', 'font.size': 8.0, ...}
```

See the {doc}`/api/style` for the complete API reference.
