# Figure Specifications

A **figure specification** declaratively defines everything about a figure: its panels, layout, style, and export settings. Specs can be written as YAML files or constructed as Python objects.

## YAML format

A complete figure spec YAML file:

```yaml
name: results-overview           # Required: unique identifier
title: "Overview of Results"     # Optional: rendered on the figure
tags: [overview, neural]         # Optional: for filtering/grouping
group: manuscript-1              # Optional: grouping key

panels:
  - name: A
    plot_type: line              # Registered plot type name
    row: 0                       # Grid position (zero-based)
    col: 0
    label: "(a)"                 # Panel label
    params:                      # Kwargs forwarded to the plot function
      color: blue
      linewidth: 1.5
    data:                        # Data binding (optional)
      source: data/timeseries.csv
      x: time
      y: voltage
      transforms: [normalize]

  - name: B
    plot_type: scatter
    row: 0
    col: 1
    label: "(b)"

layout:                          # Grid layout (optional)
  rows: 1
  cols: 2
  width_ratios: [2, 1]

style: publication               # Style override (optional)

export:                          # Per-figure export overrides (optional)
  formats: [pdf, svg, png]
  dpi: 600

metadata:                        # Arbitrary metadata (optional)
  author: "E. Poniatowski"
```

## FigureSpec

The top-level specification object. All fields except `name` are optional.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | *(required)* | Unique figure identifier |
| `title` | `str` | `""` | Display title |
| `tags` | `tuple[str, ...]` | `()` | Organizational tags |
| `group` | `str` | `""` | Grouping key |
| `panels` | `tuple[PanelSpec, ...]` | `()` | Panel definitions |
| `layout` | `dict` or `None` | `None` | Layout parameters |
| `style` | `str`, `Path`, or `dict` | `None` | Style override |
| `export` | `dict` or `None` | `None` | Export overrides |
| `title_kwargs` | `dict` or `None` | `None` | Extra kwargs for `fig.suptitle()` |
| `shared_legend` | `dict` or `None` | `None` | Figure-level shared legend settings |
| `margin_labels` | `dict[str, MarginLabelSpec]` or `None` | `None` | Edge labels for annotating rows/columns |
| `metadata` | `dict[str, str]` | `{}` | Arbitrary metadata |

## PanelSpec

Each panel occupies one region of the grid and is drawn by a registered plot function.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `name` | `str` | *(required)* | Panel identifier (e.g. `"A"`) |
| `plot_type` | `str` | *(required)* | Registered plot type name |
| `data` | `DataBinding` or `None` | `None` | Data source binding |
| `row` | `int` or `(int, int)` | `0` | Row index or span |
| `col` | `int` or `(int, int)` | `0` | Column index or span |
| `style` | `str`, `Path`, or `dict` | `None` | Per-panel style |
| `params` | `dict[str, Any]` | `{}` | Kwargs for the plot function |
| `label` | `str` | `""` | Panel label (e.g. `"(a)"`) |
| `auto_size` | `bool` | `False` | Defer sizing to constrained layout |
| `hide_spines` | `tuple[str, ...]` or `None` | `None` | Spine names to hide (e.g. `("top", "right")`) |

### Grid spanning

Panels can span multiple rows or columns using tuple notation:

```yaml
panels:
  - name: wide
    plot_type: heatmap
    row: 0
    col: [0, 2]     # Spans columns 0, 1, 2
```

## DataBinding

Binds a data source to a panel. Data is loaded, transformed, and passed as keyword arguments to the plot function.

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `source` | `str` or `Path` | `""` | Path to data file |
| `x` | `str` | `""` | Column name for x-axis |
| `y` | `str` | `""` | Column name for y-axis |
| `hue` | `str` | `""` | Grouping variable for color |
| `transforms` | `tuple[str, ...]` | `()` | Named transforms to apply |
| `params` | `dict[str, Any]` | `{}` | Extra loading parameters |

Currently supported data formats: CSV files (loaded via `csv.DictReader`).

## Margin labels

Margin labels annotate rows or columns of a panel grid by placing text (and optional background strips) along the figure edges. They are purely declarative -- no plot-function code needed.

The `margin_labels` field is a dict keyed by edge name (`"top"`, `"bottom"`, `"left"`, `"right"`), where each value is a `MarginLabelSpec`.

### Flat labels

One label per grid cell. The number of labels must match the grid dimension.

