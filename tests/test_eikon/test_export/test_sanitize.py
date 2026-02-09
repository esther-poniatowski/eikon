"""Tests for eikon.export._sanitize — filename sanitization."""

from eikon.export._sanitize import sanitize_filename


class TestSanitizeFilename:
    """sanitize_filename produces safe, deterministic filenames."""

    def test_simple_name(self) -> None:
        assert sanitize_filename("fig1") == "fig1"

    def test_strips_whitespace(self) -> None:
        assert sanitize_filename("  fig1  ") == "fig1"

    def test_replaces_illegal_chars(self) -> None:
        result = sanitize_filename('fig<1>:2"/\\|?*')
        assert "<" not in result
        assert ">" not in result
        assert ":" not in result
        assert '"' not in result
        assert "\\" not in result
        assert "|" not in result
        assert "?" not in result
        assert "*" not in result

    def test_collapses_underscores(self) -> None:
        result = sanitize_filename("fig___name")
        assert "___" not in result

    def test_strips_trailing_underscores(self) -> None:
        result = sanitize_filename("fig<>")
        assert not result.endswith("_")

    def test_empty_returns_unnamed(self) -> None:
        assert sanitize_filename("") == "unnamed"

    def test_whitespace_only_returns_unnamed(self) -> None:
        assert sanitize_filename("   ") == "unnamed"

    def test_all_illegal_returns_unnamed(self) -> None:
        assert sanitize_filename("<>:") == "unnamed"

    def test_truncates_long_names(self) -> None:
        result = sanitize_filename("a" * 300)
        assert len(result) <= 200

    def test_null_bytes_removed(self) -> None:
        result = sanitize_filename("fig\x00name")
        assert "\x00" not in result

    def test_control_chars_removed(self) -> None:
        result = sanitize_filename("fig\x01\x02name")
        assert "\x01" not in result
        assert "\x02" not in result

    def test_hyphens_and_dots_preserved(self) -> None:
        assert sanitize_filename("fig-1.overview") == "fig-1.overview"
