"""Tests for eikon.style._presets — built-in style presets."""

from eikon.style import PRESETS, StyleSheet
from eikon.style._presets import get_preset


class TestPresets:
    """Built-in preset availability and structure."""

    def test_all_presets_exist(self) -> None:
        assert "publication" in PRESETS
        assert "presentation" in PRESETS
        assert "poster" in PRESETS

    def test_presets_are_stylesheets(self) -> None:
        for name, sheet in PRESETS.items():
            assert isinstance(sheet, StyleSheet), f"{name} is not a StyleSheet"

    def test_preset_names_match_keys(self) -> None:
        for key, sheet in PRESETS.items():
            assert sheet.name == key

    def test_publication_preset_values(self) -> None:
        pub = PRESETS["publication"]
        assert pub.font_family == "serif"
        assert pub.font_size == 8.0
        assert pub.figure_size == (7.0, 5.0)

    def test_presentation_has_larger_font(self) -> None:
        pres = PRESETS["presentation"]
        pub = PRESETS["publication"]
        assert pres.font_size is not None
        assert pub.font_size is not None
        assert pres.font_size > pub.font_size

    def test_poster_has_largest_font(self) -> None:
        poster = PRESETS["poster"]
        pres = PRESETS["presentation"]
        assert poster.font_size is not None
        assert pres.font_size is not None
        assert poster.font_size > pres.font_size

    def test_get_preset_found(self) -> None:
        sheet = get_preset("publication")
        assert sheet is not None
        assert sheet.name == "publication"

    def test_get_preset_not_found(self) -> None:
        assert get_preset("nonexistent") is None

    def test_presets_have_no_extends(self) -> None:
        for name, sheet in PRESETS.items():
            assert sheet.extends == (), f"{name} should have no extends"
