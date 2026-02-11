# eikon.spec

Declarative figure and panel specifications.

For usage examples, see the {doc}`Specifications guide </guide/specifications>`.

## Classes

### FigureSpec

```
eikon.spec.FigureSpec(*, name, title="", tags=(), group="", panels=(),
                      layout=None, style=None, export=None,
                      title_kwargs=None, shared_legend=None,
                      margin_labels=None, metadata={})
```

Declarative specification for a single figure. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | *(required)* | Unique figure identifier |
| `title` | `str` | `""` | Display title |
| `tags` | `tuple[str, ...]` | `()` | Organizational tags |
| `group` | `str` | `""` | Grouping key |
| `panels` | `tuple[PanelSpec, ...]` | `()` | Panel definitions |
| `layout` | `dict[str, Any] \| None` | `None` | Layout parameters |
| `style` | `StyleRef \| None` | `None` | Style override |
| `export` | `dict[str, Any] \| None` | `None` | Export overrides |
| `title_kwargs` | `dict[str, Any] \| None` | `None` | Extra kwargs for `fig.suptitle()` |
| `shared_legend` | `dict[str, Any] \| None` | `None` | Figure-level shared legend settings |
| `margin_labels` | `dict[str, MarginLabelSpec] \| None` | `None` | Edge labels for annotating rows/columns |
| `metadata` | `dict[str, str]` | `{}` | Arbitrary metadata |

---

### PanelSpec

```
eikon.spec.PanelSpec(*, name, plot_type, data=None, row=0, col=0,
                     style=None, params={}, label="", auto_size=False,
                     hide_spines=None)
```

Specification for one axes panel. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | *(required)* | Panel identifier |
| `plot_type` | `str` | *(required)* | Registered plot type name |
| `data` | `DataBinding \| None` | `None` | Data source binding |
| `row` | `int \| tuple[int, int]` | `0` | Row index or `(start, end)` span |
| `col` | `int \| tuple[int, int]` | `0` | Column index or `(start, end)` span |
| `style` | `StyleRef \| None` | `None` | Per-panel style override |
| `params` | `dict[str, Any]` | `{}` | Kwargs for the plot function |
| `label` | `str` | `""` | Panel label (e.g. `"(a)"`) |
| `auto_size` | `bool` | `False` | Defer sizing to constrained layout |
| `hide_spines` | `tuple[str, ...] \| None` | `None` | Spine names to hide (e.g. `("top", "right")`) |

---

### DataBinding

```
eikon.spec.DataBinding(*, source="", x="", y="", hue="", transforms=(), params={})
```

Data source binding for a panel. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `source` | `str \| Path` | `""` | Path to data file |
| `x` | `str` | `""` | Column name for x-axis |
| `y` | `str` | `""` | Column name for y-axis |
| `hue` | `str` | `""` | Grouping variable |
| `transforms` | `tuple[str, ...]` | `()` | Named transforms (applied in order) |
| `params` | `dict[str, Any]` | `{}` | Extra loading parameters |

---

### MarginLabelSpec

```
eikon.spec.MarginLabelSpec(*, labels, style=MarginLabelStyle(),
                           level_styles=None, target=MarginTarget(),
                           strip_size=0.04, pad=6.0, gap=2.0,
                           zorder=2.1, label_styles=None,
                           cell_range=None)
```

Specification for labels on one edge of the figure. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `labels` | `tuple[str, ...] \| dict[str, Any]` | *(required)* | Flat tuple or nested dict hierarchy |
| `style` | `MarginLabelStyle` | *(defaults)* | Default style for all labels on this edge |
| `level_styles` | `tuple[MarginLabelStyle, ...] \| None` | `None` | Per-level style overrides (outermost first) |
| `label_styles` | `dict[str, MarginLabelStyle] \| None` | `None` | Per-label style overrides keyed by text |
| `target` | `MarginTarget` | `layout` mode | Which grid the labels align to |
| `strip_size` | `float` | `0.04` | Band height/width in figure-fraction |
| `pad` | `float` | `6.0` | Gap from axes edge to first level (points) |
| `gap` | `float` | `2.0` | Gap between stacked levels (points) |
| `zorder` | `float` | `2.1` | Drawing order |
| `cell_range` | `tuple[int, int] \| None` | `None` | `(start, end)` cell subset (0-indexed, end-exclusive) |

**Style cascade:** For each label, the renderer checks `label_styles[text]` first, then `level_styles[level]`, then the edge-wide `style` default.

---

### MarginLabelStyle

```
eikon.spec.MarginLabelStyle(*, bg_color=None, text_color="black",
                            fontsize=8.0, fontweight="normal",
                            rotation=None)
```

Visual style for margin label text and optional background strip. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bg_color` | `str \| None` | `None` | Background strip color (`None` = transparent) |
| `text_color` | `str` | `"black"` | Text color |
| `fontsize` | `float` | `8.0` | Font size in points |
| `fontweight` | `str` | `"normal"` | Font weight (`"normal"`, `"bold"`, etc.) |
| `rotation` | `float \| None` | `None` | Rotation in degrees (`None` = edge default: 0 for top/bottom, 90 for left, 270 for right) |

---

### MarginTarget

```
eikon.spec.MarginTarget(*, kind="layout", axes=None, grid=None)
```

Targeting mode for margin labels. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `kind` | `"layout" \| "virtual"` | `"layout"` | `"layout"` aligns to GridSpec cells; `"virtual"` subdivides a single panel |
| `axes` | `str \| None` | `None` | Panel name to subdivide (required for `"virtual"`) |
| `grid` | `tuple[int, int] \| None` | `None` | `(rows, cols)` of the virtual grid (required for `"virtual"`) |

## Functions

### parse_figure_spec

```
eikon.spec.parse_figure_spec(raw: dict[str, Any]) -> FigureSpec
```

Parse a raw dict into a `FigureSpec`. Validates required fields.

**Raises:** `SpecValidationError` on invalid input.

---

### parse_figure_file

```
eikon.spec.parse_figure_file(path: Path) -> FigureSpec
```

Load and parse a YAML figure spec file.

**Raises:** `SpecError` if the file cannot be read. `SpecValidationError` on invalid content.

---

### merge_spec_override

```
eikon.spec.merge_spec_override(base: FigureSpec, override: dict[str, Any]) -> FigureSpec
```

Merge runtime overrides onto a base figure spec.
