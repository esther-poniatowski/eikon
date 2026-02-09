# Eikon — Architecture & Development Plan

## Context

Eikon is a figure management library for programmatic creation, styling, and
export of scientific visualizations, built on top of matplotlib.  The project
targets Python >= 3.12 and uses setuptools as its build system.

The library addresses a common pain point in scientific workflows: managing
reproducible, publication-quality figures with consistent styling across
analyses, manuscripts, and presentations.  Manual figure management becomes
error-prone as the number of panels, conditions, and output formats grows.
Eikon provides a structured, declarative approach to figure definition,
styling, layout, rendering, and export.

---

## Design Rules

Every module, class, and function in Eikon must respect the following
constraints.  These are not aspirational — they are hard requirements that
govern every design decision.

### Separation of Concerns

Each module handles exactly **one** responsibility.  Subpackages group related
modules by domain (configuration, specification, style, layout, rendering,
export, registry, extensions).  No module reaches across domains to perform
work that belongs to another.

### Modularity

Source modules are **small and focused** — private (`_*.py`), exposed through a
curated `__init__.py`.  Users import from `eikon.config`, `eikon.spec`, etc.,
never from `eikon.config._loader`.  No file exceeds ~300 lines; when a module
grows beyond that, it is split.

### Flexibility

The library offers a **dual API**: users can define figures as Python
dataclasses (programmatic) or as YAML files (declarative).  Both paths produce
the same `FigureSpec` objects and flow through the same pipeline.

### Extensibility

Extension points use **protocols** (structural subtyping), not ABC inheritance.
Any callable matching the `PlotFunction` protocol works as a plot type.  A
decorator-based registry (`@plot_type("name")`) and entry-point discovery allow
third-party plugins without modifying eikon source.

### Robustness

All structured data uses **frozen dataclasses** (`frozen=True, kw_only=True,
slots=True`).  Configuration and specifications are validated explicitly before
use — not at the point of failure.  Every error condition has a typed exception
with a descriptive message.

All YAML schemas carry an explicit **version field** (`config_version`,
`spec_version`, `style_version`).  A compatibility layer checks the version
on load and either migrates the structure silently (for minor bumps) or
raises a clear error pointing the user to the migration guide (for breaking
changes).  This keeps the declarative API extensible over time without
silently breaking older projects or plugins.

### User-Friendly API

The public API surface is **curated**: `eikon.__init__` re-exports only the
most commonly used classes and functions.  The configuration system is
**declarative** — a single `eikon.yaml` file controls paths, defaults, styles,
and export settings.  Users never hard-code file paths in their code.

Beyond dataclass construction, the library provides **high-level convenience
functions** that hide path resolution, config loading, and registry lookups:

- `eikon.render("fig-name", formats=["pdf"], overrides={...})` — render a
  registered or on-disk figure by name, with optional per-call overrides,
  returning a `FigureHandle` that abstracts away output paths.
- `eikon.load_registry().render(tag="neural")` — render all figures matching
  a query in a single call.
- `FigureHandle` — a lightweight wrapper returned by render functions,
  exposing `.show()`, `.path(fmt)`, `.figure`, and `.spec` without requiring
  the user to manage paths or matplotlib objects directly.

These convenience surfaces are implemented in Phase 3 (render pipeline) and
composed atop the lower-level dataclass API — they do not bypass it.

### No Hard-Coded Paths

All paths in configuration are **relative** to a project root.  The root is
resolved through a three-tier strategy with explicit precedence:

1. **Explicit override** — `--project-root` CLI flag or `project_root=`
   kwarg in the Python API.
2. **Environment variable** — `EIKON_PROJECT_ROOT`, useful for CI runners,
   notebook kernels, and containerised workflows where cwd is unreliable.
3. **Auto-discovery** — walk upward from the current working directory until
   an `eikon.yaml` file is found.

If none of these produce a result, a descriptive `ConfigNotFoundError` is
raised explaining all three lookup methods.  Once resolved, the project root
is **cached per run** on the `ResolvedPaths` object to prevent accidental
cross-project bleed when the working directory changes during execution
(e.g. inside `os.chdir` blocks or notebook cells).  Absolute paths in YAML
config are rejected during validation.

### No Magic Variables

Every parameter is **explicit, typed, and documented** with a visible default
value.  No global mutable state is used for configuration.  No implicit
environment variables are read silently.

### No Fragile Code

