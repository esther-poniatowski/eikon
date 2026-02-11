"""Tests for eikon.render._margin_labels — hierarchy, geometry, and drawing."""

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
import pytest

from eikon.config._defaults import DEFAULT_CONFIG
from eikon.config._resolver import resolve_paths
from eikon.config._validation import validate_figure_spec
from eikon.ext._plot_types import _clear_registry, register_plot_type
from eikon.layout._builder import BuiltLayout, build_layout
from eikon.layout._grid import LayoutSpec
from eikon.layout._placement import resolve_placements
from eikon.render._margin_labels import (
    LabelSpan,
    compute_cell_edges,
    draw_margin_labels,
    resolve_label_hierarchy,
)
from eikon.render._pipeline import render_figure
from eikon.spec._figure import FigureSpec
from eikon.spec._margin_labels import MarginLabelSpec, MarginLabelStyle, MarginTarget
from eikon.spec._panel import PanelSpec
from eikon.spec._parse import parse_figure_spec

matplotlib.use("Agg")


@pytest.fixture(autouse=True)
def _clean_state():
    """Clean plot-type registry before each test; close figs after."""
    _clear_registry()
    yield
    plt.close("all")


def _noop_plot(ax, **kwargs):
    """Minimal plot function that does nothing."""


# ---------------------------------------------------------------------------
# resolve_label_hierarchy
# ---------------------------------------------------------------------------


class TestResolveHierarchy:
    def test_flat_labels(self) -> None:
        spans, n_levels = resolve_label_hierarchy(("A", "B", "C"))
        assert n_levels == 1
        assert len(spans) == 3
        assert spans[0] == LabelSpan(text="A", level=0, start=0, span=1)
        assert spans[1] == LabelSpan(text="B", level=0, start=1, span=1)
        assert spans[2] == LabelSpan(text="C", level=0, start=2, span=1)

    def test_hierarchical_two_levels(self) -> None:
        labels = {
            "PTD": {"active": None, "passive": None},
            "CLK": {"active": None, "passive": None},
        }
        spans, n_levels = resolve_label_hierarchy(labels)
        assert n_levels == 2

        # Level 0 (outermost): PTD spans 2, CLK spans 2
        outer = sorted(
            [s for s in spans if s.level == 0], key=lambda s: s.start,
        )
        assert len(outer) == 2
        assert outer[0] == LabelSpan(text="PTD", level=0, start=0, span=2)
        assert outer[1] == LabelSpan(text="CLK", level=0, start=2, span=2)

        # Level 1 (innermost): 4 individual labels
        inner = sorted(
            [s for s in spans if s.level == 1], key=lambda s: s.start,
        )
        assert len(inner) == 4
        assert inner[0].text == "active"
        assert inner[0].start == 0
        assert inner[1].text == "passive"
        assert inner[1].start == 1

    def test_hierarchical_with_tuple_children(self) -> None:
        labels = {"G1": ("a", "b"), "G2": ("c",)}
        spans, n_levels = resolve_label_hierarchy(labels)
        assert n_levels == 2

        outer = [s for s in spans if s.level == 0]
        assert len(outer) == 2
        g1 = next(s for s in outer if s.text == "G1")
        assert g1.span == 2
        g2 = next(s for s in outer if s.text == "G2")
        assert g2.span == 1

        inner = sorted([s for s in spans if s.level == 1], key=lambda s: s.start)
        assert [s.text for s in inner] == ["a", "b", "c"]

    def test_three_level_hierarchy(self) -> None:
        labels = {
            "Region": {
                "PTD": {"active": None, "passive": None},
            },
        }
        spans, n_levels = resolve_label_hierarchy(labels)
        assert n_levels == 3

        l0 = [s for s in spans if s.level == 0]
        assert len(l0) == 1
        assert l0[0].text == "Region"
        assert l0[0].span == 2

        l1 = [s for s in spans if s.level == 1]
        assert len(l1) == 1
        assert l1[0].text == "PTD"
        assert l1[0].span == 2

        l2 = [s for s in spans if s.level == 2]
        assert len(l2) == 2

    def test_single_label_flat(self) -> None:
        spans, n_levels = resolve_label_hierarchy(("X",))
        assert n_levels == 1
        assert len(spans) == 1
        assert spans[0] == LabelSpan(text="X", level=0, start=0, span=1)

    def test_unsupported_value_type(self) -> None:
        with pytest.raises(TypeError, match="Unsupported"):
            resolve_label_hierarchy({"bad": 42})  # type: ignore[dict-item]