```yaml
layout: {rows: 1, cols: 3}
margin_labels:
  top:
    labels: ["$k=1$", "$k=3$", "$k=6$"]
    style:
      bg_color: "#E8F0FE"
      fontsize: 8
```

### Hierarchical labels

Nested dicts express multi-level grouping. Keys are group labels; values are sub-dicts (recursive) or `null` for leaf labels. Leaf lists are also supported.

```yaml
margin_labels:
  top:
    labels:
      PTD:
        active: null
        passive: null
      CLK:
        active: null
        passive: null
    level_styles:
      - bg_color: "#D4E6F1"
        fontweight: bold
      - bg_color: "#EBF5FB"
```

This produces two levels: an outer level with "PTD" (spanning 2 columns) and "CLK" (spanning 2 columns), and an inner level with the four leaf labels.

### Per-label style overrides

Use `label_styles` to style individual labels differently from their level default. Keys are label text strings.

```yaml
margin_labels:
  top:
    labels: [A, B, C]
    label_styles:
      B:
        fontweight: bold
        bg_color: "#FFE0E0"
```

### Partial cell range

Use `cell_range` to label only a subset of the grid. The range is `[start, end)`, 0-indexed.

```yaml
layout: {rows: 1, cols: 6}
margin_labels:
  top:
    labels: [D, E, F, G]
    cell_range: [2, 6]       # Labels columns 2-5 only
```

### Virtual grid (inset grids)

For single-panel figures where the plot function draws an internal grid of subplots, use `target` with `kind: virtual` to subdivide the axes evenly.

```yaml
layout: {rows: 1, cols: 1}
margin_labels:
  top:
    labels: ["$0$", "$\\pi/6$", "$\\pi/3$", "$\\pi/2$", "$2\\pi/3$", "$5\\pi/6$"]
    style: {fontsize: 7}
    target:
      kind: virtual
      axes: gabor         # Panel name to subdivide
      grid: [3, 6]        # (rows, cols) of the virtual grid
  left:
    labels: ["$k=1$", "$k=3$", "$k=6$"]
    style: {fontsize: 7}
    target:
      kind: virtual
      axes: gabor
      grid: [3, 6]
```

### MarginLabelSpec fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `labels` | `tuple[str, ...]` or `dict` | *(required)* | Flat tuple or nested dict hierarchy |
| `style` | `MarginLabelStyle` | *(defaults)* | Default style for all labels on this edge |
| `level_styles` | `tuple[MarginLabelStyle, ...]` or `None` | `None` | Per-level style overrides (outermost first) |
| `label_styles` | `dict[str, MarginLabelStyle]` or `None` | `None` | Per-label style overrides keyed by text |
| `target` | `MarginTarget` | `layout` mode | Which grid the labels align to |
| `strip_size` | `float` | `0.04` | Band height/width in figure-fraction |
| `pad` | `float` | `6.0` | Gap from axes edge to first level (points) |
| `gap` | `float` | `2.0` | Gap between stacked levels (points) |
| `zorder` | `float` | `2.1` | Drawing order |
| `cell_range` | `tuple[int, int]` or `None` | `None` | `(start, end)` cell subset (0-indexed, end-exclusive) |

### MarginLabelStyle fields

| Field | Type | Default | Description |
|-------|------|---------|-------------|
| `bg_color` | `str` or `None` | `None` | Background strip color (`None` = transparent) |
| `text_color` | `str` | `"black"` | Text color |
| `fontsize` | `float` | `8.0` | Font size in points |
| `fontweight` | `str` | `"normal"` | Font weight (`"normal"`, `"bold"`, etc.) |
| `rotation` | `float` or `None` | `None` | Rotation in degrees (`None` = edge default: 0 for top/bottom, 90 for left, 270 for right) |

## Python API

Construct specs programmatically:

```python
from eikon import FigureSpec, PanelSpec, DataBinding

spec = FigureSpec(
    name="my-figure",
    title="My Figure",
    panels=(
        PanelSpec(
            name="A",
            plot_type="line",
            data=DataBinding(source="data/series.csv", x="time", y="value"),
        ),
        PanelSpec(
            name="B",
            plot_type="scatter",
            row=0,
            col=1,
        ),
    ),
)
```

### Parsing from YAML

```python
from eikon import parse_figure_spec
from eikon.spec import parse_figure_file

# From a dict
spec = parse_figure_spec({"name": "fig1", "panels": [...]})

# From a file
spec = parse_figure_file("specs/fig1.yaml")
```

See the {doc}`/api/spec` for the complete API reference.