No monolithic functions.  The rendering pipeline is decomposed into small,
testable steps: resolve config → resolve style → build layout → draw panels →
export.  Each step is a function with a clear input/output contract.  No
function exceeds ~40 lines.

---

## Architecture Overview

### Figure Lifecycle

A figure flows through five stages, each handled by a dedicated subpackage:

```
Specification  →  Style Resolution  →  Layout Build  →  Panel Drawing  →  Export
(FigureSpec)      (StyleSheet)         (BuiltLayout)    (PlotFunction)    (ExportHandler)
```

Each stage is a **pure transformation** (or nearly so), making the system
testable and composable.  The rendering pipeline orchestrator
(`render/_pipeline.py`) chains these stages together.

### Configuration Hierarchy

Settings are resolved through four layers, each overriding the previous:

```
Built-in Defaults  →  Project Config (eikon.yaml)  →  Figure-level Overrides  →  Runtime kwargs
```

This means:
- A bare `FigureSpec(name="fig1")` uses all defaults.
- A project-level `eikon.yaml` sets shared preferences.
- Per-figure `style:` or `export:` fields override the project defaults.
- Runtime keyword arguments override everything.

---

## Package Structure

Each stage of the figure lifecycle is implemented as a separate subpackage
under `src/eikon/`.

9 subpackages, each small and single-responsibility:

- `config/` — YAML-driven project configuration with auto-discovered project root
- `spec/` — Declarative figure definitions (Python dataclasses + YAML)
- `style/` — Composable style sheets bridging to matplotlib rcParams
- `layout/` — Grid-based multi-panel layout engine
- `render/` — Pipeline orchestrator + protocol-based plot dispatch
- `export/` — Format handlers (PDF/SVG/PNG) + batch export
- `registry/` — YAML-manifest figure tracking with tag/group queries
- `ext/` — Plugin system via decorators + entry points
- `contrib/` — Built-in matplotlib/seaborn plot type wrappers

```
src/eikon/
    __init__.py              # Public API surface (curated re-exports)
    __main__.py              # python -m eikon entry point
    cli.py                   # Typer CLI (info, init, validate, render, batch, registry)
    _types.py                # Shared type aliases: ExportFormat, Tag, DPI, StyleRef
    exceptions.py            # Exception hierarchy (EikonError → domain-specific errors)

    config/                  # Configuration system
        __init__.py          # Re-exports: load_config, ProjectConfig, ResolvedPaths
        _schema.py           # Dataclasses: ProjectConfig, PathsConfig, ExportDefaults, StyleDefaults
        _loader.py           # YAML loading, deep merging
        _resolver.py         # Project root discovery, path resolution
        _defaults.py         # Built-in default values as frozen dataclasses
        _validation.py       # Schema validation with descriptive error messages

    spec/                    # Declarative figure specifications
        __init__.py          # Re-exports: FigureSpec, PanelSpec, DataBinding
        _figure.py           # FigureSpec dataclass
        _panel.py            # PanelSpec dataclass (one axes region)
        _data.py             # DataBinding dataclass (data source references)
        _override.py         # Override/merge logic for specs
        _parse.py            # Parse FigureSpec from YAML file or dict

    style/                   # Style management
        __init__.py          # Re-exports: StyleSheet, style_context, load_style
        _sheet.py            # StyleSheet dataclass (font, palette, rc_overrides, extends)
        _composer.py         # Style merging / inheritance chain resolution
        _rcparams.py         # Convert StyleSheet → matplotlib rcParams dict + context manager
        _presets.py          # Built-in style presets: publication, presentation, poster
        _loader.py           # Load from preset name, .mplstyle file, or YAML

    layout/                  # Layout engine
        __init__.py          # Re-exports: LayoutSpec, BuiltLayout, build_layout
        _grid.py             # LayoutSpec dataclass (rows, cols, ratios, spacing)
        _placement.py        # Resolve PanelSpec row/col → grid slices
        _constraints.py      # Layout validation (bounds, overlap detection)
        _builder.py          # Build matplotlib Figure + dict[panel_name, Axes]
        _shared_axes.py      # Shared-x/y axis linking across panels
        _colorbars.py        # Colorbar attachment (constrained-layout aware)
        _insets.py           # Inset axes creation and registration

    render/                  # Rendering pipeline
        __init__.py          # Re-exports: render_figure, FigureHandle
        _context.py          # RenderContext (mutable state during rendering)
        _pipeline.py         # Orchestrator: spec → style → layout → draw → export
        _drawing.py          # Dispatch draw calls to registered plot functions
        _protocols.py        # PlotFunction, ExportHandler, DataTransform protocols
        _handle.py           # FigureHandle — lightweight render result wrapper

    export/                  # Export pipeline
        __init__.py          # Re-exports: batch_export, ExportSpec
        _config.py           # ExportSpec + ResolvedExportConfig dataclasses
        _handlers.py         # PdfHandler, SvgHandler, PngHandler
        _metadata.py         # Metadata injection (PDF keywords, PNG text chunks)
        _paths.py            # Output path construction with template variables
        _sanitize.py         # Filename sanitization (cross-platform safe)
        _batch.py            # Batch export across figures/formats

    registry/                # Figure registry
        __init__.py          # Re-exports: Registry
        _registry.py         # Registry class (CRUD, YAML manifest persistence)
        _index.py            # Manifest file I/O
        _query.py            # Query/filter by tags, groups
        _locking.py          # Advisory file locks for concurrent manifest access

    ext/                     # Extension / plugin system
        __init__.py          # Re-exports: register_plot_type, plot_type decorator
        _hooks.py            # Hook definitions (pre/post render/export) and dispatch
        _plot_types.py       # Plot type registry (string-keyed dict of PlotFunction)
        _discovery.py        # Entry-point based plugin discovery

    contrib/                 # Built-in plot type wrappers
        __init__.py
        _matplotlib.py       # @plot_type("line"), @plot_type("scatter"), etc.
        _seaborn.py          # @plot_type("sns.lineplot"), etc. (lazy import)
```