# ---------------------------------------------------------------------------
# compute_cell_edges
# ---------------------------------------------------------------------------


def _make_built(
    rows: int = 1,
    cols: int = 3,
    *,
    wspace: float | None = None,
    hspace: float | None = None,
) -> BuiltLayout:
    layout = LayoutSpec(
        rows=rows, cols=cols, constrained_layout=False,
        wspace=wspace, hspace=hspace,
    )
    panels = tuple(
        PanelSpec(name=f"p{r}_{c}", plot_type="noop", row=r, col=c)
        for r in range(rows)
        for c in range(cols)
    )
    placements = resolve_placements(panels, layout)
    return build_layout(layout, placements, figure_size=(6, 4))


class TestComputeCellEdges:
    def test_layout_top_edges(self) -> None:
        built = _make_built(rows=1, cols=3)
        target = MarginTarget(kind="layout")
        starts, ends, anchor_min, anchor_max = compute_cell_edges(
            built.figure, built, target, "top",
        )
        # 3 columns → 3 cells
        assert len(starts) == 3
        assert len(ends) == 3
        # starts should be ascending (left to right)
        assert np.all(np.diff(starts) > 0)
        # Each cell: start < end
        assert np.all(starts < ends)
        # Anchor bounds are perpendicular (y-axis for top/bottom)
        assert anchor_max > anchor_min

    def test_layout_left_edges(self) -> None:
        built = _make_built(rows=3, cols=1)
        target = MarginTarget(kind="layout")
        starts, ends, anchor_min, anchor_max = compute_cell_edges(
            built.figure, built, target, "left",
        )
        # 3 rows → 3 cells
        assert len(starts) == 3
        assert len(ends) == 3
        # Each cell: start < end (bot[i] < top[i])
        assert np.all(starts < ends)

    def test_layout_top_with_wspace(self) -> None:
        """Columns with wspace > 0 must still produce exactly ncols cells."""
        built = _make_built(rows=1, cols=3, wspace=0.4)
        target = MarginTarget(kind="layout")
        starts, ends, _, _ = compute_cell_edges(
            built.figure, built, target, "top",
        )
        assert len(starts) == 3
        assert len(ends) == 3
        # With wspace, there are gaps: end[i] < start[i+1]
        for i in range(len(starts) - 1):
            assert ends[i] < starts[i + 1]

    def test_layout_left_with_hspace(self) -> None:
        """Rows with hspace > 0 must still produce exactly nrows cells."""
        built = _make_built(rows=3, cols=1, hspace=0.4)
        target = MarginTarget(kind="layout")
        starts, ends, _, _ = compute_cell_edges(
            built.figure, built, target, "left",
        )
        assert len(starts) == 3
        assert len(ends) == 3
        assert np.all(starts < ends)

    def test_virtual_top_edges(self) -> None:
        built = _make_built(rows=1, cols=1)
        target = MarginTarget(kind="virtual", axes="p0_0", grid=(3, 6))
        starts, ends, anchor_min, anchor_max = compute_cell_edges(
            built.figure, built, target, "top",
        )
        assert len(starts) == 6  # 6 cols
        assert len(ends) == 6
        assert np.all(np.diff(starts) > 0)
        assert np.all(starts < ends)
        # Evenly spaced
        np.testing.assert_allclose(np.diff(starts), np.diff(starts)[0])

    def test_virtual_left_edges(self) -> None:
        built = _make_built(rows=1, cols=1)
        target = MarginTarget(kind="virtual", axes="p0_0", grid=(3, 6))
        starts, ends, anchor_min, anchor_max = compute_cell_edges(
            built.figure, built, target, "left",
        )
        assert len(starts) == 3  # 3 rows
        assert len(ends) == 3
        # Each cell: start < end
        assert np.all(starts < ends)
        # Row 0 (first element) should have higher y than row 2 (last)
        assert ends[0] > ends[2]

    def test_virtual_missing_axes_raises(self) -> None:
        built = _make_built(rows=1, cols=1)
        target = MarginTarget(kind="virtual", axes=None, grid=(3, 6))
        with pytest.raises(ValueError, match="axes"):
            compute_cell_edges(built.figure, built, target, "top")

    def test_virtual_missing_grid_raises(self) -> None:
        built = _make_built(rows=1, cols=1)
        target = MarginTarget(kind="virtual", axes="p0_0", grid=None)
        with pytest.raises(ValueError, match="grid"):
            compute_cell_edges(built.figure, built, target, "top")

    def test_virtual_missing_panel_raises(self) -> None:
        built = _make_built(rows=1, cols=1)
        target = MarginTarget(kind="virtual", axes="nonexistent", grid=(2, 2))
        with pytest.raises(ValueError, match="not found"):
            compute_cell_edges(built.figure, built, target, "top")


