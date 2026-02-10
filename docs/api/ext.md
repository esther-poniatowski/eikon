# eikon.ext

Extension system: plot type registry, data transforms, lifecycle hooks, and plugin discovery.

For usage examples, see the {doc}`Extensions guide </guide/extensions>`.

## Enums

### HookName

```
eikon.ext.HookName
```

Lifecycle hook points in the figure pipeline.

| Member | Value | Description |
|--------|-------|-------------|
| `PRE_RENDER` | `"pre_render"` | Before style/layout |
| `POST_RENDER` | `"post_render"` | After all panels drawn |
| `PRE_EXPORT` | `"pre_export"` | Before export starts |
| `POST_EXPORT` | `"post_export"` | After all exports complete |

## Plot Type Registry

### register_plot_type

```
eikon.ext.register_plot_type(name: str, fn: Callable[..., None]) -> None
```

Register a plot function under a string key.

---

### get_plot_type

```
eikon.ext.get_plot_type(name: str) -> Callable[..., None]
```

Look up a registered plot function by name.

**Raises:** `UnknownPlotTypeError` if not registered.

---

### list_plot_types

```
eikon.ext.list_plot_types() -> list[str]
```

Return a sorted list of all registered plot type names.

---

### plot_type

```
@eikon.ext.plot_type(name: str)
```

Decorator to register a function as a named plot type.

```python
@plot_type("violin")
def draw_violin(ax, /, **kwargs):
    ax.violinplot(kwargs.get("data", []))
```

Returns the original function unmodified.

## Data Transforms

### register_transform

```
eikon.ext.register_transform(name: str, fn: Callable[[Any], Any]) -> None
```

Register a data transform function under a string key.

---

### apply_transforms

```
eikon.ext.apply_transforms(data: Any, names: tuple[str, ...]) -> Any
```

Apply named transforms in order. Each transform receives the output of the previous one.

**Raises:** `RenderError` if a transform name is not registered.

---

### list_transforms

```
eikon.ext.list_transforms() -> list[str]
```

Return a sorted list of all registered transform names.

---

### clear_transforms

```
eikon.ext.clear_transforms() -> None
```

Remove all registered transforms. Primarily for testing.

## Lifecycle Hooks

### register_hook

```
eikon.ext.register_hook(hook: HookName, fn: Callable) -> None
```

Register a callback for a lifecycle hook. Multiple callbacks can be registered for the same hook.

---

### fire_hook

```
eikon.ext.fire_hook(hook: HookName, **kwargs: Any) -> None
```

Fire all callbacks registered for a hook, passing context as keyword arguments.

---

### clear_hooks

```
eikon.ext.clear_hooks() -> None
```

Remove all registered hooks. Primarily for testing.

## Plugin Discovery

### discover_plugins

```
eikon.ext.discover_plugins() -> None
```

Discover and load plugins registered via the `eikon.plugins` entry point group. Each plugin's registration function is called once.