---

## Core Dataclasses

All dataclasses use `@dataclass(frozen=True, kw_only=True, slots=True)` —
immutable, keyword-only, memory-efficient.  Type aliases use the Python 3.12
`type` keyword.

### Configuration (`config/_schema.py`) — Phase 1 ✓

| Class | Fields | Purpose |
|-------|--------|---------|
| `PathsConfig` | `output_dir`, `styles_dir`, `specs_dir`, `data_dir` (all `Path`, relative) | Directory layout |
| `ExportDefaults` | `formats`, `dpi`, `transparent`, `bbox_inches`, `pad_inches`, `metadata` | Default export settings |
| `StyleDefaults` | `base_style`, `font_family`, `font_size`, `figure_size` | Default style settings |
| `ProjectConfig` | `paths`, `export`, `style`, `registry_file` | Top-level project config |

### Specifications (`spec/`) — Phase 1 ✓

| Class | Fields | Purpose |
|-------|--------|---------|
| `FigureSpec` | `name`, `title`, `tags`, `group`, `panels`, `layout`, `style`, `export`, `metadata` | Full figure definition |
| `PanelSpec` | `name`, `plot_type`, `data`, `row`, `col`, `style`, `params`, `label` | One axes panel |
| `DataBinding` | `source`, `x`, `y`, `hue`, `transforms`, `params` | Data reference |

### Style (`style/_sheet.py`) — Phase 2 ✓

| Class | Fields | Purpose |
|-------|--------|---------|
| `StyleSheet` | `name`, `font_family`, `font_size`, `line_width`, `palette`, `figure_size`, `rc_overrides`, `extends` | Composable style unit |

### Layout (`layout/_grid.py`) — Phase 2 ✓

| Class | Fields | Purpose |
|-------|--------|---------|
| `LayoutSpec` | `rows`, `cols`, `width_ratios`, `height_ratios`, `wspace`, `hspace`, `constrained_layout` | Grid layout definition |
| `BuiltLayout` | `figure`, `axes` (dict[str, Axes]) | Realized matplotlib objects |

### Render (`render/_handle.py`) — Phase 3

| Class | Fields | Purpose |
|-------|--------|---------|
| `FigureHandle` | `spec`, `figure`, `layout`, `export_paths` | Lightweight render result; exposes `.show()`, `.path(fmt)`, `.close()` |

### Export (`export/_config.py`) — Phase 4

| Class | Fields | Purpose |
|-------|--------|---------|
| `ExportSpec` | `formats`, `dpi`, `transparent`, `filename_template`, `subdirectory` | Per-figure export overrides |
| `ResolvedExportConfig` | All fields non-optional | Fully resolved export settings |

---

