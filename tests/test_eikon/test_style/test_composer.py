"""Tests for eikon.style._composer — style merging and chain resolution."""

import pytest

from eikon.exceptions import StyleNotFoundError
from eikon.style import StyleSheet, compose_styles, resolve_style_chain


class TestComposeStyles:
    """Direct style composition (no inheritance chains)."""

    def test_single_sheet(self) -> None:
        sheet = StyleSheet(name="only", font_size=12.0)
        result = compose_styles(sheet)
        assert result.name == "only"
        assert result.font_size == 12.0

    def test_two_sheets_rightmost_wins(self) -> None:
        base = StyleSheet(name="base", font_size=10.0, font_family="serif")
        top = StyleSheet(name="top", font_size=14.0)
        result = compose_styles(base, top)
        assert result.name == "top"
        assert result.font_size == 14.0
        # Inherit non-overridden fields from base
        assert result.font_family == "serif"

    def test_three_sheets(self) -> None:
        a = StyleSheet(name="a", font_size=8.0, line_width=0.5)
        b = StyleSheet(name="b", font_size=10.0)
        c = StyleSheet(name="c", line_width=1.5)
        result = compose_styles(a, b, c)
        assert result.name == "c"
        assert result.font_size == 10.0  # from b
        assert result.line_width == 1.5  # from c

    def test_rc_overrides_deep_merged(self) -> None:
        base = StyleSheet(
            name="base",
            rc_overrides={"axes.grid": True, "grid.alpha": 0.3},
        )
        top = StyleSheet(
            name="top",
            rc_overrides={"grid.alpha": 0.5, "axes.linewidth": 1.0},
        )
        result = compose_styles(base, top)
        assert result.rc_overrides == {
            "axes.grid": True,
            "grid.alpha": 0.5,
            "axes.linewidth": 1.0,
        }

    def test_none_fields_do_not_override(self) -> None:
        base = StyleSheet(name="base", palette=("#aaa", "#bbb"))
        top = StyleSheet(name="top")  # palette is None
        result = compose_styles(base, top)
        assert result.palette == ("#aaa", "#bbb")

    def test_empty_raises(self) -> None:
        with pytest.raises(ValueError, match="at least one"):
            compose_styles()

    def test_extends_cleared_after_compose(self) -> None:
        a = StyleSheet(name="a", extends=("parent",))
        b = StyleSheet(name="b")
        result = compose_styles(a, b)
        assert result.extends == ()


class TestResolveStyleChain:
    """Style chain resolution with extends."""

    def test_no_extends(self) -> None:
        sheet = StyleSheet(name="leaf", font_size=10.0)
        result = resolve_style_chain(sheet, {})
        assert result.name == "leaf"
        assert result.font_size == 10.0

    def test_single_parent(self) -> None:
        parent = StyleSheet(name="parent", font_family="serif", font_size=8.0)
        child = StyleSheet(name="child", font_size=12.0, extends=("parent",))
        registry = {"parent": parent}
        result = resolve_style_chain(child, registry)
        assert result.name == "child"
        assert result.font_size == 12.0
        assert result.font_family == "serif"  # inherited

    def test_multi_level_chain(self) -> None:
        grandparent = StyleSheet(
            name="gp", font_family="serif", font_size=8.0, line_width=0.5,
        )
        parent = StyleSheet(
            name="parent", font_size=10.0, extends=("gp",),
        )
        child = StyleSheet(
            name="child", line_width=1.0, extends=("parent",),
        )
        registry = {"gp": grandparent, "parent": parent}
        result = resolve_style_chain(child, registry)
        assert result.font_family == "serif"  # from grandparent
        assert result.font_size == 10.0  # from parent
        assert result.line_width == 1.0  # from child

    def test_multiple_parents(self) -> None:
        a = StyleSheet(name="a", font_family="serif", font_size=8.0)
        b = StyleSheet(name="b", font_family="sans-serif", line_width=1.0)
        child = StyleSheet(name="child", extends=("a", "b"))
        registry = {"a": a, "b": b}
        result = resolve_style_chain(child, registry)
        # b wins over a for font_family (rightmost parent wins)
        assert result.font_family == "sans-serif"
        assert result.font_size == 8.0  # from a
        assert result.line_width == 1.0  # from b

    def test_circular_reference_detected(self) -> None:
        a = StyleSheet(name="a", extends=("b",))
        b = StyleSheet(name="b", extends=("a",))
        registry = {"a": a, "b": b}
        with pytest.raises(ValueError, match="Circular"):
            resolve_style_chain(a, registry)

    def test_missing_parent_raises(self) -> None:
        child = StyleSheet(name="child", extends=("missing",))
        with pytest.raises(StyleNotFoundError):
            resolve_style_chain(child, {})
