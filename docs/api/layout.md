<a id="layout"></a>

# Layout

Grid layout, panel placement, validation, shared axes, colorbars, and insets.

<a id="module-eikon.layout._grid"></a>

<a id="layout-grid"></a>

## Layout Grid

Grid layout specification dataclass.

A [`LayoutSpec`](#eikon.layout._grid.LayoutSpec) declaratively describes the grid structure of a
multi-panel figure: number of rows/columns, size ratios, and spacing.

<a id="eikon.layout._grid.LayoutSpec"></a>

### *class* eikon.layout._grid.LayoutSpec(\*, rows=1, cols=1, width_ratios=None, height_ratios=None, wspace=None, hspace=None, constrained_layout=True)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Declarative specification for a figure’s grid layout.

<a id="eikon.layout._grid.LayoutSpec.rows"></a>

#### rows *: [int](https://docs.python.org/3/library/functions.html#int)*

Number of grid rows (>= 1).

<a id="eikon.layout._grid.LayoutSpec.cols"></a>

#### cols *: [int](https://docs.python.org/3/library/functions.html#int)*

Number of grid columns (>= 1).

<a id="eikon.layout._grid.LayoutSpec.width_ratios"></a>

#### width_ratios *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[float](https://docs.python.org/3/library/functions.html#float), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Relative column widths.  Length must equal `cols` when set.

<a id="eikon.layout._grid.LayoutSpec.height_ratios"></a>

#### height_ratios *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[float](https://docs.python.org/3/library/functions.html#float), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Relative row heights.  Length must equal `rows` when set.

<a id="eikon.layout._grid.LayoutSpec.wspace"></a>

#### wspace *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Horizontal spacing between panels (fraction of average axis width).

<a id="eikon.layout._grid.LayoutSpec.hspace"></a>

#### hspace *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Vertical spacing between panels (fraction of average axis height).

<a id="eikon.layout._grid.LayoutSpec.constrained_layout"></a>

#### constrained_layout *: [bool](https://docs.python.org/3/library/functions.html#bool)*

Whether to use matplotlib’s constrained layout engine.

<a id="module-eikon.layout._placement"></a>

<a id="panel-placement"></a>

## Panel Placement

Resolve panel positions to grid slices.

Converts the `row` / `col` fields of `PanelSpec` (which accept
either a single `int` or a `(start, end)` tuple) into `slice` objects
suitable for subscripting a matplotlib `GridSpec`.

<a id="eikon.layout._placement.PanelPlacement"></a>

### *class* eikon.layout._placement.PanelPlacement(\*, panel_name, row_slice, col_slice)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Resolved position of a panel within the grid.

<a id="eikon.layout._placement.PanelPlacement.panel_name"></a>

#### panel_name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Name of the panel this placement belongs to.

<a id="eikon.layout._placement.PanelPlacement.row_slice"></a>

#### row_slice *: [slice](https://docs.python.org/3/library/functions.html#slice)*

Row span as a `slice` for `GridSpec` subscripting.

<a id="eikon.layout._placement.PanelPlacement.col_slice"></a>

#### col_slice *: [slice](https://docs.python.org/3/library/functions.html#slice)*

Column span as a `slice` for `GridSpec` subscripting.

<a id="eikon.layout._placement.resolve_placements"></a>

### eikon.layout._placement.resolve_placements(panels, layout)

Convert panel row/col fields to grid slice placements.

* **Parameters:**
  * **panels** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*PanelSpec*](spec.md#eikon.spec._panel.PanelSpec) *,*  *...* *]*) – Panel specifications with `row` and `col` fields.
  * **layout** ([*LayoutSpec*](#eikon.layout._grid.LayoutSpec)) – The grid layout to place panels within.
* **Returns:**
  One placement per panel, in the same order.
* **Return type:**
  [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[PanelPlacement](#eikon.layout._placement.PanelPlacement), …]

<a id="module-eikon.layout._builder"></a>

<a id="layout-building"></a>

## Layout Building

Build a matplotlib Figure with positioned Axes from layout specs.

The builder is the final step of the layout pipeline: it takes a
validated `LayoutSpec` and resolved `PanelPlacement` objects
and produces a real `matplotlib.figure.Figure` with one `Axes` per
panel.

<a id="eikon.layout._builder.BuiltLayout"></a>

### *class* eikon.layout._builder.BuiltLayout(\*, figure, axes, grid_spec)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Result of building a layout: a Figure and its named Axes.

<a id="eikon.layout._builder.BuiltLayout.figure"></a>

#### figure *: Figure*

The matplotlib Figure object.

<a id="eikon.layout._builder.BuiltLayout.axes"></a>

#### axes *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Mapping from panel names to their Axes objects.

<a id="eikon.layout._builder.BuiltLayout.grid_spec"></a>

#### grid_spec *: [Any](https://docs.python.org/3/library/typing.html#typing.Any)*

<a id="eikon.layout._builder.build_layout"></a>

### eikon.layout._builder.build_layout(layout, placements, \*, figure_size=(6.4, 4.8), dpi=100)

Create a matplotlib Figure with positioned Axes.

* **Parameters:**
  * **layout** ([*LayoutSpec*](#eikon.layout._grid.LayoutSpec)) – Grid layout specification.
  * **placements** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*PanelPlacement*](#eikon.layout._placement.PanelPlacement) *,*  *...* *]*) – Resolved panel placements (from `resolve_placements()`).
  * **figure_size** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*float*](https://docs.python.org/3/library/functions.html#float) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *]*) – Figure dimensions `(width, height)` in inches.
  * **dpi** ([*int*](https://docs.python.org/3/library/functions.html#int) *|* [*float*](https://docs.python.org/3/library/functions.html#float)) – Resolution in dots per inch.
* **Returns:**
  The Figure and a `dict[str, Axes]` mapping panel names.
* **Return type:**
  [BuiltLayout](#eikon.layout._builder.BuiltLayout)

<a id="module-eikon.layout._constraints"></a>

<a id="layout-constraints"></a>

## Layout Constraints

Layout validation — bounds checking and overlap detection.

Validates that panel placements fit within the grid and that no two
panels occupy intersecting cells.

<a id="eikon.layout._constraints.validate_layout"></a>

### eikon.layout._constraints.validate_layout(placements, layout)

Validate layout constraints and return a list of error messages.

Checks performed:

1. Grid dimensions are positive.
2. Ratio lengths match grid dimensions (when provided).
3. Panels occupy at least one cell.
4. No two panels overlap.

* **Parameters:**
  * **placements** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*PanelPlacement*](#eikon.layout._placement.PanelPlacement) *,*  *...* *]*) – Resolved panel placements.
  * **layout** ([*LayoutSpec*](#eikon.layout._grid.LayoutSpec)) – The grid layout specification.
* **Returns:**
  Validation error messages (empty if valid).
* **Return type:**
  [list](https://docs.python.org/3/library/stdtypes.html#list)[[str](https://docs.python.org/3/library/stdtypes.html#str)]
* **Raises:**
  [**PanelOverlapError**](types.md#eikon.exceptions.PanelOverlapError) – If two panels occupy intersecting grid cells.

<a id="module-eikon.layout._shared_axes"></a>

<a id="shared-axes"></a>

## Shared Axes

Shared-axis linking across panels.

Provides a helper to create shared-x or shared-y axis groups across
named panels after layout build.  This is a thin wrapper around
matplotlib’s `Axes.sharex` / `Axes.sharey`.

<a id="eikon.layout._shared_axes.link_axes"></a>

### eikon.layout._shared_axes.link_axes(built, groups, axis='both')

Link axes across panels so they share scales.

Within each group, the first panel becomes the reference and all
subsequent panels share its x-axis, y-axis, or both.

* **Parameters:**
  * **built** ([*BuiltLayout*](#eikon.layout._builder.BuiltLayout)) – A built layout containing the axes dict.
  * **groups** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,*  *...* *]* *,*  *...* *]*) – Groups of panel names to link.  Each inner tuple is one group.
  * **axis** (`"x"` | `"y"` | `"both"`) – Which axis to share.
* **Raises:**
  [**LayoutError**](types.md#eikon.exceptions.LayoutError) – If a panel name is not found in the built layout.

<a id="module-eikon.layout._colorbars"></a>

<a id="colorbars"></a>

## Colorbars

Colorbar attachment for layout panels.

Provides a constrained-layout-aware helper to attach a colorbar to a
specific panel in a built layout.

<a id="eikon.layout._colorbars.add_colorbar"></a>

### eikon.layout._colorbars.add_colorbar(built, panel_name, mappable, \*, position='right', size='5%', pad=0.05, \*\*kwargs)

Attach a colorbar to a panel in the built layout.

Uses `fig.colorbar` which is compatible with constrained layout.

* **Parameters:**
  * **built** ([*BuiltLayout*](#eikon.layout._builder.BuiltLayout)) – A built layout containing the figure and axes dict.
  * **panel_name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the panel to attach the colorbar to.
  * **mappable** (*ScalarMappable*) – The matplotlib mappable (e.g. `AxesImage`) to draw the colorbar for.
  * **position** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Location: `"right"`, `"left"`, `"top"`, or `"bottom"`.
  * **size** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Colorbar width as a percentage string (e.g. `"5%"`).
  * **pad** ([*float*](https://docs.python.org/3/library/functions.html#float)) – Padding between the axes and colorbar.
  * **\*\*kwargs** (*Any*) – Additional keyword arguments passed to `fig.colorbar`.
* **Returns:**
  The created matplotlib colorbar.
* **Return type:**
  Colorbar
* **Raises:**
  [**LayoutError**](types.md#eikon.exceptions.LayoutError) – If *panel_name* is not found in the built layout.

<a id="module-eikon.layout._insets"></a>

<a id="insets"></a>

## Insets

Inset axes creation and registration.

Provides a helper to create an inset axes within an existing panel and
register it in the `BuiltLayout.axes` dict for downstream use.

<a id="eikon.layout._insets.add_inset"></a>

### eikon.layout._insets.add_inset(built, parent_panel, name, bounds)

Create an inset axes and register it in the layout.

* **Parameters:**
  * **built** ([*BuiltLayout*](#eikon.layout._builder.BuiltLayout)) – A built layout containing the figure and axes dict.
  * **parent_panel** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name of the panel to create the inset within.
  * **name** ([*str*](https://docs.python.org/3/library/stdtypes.html#str)) – Name for the new inset axes.
  * **bounds** ([*tuple*](https://docs.python.org/3/library/stdtypes.html#tuple) *[*[*float*](https://docs.python.org/3/library/functions.html#float) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *,* [*float*](https://docs.python.org/3/library/functions.html#float) *]*) – `(x, y, width, height)` in axes-relative coordinates (0–1).
* **Returns:**
  A new `BuiltLayout` with the inset axes added to the `axes` dict.
* **Return type:**
  [BuiltLayout](#eikon.layout._builder.BuiltLayout)
* **Raises:**
  [**LayoutError**](types.md#eikon.exceptions.LayoutError) – If *parent_panel* is not found or *name* already exists.
