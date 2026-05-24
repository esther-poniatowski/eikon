# Eikon Package

Declarative figure specifications, rendering, export, registry, and extension APIs.

## Top-Level Entry Points

`eikon` re-exports the public objects documented in the sections below. The
top-level convenience functions are documented here to avoid duplicate API
targets for re-exported classes.

```{eval-rst}
.. autofunction:: eikon.info

.. autofunction:: eikon.render
```

## Shared Types

```{eval-rst}
.. automodule:: eikon._types
   :members:
   :undoc-members:
   :show-inheritance:
```

## Exceptions

```{eval-rst}
.. automodule:: eikon.exceptions
   :members:
   :undoc-members:
   :show-inheritance:
```

## Configuration Schema

```{eval-rst}
.. automodule:: eikon.config._schema
   :members:
   :undoc-members:
   :show-inheritance:
```

## Configuration Loading

```{eval-rst}
.. automodule:: eikon.config._loader
   :members:
   :undoc-members:
   :show-inheritance:
```

## Configuration Resolution

```{eval-rst}
.. automodule:: eikon.config._resolver
   :members:
   :undoc-members:
   :show-inheritance:
```

## Project Sessions

```{eval-rst}
.. automodule:: eikon.config._session
   :members:
   :undoc-members:
   :show-inheritance:
```

## Configuration Validation

```{eval-rst}
.. automodule:: eikon.config._validation
   :members:
   :undoc-members:
   :show-inheritance:
```

## Figure Specifications

```{eval-rst}
.. automodule:: eikon.spec._figure
   :members:
   :undoc-members:
   :show-inheritance:
```

## Panel Specifications

```{eval-rst}
.. automodule:: eikon.spec._panel
   :members:
   :undoc-members:
   :show-inheritance:
```

## Data Bindings

```{eval-rst}
.. automodule:: eikon.spec._data
   :members:
   :undoc-members:
   :show-inheritance:
```

## Margin Labels

```{eval-rst}
.. automodule:: eikon.spec._margin_labels
   :members:
   :undoc-members:
   :show-inheritance:
```

## Specification Overrides

```{eval-rst}
.. automodule:: eikon.spec._override
   :members:
   :undoc-members:
   :show-inheritance:
```

## Specification Parsing

```{eval-rst}
.. automodule:: eikon.spec._parse
   :members:
   :undoc-members:
   :show-inheritance:
```

## Style Sheets

```{eval-rst}
.. automodule:: eikon.style._sheet
   :members:
   :undoc-members:
   :show-inheritance:
```

## Style Loading

```{eval-rst}
.. automodule:: eikon.style._loader
   :members:
   :undoc-members:
   :show-inheritance:
```

## Style Composition

```{eval-rst}
.. automodule:: eikon.style._composer
   :members:
   :undoc-members:
   :show-inheritance:
```

## Style Presets

```{eval-rst}
.. automodule:: eikon.style._presets
   :members:
   :undoc-members:
   :show-inheritance:
```

## Matplotlib Parameters

```{eval-rst}
.. automodule:: eikon.style._rcparams
   :members:
   :undoc-members:
   :show-inheritance:
```

## Layout Grid

```{eval-rst}
.. automodule:: eikon.layout._grid
   :members:
   :undoc-members:
   :show-inheritance:
```

## Panel Placement

```{eval-rst}
.. automodule:: eikon.layout._placement
   :members:
   :undoc-members:
   :show-inheritance:
```

## Layout Building

```{eval-rst}
.. automodule:: eikon.layout._builder
   :members:
   :undoc-members:
   :show-inheritance:
```

## Layout Constraints

```{eval-rst}
.. automodule:: eikon.layout._constraints
   :members:
   :undoc-members:
   :show-inheritance:
```

## Shared Axes

```{eval-rst}
.. automodule:: eikon.layout._shared_axes
   :members:
   :undoc-members:
   :show-inheritance:
```

## Colorbars

