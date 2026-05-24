<a id="top-level-entry-points"></a>

# Top-Level Entry Points

Convenience functions exposed directly from the `eikon` package.

`eikon` re-exports the public objects documented in the package-specific API
files. Only the top-level convenience functions are documented here to avoid
duplicate API targets for re-exported classes.

<a id="eikon.info"></a>

### eikon.info()

Format diagnostic information on package and platform.

<a id="eikon.render"></a>

### eikon.render(name_or_spec, \*, config=None, resolved_paths=None, session=None, formats=(), overrides=None, show=False, strict=True, extensions=None)

Convenience function: render a figure by name or spec.

This is the primary high-level entry point.  It accepts either a
`FigureSpec` object or a string name (resolved as a YAML
file path via the project config’s specs directory).

* **Parameters:**
  * **name_or_spec** ([*str*](https://docs.python.org/3/library/stdtypes.html#str) *|* [*FigureSpec*](spec.md#eikon.spec._figure.FigureSpec)) – A `FigureSpec` instance, or a string name / path to a YAML
    spec file.
  * **config** ([*ProjectConfig*](config.md#eikon.config._schema.ProjectConfig) *,* *optional*) – Project configuration.  If `None`, uses built-in defaults.
  * **resolved_paths** ([*ResolvedPaths*](config.md#eikon.config._resolver.ResolvedPaths) *,* *optional*) – Pre-resolved paths.  Prefer passing a *session* instead.
  * **session** ([*ProjectSession*](config.md#eikon.config._session.ProjectSession) *,* *optional*) – A pre-built session.  Takes precedence over *config* and
    *resolved_paths* when provided.
  * **formats** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]*) – Export format names (e.g. `("pdf", "svg")`).
  * **overrides** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* [*object*](https://docs.python.org/3/library/functions.html#object) *]* *,* *optional*) – Per-call overrides forwarded to the pipeline.
  * **show** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – Whether to display the figure interactively.
  * **strict** ([*bool*](https://docs.python.org/3/library/functions.html#bool)) – If `True` (default), let config/path errors propagate.
    If `False`, fall back to built-in defaults.
* **Returns:**
  A handle to the rendered figure.
* **Return type:**
  [FigureHandle](render.md#eikon.render._handle.FigureHandle)
