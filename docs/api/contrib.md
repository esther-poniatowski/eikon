<a id="contributions"></a>

# Contributions

Built-in plotting contributions backed by Matplotlib and optional Seaborn support.

<a id="module-eikon.contrib._matplotlib"></a>

<a id="matplotlib-contributions"></a>

## Matplotlib Contributions

Built-in matplotlib plot type wrappers.

Each function is registered via `@plot_type("name")` and delegates to
the corresponding matplotlib `Axes` method.  The `params` dict from
`PanelSpec` is forwarded as keyword arguments.

<a id="module-eikon.contrib._seaborn"></a>

<a id="seaborn-contributions"></a>

## Seaborn Contributions

Built-in seaborn plot type wrappers (lazy import).

Seaborn is imported only when one of its plot types is first invoked,
keeping it an optional dependency.
