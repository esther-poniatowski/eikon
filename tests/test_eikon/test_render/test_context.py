"""Tests for eikon.render._context — RenderContext."""

from eikon.config._defaults import DEFAULT_CONFIG
from eikon.render._context import RenderContext
from eikon.spec._figure import FigureSpec


class TestRenderContext:
    """RenderContext construction and default values."""

    def test_construction_minimal(self) -> None:
        spec = FigureSpec(name="fig1")
        ctx = RenderContext(spec=spec, config=DEFAULT_CONFIG)
        assert ctx.spec is spec
        assert ctx.config is DEFAULT_CONFIG
        assert ctx.style is None
        assert ctx.layout is None
        assert ctx.export_formats == ()
        assert ctx.show is False
        assert ctx.overrides == {}

    def test_construction_with_options(self) -> None:
        spec = FigureSpec(name="fig1")
        ctx = RenderContext(
            spec=spec,
            config=DEFAULT_CONFIG,
            export_formats=("pdf", "svg"),
            show=True,
            overrides={"dpi": 600},
        )
        assert ctx.export_formats == ("pdf", "svg")
        assert ctx.show is True
        assert ctx.overrides == {"dpi": 600}

    def test_mutable_style(self) -> None:
        """RenderContext is mutable — style can be set after construction."""
        from eikon.style._sheet import StyleSheet

        spec = FigureSpec(name="fig1")
        ctx = RenderContext(spec=spec, config=DEFAULT_CONFIG)
        sheet = StyleSheet(name="test")
        ctx.style = sheet
        assert ctx.style is sheet