```{eval-rst}
.. automodule:: eikon.layout._colorbars
   :members:
   :undoc-members:
   :show-inheritance:
```

## Insets

```{eval-rst}
.. automodule:: eikon.layout._insets
   :members:
   :undoc-members:
   :show-inheritance:
```

## Render Protocols

```{eval-rst}
.. automodule:: eikon.render._protocols
   :members:
   :undoc-members:
   :show-inheritance:
```

## Render Handles

```{eval-rst}
.. automodule:: eikon.render._handle
   :members:
   :undoc-members:
   :show-inheritance:
```

## Render Contexts

```{eval-rst}
.. automodule:: eikon.render._context
   :members:
   :undoc-members:
   :show-inheritance:
```

## Render Data Loading

```{eval-rst}
.. automodule:: eikon.render._data
   :members:
   :undoc-members:
   :show-inheritance:
```

## Drawing

```{eval-rst}
.. automodule:: eikon.render._drawing
   :members:
   :undoc-members:
   :show-inheritance:
```

## Render Pipeline

```{eval-rst}
.. automodule:: eikon.render._pipeline
   :members:
   :undoc-members:
   :show-inheritance:
```

## Render Margin Labels

```{eval-rst}
.. automodule:: eikon.render._margin_labels
   :members:
   :undoc-members:
   :show-inheritance:
```

## Export Configuration

```{eval-rst}
.. automodule:: eikon.export._config
   :members:
   :undoc-members:
   :show-inheritance:
```

## Export Batch

```{eval-rst}
.. automodule:: eikon.export._batch
   :members:
   :undoc-members:
   :show-inheritance:
```

## Export Handlers

```{eval-rst}
.. automodule:: eikon.export._handlers
   :members:
   :undoc-members:
   :show-inheritance:
```

## Export Metadata

```{eval-rst}
.. automodule:: eikon.export._metadata
   :members:
   :undoc-members:
   :show-inheritance:
```

## Export Paths

```{eval-rst}
.. automodule:: eikon.export._paths
   :members:
   :undoc-members:
   :show-inheritance:
```

## Filename Sanitization

```{eval-rst}
.. automodule:: eikon.export._sanitize
   :members:
   :undoc-members:
   :show-inheritance:
```

## Registry

```{eval-rst}
.. automodule:: eikon.registry._registry
   :members:
   :undoc-members:
   :show-inheritance:
```

## Registry Index

```{eval-rst}
.. automodule:: eikon.registry._index
   :members:
   :undoc-members:
   :show-inheritance:
```

## Registry Queries

```{eval-rst}
.. automodule:: eikon.registry._query
   :members:
   :undoc-members:
   :show-inheritance:
```

## Registry Locking

```{eval-rst}
.. automodule:: eikon.registry._locking
   :members:
   :undoc-members:
   :show-inheritance:
```

## Extension Registry

```{eval-rst}
.. automodule:: eikon.ext._registry
   :members:
   :undoc-members:
   :show-inheritance:
```

## Plot Types

```{eval-rst}
.. automodule:: eikon.ext._plot_types
   :members:
   :undoc-members:
   :show-inheritance:
```

## Data Transforms

```{eval-rst}
.. automodule:: eikon.ext._transforms
   :members:
   :undoc-members:
   :show-inheritance:
```

## Lifecycle Hooks

```{eval-rst}
.. automodule:: eikon.ext._hooks
   :members:
   :undoc-members:
   :show-inheritance:
```

## Plugin Discovery

```{eval-rst}
.. automodule:: eikon.ext._discovery
   :members:
   :undoc-members:
   :show-inheritance:
```

## Matplotlib Contributions

```{eval-rst}
.. automodule:: eikon.contrib._matplotlib
   :members:
   :undoc-members:
   :show-inheritance:
```

## Seaborn Contributions

```{eval-rst}
.. automodule:: eikon.contrib._seaborn
   :members:
   :undoc-members:
   :show-inheritance:
```
