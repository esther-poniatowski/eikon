"""Tests for eikon.spec._margin_labels — dataclass construction and defaults."""

import pytest

from eikon.spec._margin_labels import MarginLabelSpec, MarginLabelStyle, MarginTarget


class TestMarginLabelStyle:
    def test_defaults(self) -> None:
        s = MarginLabelStyle()
        assert s.bg_color is None
        assert s.text_color == "black"
        assert s.fontsize == 8.0
        assert s.fontweight == "normal"
        assert s.rotation is None

    def test_custom(self) -> None:
        s = MarginLabelStyle(bg_color="#E8F0FE", fontweight="bold", rotation=45.0)
        assert s.bg_color == "#E8F0FE"
        assert s.fontweight == "bold"
        assert s.rotation == 45.0

    def test_frozen(self) -> None:
        s = MarginLabelStyle()
        with pytest.raises(AttributeError):
            s.fontsize = 12.0  # type: ignore[misc]


class TestMarginTarget:
    def test_layout_default(self) -> None:
        t = MarginTarget()
        assert t.kind == "layout"
        assert t.axes is None
        assert t.grid is None

    def test_virtual(self) -> None:
        t = MarginTarget(kind="virtual", axes="gabor", grid=(3, 6))
        assert t.kind == "virtual"
        assert t.axes == "gabor"
        assert t.grid == (3, 6)


class TestMarginLabelSpec:
    def test_flat_labels(self) -> None:
        spec = MarginLabelSpec(labels=("A", "B", "C"))
        assert spec.labels == ("A", "B", "C")
        assert spec.strip_size == 0.04
        assert spec.pad == 6.0
        assert spec.gap == 2.0
        assert spec.zorder == 2.1
        assert spec.target.kind == "layout"
        assert spec.level_styles is None
        assert spec.label_styles is None
        assert spec.cell_range is None

    def test_hierarchical_labels(self) -> None:
        labels = {"G1": {"a": None, "b": None}, "G2": {"c": None}}
        spec = MarginLabelSpec(labels=labels)
        assert isinstance(spec.labels, dict)
        assert "G1" in spec.labels

    def test_level_styles(self) -> None:
        spec = MarginLabelSpec(
            labels=("A",),
            level_styles=(
                MarginLabelStyle(bg_color="red"),
                MarginLabelStyle(bg_color="blue"),
            ),
        )
        assert len(spec.level_styles) == 2
        assert spec.level_styles[0].bg_color == "red"

    def test_label_styles(self) -> None:
        spec = MarginLabelSpec(
            labels=("A", "B"),
            label_styles={
                "B": MarginLabelStyle(fontweight="bold", bg_color="#FFE0E0"),
            },
        )
        assert spec.label_styles is not None
        assert "B" in spec.label_styles
        assert spec.label_styles["B"].fontweight == "bold"

    def test_cell_range(self) -> None:
        spec = MarginLabelSpec(labels=("A", "B"), cell_range=(1, 3))
        assert spec.cell_range == (1, 3)

    def test_frozen(self) -> None:
        spec = MarginLabelSpec(labels=("A",))
        with pytest.raises(AttributeError):
            spec.pad = 10.0  # type: ignore[misc]
