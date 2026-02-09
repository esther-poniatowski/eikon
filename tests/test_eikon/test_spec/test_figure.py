"""Tests for eikon.spec._figure."""

from eikon.spec._figure import FigureSpec
from eikon.spec._panel import PanelSpec


class TestFigureSpec:
    def test_minimal(self):
        spec = FigureSpec(name="test")
        assert spec.name == "test"
        assert spec.title == ""
        assert spec.tags == ()
        assert spec.panels == ()
        assert spec.layout is None

    def test_with_panels(self):
        panel = PanelSpec(name="A", plot_type="line")
        spec = FigureSpec(name="fig", panels=(panel,))
        assert len(spec.panels) == 1
        assert spec.panels[0].name == "A"

    def test_frozen(self):
        spec = FigureSpec(name="test")
        try:
            spec.name = "other"  # type: ignore[misc]
            assert False, "Should have raised"
        except AttributeError:
            pass
