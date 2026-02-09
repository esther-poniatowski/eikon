"""Tests for eikon.spec._override."""

from eikon.spec._figure import FigureSpec
from eikon.spec._override import merge_spec_override


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
        base = FigureSpec(name="fig", layout={"rows": 1, "cols": 2})
        merged = merge_spec_override(base, {"layout": {"cols": 3}})
        assert merged.layout == {"rows": 1, "cols": 3}

    def test_immutability(self):
        base = FigureSpec(name="fig", title="Original")
        merge_spec_override(base, {"title": "Changed"})
        assert base.title == "Original"
