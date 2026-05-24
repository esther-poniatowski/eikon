<a id="extensions"></a>

# Extensions

Runtime extension registry, plot types, transforms, lifecycle hooks, and plugin discovery.

<a id="module-eikon.ext._registry"></a>

<a id="extension-registry"></a>

## Extension Registry

Explicit extension registry and runtime bootstrap helpers.

<a id="eikon.ext._registry.ExtensionRegistry"></a>

### *class* eikon.ext._registry.ExtensionRegistry(\*, plot_types=None, hooks=None, transforms=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Container for plot types, hooks, and transforms.

<a id="eikon.ext._registry.ExtensionRegistry.clone"></a>

#### clone()

<a id="eikon.ext._registry.ExtensionRegistry.register_plot_type"></a>

#### register_plot_type(name, fn)

<a id="eikon.ext._registry.ExtensionRegistry.get_plot_type"></a>

#### get_plot_type(name)

<a id="eikon.ext._registry.ExtensionRegistry.list_plot_types"></a>

#### list_plot_types()

<a id="eikon.ext._registry.ExtensionRegistry.clear_plot_types"></a>

#### clear_plot_types()

<a id="eikon.ext._registry.ExtensionRegistry.register_hook"></a>

#### register_hook(hook, fn)

<a id="eikon.ext._registry.ExtensionRegistry.fire_hook"></a>

#### fire_hook(hook, \*\*kwargs)

<a id="eikon.ext._registry.ExtensionRegistry.clear_hooks"></a>

#### clear_hooks()

<a id="eikon.ext._registry.ExtensionRegistry.register_transform"></a>

#### register_transform(name, fn)

<a id="eikon.ext._registry.ExtensionRegistry.list_transforms"></a>

#### list_transforms()

<a id="eikon.ext._registry.ExtensionRegistry.clear_transforms"></a>

#### clear_transforms()

<a id="eikon.ext._registry.ExtensionRegistry.apply_transforms"></a>

#### apply_transforms(data, names)

<a id="eikon.ext._registry.build_runtime_registry"></a>

### eikon.ext._registry.build_runtime_registry()

Return a bootstrapped snapshot for one render/runtime session.

<a id="eikon.ext._registry.get_default_registry"></a>

### eikon.ext._registry.get_default_registry()

Return the mutable process-local default registry.

<a id="module-eikon.ext._plot_types"></a>

<a id="plot-types"></a>

## Plot Types

Plot type registry — string-keyed dictionary of plot functions.

Provides a global registry of plot functions, a `@plot_type` decorator
for registration, and a lookup function used by the drawing module.

<a id="eikon.ext._plot_types.register_plot_type"></a>

### eikon.ext._plot_types.register_plot_type(name, fn)

Register a plot function under a string key.

* **Parameters:**
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The plot type name (e.g. `"line"`, `"scatter"`).
  * **fn** ([*PlotFunction*](render.md#eikon.render._protocols.PlotFunction)) – A callable matching the `PlotFunction` protocol.

<a id="eikon.ext._plot_types.get_plot_type"></a>

### eikon.ext._plot_types.get_plot_type(name)

Look up a registered plot function by name.

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The plot type name.
* **Returns:**
  The registered plot function.
* **Return type:**
  [PlotFunction](render.md#eikon.render._protocols.PlotFunction)
* **Raises:**
  [**UnknownPlotTypeError**](types.md#eikon.exceptions.UnknownPlotTypeError) – If no plot type is registered under *name*.

<a id="eikon.ext._plot_types.plot_type"></a>

### eikon.ext._plot_types.plot_type(name)

Decorator to register a function as a named plot type.

Usage:

```default
@plot_type("line")
def draw_line(ax, /, **kwargs):
    ax.plot(kwargs.get("x", []), kwargs.get("y", []))
```

* **Parameters:**
  **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – The plot type name to register under.
* **Returns:**
  The original function, unmodified.
* **Return type:**
  Callable

<a id="eikon.ext._plot_types.list_plot_types"></a>

### eikon.ext._plot_types.list_plot_types()

Return a sorted list of all registered plot type names.

<a id="module-eikon.ext._transforms"></a>

<a id="data-transforms"></a>

## Data Transforms

Registry and application of data transforms.

Transforms are simple callables that accept a data object and return a
transformed data object. They are addressed by string name to keep the
declarative YAML surface stable.

<a id="eikon.ext._transforms.register_transform"></a>

### eikon.ext._transforms.register_transform(name, fn)

<a id="eikon.ext._transforms.apply_transforms"></a>

### eikon.ext._transforms.apply_transforms(data, names)

<a id="eikon.ext._transforms.list_transforms"></a>

### eikon.ext._transforms.list_transforms()

<a id="module-eikon.ext._hooks"></a>

<a id="lifecycle-hooks"></a>

## Lifecycle Hooks

Lifecycle hook system for rendering and export events.

Hooks allow users to inject custom logic at well-defined points in the
render/export pipeline without modifying eikon source.

<a id="eikon.ext._hooks.HookName"></a>

### *class* eikon.ext._hooks.HookName(\*values)

Bases: [`Enum`](https://docs.python.org/3/library/enum.html#enum.Enum)

Well-defined hook points in the figure lifecycle.

<a id="eikon.ext._hooks.HookName.PRE_RENDER"></a>

#### PRE_RENDER *= 'pre_render'*

<a id="eikon.ext._hooks.HookName.POST_RENDER"></a>

#### POST_RENDER *= 'post_render'*

<a id="eikon.ext._hooks.HookName.PRE_EXPORT"></a>

#### PRE_EXPORT *= 'pre_export'*

<a id="eikon.ext._hooks.HookName.POST_EXPORT"></a>

#### POST_EXPORT *= 'post_export'*

<a id="eikon.ext._hooks.register_hook"></a>

### eikon.ext._hooks.register_hook(hook, fn)

Register a callback for a lifecycle hook.

* **Parameters:**
  * **hook** ([*HookName*](#eikon.ext._hooks.HookName)) – The hook point to attach to.
  * **fn** (*HookFunction*) – A callable invoked when the hook fires.

<a id="eikon.ext._hooks.fire_hook"></a>

### eikon.ext._hooks.fire_hook(hook, \*\*kwargs)

Fire all callbacks registered for a hook.

* **Parameters:**
  * **hook** ([*HookName*](#eikon.ext._hooks.HookName)) – The hook point to fire.
  * **\*\*kwargs** (*Any*) – Context passed to each callback.

<a id="eikon.ext._hooks.clear_hooks"></a>

### eikon.ext._hooks.clear_hooks()

Remove all registered hooks.  For testing only.

<a id="module-eikon.ext._discovery"></a>

<a id="plugin-discovery"></a>

## Plugin Discovery

Entry-point based plugin discovery.

Discovers and loads third-party plot types and hooks registered via
the `eikon.plot_types` entry-point group in `pyproject.toml`.

<a id="eikon.ext._discovery.discover_plugins"></a>

### eikon.ext._discovery.discover_plugins(group='eikon.plot_types')

Load all entry points in the given group.

Each entry point should be a module that, when imported, registers
its plot types via `@plot_type("name")` or
`register_plot_type(name, fn)`.

* **Parameters:**
  **group** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Entry-point group name to discover.
* **Returns:**
  Number of entry points successfully loaded.
* **Return type:**
  [int](https://docs.python.org/3/library/functions.html#int)