## Key Design Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Data modeling | `dataclasses` (frozen, slotted) | No extra dependency; strict mypy; Python 3.12 features |
| Extensibility | Protocols, not ABC inheritance | Structural subtyping; any matching callable works |
| Config format | YAML with schema versions | Human-readable; forward-compatible; migration-safe |
| Style system | Custom `StyleSheet` → rcParams bridge | High-level abstractions + escape hatch to raw matplotlib |
| Style concurrency | Per-render `rc_context`, main-thread only | Avoids global rcParams races; `ProcessPool` for parallelism |
| Plot dispatch | String-keyed registry + `@plot_type` decorator | Simple, discoverable, extensible via entry points |
| Layout | Thin wrapper over `matplotlib.gridspec.GridSpec` | No reinvention; adds validation and declarative addressing |
| Layout extras | Composable post-build helpers (shared axes, colorbars, insets) | Keeps core builder small; opt-in complexity |
| Layout engine | `layout='constrained'` (not tight_layout) | Modern API, handles colorbars and complex grids |
| Export | Handler-per-format + filename sanitizer | Safe cross-platform filenames; collision strategies |
| Path resolution | Explicit override → env var → auto-discovery | Works in CI, notebooks, and interactive shells |
| Registry | YAML manifest with advisory file locking | Human-readable; concurrent-safe; version-controllable |
| Convenience API | `eikon.render()` + `FigureHandle` wrappers | Path-free declarative workflow; one-call rendering |
| CLI | Typer (already chosen) | Type-driven, auto-generated help |

---

## YAML Configuration Schemas

### Project configuration (`eikon.yaml`)

```yaml
config_version: 1                   # Schema version for forward compatibility

paths:
  output_dir: output/figures        # Relative to project root
  styles_dir: config/styles
  specs_dir: config/figure-specs
  data_dir: data/processed

export:
  formats: [pdf, svg]
  dpi: 300
  transparent: false
  metadata:
    author: "Author Name"
    project: "Project Title"

style:
  base_style: "seaborn-v0_8-paper"
  font_family: "sans-serif"
  font_size: 8.0
  figure_size: [7.0, 5.0]

registry_file: .eikon/registry.yaml
```

### Figure specification (`specs/fig1.yaml`)

```yaml
spec_version: 1                     # Schema version for forward compatibility
name: fig1-overview
title: "Overview of Results"
tags: [overview, neural, figure-1]
group: manuscript-1
panels:
  - name: A
    plot_type: line
    row: 0
    col: 0
    params:
      color: blue
    label: "(a)"
  - name: B
    plot_type: scatter
    row: 0
    col: 1
    data:
      source: results.csv
      x: time
      y: amplitude
    label: "(b)"
layout:
  rows: 1
  cols: 2
  width_ratios: [2, 1]
style: publication
export:
  formats: [pdf, svg, png]
  dpi: 600
```

### Style sheet (`styles/custom.yaml`)

```yaml
style_version: 1                    # Schema version for forward compatibility
name: custom-style
extends: [publication]              # Inherit from built-in preset
font_family: sans-serif
font_size: 9.0
line_width: 1.0
palette: ["#1b9e77", "#d95f02", "#7570b3"]
figure_size: [7.0, 4.5]
rc_overrides:                       # Escape hatch to raw rcParams
  axes.grid: true
  grid.alpha: 0.3
```

---

## CLI Commands

| Command | Phase | Description |
|---------|-------|-------------|
| `eikon info` | 1 ✓ | Version and platform diagnostics |
| `eikon init [path]` | 1 ✓ | Create `eikon.yaml` + directory structure |
| `eikon validate <path>` | 1 ✓ | Validate config or figure spec YAML |
| `eikon render <spec> [--format ...] [--show]` | 4 | Render and export one figure |
| `eikon batch [--tag ...] [--group ...]` | 6 | Batch render filtered figures |
| `eikon registry list\|add\|remove\|show` | 5 | Manage figure registry |

**Global option**: `--project-root <path>` — available on all commands,
overrides auto-discovery of the project root.  Also settable via the
`EIKON_PROJECT_ROOT` environment variable.

---

## Cross-Cutting Concerns

Several concerns span multiple subpackages.  Rather than scattering them
across phase descriptions, they are documented here as architectural
invariants.

### Project Root Resolution

The project root is resolved exactly once per run via a three-tier strategy
(explicit flag → `EIKON_PROJECT_ROOT` env var → upward walk for
`eikon.yaml`).  The resolved root is stored on `ResolvedPaths` and never
re-computed.  All subpackages that need paths receive them through
`ResolvedPaths`, never by calling the resolver themselves.  This prevents
cross-project bleed in notebooks, CI, and scripts that change directories.

