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
