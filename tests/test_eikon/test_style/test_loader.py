"""Tests for eikon.style._loader — load styles from various sources."""

from pathlib import Path

import pytest

from eikon.exceptions import StyleError, StyleNotFoundError
from eikon.style import StyleSheet, load_style


class TestLoadFromDict:
    """Load StyleSheet from a raw dict."""

    def test_minimal_dict(self) -> None:
        sheet = load_style({"name": "test"})
        assert sheet.name == "test"

    def test_full_dict(self) -> None:
        sheet = load_style({
            "name": "full",
            "font_family": "serif",
            "font_size": 10.0,
            "line_width": 1.0,
            "palette": ["#aaa", "#bbb"],
            "figure_size": [7.0, 5.0],
            "rc_overrides": {"axes.grid": True},
            "extends": ["publication"],
        })
        assert sheet.font_family == "serif"
        assert sheet.palette == ("#aaa", "#bbb")
        assert sheet.figure_size == (7.0, 5.0)
        assert sheet.extends == ("publication",)

    def test_missing_name_uses_unnamed(self) -> None:
        sheet = load_style({"font_size": 12.0})
        assert sheet.name == "unnamed"

    def test_extends_as_string(self) -> None:
        sheet = load_style({"name": "t", "extends": "publication"})
        assert sheet.extends == ("publication",)


class TestLoadFromPreset:
    """Load StyleSheet from a built-in preset name."""

    def test_publication(self) -> None:
        sheet = load_style("publication")
        assert sheet.name == "publication"
        assert sheet.font_family == "sans-serif"

    def test_presentation(self) -> None:
        sheet = load_style("presentation")
        assert sheet.name == "presentation"

    def test_poster(self) -> None:
        sheet = load_style("poster")
        assert sheet.name == "poster"


class TestLoadFromMatplotlibStyle:
    """Load StyleSheet wrapping a matplotlib built-in style."""

    def test_ggplot_style(self) -> None:
        sheet = load_style("ggplot")
        assert sheet.name == "ggplot"
        assert len(sheet.rc_overrides) > 0

    def test_nonexistent_style(self) -> None:
        with pytest.raises(StyleNotFoundError):
            load_style("this-style-definitely-does-not-exist-xyz")


class TestLoadFromYamlFile:
    """Load StyleSheet from a YAML file."""

    def test_yaml_file(self, tmp_path: Path) -> None:
        style_file = tmp_path / "custom.yaml"
        style_file.write_text(
            "name: custom\nfont_family: monospace\nfont_size: 11.0\n",
            encoding="utf-8",
        )
        sheet = load_style(style_file)
        assert sheet.name == "custom"
        assert sheet.font_family == "monospace"

    def test_yaml_file_name_from_stem(self, tmp_path: Path) -> None:
        style_file = tmp_path / "my-style.yaml"
        style_file.write_text("font_size: 9.0\n", encoding="utf-8")
        sheet = load_style(style_file)
        assert sheet.name == "my-style"

    def test_yaml_string_ref_with_search_dirs(self, tmp_path: Path) -> None:
        style_file = tmp_path / "found.yaml"
        style_file.write_text("name: found\n", encoding="utf-8")
        sheet = load_style("found.yaml", search_dirs=(tmp_path,))
        assert sheet.name == "found"

    def test_yaml_name_resolved_via_search(self, tmp_path: Path) -> None:
        style_file = tmp_path / "mystyle.yaml"
        style_file.write_text("name: mystyle\n", encoding="utf-8")
        sheet = load_style("mystyle", search_dirs=(tmp_path,))
        assert sheet.name == "mystyle"

    def test_missing_yaml_file_raises(self) -> None:
        with pytest.raises(StyleNotFoundError):
            load_style(Path("/nonexistent/style.yaml"))

    def test_invalid_yaml_raises(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "bad.yaml"
        bad_file.write_text(":::: not valid yaml ::::\n", encoding="utf-8")
        with pytest.raises(StyleError, match="Failed to parse"):
            load_style(bad_file)

    def test_non_mapping_yaml_raises(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "list.yaml"
        bad_file.write_text("- item1\n- item2\n", encoding="utf-8")
        with pytest.raises(StyleError, match="must contain a YAML mapping"):
            load_style(bad_file)

    def test_mplstyle_file(self, tmp_path: Path) -> None:
        style_file = tmp_path / "custom.mplstyle"
        style_file.write_text("axes.grid: True\nlines.linewidth: 2\n", encoding="utf-8")
        sheet = load_style(style_file)
        assert sheet.name == "custom"
        assert len(sheet.rc_overrides) > 0

    def test_yaml_file_string_ending(self, tmp_path: Path) -> None:
        style_file = tmp_path / "test.yaml"
        style_file.write_text("name: test\n", encoding="utf-8")
        sheet = load_style("test.yaml", search_dirs=(tmp_path,))
        assert sheet.name == "test"

    def test_yaml_file_not_found_raises(self) -> None:
        with pytest.raises(StyleNotFoundError):
            load_style("nonexistent.yaml")


class TestParseMplstyleInlineComments:
    """Regression: _parse_mplstyle must strip inline comments from values."""

    def test_inline_comment_stripped(self, tmp_path: Path) -> None:
        style_file = tmp_path / "commented.mplstyle"
        style_file.write_text(
            "font.size : 12  # points\nlines.linewidth : 1.5  # default\n",
            encoding="utf-8",
        )
        sheet = load_style(style_file)
        rc = sheet.rc_overrides
        # Values should not contain inline comments
        for key, val in rc.items():
            if isinstance(val, str):
                assert "#" not in val, f"{key}={val!r} still contains '#'"

    def test_hash_in_color_value_preserved(self, tmp_path: Path) -> None:
        style_file = tmp_path / "colors.mplstyle"
        style_file.write_text(
            "axes.facecolor : '#ffffff'\n",
            encoding="utf-8",
        )
        sheet = load_style(style_file)
        # Quoted color values with '#' should be preserved
        assert sheet.rc_overrides.get("axes.facecolor") is not None


class TestLoadFromDictAdvanced:
    """Advanced _from_dict paths — version checks, edge cases."""

    def test_style_version_valid(self) -> None:
        sheet = load_style({"name": "versioned", "style_version": 1})
        assert sheet.name == "versioned"

    def test_style_version_too_new_raises(self) -> None:
        with pytest.raises(StyleError, match="newer than supported"):
            load_style({"name": "future", "style_version": 999})

    def test_style_version_not_int_raises(self) -> None:
        with pytest.raises(StyleError, match="must be an integer"):
            load_style({"name": "bad", "style_version": "one"})

    def test_extends_as_list(self) -> None:
        sheet = load_style({"name": "t", "extends": ["a", "b"]})
        assert sheet.extends == ("a", "b")

    def test_extends_non_string_non_list(self) -> None:
        sheet = load_style({"name": "t", "extends": 42})
        assert sheet.extends == ()

    def test_palette_as_tuple(self) -> None:
        sheet = load_style({"name": "t", "palette": ("red", "blue")})
        assert sheet.palette == ("red", "blue")

    def test_palette_non_list_ignored(self) -> None:
        sheet = load_style({"name": "t", "palette": "red"})
        assert sheet.palette is None

    def test_figure_size_wrong_length_ignored(self) -> None:
        sheet = load_style({"name": "t", "figure_size": [7.0]})
        assert sheet.figure_size is None

    def test_rc_overrides_non_dict_ignored(self) -> None:
        sheet = load_style({"name": "t", "rc_overrides": "not a dict"})
        assert sheet.rc_overrides == {}