### Schema Versioning and Migration

Every YAML schema carries a version field (`config_version`,
`spec_version`, `style_version`) defaulting to `1`.  The loaders
(`config/_loader.py`, `spec/_parse.py`, `style/_loader.py`) check the
version on load:

- **Same major version**: load normally.
- **Older minor version**: apply automatic migrations (field renames, default
  additions) and emit a deprecation warning.
- **Newer or incompatible version**: raise a descriptive error with a
  pointer to the migration guide.

This allows the YAML contracts to evolve without breaking existing projects.

### Concurrency and Thread Safety

matplotlib's `rcParams` are process-global mutable state.  Eikon mitigates
this:

1. **Style isolation**: Every render call wraps drawing in a
   `style_context()` that snapshots and restores `rcParams`.  No style
   state leaks between figures.
2. **Single-threaded rendering**: The pipeline runs on the main thread.
   Batch rendering is sequential by default.
3. **Process-based parallelism** (future): If parallel batch rendering is
   needed, each figure is rendered in a separate subprocess via
   `ProcessPoolExecutor`, giving each worker its own `rcParams` copy.
4. **Registry locking**: The YAML manifest uses advisory file locks
   (`_locking.py`) so concurrent processes can safely read/write the
   registry.

### Filename Safety

All export filenames pass through a deterministic sanitizer
(`export/_sanitize.py`) before reaching the filesystem.  The sanitizer:

- Strips path separators, null bytes, and control characters.
- Replaces characters illegal on Windows (`<>:"/\\|?*`) with underscores.
- Truncates to 200 characters (leaving room for extensions and suffixes).
- Handles collision via a configurable strategy (`overwrite` / `increment` /
  `fail`).

---

## Development Phases

### Phase 1: Foundation — Config + Specs + Exceptions ✓

**Status**: Complete.

**Delivered**:
- `_types.py` — `ExportFormat`, `Tag`, `DPI`, `StyleRef`
- `exceptions.py` — 14 exception classes in a typed hierarchy
- `config/` — `ProjectConfig`, `PathsConfig`, `ExportDefaults`, `StyleDefaults`,
  YAML loader, deep merging, project root discovery, path resolution, validation
- `spec/` — `FigureSpec`, `PanelSpec`, `DataBinding`, YAML parser, override logic
- CLI `init` + `validate` commands
- 68 tests, mypy strict clean, ruff clean

**Milestone**: `eikon init` creates a project.  `eikon validate` checks YAML
files.  Python API constructs and validates specs.

---

### Phase 2: Style System + Layout Engine ✓

**Status**: Complete.

**Goal**: Users can define composable styles and multi-panel layouts.  Layouts
produce real `matplotlib.figure.Figure` + `Axes` objects.

#### Style subpackage (`style/`)

| Module | Responsibility | Key types / functions |
|--------|---------------|----------------------|
| `_sheet.py` | `StyleSheet` dataclass | `StyleSheet(name, font_family, font_size, line_width, palette, figure_size, rc_overrides, extends)` |
| `_composer.py` | Merge/flatten style chains | `compose_styles(*sheets) → StyleSheet`, `resolve_style_chain(sheet, registry) → StyleSheet` |
| `_rcparams.py` | Bridge to matplotlib | `to_rcparams(sheet) → dict`, `style_context(sheet) → ContextManager` |
| `_presets.py` | Built-in presets | `PRESETS: dict[str, StyleSheet]` with `publication`, `presentation`, `poster` |
| `_loader.py` | Load from any `StyleRef` | `load_style(ref, search_dirs) → StyleSheet` — resolves preset names, matplotlib styles, `.mplstyle` files, YAML files |

**Style composition**: Styles list parent names in `extends`.  The composer
resolves the chain depth-first, then overlays the leaf's fields.  Conflicts are
resolved right-most-wins.  `rc_overrides` dicts are deep-merged.

**rcParams mapping**:

| `StyleSheet` field | matplotlib `rcParams` key(s) |
|--------------------|------------------------------|
| `font_family` | `font.family` |
| `font_size` | `font.size` |
| `line_width` | `lines.linewidth` |
| `palette` | `axes.prop_cycle` (via `cycler`) |
| `figure_size` | `figure.figsize` |
| `rc_overrides` | Direct merge into rcParams dict |

**Context manager**: `style_context(sheet)` uses `matplotlib.rc_context` to
temporarily apply the computed rcParams, reverting on exit.

