# eikon.layout

Layout engine: grid specifications, panel placement, shared axes, colorbars, and insets.

For usage examples, see the {doc}`Layouts guide </guide/layouts>`.

## Classes

### LayoutSpec

```
eikon.layout.LayoutSpec(*, rows=1, cols=1, width_ratios=None,
                        height_ratios=None, wspace=None, hspace=None,
                        constrained_layout=True)
```

Declarative grid layout specification. Frozen dataclass.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `rows` | `int` | `1` | Number of grid rows |
| `cols` | `int` | `1` | Number of grid columns |
| `width_ratios` | `tuple[float, ...] \| None` | `None` | Relative column widths |
| `height_ratios` | `tuple[float, ...] \| None` | `None` | Relative row heights |
| `wspace` | `float \| None` | `None` | Horizontal spacing |
| `hspace` | `float \| None` | `None` | Vertical spacing |
| `constrained_layout` | `bool` | `True` | Use constrained layout engine |

---

### PanelPlacement

```
eikon.layout.PanelPlacement(*, panel_name, row_slice, col_slice)
```

Resolved position of a panel in the grid. Frozen dataclass.

| Field | Type | Description |
|-------|------|-------------|
| `panel_name` | `str` | Panel identifier |
| `row_slice` | `slice` | Row range in the GridSpec |
| `col_slice` | `slice` | Column range in the GridSpec |

---

### BuiltLayout

```
eikon.layout.BuiltLayout(*, figure, axes)
```

A constructed matplotlib Figure with named Axes. Frozen dataclass.

| Field | Type | Description |
|-------|------|-------------|
| `figure` | `Figure` | The matplotlib Figure |
| `axes` | `dict[str, Axes]` | Panel name to Axes mapping |

## Functions

### build_layout

```
eikon.layout.build_layout(layout: LayoutSpec,
                          placements: tuple[PanelPlacement, ...],
                          *, figure_size=(6.4, 4.8), dpi=100) -> BuiltLayout
```

Build a matplotlib Figure with Axes positioned according to the layout and placements.

---

### resolve_placements

```
eikon.layout.resolve_placements(panels: tuple[PanelSpec, ...],
                                layout: LayoutSpec) -> tuple[PanelPlacement, ...]
```

Convert `PanelSpec` row/col fields into `PanelPlacement` objects with grid slices.

---

### validate_layout

```
eikon.layout.validate_layout(placements: tuple[PanelPlacement, ...],
                             layout: LayoutSpec) -> list[str]
```

Check for layout problems (overlaps, out-of-bounds). Returns a list of error messages (empty if valid).

---

### validate_layout_strict

```
eikon.layout.validate_layout_strict(placements: tuple[PanelPlacement, ...],
                                    layout: LayoutSpec) -> None
```

Like `validate_layout`, but raises on errors.

**Raises:** `LayoutError`, `PanelOverlapError`

---

### link_axes

```
eikon.layout.link_axes(built: BuiltLayout,
                       groups: tuple[tuple[str, ...], ...],
                       axis: Literal["x", "y", "both"] = "both") -> None
```

Share axis scales across groups of panels. Modifies the layout in place.

---

### add_colorbar

```
eikon.layout.add_colorbar(built: BuiltLayout, panel_name: str,
                          mappable: ScalarMappable, *, position="right",
                          size="5%", pad=0.05, **kwargs) -> Axes
```

Add a colorbar adjacent to a panel.

- `position`: `"right"`, `"left"`, `"top"`, or `"bottom"`
- `size`: Width as a percentage string
- `pad`: Padding between axes and colorbar

---

### add_inset

```
eikon.layout.add_inset(built: BuiltLayout, parent_panel: str,
                       name: str,
                       bounds: tuple[float, float, float, float]) -> BuiltLayout
```

Add an inset axes inside an existing panel. Returns a new `BuiltLayout` with the inset added to `axes`.

- `bounds`: `(x, y, width, height)` in axes-relative coordinates `[0, 1]`
