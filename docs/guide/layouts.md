# Layouts

The layout engine translates declarative grid specifications into matplotlib `Figure` and `Axes` objects. It wraps matplotlib's `GridSpec` with validation, declarative addressing, and support for shared axes, colorbars, and insets.

## LayoutSpec

A `LayoutSpec` defines the grid structure:

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `rows` | `int` | `1` | Number of grid rows |
| `cols` | `int` | `1` | Number of grid columns |
| `width_ratios` | `tuple[float, ...]` or `None` | `None` | Relative column widths |
| `height_ratios` | `tuple[float, ...]` or `None` | `None` | Relative row heights |
| `wspace` | `float` or `None` | `None` | Horizontal spacing |
| `hspace` | `float` or `None` | `None` | Vertical spacing |
| `constrained_layout` | `bool` | `True` | Use matplotlib's constrained layout engine |

## YAML layout definition

In a figure spec:

```yaml
layout:
  rows: 2
  cols: 3
  width_ratios: [1, 2, 1]
  height_ratios: [3, 1]
  wspace: 0.3
  hspace: 0.4
```

Panels reference their grid position with `row` and `col`:

```yaml
panels:
  - name: main
    plot_type: heatmap
    row: 0
    col: [0, 2]      # Span columns 0-2
  - name: colorbar
    plot_type: line
    row: 1
    col: 1
```

## Building layouts in Python

```python
from eikon import LayoutSpec, build_layout
from eikon.layout import resolve_placements, PanelPlacement

layout = LayoutSpec(rows=2, cols=2, width_ratios=(2, 1))

# Resolve panel positions
placements = resolve_placements(spec.panels, layout)

# Build the matplotlib Figure + Axes
built = build_layout(layout, placements, figure_size=(8, 6))

print(built.figure)     # matplotlib Figure
print(built.axes)       # {"A": <Axes>, "B": <Axes>, ...}
```

## Layout validation

Validate that panels don't overlap and fit within the grid:

```python
from eikon.layout import validate_layout, validate_layout_strict

errors = validate_layout(placements, layout)
# Returns a list of error strings (empty if valid)

validate_layout_strict(placements, layout)
# Raises LayoutError or PanelOverlapError on problems
```

## Shared axes

Link axes across panels so they share the same scale:

```python
from eikon.layout import link_axes

# Share both x and y axes between panels A and B
link_axes(built, groups=(("A", "B"),), axis="both")

# Share only x axes
link_axes(built, groups=(("A", "B"),), axis="x")

# Multiple groups
link_axes(built, groups=(("A", "B"), ("C", "D")), axis="y")
```

## Colorbars

Add a colorbar to a panel:

```python
from eikon.layout import add_colorbar

# After drawing a mappable (e.g. imshow, pcolormesh)
im = built.axes["heatmap"].imshow(data)
add_colorbar(built, "heatmap", im, position="right", size="5%", pad=0.05)
```

Parameters:
- `position`: `"right"`, `"left"`, `"top"`, or `"bottom"`
- `size`: Width as a percentage string (e.g. `"5%"`)
- `pad`: Padding between the axes and the colorbar

## Insets

Add an inset axes inside an existing panel:

```python
from eikon.layout import add_inset

# bounds = (x, y, width, height) in axes coordinates [0, 1]
built = add_inset(built, parent_panel="A", name="A_inset", bounds=(0.6, 0.6, 0.35, 0.35))

# Draw into the inset
built.axes["A_inset"].plot(...)
```

See the {doc}`/api/layout` for the complete API reference.