**Thread safety and re-entrancy**: matplotlib `rcParams` are global mutable
state, making concurrent style application unsafe across threads.  The
design addresses this at two levels:

- **Nesting**: `style_context` is fully re-entrant — nested contexts
  restore the correct outer state on exit, even when an exception is raised.
  This is guaranteed by `matplotlib.rc_context`'s stack-based design.
- **Concurrency**: During batch rendering (Phase 6), each figure is rendered
  inside its own `style_context` on the **main thread**.  The pipeline
  orchestrator (`render/_pipeline.py`) must never apply styles outside a
  context manager.  If future parallelism is needed (e.g. `ProcessPool`),
  each worker process gets an independent `rcParams` copy — documented in
  the rendering pipeline's docstring.
- **Guard**: `style_context` captures a snapshot of the keys it modifies on
  entry and asserts they are restored on exit (debug-mode check), catching
  accidental leakage from plot functions that mutate `rcParams` directly.

#### Layout subpackage (`layout/`)

| Module | Responsibility | Key types / functions |
|--------|---------------|----------------------|
| `_grid.py` | `LayoutSpec` dataclass | `LayoutSpec(rows, cols, width_ratios, height_ratios, wspace, hspace, constrained_layout)` |
| `_placement.py` | Panel position resolution | `PanelPlacement(panel_name, row_slice, col_slice)`, `resolve_placements(panels, layout) → tuple[PanelPlacement, ...]` |
| `_constraints.py` | Validation | `validate_layout(panels, layout) → list[str]` — checks bounds, detects overlaps |
| `_builder.py` | Build Figure + Axes | `BuiltLayout(figure, axes)`, `build_layout(layout, panels, figure_size, dpi) → BuiltLayout` |

**Panel addressing**: `PanelSpec.row` and `PanelSpec.col` accept either a
single `int` (one cell) or a `tuple[int, int]` (span from start to end,
exclusive).  The placement resolver converts these to `slice` objects used for
`GridSpec` subscripting.

**Overlap detection**: After resolving placements, `validate_layout` checks
that no two panels occupy intersecting grid cells.  If they do, it raises
`PanelOverlapError`.

**Builder**: `build_layout` creates a `matplotlib.figure.Figure` with
`layout='constrained'` (or `'none'` if `constrained_layout=False`), attaches a
`GridSpec` via `fig.add_gridspec(...)`, and creates one `Axes` per panel via
`fig.add_subplot(gs[row_slice, col_slice])`.  Returns `BuiltLayout` with a
`dict[str, Axes]` mapping panel names to their axes.

#### Extended layout features

The base `_grid.py` + `_builder.py` handle the common case (rectangular grid
of independent panels).  Three additional modules keep `_builder.py` small
while covering complex scientific figures:

| Module | Responsibility |
|--------|---------------|
| `_shared_axes.py` | `link_axes(built, groups, axis)` — create shared-x/y axis groups across named panels after build (thin wrapper around `ax.sharex/sharey`) |
| `_colorbars.py` | `add_colorbar(built, panel_name, mappable, *, position, size, pad)` — attach a colorbar to a panel using `fig.colorbar` with `constrained_layout`-compatible anchoring |
| `_insets.py` | `add_inset(built, parent_panel, name, bounds)` — create an inset axes via `ax.inset_axes(bounds)` and register it in the `BuiltLayout.axes` dict |

These are **opt-in composable helpers** called after `build_layout`, not
entangled with the builder itself.  This keeps the core layout path simple
while covering colorbars, shared axes, and inset panels — the three most
common complex-figure needs.

**Autosizing hook**: `PanelSpec` accepts an optional `auto_size: bool`
field (default `False`).  When `True`, `_builder.py` defers the figure size
to matplotlib's constrained-layout solver rather than using the explicit
`figure_size`.  This allows the engine to compute a size that avoids label
clipping, useful for figures with many tick labels or long axis titles.

**Milestone**: Given a `FigureSpec` with layout and style, `build_layout()`
produces a matplotlib `Figure` with correctly positioned `Axes`.  Shared
axes, colorbars, and insets are composable post-build.  Styles apply via
context manager.

---

### Phase 3: Rendering Pipeline + Built-in Plot Types

**Goal**: End-to-end rendering from spec to displayed matplotlib figure.

#### Render subpackage (`render/`)

