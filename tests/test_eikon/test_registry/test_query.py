"""Tests for eikon.registry._query — tag and group filtering."""

from __future__ import annotations

from eikon.registry._query import filter_by_group, filter_by_tags, filter_entries


def _sample_entries() -> dict[str, dict[str, object]]:
    return {
        "fig-a": {"tags": ["neural", "overview"], "group": "manuscript-1"},
        "fig-b": {"tags": ["neural"], "group": "manuscript-2"},
        "fig-c": {"tags": ["behavioral", "overview"], "group": "manuscript-1"},
        "fig-d": {"tags": [], "group": ""},
    }


class TestFilterByTags:
    """filter_by_tags returns entries matching any/all tags."""

    def test_empty_tags_returns_all(self) -> None:
        entries = _sample_entries()
        result = filter_by_tags(entries, ())
        assert len(result) == 4

    def test_single_tag_any(self) -> None:
        entries = _sample_entries()
        result = filter_by_tags(entries, ("neural",))
        assert set(result) == {"fig-a", "fig-b"}

    def test_multiple_tags_any(self) -> None:
        entries = _sample_entries()
        result = filter_by_tags(entries, ("neural", "behavioral"))
        assert set(result) == {"fig-a", "fig-b", "fig-c"}

    def test_multiple_tags_match_all(self) -> None:
        entries = _sample_entries()
        result = filter_by_tags(entries, ("neural", "overview"), match_all=True)
        assert set(result) == {"fig-a"}

    def test_no_match(self) -> None:
        entries = _sample_entries()
        result = filter_by_tags(entries, ("nonexistent",))
        assert result == {}


class TestFilterByGroup:
    """filter_by_group returns entries belonging to a group."""

    def test_match(self) -> None:
        entries = _sample_entries()
        result = filter_by_group(entries, "manuscript-1")
        assert set(result) == {"fig-a", "fig-c"}

    def test_empty_group_match(self) -> None:
        entries = _sample_entries()
        result = filter_by_group(entries, "")
        assert set(result) == {"fig-d"}

    def test_no_match(self) -> None:
        entries = _sample_entries()
        result = filter_by_group(entries, "nonexistent")
        assert result == {}


class TestFilterEntries:
    """filter_entries combines tag and group filters."""

    def test_no_filters_returns_all(self) -> None:
        entries = _sample_entries()
        result = filter_entries(entries)
        assert len(result) == 4

    def test_tag_and_group(self) -> None:
        entries = _sample_entries()
        result = filter_entries(entries, tags=("neural",), group="manuscript-1")
        assert set(result) == {"fig-a"}

    def test_only_group(self) -> None:
        entries = _sample_entries()
        result = filter_entries(entries, group="manuscript-2")
        assert set(result) == {"fig-b"}

    def test_only_tags(self) -> None:
        entries = _sample_entries()
        result = filter_entries(entries, tags=("overview",))
        assert set(result) == {"fig-a", "fig-c"}
