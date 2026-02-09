"""Tests for eikon.style._rcparams — rcParams bridge and context manager."""

import matplotlib as mpl

from eikon.style import StyleSheet, style_context, to_rcparams


class TestToRcparams:
    """Convert StyleSheet to rcParams dict."""

    def test_empty_sheet(self) -> None:
        sheet = StyleSheet(name="empty")
        params = to_rcparams(sheet)
        assert params == {}

    def test_font_family(self) -> None:
        sheet = StyleSheet(name="t", font_family="sans-serif")
        params = to_rcparams(sheet)
        assert params["font.family"] == "sans-serif"

    def test_font_size(self) -> None:
        sheet = StyleSheet(name="t", font_size=14.0)
        params = to_rcparams(sheet)
        assert params["font.size"] == 14.0

    def test_line_width(self) -> None:
        sheet = StyleSheet(name="t", line_width=2.0)
        params = to_rcparams(sheet)
        assert params["lines.linewidth"] == 2.0

    def test_palette(self) -> None:
        colors = ("#ff0000", "#00ff00", "#0000ff")
        sheet = StyleSheet(name="t", palette=colors)
        params = to_rcparams(sheet)
        cycle = params["axes.prop_cycle"]
        cycle_colors = cycle.by_key()["color"]
        assert cycle_colors == list(colors)

    def test_empty_palette_excluded(self) -> None:
        sheet = StyleSheet(name="t", palette=())
        params = to_rcparams(sheet)
        assert "axes.prop_cycle" not in params

    def test_figure_size(self) -> None:
        sheet = StyleSheet(name="t", figure_size=(10.0, 8.0))
        params = to_rcparams(sheet)
        assert params["figure.figsize"] == [10.0, 8.0]

    def test_rc_overrides_merged(self) -> None:
        sheet = StyleSheet(
            name="t",
            font_size=12.0,
            rc_overrides={"axes.grid": True, "font.size": 99.0},
        )
        params = to_rcparams(sheet)
        # rc_overrides win over explicit fields
        assert params["font.size"] == 99.0
        assert params["axes.grid"] is True

    def test_all_fields(self) -> None:
        sheet = StyleSheet(
            name="full",
            font_family="monospace",
            font_size=10.0,
            line_width=1.5,
            palette=("#aaa",),
            figure_size=(7.0, 5.0),
            rc_overrides={"axes.linewidth": 0.5},
        )
        params = to_rcparams(sheet)
        assert "font.family" in params
        assert "font.size" in params
        assert "lines.linewidth" in params
        assert "axes.prop_cycle" in params
        assert "figure.figsize" in params
        assert "axes.linewidth" in params


class TestStyleContext:
    """Context manager for temporary style application."""

    def test_applies_and_reverts(self) -> None:
        original_size = mpl.rcParams["font.size"]
        sheet = StyleSheet(name="t", font_size=99.0)

        with style_context(sheet):
            assert mpl.rcParams["font.size"] == 99.0

        assert mpl.rcParams["font.size"] == original_size

    def test_reverts_on_exception(self) -> None:
        original_size = mpl.rcParams["font.size"]
        sheet = StyleSheet(name="t", font_size=99.0)

        try:
            with style_context(sheet):
                assert mpl.rcParams["font.size"] == 99.0
                raise RuntimeError("boom")
        except RuntimeError:
            pass

        assert mpl.rcParams["font.size"] == original_size

    def test_nested_contexts(self) -> None:
        original = mpl.rcParams["font.size"]
        outer = StyleSheet(name="outer", font_size=20.0)
        inner = StyleSheet(name="inner", font_size=30.0)

        with style_context(outer):
            assert mpl.rcParams["font.size"] == 20.0
            with style_context(inner):
                assert mpl.rcParams["font.size"] == 30.0
            assert mpl.rcParams["font.size"] == 20.0

        assert mpl.rcParams["font.size"] == original