| Module | Responsibility |
|--------|---------------|
| `_protocols.py` | `PlotFunction`, `FigurePostProcessor`, `DataTransform` protocols |
| `_context.py` | `RenderContext` — mutable state holding spec, config, built layout, resolved style |
| `_pipeline.py` | `render_figure(spec, config, *, show, export) → FigureHandle` — the orchestrator |
| `_drawing.py` | `draw_panel(ax, panel, plot_registry) → None` — dispatches to registered plot function |
| `_handle.py` | `FigureHandle` — lightweight result wrapper (see below) |

**Pipeline decomposition** (inside `render_figure`):

1. `_resolve_config(config)` → `ProjectConfig`
2. `_resolve_style(spec, config)` → `StyleSheet`
3. `_build(spec, style, config)` → `BuiltLayout`
4. `_draw_panels(ctx)` → side-effects on axes
5. `_post_process(ctx)` → apply titles, labels
6. `_export(ctx)` → write files (delegated to export subpackage)

Each step is a small function (~10–30 lines) with a clear contract.

**`FigureHandle`**: The return value of `render_figure()` and the
convenience function `eikon.render()`.  It wraps the rendering result
without exposing raw paths or matplotlib internals unless the user wants
them:

```python
handle = eikon.render("fig1-overview", formats=["pdf", "svg"])
handle.show()                    # display interactively
handle.path("pdf")               # → Path to the exported PDF
handle.figure                    # → matplotlib Figure
handle.spec                      # → FigureSpec used
handle.close()                   # close the matplotlib Figure
```

**Convenience API** (in `eikon.__init__`):

| Function | Signature | Purpose |
|----------|-----------|---------|
| `eikon.render()` | `(name_or_spec, *, config, formats, overrides, show) → FigureHandle` | One-call render by name (registry lookup) or by `FigureSpec` / YAML path, with optional per-call overrides |
| `eikon.load_registry()` | `(*, config) → Registry` | Load the project registry using auto-discovered config |

These are thin wrappers composing config loading, registry lookup, and the
render pipeline — they do not add logic, just reduce boilerplate.

#### Extension subpackage (`ext/`)

| Module | Responsibility |
|--------|---------------|
| `_plot_types.py` | `register_plot_type(name, fn)`, `get_plot_type(name)`, `@plot_type("name")` decorator |
| `_discovery.py` | `discover_plugins(group)` — loads entry points from `eikon.plot_types` group |
| `_hooks.py` | `HookName` enum, `register_hook(hook, fn)`, `fire_hook(hook, **kwargs)` |

#### Contrib subpackage (`contrib/`)

| Module | Plot types registered |
|--------|---------------------|
| `_matplotlib.py` | `line`, `scatter`, `bar`, `barh`, `hist`, `heatmap`, `contour`, `errorbar` |
| `_seaborn.py` | `sns.lineplot`, `sns.scatterplot`, `sns.heatmap`, `sns.boxplot`, `sns.violinplot` (lazy import) |

**Milestone**: `eikon.render("fig-name")` renders a complete multi-panel
figure and returns a `FigureHandle`.  Users register custom plot types with
`@plot_type("name")`.  The convenience API (`eikon.render()`,
`eikon.load_registry()`) is functional.

---

### Phase 4: Export Pipeline

**Goal**: Figures export to PDF, SVG, PNG with metadata and configurable paths.

#### Export subpackage (`export/`)

| Module | Responsibility |
|--------|---------------|
| `_config.py` | `ExportSpec`, `ResolvedExportConfig` dataclasses, `resolve_export_config()` |
| `_handlers.py` | `PdfHandler`, `SvgHandler`, `PngHandler` — each wraps `fig.savefig()` with format-specific options |
| `_metadata.py` | `inject_pdf_metadata(path, metadata)`, `inject_png_metadata(path, metadata)` |
| `_paths.py` | `build_export_path(spec, fmt, config, output_dir) → Path` — template variables: `{name}`, `{group}`, `{date}`, `{format}` |
| `_sanitize.py` | `sanitize_filename(name) → str` — deterministic sanitizer (strip/replace unsafe chars, enforce length limits, cross-platform safe) |
| `_batch.py` | `batch_export(specs, config) → list[ExportResult]` |

**Filename collision handling**: When `build_export_path` produces a path
that already exists, the behavior is controlled by a `collision` parameter
on `ExportSpec`:

- `"overwrite"` (default) — silently overwrite the existing file.
- `"increment"` — append a numeric suffix (`_1`, `_2`, …) to avoid
  collision.
