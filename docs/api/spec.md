# eikon.spec

Declarative figure and panel specifications.

For usage examples, see the {doc}`Specifications guide </guide/specifications>`.

## Classes

### FigureSpec

```
eikon.spec.FigureSpec(*, name, title="", tags=(), group="", panels=(),
                      layout=None, style=None, export=None, metadata={})
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
| `metadata` | `dict[str, str]` | `{}` | Arbitrary metadata |

---

### PanelSpec

```
eikon.spec.PanelSpec(*, name, plot_type, data=None, row=0, col=0,
                     style=None, params={}, label="", auto_size=False)
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
