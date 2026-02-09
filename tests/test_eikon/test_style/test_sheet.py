"""Tests for eikon.style._sheet — StyleSheet dataclass."""

from dataclasses import FrozenInstanceError

import pytest

from eikon.style import StyleSheet


class TestStyleSheet:
    """StyleSheet construction and immutability."""

    def test_minimal_construction(self) -> None:
        sheet = StyleSheet(name="test")
        assert sheet.name == "test"
        assert sheet.font_family is None
        assert sheet.font_size is None
        assert sheet.line_width is None
        assert sheet.palette is None
        assert sheet.figure_size is None
        assert sheet.rc_overrides == {}
        assert sheet.extends == ()

    def test_full_construction(self) -> None:
        sheet = StyleSheet(
            name="full",
            font_family="serif",
            font_size=10.0,
            line_width=1.0,
            palette=("#ff0000", "#00ff00"),
            figure_size=(8.0, 6.0),
            rc_overrides={"axes.grid": True},
            extends=("publication",),
        )
        assert sheet.font_family == "serif"
        assert sheet.palette == ("#ff0000", "#00ff00")
        assert sheet.extends == ("publication",)

    def test_frozen(self) -> None:
        sheet = StyleSheet(name="frozen")
        with pytest.raises(FrozenInstanceError):
            sheet.name = "changed"  # type: ignore[misc]

    def test_equality(self) -> None:
        a = StyleSheet(name="eq", font_size=10.0)
        b = StyleSheet(name="eq", font_size=10.0)
        assert a == b

    def test_inequality(self) -> None:
        a = StyleSheet(name="a", font_size=10.0)
        b = StyleSheet(name="b", font_size=10.0)
        assert a != b
