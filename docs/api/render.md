<a id="render"></a>

# Render

Rendering protocols, handles, context, data loading, drawing, pipeline, and margin labels.

<a id="module-eikon.render._protocols"></a>

<a id="render-protocols"></a>

## Render Protocols

Protocol definitions for rendering extensibility.

All rendering extension points are defined as [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)
classes — any callable matching the signature works, with no base-class
registration required.

<a id="eikon.render._protocols.PlotFunction"></a>

### *class* eikon.render._protocols.PlotFunction(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Protocol for a function that draws into a matplotlib Axes.

* **Parameters:**
  * **ax** (*Axes*) – The matplotlib Axes to draw into.
  * **\*\*kwargs** (*Any*) – Keyword arguments from `PanelSpec.params` and resolved data.

<a id="eikon.render._protocols.FigurePostProcessor"></a>

### *class* eikon.render._protocols.FigurePostProcessor(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Protocol for a post-processing step applied after all panels are drawn.

* **Parameters:**
  * **figure** (*Figure*) – The matplotlib Figure.
  * **axes** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Axes* *]*) – Panel-name-to-Axes mapping.

<a id="eikon.render._protocols.DataTransform"></a>

### *class* eikon.render._protocols.DataTransform(\*args, \*\*kwargs)

Bases: [`Protocol`](https://docs.python.org/3/library/typing.html#typing.Protocol)

Protocol for a data transformation applied before drawing.

* **Parameters:**
  **data** (*Any*) – Raw data from the data binding.
* **Returns:**
  Transformed data passed to the plot function.
* **Return type:**
  Any

<a id="module-eikon.render._handle"></a>

<a id="render-handles"></a>

## Render Handles

FigureHandle — lightweight wrapper around a rendered figure.

A [`FigureHandle`](#eikon.render._handle.FigureHandle) is the primary return type of
`render_figure()` and the convenience `eikon.render()` function.
It provides access to the figure, spec, layout, and export paths
without requiring the user to manage matplotlib or filesystem details.

<a id="eikon.render._handle.FigureHandle"></a>

### *class* eikon.render._handle.FigureHandle(\*, spec, figure, axes=<factory>, export_paths=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Result of rendering a figure.

<a id="eikon.render._handle.FigureHandle.spec"></a>

#### spec *: [Any](https://docs.python.org/3/library/typing.html#typing.Any)*

The `FigureSpec` that was rendered.

<a id="eikon.render._handle.FigureHandle.figure"></a>

#### figure *: [Any](https://docs.python.org/3/library/typing.html#typing.Any)*

The matplotlib `Figure` object.

<a id="eikon.render._handle.FigureHandle.axes"></a>

#### axes *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Panel-name-to-`Axes` mapping.

<a id="eikon.render._handle.FigureHandle.export_paths"></a>

#### export_paths *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)]*

Format-to-path mapping of exported files (empty if not exported).

<a id="eikon.render._handle.FigureHandle.show"></a>

#### show()

Display the figure interactively via `plt.show()`.

<a id="eikon.render._handle.FigureHandle.path"></a>

#### path(fmt)

Return the export path for a given format, or `None`.

* **Parameters:**
  **fmt** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Export format key (e.g. `"pdf"`, `"svg"`).

<a id="eikon.render._handle.FigureHandle.save"></a>

#### save(path, \*, dpi=300, bbox_inches='tight', close=True, \*\*kwargs)

Save the figure to a file and optionally close it.

* **Parameters:**
  * **path** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* *Path*) – Destination file path (e.g. `"output/fig.pdf"`).
    Parent directories are created automatically.
  * **dpi** ([*int*](https://docs.python.org/3/library/functions.html#int)) – Resolution in dots per inch.
  * **bbox_inches** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Bounding-box option forwarded to
    `matplotlib.figure.Figure.savefig()`.
  * **close** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether to close the figure after saving (default `True`).
  * **\*\*kwargs** ([*Any*](https://docs.python.org/3/library/typing.html#typing.Any)) – Extra keyword arguments forwarded to `savefig`.
* **Returns:**
  The resolved output path.
* **Return type:**
  Path

<a id="eikon.render._handle.FigureHandle.close"></a>

#### close()

Close the matplotlib Figure to free memory.

<a id="module-eikon.render._context"></a>

<a id="render-contexts"></a>

## Render Contexts

Render context — mutable state carried through the rendering pipeline.

The [`RenderContext`](#eikon.render._context.RenderContext) is an internal object that accumulates state
as the pipeline progresses through its stages.  It is not part of the
public API.

<a id="eikon.render._context.RenderContext"></a>

### *class* eikon.render._context.RenderContext(\*, spec, config, paths, style=None, layout=None, export_formats=(), show=False, overrides=<factory>, data=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Mutable state for a single render pass.

<a id="eikon.render._context.RenderContext.spec"></a>

#### spec *: [FigureSpec](spec.md#eikon.spec._figure.FigureSpec)*

The figure specification being rendered.

<a id="eikon.render._context.RenderContext.config"></a>

#### config *: [ProjectConfig](config.md#eikon.config._schema.ProjectConfig)*

The resolved project configuration.

<a id="eikon.render._context.RenderContext.paths"></a>

#### paths *: [ResolvedPaths](config.md#eikon.config._resolver.ResolvedPaths)*

<a id="eikon.render._context.RenderContext.style"></a>

#### style *: [StyleSheet](style.md#eikon.style._sheet.StyleSheet) | [None](https://docs.python.org/3/library/constants.html#None)*

The resolved style sheet (set during style resolution).

<a id="eikon.render._context.RenderContext.layout"></a>

#### layout *: [BuiltLayout](layout.md#eikon.layout._builder.BuiltLayout) | [None](https://docs.python.org/3/library/constants.html#None)*

The built layout (set during layout building).

<a id="eikon.render._context.RenderContext.export_formats"></a>

#### export_formats *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

Formats to export (empty = no export).

<a id="eikon.render._context.RenderContext.show"></a>

#### show *: [bool](https://docs.python.org/3/library/functions.html#bool)*

Whether to display the figure interactively after rendering.

<a id="eikon.render._context.RenderContext.overrides"></a>

#### overrides *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Per-call keyword overrides.

<a id="eikon.render._context.RenderContext.data"></a>

#### data *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]]*

<a id="module-eikon.render._data"></a>

<a id="render-data-loading"></a>

## Render Data Loading

Data resolution utilities for the rendering pipeline.

Resolves [`DataBinding`](spec.md#eikon.spec._data.DataBinding) instances into concrete
keyword arguments that are forwarded to plot functions. Data files are
resolved relative to the project’s configured `data_dir` and loaded
using lightweight, dependency-tolerant logic (pandas if available,
fallback to the stdlib CSV reader).

<a id="eikon.render._data.resolve_data_binding"></a>

### eikon.render._data.resolve_data_binding(binding, data_dir, \*, extensions=None)

Load data for a panel and return kwargs for the plot function.

Returns a dict containing at least `data` (the loaded table-like
object) plus `x`/`y`/`hue` keys when the binding specifies
corresponding columns.

<a id="module-eikon.render._drawing"></a>

<a id="drawing"></a>

## Drawing

Panel drawing dispatch — route draw calls to registered plot functions.

This module connects the rendering pipeline to the extension registry:
for each panel, it looks up the registered plot function by
`PanelSpec.plot_type` and invokes it on the corresponding `Axes`.

<a id="eikon.render._drawing.draw_panel"></a>

### eikon.render._drawing.draw_panel(ax, panel, \*, data_dir, extensions=None)

Draw a single panel using its registered plot function.

* **Parameters:**
  * **ax** (*Axes*) – The matplotlib Axes to draw into.
  * **panel** ([*PanelSpec*](spec.md#eikon.spec._panel.PanelSpec)) – The panel specification containing plot_type and params.
* **Raises:**
  [**UnknownPlotTypeError**](types.md#eikon.exceptions.UnknownPlotTypeError) – If the panel’s `plot_type` is not registered.

<a id="eikon.render._drawing.draw_all_panels"></a>

### eikon.render._drawing.draw_all_panels(axes, panels, \*, data_dir, extensions=None)

Draw all panels into their corresponding axes.

* **Parameters:**
  * **axes** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Axes* *]*) – Panel-name-to-Axes mapping from `BuiltLayout`.
  * **panels** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*PanelSpec*](spec.md#eikon.spec._panel.PanelSpec) *,*  *...* *]*) – Panel specifications to draw.

<a id="module-eikon.render._pipeline"></a>

<a id="render-pipeline"></a>

## Render Pipeline

Rendering pipeline orchestrator.

Chains the rendering stages: config -> style -> layout -> draw -> post-process -> export.
Each stage is a pure function with explicit typed inputs and outputs.
The orchestrator composes stages without mutable shared state.

<a id="eikon.render._pipeline.render_figure"></a>

### eikon.render._pipeline.render_figure(spec, \*, session=None, config=None, resolved_paths=None, formats=(), show=False, overrides=None, extensions=None)

Render a figure from its specification — the main pipeline entry point.

* **Parameters:**
  * **spec** ([*FigureSpec*](spec.md#eikon.spec._figure.FigureSpec)) – The figure specification to render.
  * **session** ([*ProjectSession*](config.md#eikon.config._session.ProjectSession) *,* *optional*) – A pre-built project session.  Takes precedence over *config*
    and *resolved_paths*.
  * **config** ([*ProjectConfig*](config.md#eikon.config._schema.ProjectConfig) *,* *optional*) – Project configuration.  Defaults to built-in defaults.
  * **resolved_paths** ([*ResolvedPaths*](config.md#eikon.config._resolver.ResolvedPaths) *,* *optional*) – Pre-resolved paths.
  * **formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Export format names (e.g. `("pdf", "svg")`).  Empty = no export.
  * **show** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether to display the figure interactively after rendering.
  * **overrides** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]* *,* *optional*) – Per-call keyword overrides forwarded to the pipeline.
* **Returns:**
  A handle to the rendered figure.
* **Return type:**
  [FigureHandle](#eikon.render._handle.FigureHandle)
* **Raises:**
  [**RenderError**](types.md#eikon.exceptions.RenderError) – If any stage of the pipeline fails.

<a id="module-eikon.render._margin_labels"></a>

<a id="render-margin-labels"></a>

## Render Margin Labels

Margin label rendering — hierarchy resolution, geometry, and drawing.

Converts declarative `MarginLabelSpec` definitions into positioned
text and optional background patches on a matplotlib Figure.

<a id="eikon.render._margin_labels.draw_margin_labels"></a>

### eikon.render._margin_labels.draw_margin_labels(fig, built, margin_labels)

Render margin labels on the figure.

* **Parameters:**
  * **fig** (*Figure*) – The matplotlib figure to draw on.
  * **built** ([*BuiltLayout*](layout.md#eikon.layout._builder.BuiltLayout)) – The built layout (provides `grid_spec` and `axes`).
  * **margin_labels** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*MarginLabelSpec*](spec.md#eikon.spec._margin_labels.MarginLabelSpec) *]*) – Mapping from edge name to label spec.