- `"fail"` — raise `ExportError` immediately.

All filenames pass through `sanitize_filename()` before reaching the
filesystem — this strips path separators, null bytes, and characters illegal
on Windows/macOS, and truncates to a safe length.

**CLI addition**: `eikon render <spec> [--format pdf svg] [--output dir] [--show]`

**Milestone**: `eikon render specs/fig1.yaml --format pdf svg` produces
publication-quality exports with safe, deterministic filenames.

---

### Phase 5: Figure Registry

**Goal**: Track and organize figures across analyses with persistent state.

#### Registry subpackage (`registry/`)

| Module | Responsibility |
|--------|---------------|
| `_registry.py` | `Registry` class — `register(spec)`, `get(name)`, `list_all()`, `query(tags, group)`, `remove(name)`, `save()`, `load()` |
| `_index.py` | YAML manifest I/O (`eikon-registry.yaml`) |
| `_query.py` | Filter logic for tags and groups |
| `_locking.py` | File-based advisory locking for concurrent access to the manifest |

**Concurrency safety**: The registry manifest is a shared file that may be
written concurrently during batch rendering or parallel CI jobs.
`_locking.py` provides a `registry_lock(path)` context manager using
`fcntl.flock` (Unix) / `msvcrt.locking` (Windows) advisory locks.  All
`save()` and `load()` operations acquire the lock to prevent partial reads
or lost writes.  If the lock cannot be acquired within a configurable
timeout (default 5 s), a `RegistryError` is raised with a clear message.

**Name collision**: `register(spec)` checks for duplicate names.  If a
figure with the same name already exists, the behavior is controlled by
`on_conflict`:

- `"update"` (default) — replace the existing entry.
- `"fail"` — raise `RegistryError`.
- `"skip"` — silently keep the existing entry.

**CLI addition**: `eikon registry list|add|remove|show [--tag ...] [--group ...]`

**Milestone**: `eikon registry list --tag neural` filters figures.  Registry
persists across sessions in a version-controllable YAML manifest with safe
concurrent access.

---

### Phase 6: Batch Operations + CLI Polish

**Goal**: Full batch workflow with progress reporting and lifecycle hooks.

**Deliverables**:
- `eikon batch [--tag ...] [--group ...]` with Rich progress bars
- Hook system: `pre_render`, `post_render`, `pre_export`, `post_export`
- Error reporting improvements (Rich-formatted validation summaries)
- `eikon init` generates a complete template with example spec

**Milestone**: `eikon batch --tag manuscript-1` renders and exports all tagged
figures.  Hooks allow custom post-processing (e.g., watermarking, metadata
injection).

---

### Phase 7: Documentation + Hardening

**Goal**: Comprehensive documentation and production readiness.

**Deliverables**:
- `docs/guide/` — Getting started, configuration, styles, layouts, export, registry
- `docs/api/` — Auto-generated API reference (Sphinx + autodoc)
- `docs/adr/` — Architecture Decision Records for key choices
- 100% mypy strict type coverage
- Test coverage >= 90%
- Version bump to 0.1.0

**Milestone**: Documentation site builds.  All CI checks pass.  Package is
installable and functional end-to-end.

---

## Test Strategy

Tests mirror the source structure: `tests/test_eikon/test_<subpackage>/` for
each subpackage, with one test file per source module.

| Phase | Test files | Focus |
|-------|-----------|-------|
| 1 ✓ | `test_types.py`, `test_exceptions.py`, `test_config/`, `test_spec/`, `test_cli.py` | Dataclass construction, validation, YAML loading, CLI commands |
| 2 ✓ | `test_style/`, `test_layout/` | Style composition, rcParams conversion, thread-safety guards, grid placement, overlap detection, Figure+Axes building, shared axes / colorbars / insets |
| 3 | `test_render/`, `test_ext/` | Pipeline integration, plot type registry, drawing dispatch, `FigureHandle`, convenience API |
| 4 | `test_export/` | Format handlers, path construction, filename sanitization, collision strategies, batch export |
| 5 | `test_registry/` | CRUD, persistence, querying, concurrent locking, name collision |
| 6 | `test_cli.py` (extended) | Batch command, hook dispatch, `--project-root` flag |

## Verification (after every phase)

```bash
source ~/miniconda3/etc/profile.d/conda.sh && conda activate eikon
python -m pytest tests/ -v           # All tests pass
mypy src/eikon/ --strict             # No type errors
ruff check src/eikon/                # No lint errors
```