# ---------------------------------------------------------------------------
# draw_margin_labels
# ---------------------------------------------------------------------------


class TestDrawMarginLabels:
    def test_flat_top_labels(self) -> None:
        built = _make_built(rows=1, cols=3)
        fig = built.figure
        margin_labels = {
            "top": MarginLabelSpec(labels=("A", "B", "C")),
        }
        # Should not raise
        draw_margin_labels(fig, built, margin_labels)

        # Check that 3 text artists were added
        texts = [t for t in fig.texts if t.get_text() in ("A", "B", "C")]
        assert len(texts) == 3

    def test_hierarchical_labels_with_patches(self) -> None:
        built = _make_built(rows=1, cols=4)
        fig = built.figure
        margin_labels = {
            "top": MarginLabelSpec(
                labels={
                    "G1": {"a": None, "b": None},
                    "G2": {"c": None, "d": None},
                },
                level_styles=(
                    MarginLabelStyle(bg_color="#D4E6F1"),
                    MarginLabelStyle(bg_color="#EBF5FB"),
                ),
            ),
        }
        draw_margin_labels(fig, built, margin_labels)

        # 6 text artists: G1, G2, a, b, c, d
        all_texts = {t.get_text() for t in fig.texts}
        assert {"G1", "G2", "a", "b", "c", "d"}.issubset(all_texts)

        # Background patches should have been added
        assert len(fig.patches) >= 6

    def test_left_labels_rotated(self) -> None:
        built = _make_built(rows=3, cols=1)
        fig = built.figure
        margin_labels = {
            "left": MarginLabelSpec(labels=("R1", "R2", "R3")),
        }
        draw_margin_labels(fig, built, margin_labels)

        texts = [t for t in fig.texts if t.get_text() in ("R1", "R2", "R3")]
        assert len(texts) == 3
        for t in texts:
            assert t.get_rotation() == 90.0

    def test_right_labels_rotated(self) -> None:
        built = _make_built(rows=2, cols=1)
        fig = built.figure
        margin_labels = {
            "right": MarginLabelSpec(labels=("X", "Y")),
        }
        draw_margin_labels(fig, built, margin_labels)

        texts = [t for t in fig.texts if t.get_text() in ("X", "Y")]
        assert len(texts) == 2
        for t in texts:
            assert t.get_rotation() == 270.0

    def test_bottom_labels(self) -> None:
        built = _make_built(rows=1, cols=2)
        fig = built.figure
        margin_labels = {
            "bottom": MarginLabelSpec(labels=("L", "R")),
        }
        draw_margin_labels(fig, built, margin_labels)

        texts = [t for t in fig.texts if t.get_text() in ("L", "R")]
        assert len(texts) == 2

    def test_invalid_edge(self) -> None:
        built = _make_built()
        with pytest.raises(ValueError, match="Invalid margin label edge"):
            draw_margin_labels(built.figure, built, {"diagonal": MarginLabelSpec(labels=("X",))})

    def test_multiple_edges(self) -> None:
        built = _make_built(rows=2, cols=3)
        fig = built.figure
        margin_labels = {
            "top": MarginLabelSpec(labels=("C1", "C2", "C3")),
            "left": MarginLabelSpec(labels=("R1", "R2")),
        }
        draw_margin_labels(fig, built, margin_labels)

        all_texts = {t.get_text() for t in fig.texts}
        assert {"C1", "C2", "C3", "R1", "R2"}.issubset(all_texts)

    def test_custom_style(self) -> None:
        built = _make_built(rows=1, cols=2)
        fig = built.figure
        margin_labels = {
            "top": MarginLabelSpec(
                labels=("A", "B"),
                style=MarginLabelStyle(
                    text_color="red", fontsize=12.0, fontweight="bold",
                ),
            ),
        }
        draw_margin_labels(fig, built, margin_labels)

        texts = [t for t in fig.texts if t.get_text() in ("A", "B")]
        for t in texts:
            assert t.get_color() == "red"
            assert t.get_fontsize() == 12.0
            assert t.get_fontweight() == "bold"

    def test_labels_with_wspace(self) -> None:
        """Labels should render correctly when columns have spacing gaps."""
        built = _make_built(rows=1, cols=3, wspace=0.5)
        fig = built.figure
        margin_labels = {
            "top": MarginLabelSpec(labels=("A", "B", "C")),
        }
        draw_margin_labels(fig, built, margin_labels)

        texts = [t for t in fig.texts if t.get_text() in ("A", "B", "C")]
        assert len(texts) == 3
        # Labels should be in left-to-right order by x-position
        xs = sorted((t.get_position()[0], t.get_text()) for t in texts)
        assert [x[1] for x in xs] == ["A", "B", "C"]


