# Rendering

The render pipeline orchestrates the full figure lifecycle: spec parsing, style application, layout construction, panel drawing, and export.

## High-level API

The simplest way to render a figure:

```python
import eikon

# From a YAML spec file
handle = eikon.render("my-figure", formats=("pdf", "svg"))

# From a FigureSpec object
spec = eikon.FigureSpec(
    name="quick",
    panels=(eikon.PanelSpec(name="A", plot_type="line"),),
)
handle = eikon.render(spec, formats=("png",))
```

`render()` returns a `FigureHandle`:

```python
handle.figure        # The matplotlib Figure
handle.axes          # {"A": <Axes>, ...}
handle.export_paths  # {"pdf": Path(...), "svg": Path(...)}
handle.show()        # Display interactively
handle.close()       # Close the figure and free memory
```

## Pipeline stages

The `render_figure()` function (used internally by `render()`) executes these stages:

1. **Spec resolution** — Parse the YAML spec or accept a `FigureSpec` object.
2. **Style resolution** — Load and compose the style chain, convert to `rcParams`.
3. **Layout construction** — Build the matplotlib `Figure` and `Axes` from the `LayoutSpec`.
4. **Panel drawing** — For each panel, look up the registered plot function and call it with the resolved axes, data, and parameters.
5. **Export** — Save the figure to the requested formats.

```python
from eikon import render_figure, FigureSpec, PanelSpec

spec = FigureSpec(name="fig", panels=(PanelSpec(name="A", plot_type="line"),))
handle = render_figure(spec, formats=("pdf",))
handle.close()
```

## Plot types

Each panel references a registered plot type by name. Plot functions must match the `PlotFunction` protocol:

```python
def my_plot(ax, /, **kwargs):
    """Draw into the given Axes."""
    ...
```

The positional `ax` is a matplotlib `Axes`. Keyword arguments come from:
- `PanelSpec.params` — explicit parameters from the spec
- Data binding columns (`x`, `y`, `hue`) — resolved from the data source

See {doc}`extensions` for how to register plot types.

## Data binding

When a panel has a `data` field, the pipeline:

1. Loads the data source (CSV file via `csv.DictReader`).
2. Applies transforms in order (see {doc}`extensions`).
3. Extracts columns (`x`, `y`, `hue`) into keyword arguments.
4. Merges them with `PanelSpec.params`.
5. Passes everything to the plot function.

```yaml
panels:
  - name: A
    plot_type: line
    data:
      source: data/timeseries.csv
      x: time
      y: voltage
      transforms: [normalize, smooth]
    params:
      color: blue
```

The plot function receives `ax`, `x=[...], y=[...], color="blue"`.

## Lifecycle hooks

Inject custom logic at defined points in the pipeline:

| Hook | Fires when |
|------|-----------|
| `PRE_RENDER` | Before style application and layout build |
| `POST_RENDER` | After all panels are drawn |
| `PRE_EXPORT` | Before export begins |
| `POST_EXPORT` | After all formats are exported |

```python
from eikon.ext import register_hook, HookName

def log_render(*, spec, **kwargs):
    print(f"Rendering {spec.name}")

register_hook(HookName.PRE_RENDER, log_render)
```

See {doc}`extensions` for details on the hook system.

## Overrides

Pass runtime overrides to the pipeline:

```python
handle = eikon.render("my-figure", overrides={"dpi": 600})
```

Overrides are forwarded through the render context and can influence export settings.

See the {doc}`/api/render` for the complete API reference.
