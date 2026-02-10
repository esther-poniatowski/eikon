# Extensions

Eikon is designed to be extensible. You can register custom plot types, data transforms, and lifecycle hooks without modifying eikon's source code.

## Plot types

### Registering with the decorator

The `@plot_type` decorator registers a function as a named plot type:

```python
from eikon.ext import plot_type

@plot_type("violin")
def draw_violin(ax, /, **kwargs):
    data = kwargs.get("data", [])
    ax.violinplot(data)
    ax.set_ylabel(kwargs.get("ylabel", ""))
```

The function must accept a positional matplotlib `Axes` argument and keyword arguments. It matches the `PlotFunction` protocol (see {doc}`/api/render`).

### Programmatic registration

```python
from eikon.ext import register_plot_type

def my_custom_plot(ax, /, **kwargs):
    ax.bar(kwargs["x"], kwargs["y"])

register_plot_type("custom_bar", my_custom_plot)
```

### Listing and looking up plot types

```python
from eikon.ext import list_plot_types, get_plot_type

print(list_plot_types())   # ["custom_bar", "line", "scatter", "violin", ...]

fn = get_plot_type("violin")
fn(ax, data=[1, 2, 3])
```

### Built-in plot types (contrib)

Eikon ships with wrappers for common matplotlib and seaborn plot types in the `eikon.contrib` module. These are registered automatically when the render pipeline runs:

**matplotlib**: `line`, `scatter`, `bar`, `hist`, `imshow`, and more.

**seaborn** (lazy-loaded): `sns.lineplot`, `sns.scatterplot`, `sns.boxplot`, etc.

## Data transforms

Transforms are functions that process data between loading and plotting. They are referenced by name in YAML specs.

### Registering transforms

```python
from eikon.ext import register_transform

def normalize(data):
    """Normalize all numeric columns to [0, 1]."""
    import numpy as np
    for key in data:
        if isinstance(data[key], list):
            arr = np.array(data[key], dtype=float)
            data[key] = ((arr - arr.min()) / (arr.max() - arr.min())).tolist()
    return data

register_transform("normalize", normalize)
```

### Using transforms in specs

```yaml
panels:
  - name: A
    plot_type: line
    data:
      source: data/raw.csv
      x: time
      y: voltage
      transforms: [normalize, smooth]  # Applied in order
```

### Listing and clearing transforms

```python
from eikon.ext import list_transforms, clear_transforms

print(list_transforms())  # ["normalize", "smooth"]
clear_transforms()        # Remove all (useful in tests)
```

## Lifecycle hooks

Hooks let you inject logic at specific points in the render/export pipeline.

### Hook points

| Hook | Fires when | Context kwargs |
|------|-----------|----------------|
| `PRE_RENDER` | Before style/layout | `spec` |
| `POST_RENDER` | After all panels drawn | `spec`, `figure`, `axes` |
| `PRE_EXPORT` | Before export starts | `spec`, `figure` |
| `POST_EXPORT` | After all exports complete | `spec`, `export_paths` |

### Registering hooks

```python
from eikon.ext import register_hook, HookName

def on_post_render(*, spec, figure, axes, **kwargs):
    """Add a watermark after all panels are drawn."""
    figure.text(0.5, 0.5, "DRAFT", fontsize=40, alpha=0.1,
                ha="center", va="center", transform=figure.transFigure)

register_hook(HookName.POST_RENDER, on_post_render)
```

### Clearing hooks

```python
from eikon.ext import clear_hooks
clear_hooks()  # Remove all hooks (useful in tests)
```

## Plugin discovery

Eikon supports entry-point-based plugin discovery. Third-party packages can register plot types, transforms, and hooks automatically.

In a plugin's `pyproject.toml`:

```toml
[project.entry-points."eikon.plugins"]
my_plugin = "my_plugin:register"
```

The plugin's `register()` function is called during `discover_plugins()`:

```python
# my_plugin/__init__.py
from eikon.ext import plot_type, register_transform

def register():
    @plot_type("my_fancy_plot")
    def fancy_plot(ax, /, **kwargs):
        ...

    register_transform("my_transform", lambda data: data)
```

Call `discover_plugins()` to load all installed plugins:

```python
from eikon.ext import discover_plugins
discover_plugins()
```

See the {doc}`/api/ext` for the complete API reference.