# ---------------------------------------------------------------------------
# Span-count validation
# ---------------------------------------------------------------------------


class TestSpanValidation:
    def test_too_few_labels(self) -> None:
        built = _make_built(rows=1, cols=3)
        margin_labels = {
            "top": MarginLabelSpec(labels=("A", "B")),  # 2 labels, 3 cols
        }
        with pytest.raises(ValueError, match="spans 2 cells but the grid has 3"):
            draw_margin_labels(built.figure, built, margin_labels)

    def test_too_many_labels(self) -> None:
        built = _make_built(rows=1, cols=2)
        margin_labels = {
            "top": MarginLabelSpec(labels=("A", "B", "C")),  # 3 labels, 2 cols
        }
        with pytest.raises(ValueError, match="spans 3 cells but the grid has 2"):
            draw_margin_labels(built.figure, built, margin_labels)


# ---------------------------------------------------------------------------
# Per-label styles
# ---------------------------------------------------------------------------


class TestPerLabelStyles:
    def test_label_style_override(self) -> None:
        built = _make_built(rows=1, cols=3)
        fig = built.figure
        margin_labels = {
            "top": MarginLabelSpec(
                labels=("A", "B", "C"),
                style=MarginLabelStyle(text_color="black", fontsize=8.0),
                label_styles={
                    "B": MarginLabelStyle(text_color="red", fontweight="bold", fontsize=12.0),
                },
            ),
        }
        draw_margin_labels(fig, built, margin_labels)

        b_text = next(t for t in fig.texts if t.get_text() == "B")
        assert b_text.get_color() == "red"
        assert b_text.get_fontsize() == 12.0
        assert b_text.get_fontweight() == "bold"

        # Other labels should use the edge default style
        a_text = next(t for t in fig.texts if t.get_text() == "A")
        assert a_text.get_color() == "black"
        assert a_text.get_fontsize() == 8.0

    def test_label_style_with_bg_color(self) -> None:
        built = _make_built(rows=1, cols=2)
        fig = built.figure
        margin_labels = {
            "top": MarginLabelSpec(
                labels=("A", "B"),
                label_styles={
                    "A": MarginLabelStyle(bg_color="#FFE0E0"),
                },
            ),
        }
        draw_margin_labels(fig, built, margin_labels)

        # Only label A should have a background patch
        assert len(fig.patches) == 1


