<a id="specifications"></a>

# Specifications

Declarative figure, panel, data, margin-label, override, and parsing APIs.

<a id="module-eikon.spec._figure"></a>

<a id="figure-specifications"></a>

## Figure Specifications

Figure specification — the central declarative abstraction.

A [`FigureSpec`](#eikon.spec._figure.FigureSpec) fully describes a figure: its panels, layout,
style, export settings, and organizational metadata.

<a id="eikon.spec._figure.FigureSpec"></a>

### *class* eikon.spec._figure.FigureSpec(\*, name, title='', tags=(), group='', panels=(), layout=None, style=None, export=None, title_kwargs=None, shared_legend=None, margin_labels=None, metadata=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Declarative specification for a single figure.

<a id="eikon.spec._figure.FigureSpec.name"></a>

#### name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Unique identifier for this figure within the project.

<a id="eikon.spec._figure.FigureSpec.title"></a>

#### title *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Display title rendered on the figure.

<a id="eikon.spec._figure.FigureSpec.tags"></a>

#### tags *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[Tag, ...]*

Organizational tags for filtering and grouping.

<a id="eikon.spec._figure.FigureSpec.group"></a>

#### group *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Grouping key (e.g. `"manuscript-1"`).

<a id="eikon.spec._figure.FigureSpec.panels"></a>

#### panels *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[PanelSpec](#eikon.spec._panel.PanelSpec), ...]*

Ordered panel definitions composing this figure.

<a id="eikon.spec._figure.FigureSpec.layout"></a>

#### layout *: [LayoutSpec](layout.md#eikon.layout._grid.LayoutSpec) | [None](https://docs.python.org/3/library/constants.html#None)*

Layout specification (rows, cols, ratios). `None` implies a
single-panel figure.

<a id="eikon.spec._figure.FigureSpec.style"></a>

#### style *: StyleRef | [None](https://docs.python.org/3/library/constants.html#None)*

Figure-level style override.

<a id="eikon.spec._figure.FigureSpec.export"></a>

#### export *: [ExportSpec](export.md#eikon.export._config.ExportSpec) | [None](https://docs.python.org/3/library/constants.html#None)*

Per-figure export settings override.

<a id="eikon.spec._figure.FigureSpec.title_kwargs"></a>

#### title_kwargs *: [TitleConfig](#eikon.spec._figure.TitleConfig) | [None](https://docs.python.org/3/library/constants.html#None)*

Extra keyword arguments forwarded to
`matplotlib.figure.Figure.suptitle()`.  `None` uses
matplotlib defaults.

<a id="eikon.spec._figure.FigureSpec.shared_legend"></a>

#### shared_legend *: [SharedLegendConfig](#eikon.spec._figure.SharedLegendConfig) | [None](https://docs.python.org/3/library/constants.html#None)*

If set, collect legend handles from the first panel that has them
and render a single figure-level legend.

<a id="eikon.spec._figure.FigureSpec.margin_labels"></a>

#### margin_labels *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [MarginLabelSpec](#eikon.spec._margin_labels.MarginLabelSpec)] | [None](https://docs.python.org/3/library/constants.html#None)*

Edge labels for annotating rows or columns.  Keys are edge
names (`"top"`, `"bottom"`, `"left"`, `"right"`).

<a id="eikon.spec._figure.FigureSpec.metadata"></a>

#### metadata *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [str](https://docs.python.org/3/library/stdtypes.html#str)]*

Arbitrary metadata fields (e.g. author, project).

<a id="eikon.spec._figure.TitleConfig"></a>

### *class* eikon.spec._figure.TitleConfig(\*, fontsize=None, fontweight=None, y=None, x=None, ha=None, extra=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Keyword arguments forwarded to `matplotlib.figure.Figure.suptitle()`.

<a id="eikon.spec._figure.TitleConfig.fontsize"></a>

#### fontsize *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Font size in points.

<a id="eikon.spec._figure.TitleConfig.fontweight"></a>

#### fontweight *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Font weight (e.g. `"bold"`).

<a id="eikon.spec._figure.TitleConfig.y"></a>

#### y *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Vertical position in figure coordinates.

<a id="eikon.spec._figure.TitleConfig.x"></a>

#### x *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Horizontal position in figure coordinates.

<a id="eikon.spec._figure.TitleConfig.ha"></a>

#### ha *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Horizontal alignment.

<a id="eikon.spec._figure.TitleConfig.extra"></a>

#### extra *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Additional keyword arguments forwarded verbatim.

<a id="eikon.spec._figure.TitleConfig.to_kwargs"></a>

#### to_kwargs()

Return a dict suitable for `fig.suptitle(**kwargs)`.

<a id="eikon.spec._figure.SharedLegendConfig"></a>

### *class* eikon.spec._figure.SharedLegendConfig(\*, loc=None, ncol=None, fontsize=None, frameon=None, extra=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Configuration for a shared figure-level legend.

<a id="eikon.spec._figure.SharedLegendConfig.loc"></a>

#### loc *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Legend location (e.g. `"upper right"`).

<a id="eikon.spec._figure.SharedLegendConfig.ncol"></a>

#### ncol *: [int](https://docs.python.org/3/library/functions.html#int) | [None](https://docs.python.org/3/library/constants.html#None)*

Number of legend columns.

<a id="eikon.spec._figure.SharedLegendConfig.fontsize"></a>

#### fontsize *: [float](https://docs.python.org/3/library/functions.html#float) | [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Font size for legend text.

<a id="eikon.spec._figure.SharedLegendConfig.frameon"></a>

#### frameon *: [bool](https://docs.python.org/3/library/functions.html#bool) | [None](https://docs.python.org/3/library/constants.html#None)*

Whether to draw the legend frame.

<a id="eikon.spec._figure.SharedLegendConfig.extra"></a>

#### extra *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Additional keyword arguments forwarded verbatim.

<a id="eikon.spec._figure.SharedLegendConfig.to_kwargs"></a>

#### to_kwargs()

Return a dict suitable for `fig.legend(**kwargs)`.

<a id="module-eikon.spec._panel"></a>

<a id="panel-specifications"></a>

## Panel Specifications

Panel specification for a single axes region within a figure.

A [`PanelSpec`](#eikon.spec._panel.PanelSpec) describes one axes panel: its plot type, position
in the grid layout, data binding, and per-panel style overrides.

<a id="eikon.spec._panel.PanelSpec"></a>

### *class* eikon.spec._panel.PanelSpec(\*, name, plot_type, data=None, row=0, col=0, style=None, params=<factory>, label='', auto_size=False, hide_spines=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Specification for one axes panel within a figure.

<a id="eikon.spec._panel.PanelSpec.name"></a>

#### name *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Panel identifier (e.g. `"A"`, `"top-left"`).

<a id="eikon.spec._panel.PanelSpec.plot_type"></a>

#### plot_type *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Registry key for the plot function to invoke.

<a id="eikon.spec._panel.PanelSpec.data"></a>

#### data *: [DataBinding](#eikon.spec._data.DataBinding) | [None](https://docs.python.org/3/library/constants.html#None)*

Data source reference. `None` if data is passed via `params`.

<a id="eikon.spec._panel.PanelSpec.row"></a>

#### row *: [int](https://docs.python.org/3/library/functions.html#int) | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int), [int](https://docs.python.org/3/library/functions.html#int)]*

Row index (zero-based) or `(start, end)` span in the grid.

<a id="eikon.spec._panel.PanelSpec.col"></a>

#### col *: [int](https://docs.python.org/3/library/functions.html#int) | [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int), [int](https://docs.python.org/3/library/functions.html#int)]*

Column index (zero-based) or `(start, end)` span in the grid.

<a id="eikon.spec._panel.PanelSpec.style"></a>

#### style *: StyleRef | [None](https://docs.python.org/3/library/constants.html#None)*

Per-panel style override.

<a id="eikon.spec._panel.PanelSpec.params"></a>

#### params *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Keyword arguments forwarded to the plot function.

<a id="eikon.spec._panel.PanelSpec.label"></a>

#### label *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Panel label rendered on the axes (e.g. `"(a)"`, `"(b)"`).

<a id="eikon.spec._panel.PanelSpec.auto_size"></a>

#### auto_size *: [bool](https://docs.python.org/3/library/functions.html#bool)*

When `True`, defer figure size to the constrained-layout solver
rather than using the explicit `figure_size`.

<a id="eikon.spec._panel.PanelSpec.hide_spines"></a>

#### hide_spines *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Spine names to hide on this panel’s axes.  Common values are
`("top", "right")` for a cleaner look.  Valid names:
`"top"`, `"bottom"`, `"left"`, `"right"`.
`None` (default) keeps all spines visible.

<a id="module-eikon.spec._data"></a>

<a id="data-bindings"></a>

## Data Bindings

Data binding specification for figure panels.

A [`DataBinding`](#eikon.spec._data.DataBinding) describes how data is sourced and prepared
before being passed to a plot function.

<a id="eikon.spec._data.DataBinding"></a>

### *class* eikon.spec._data.DataBinding(\*, source='', x='', y='', hue='', transforms=(), params=<factory>)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Reference to data for a panel.

<a id="eikon.spec._data.DataBinding.source"></a>

#### source *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [Path](https://docs.python.org/3/library/pathlib.html#pathlib.Path)*

Path to a data file or a named data source identifier.

<a id="eikon.spec._data.DataBinding.x"></a>

#### x *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Column or field name for the x-axis variable.

<a id="eikon.spec._data.DataBinding.y"></a>

#### y *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Column or field name for the y-axis variable.

<a id="eikon.spec._data.DataBinding.hue"></a>

#### hue *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Grouping variable name for color coding.

<a id="eikon.spec._data.DataBinding.transforms"></a>

#### transforms *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...]*

Named transforms to apply in order before plotting.

<a id="eikon.spec._data.DataBinding.params"></a>

#### params *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Additional parameters passed to data loading or transforms.

<a id="module-eikon.spec._margin_labels"></a>

<a id="margin-labels"></a>

## Margin Labels

Margin label specification dataclasses.

Declarative types for figure-edge labels that annotate rows or columns
of a panel grid (or a virtual inset grid within a single panel).

<a id="eikon.spec._margin_labels.MarginLabelSpec"></a>

### *class* eikon.spec._margin_labels.MarginLabelSpec(\*, labels, style=MarginLabelStyle(bg_color=None, text_color='black', fontsize=8.0, fontweight='normal', rotation=None), level_styles=None, target=MarginTarget(kind='layout', axes=None, grid=None), strip_size=0.04, pad=6.0, gap=2.0, zorder=2.1, label_styles=None, cell_range=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Specification for labels on one edge of the figure.

<a id="eikon.spec._margin_labels.MarginLabelSpec.labels"></a>

#### labels *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[str](https://docs.python.org/3/library/stdtypes.html#str), ...] | [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [Any](https://docs.python.org/3/library/typing.html#typing.Any)]*

Label content.  A flat tuple gives one label per grid cell.
A nested dict expresses hierarchy — keys are group labels,
values are sub-dicts (recursive) or `None` / tuples of
leaf labels.

<a id="eikon.spec._margin_labels.MarginLabelSpec.style"></a>

#### style *: [MarginLabelStyle](#eikon.spec._margin_labels.MarginLabelStyle)*

Default style applied to all labels on this edge.

<a id="eikon.spec._margin_labels.MarginLabelSpec.level_styles"></a>

#### level_styles *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[MarginLabelStyle](#eikon.spec._margin_labels.MarginLabelStyle), ...] | [None](https://docs.python.org/3/library/constants.html#None)*

Per-level style overrides (outermost level first).  Falls
back to `style` for any level without an override.

<a id="eikon.spec._margin_labels.MarginLabelSpec.target"></a>

#### target *: [MarginTarget](#eikon.spec._margin_labels.MarginTarget)*

Which grid the labels align to.

<a id="eikon.spec._margin_labels.MarginLabelSpec.strip_size"></a>

#### strip_size *: [float](https://docs.python.org/3/library/functions.html#float)*

Height (for top/bottom) or width (for left/right) of each
label band, in figure-fraction units.

<a id="eikon.spec._margin_labels.MarginLabelSpec.pad"></a>

#### pad *: [float](https://docs.python.org/3/library/functions.html#float)*

Gap between the axes edge and the first label level, in points.

<a id="eikon.spec._margin_labels.MarginLabelSpec.gap"></a>

#### gap *: [float](https://docs.python.org/3/library/functions.html#float)*

Gap between stacked label levels, in points.

<a id="eikon.spec._margin_labels.MarginLabelSpec.zorder"></a>

#### zorder *: [float](https://docs.python.org/3/library/functions.html#float)*

Drawing order for label text and background patches.

<a id="eikon.spec._margin_labels.MarginLabelSpec.label_styles"></a>

#### label_styles *: [dict](https://docs.python.org/3/library/stdtypes.html#dict)[[str](https://docs.python.org/3/library/stdtypes.html#str), [MarginLabelStyle](#eikon.spec._margin_labels.MarginLabelStyle)] | [None](https://docs.python.org/3/library/constants.html#None)*

Per-label style overrides keyed by label text.  When a label’s
text matches a key here, this style is used instead of the
level/edge default.

<a id="eikon.spec._margin_labels.MarginLabelSpec.cell_range"></a>

#### cell_range *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int), [int](https://docs.python.org/3/library/functions.html#int)] | [None](https://docs.python.org/3/library/constants.html#None)*

`(start, end)` restricting which cells of the grid the labels
cover (0-indexed, end-exclusive).  `None` = all cells along
the relevant axis.

<a id="eikon.spec._margin_labels.MarginLabelStyle"></a>

### *class* eikon.spec._margin_labels.MarginLabelStyle(\*, bg_color=None, text_color='black', fontsize=8.0, fontweight='normal', rotation=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Visual style for margin label text and optional background strip.

<a id="eikon.spec._margin_labels.MarginLabelStyle.bg_color"></a>

#### bg_color *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Background color for the label strip.  `None` = transparent.

<a id="eikon.spec._margin_labels.MarginLabelStyle.text_color"></a>

#### text_color *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Text color.

<a id="eikon.spec._margin_labels.MarginLabelStyle.fontsize"></a>

#### fontsize *: [float](https://docs.python.org/3/library/functions.html#float)*

Font size in points.

<a id="eikon.spec._margin_labels.MarginLabelStyle.fontweight"></a>

#### fontweight *: [str](https://docs.python.org/3/library/stdtypes.html#str)*

Font weight (`"normal"`, `"bold"`, etc.).

<a id="eikon.spec._margin_labels.MarginLabelStyle.rotation"></a>

#### rotation *: [float](https://docs.python.org/3/library/functions.html#float) | [None](https://docs.python.org/3/library/constants.html#None)*

Text rotation in degrees.  `None` = edge default
(0 for top/bottom, 90 for left, 270 for right).

<a id="eikon.spec._margin_labels.MarginTarget"></a>

### *class* eikon.spec._margin_labels.MarginTarget(\*, kind='layout', axes=None, grid=None)

Bases: [`object`](https://docs.python.org/3/library/functions.html#object)

Which axes grid the margin labels align to.

For `kind="layout"` (the default), labels align to the figure’s
GridSpec cells.  For `kind="virtual"`, labels subdivide a single
panel’s axes evenly — useful for inset grids drawn inside plot
functions.

<a id="eikon.spec._margin_labels.MarginTarget.kind"></a>

#### kind *: [Literal](https://docs.python.org/3/library/typing.html#typing.Literal)['layout', 'virtual']*

Targeting mode.

<a id="eikon.spec._margin_labels.MarginTarget.axes"></a>

#### axes *: [str](https://docs.python.org/3/library/stdtypes.html#str) | [None](https://docs.python.org/3/library/constants.html#None)*

Panel name whose axes to subdivide (required for `"virtual"`).

<a id="eikon.spec._margin_labels.MarginTarget.grid"></a>

#### grid *: [tuple](https://docs.python.org/3/library/stdtypes.html#tuple)[[int](https://docs.python.org/3/library/functions.html#int), [int](https://docs.python.org/3/library/functions.html#int)] | [None](https://docs.python.org/3/library/constants.html#None)*

`(rows, cols)` of the virtual grid (required for `"virtual"`).

<a id="module-eikon.spec._override"></a>

<a id="specification-overrides"></a>

## Specification Overrides

Override and merge logic for figure specifications.

Provides utilities to apply partial overrides to `FigureSpec`
instances, producing new immutable specs with the overrides applied.

<a id="eikon.spec._override.merge_spec_override"></a>

### eikon.spec._override.merge_spec_override(base, override)

Apply a dictionary of overrides to a figure specification.

Only fields present in *override* are changed.  Nested dictionaries
(`layout`, `export`, `metadata`) are shallow-merged rather than
replaced outright; typed dataclass fields are re-parsed from raw
dicts when provided.

* **Parameters:**
  * **base** ([*FigureSpec*](#eikon.spec._figure.FigureSpec)) – The base specification.
  * **override** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict) *[*[*str*](https://docs.python.org/3/library/stdtypes.html#str) *,* *Any* *]*) – Fields to override.
* **Returns:**
  A new specification with overrides applied.
* **Return type:**
  [FigureSpec](#eikon.spec._figure.FigureSpec)

<a id="module-eikon.spec._parse"></a>

<a id="specification-parsing"></a>

## Specification Parsing

Parse figure specifications from YAML files or dictionaries.

Converts raw dictionaries (typically loaded from YAML) into validated
`FigureSpec` instances.

<a id="eikon.spec._parse.parse_figure_file"></a>

### eikon.spec._parse.parse_figure_file(path)

Load and parse a figure specification from a YAML file.

* **Parameters:**
  **path** (*Path*) – Path to the YAML file.
* **Returns:**
  Parsed and validated figure specification.
* **Return type:**
  [FigureSpec](#eikon.spec._figure.FigureSpec)
* **Raises:**
  * [**ConfigError**](types.md#eikon.exceptions.ConfigError) – If the file cannot be read or parsed.
  * [**SpecValidationError**](types.md#eikon.exceptions.SpecValidationError) – If the specification fails validation.

<a id="eikon.spec._parse.parse_figure_spec"></a>

### eikon.spec._parse.parse_figure_spec(raw)

Parse a figure specification from a dictionary.

* **Parameters:**
  **raw** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) – Dictionary representation of a figure specification.
* **Returns:**
  Parsed and validated figure specification.
* **Return type:**
  [FigureSpec](#eikon.spec._figure.FigureSpec)
* **Raises:**
  [**SpecValidationError**](types.md#eikon.exceptions.SpecValidationError) – If the specification fails validation.

<a id="eikon.spec._parse.parse_layout_spec"></a>

### eikon.spec._parse.parse_layout_spec(raw)

Convert a raw layout dictionary to a `LayoutSpec`.

* **Parameters:**
  **raw** ([*dict*](https://docs.python.org/3/library/stdtypes.html#dict)) – Dictionary representation of a layout specification, typically
  from the `layout` key of a figure YAML file.
* **Returns:**
  Parsed layout specification.
* **Return type:**
  [LayoutSpec](layout.md#eikon.layout._grid.LayoutSpec)
