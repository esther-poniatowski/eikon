"""Tests for eikon.spec._override."""

from eikon.layout._grid import LayoutSpec
from eikon.spec._figure import FigureSpec
from eikon.spec._override import merge_spec_override
from eikon.spec._panel import PanelSpec


class TestMergeSpecOverride:
    def test_override_title(self):
        base = FigureSpec(name="fig", title="Original")
        merged = merge_spec_override(base, {"title": "New Title"})
        assert merged.title == "New Title"
        assert merged.name == "fig"

    def test_merge_metadata(self):
        base = FigureSpec(name="fig", metadata={"author": "A"})
        merged = merge_spec_override(base, {"metadata": {"project": "P"}})
        assert merged.metadata == {"author": "A", "project": "P"}

    def test_override_tags(self):
        base = FigureSpec(name="fig", tags=("a",))
        merged = merge_spec_override(base, {"tags": ["b", "c"]})
        assert merged.tags == ("b", "c")

    def test_merge_layout(self):
        base = FigureSpec(name="fig", layout=LayoutSpec(rows=1, cols=2))
        merged = merge_spec_override(base, {"layout": {"cols": 3}})
        assert isinstance(merged.layout, LayoutSpec)
        assert merged.layout.rows == 1
        assert merged.layout.cols == 3

    def test_override_panels_from_dicts(self):
        base = FigureSpec(
            name="fig",
            panels=(PanelSpec(name="A", plot_type="line"),),
        )
        merged = merge_spec_override(base, {
            "panels": [
                {"name": "X", "plot_type": "scatter"},
                {"name": "Y", "plot_type": "bar"},
            ],
        })
        assert len(merged.panels) == 2
        assert merged.panels[0].name == "X"
        assert merged.panels[1].plot_type == "bar"

    def test_override_panels_from_panelspec(self):
        base = FigureSpec(name="fig", panels=())
        new_panel = PanelSpec(name="Z", plot_type="heatmap")
        merged = merge_spec_override(base, {"panels": [new_panel]})
        assert len(merged.panels) == 1
        assert merged.panels[0].name == "Z"

    def test_immutability(self):
        base = FigureSpec(name="fig", title="Original")
        merge_spec_override(base, {"title": "Changed"})
        assert base.title == "Original"