# ---------------------------------------------------------------------------
# Cell range
# ---------------------------------------------------------------------------


class TestCellRange:
    def test_cell_range_subset(self) -> None:
        """Labels on a subset of columns."""
        built = _make_built(rows=1, cols=4)
        fig = built.figure
        margin_labels = {
            "top": MarginLabelSpec(
                labels=("B", "C"),
                cell_range=(1, 3),
            ),
        }
        draw_margin_labels(fig, built, margin_labels)

        texts = [t for t in fig.texts if t.get_text() in ("B", "C")]
        assert len(texts) == 2

    def test_cell_range_rows(self) -> None:
        """Labels on a subset of rows."""
        built = _make_built(rows=4, cols=1)
        fig = built.figure
        margin_labels = {
            "left": MarginLabelSpec(
                labels=("R1", "R2"),
                cell_range=(0, 2),
            ),
        }
        draw_margin_labels(fig, built, margin_labels)

        texts = [t for t in fig.texts if t.get_text() in ("R1", "R2")]
        assert len(texts) == 2


# ---------------------------------------------------------------------------
# Pipeline integration
# ---------------------------------------------------------------------------


class TestPipelineIntegration:
    def test_render_with_margin_labels(self, tmp_path) -> None:
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="test-margin",
            panels=(
                PanelSpec(name="A", plot_type="noop", row=0, col=0),
                PanelSpec(name="B", plot_type="noop", row=0, col=1),
            ),
            layout={"rows": 1, "cols": 2},
            margin_labels={
                "top": MarginLabelSpec(labels=("Col 1", "Col 2")),
            },
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.figure is not None

        texts = {t.get_text() for t in handle.figure.texts}
        assert "Col 1" in texts
        assert "Col 2" in texts

    def test_render_without_margin_labels(self, tmp_path) -> None:
        """Existing figures without margin_labels should be unaffected."""
        register_plot_type("noop", _noop_plot)
        spec = FigureSpec(
            name="test-no-margin",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        handle = render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.figure is not None


# ---------------------------------------------------------------------------
# YAML parsing
# ---------------------------------------------------------------------------


class TestYAMLParsing:
    def test_hierarchical_yaml_lists_become_tuples(self) -> None:
        """YAML lists inside hierarchical labels must be converted to tuples."""
        raw = {
            "name": "test-yaml",
            "margin_labels": {
                "top": {
                    "labels": {
                        "G1": ["a", "b"],
                        "G2": ["c"],
                    },
                },
            },
        }
        spec = parse_figure_spec(raw)
        assert spec.margin_labels is not None
        top = spec.margin_labels["top"]
        assert isinstance(top.labels, dict)
        assert top.labels["G1"] == ("a", "b")
        assert top.labels["G2"] == ("c",)

    def test_flat_yaml_list_becomes_tuple(self) -> None:
        raw = {
            "name": "test-yaml",
            "margin_labels": {
                "top": {"labels": ["A", "B"]},
            },
        }
        spec = parse_figure_spec(raw)
        assert spec.margin_labels is not None
        assert spec.margin_labels["top"].labels == ("A", "B")

    def test_label_styles_parsed(self) -> None:
        raw = {
            "name": "test-yaml",
            "margin_labels": {
                "top": {
                    "labels": ["A", "B"],
                    "label_styles": {
                        "B": {"fontweight": "bold", "bg_color": "#FFE0E0"},
                    },
                },
            },
        }
        spec = parse_figure_spec(raw)
        assert spec.margin_labels is not None
        top = spec.margin_labels["top"]
        assert top.label_styles is not None
        assert "B" in top.label_styles
        assert top.label_styles["B"].fontweight == "bold"
        assert top.label_styles["B"].bg_color == "#FFE0E0"

    def test_cell_range_parsed(self) -> None:
        raw = {
            "name": "test-yaml",
            "margin_labels": {
                "top": {
                    "labels": ["A", "B"],
                    "cell_range": [1, 3],
                },
            },
        }
        spec = parse_figure_spec(raw)
        assert spec.margin_labels is not None
        assert spec.margin_labels["top"].cell_range == (1, 3)

    def test_nested_dict_with_null_leaves(self) -> None:
        """YAML null values (None) in nested dicts should be preserved."""
        raw = {
            "name": "test-yaml",
            "margin_labels": {
                "top": {
                    "labels": {
                        "PTD": {"active": None, "passive": None},
                    },
                },
            },
        }
        spec = parse_figure_spec(raw)
        assert spec.margin_labels is not None
        labels = spec.margin_labels["top"].labels
        assert isinstance(labels, dict)
        assert labels["PTD"]["active"] is None


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


class TestValidation:
    def test_valid_margin_labels(self) -> None:
        raw = {
            "name": "test",
            "margin_labels": {
                "top": {"labels": ["A", "B"]},
            },
        }
        errors = validate_figure_spec(raw)
        assert not errors

    def test_bad_edge(self) -> None:
        raw = {
            "name": "test",
            "margin_labels": {
                "diagonal": {"labels": ["A"]},
            },
        }
        errors = validate_figure_spec(raw)
        assert any("invalid" in e.lower() or "diagonal" in e for e in errors)

    def test_missing_labels(self) -> None:
        raw = {
            "name": "test",
            "margin_labels": {
                "top": {"style": {}},
            },
        }
        errors = validate_figure_spec(raw)
        assert any("labels" in e for e in errors)

    def test_virtual_missing_grid(self) -> None:
        raw = {
            "name": "test",
            "margin_labels": {
                "top": {
                    "labels": ["A"],
                    "target": {"kind": "virtual", "axes": "panel"},
                },
            },
        }
        errors = validate_figure_spec(raw)
        assert any("grid" in e for e in errors)

    def test_virtual_missing_axes(self) -> None:
        raw = {
            "name": "test",
            "margin_labels": {
                "top": {
                    "labels": ["A"],
                    "target": {"kind": "virtual", "grid": [3, 6]},
                },
            },
        }
        errors = validate_figure_spec(raw)
        assert any("axes" in e for e in errors)

    def test_not_a_dict(self) -> None:
        raw = {
            "name": "test",
            "margin_labels": "bad",
        }
        errors = validate_figure_spec(raw)
        assert any("mapping" in e for e in errors)

    def test_label_styles_not_a_dict(self) -> None:
        raw = {
            "name": "test",
            "margin_labels": {
                "top": {"labels": ["A"], "label_styles": "bad"},
            },
        }
        errors = validate_figure_spec(raw)
        assert any("label_styles" in e for e in errors)

    def test_cell_range_not_a_list(self) -> None:
        raw = {
            "name": "test",
            "margin_labels": {
                "top": {"labels": ["A"], "cell_range": "bad"},
            },
        }
        errors = validate_figure_spec(raw)
        assert any("cell_range" in e for e in errors)

    def test_cell_range_bad_values(self) -> None:
        raw = {
            "name": "test",
            "margin_labels": {
                "top": {"labels": ["A"], "cell_range": [3, 1]},
            },
        }
        errors = validate_figure_spec(raw)
        assert any("cell_range" in e for e in errors)

    def test_cell_range_non_integer(self) -> None:
        raw = {
            "name": "test",
            "margin_labels": {
                "top": {"labels": ["A"], "cell_range": [1.5, 3.5]},
            },
        }
        errors = validate_figure_spec(raw)
        assert any("cell_range" in e for e in errors)
