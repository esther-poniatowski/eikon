# eikon.render

Rendering pipeline: figure orchestration, protocols, and figure handles.

For usage examples, see the {doc}`Rendering guide </guide/rendering>`.

## Classes

### FigureHandle

```
eikon.render.FigureHandle(*, spec, figure, axes={}, export_paths={})
```

Handle to a rendered figure. Mutable dataclass (not frozen).

| Field | Type | Description |
|-------|------|-------------|
| `spec` | `FigureSpec` | The specification used to render |
| `figure` | `Figure` | The matplotlib Figure |
| `axes` | `dict[str, Axes]` | Panel name to Axes mapping |
| `export_paths` | `dict[str, Path]` | Format name to exported file path |

**Methods:**

```
handle.show() -> None
```
Display the figure interactively via `plt.show()`.

```
handle.path(fmt: str) -> Path | None
```
Get the export path for a specific format, or `None` if not exported.

```
handle.close() -> None
```
Close the figure and free memory.

## Protocols

### PlotFunction

```python
class PlotFunction(Protocol):
    def __call__(self, ax: Axes, /, **kwargs: Any) -> None: ...
```

Protocol for functions that draw into a matplotlib Axes. Any callable matching this signature works — no base class needed.

- `ax` — The matplotlib Axes to draw into (positional-only).
- `**kwargs` — Keyword arguments from `PanelSpec.params` and resolved data columns.

---

### FigurePostProcessor

```python
class FigurePostProcessor(Protocol):
    def __call__(self, figure: Figure, axes: dict[str, Axes], /) -> None: ...
```

Protocol for post-processing steps applied after all panels are drawn.

---

### DataTransform

```python
class DataTransform(Protocol):
    def __call__(self, data: Any, /) -> Any: ...
```

Protocol for data transformations applied before drawing.

## Margin labels

The `render_figure` pipeline automatically draws margin labels when `FigureSpec.margin_labels` is set. Labels are rendered after all panels are drawn and the layout is finalized.

The internal entry point is `draw_margin_labels`, which resolves label hierarchies into positioned text and optional background patches. See the {doc}`Specifications guide </guide/specifications>` for the declarative YAML syntax.

## Functions

### render_figure

```
eikon.render.render_figure(spec: FigureSpec, *, config=None,
                           resolved_paths=None, formats=(),
                           show=False, overrides=None) -> FigureHandle
```

Full render pipeline: spec → style → layout → draw → export.

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `spec` | `FigureSpec` | *(required)* | Figure specification |
| `config` | `ProjectConfig \| None` | `None` | Project config (defaults if `None`) |
| `resolved_paths` | `ResolvedPaths \| None` | `None` | Resolved paths |
| `formats` | `tuple[str, ...]` | `()` | Export format names |
| `show` | `bool` | `False` | Display interactively |
| `overrides` | `dict[str, object] \| None` | `None` | Runtime overrides |

**Returns:** `FigureHandle` with the rendered figure and export paths.

---

### render (convenience)

```
eikon.render(name_or_spec: str | FigureSpec, *, config=None,
             resolved_paths=None, formats=(), overrides=None,
             show=False) -> FigureHandle
```

High-level entry point. Accepts a `FigureSpec` or a string name. Strings are resolved via the registry first, then as file paths under the specs directory.

See the root package documentation for details.
