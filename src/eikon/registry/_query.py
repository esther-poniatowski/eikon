"""Query and filter logic for registry entries.

Provides functions to filter registry entries by tags, group,
or arbitrary predicates.
"""

from __future__ import annotations

from typing import Any

__all__ = ["filter_by_tags", "filter_by_group", "filter_entries"]


def filter_by_tags(
    entries: dict[str, dict[str, Any]],
    tags: tuple[str, ...],
    *,
    match_all: bool = False,
) -> dict[str, dict[str, Any]]:
    """Filter entries that have any (or all) of the given tags.

    Parameters
    ----------
    entries : dict[str, dict[str, Any]]
        Registry entries to filter.
    tags : tuple[str, ...]
        Tags to match against.
    match_all : bool
        If ``True``, an entry must have **all** tags.
        If ``False`` (default), an entry must have **any** tag.

    Returns
    -------
    dict[str, dict[str, Any]]
        Filtered entries.
    """
    if not tags:
        return dict(entries)

    tag_set = set(tags)
    result: dict[str, dict[str, Any]] = {}

    for name, entry in entries.items():
        entry_tags = set(entry.get("tags", []))
        if match_all:
            if tag_set <= entry_tags:
                result[name] = entry
        else:
            if tag_set & entry_tags:
                result[name] = entry

    return result


def filter_by_group(
    entries: dict[str, dict[str, Any]],
    group: str,
) -> dict[str, dict[str, Any]]:
    """Filter entries belonging to a specific group.

    Parameters
    ----------
    entries : dict[str, dict[str, Any]]
        Registry entries to filter.
    group : str
        Group name to match.

    Returns
    -------
    dict[str, dict[str, Any]]
        Filtered entries.
    """
    return {
        name: entry
        for name, entry in entries.items()
        if entry.get("group", "") == group
    }


def filter_entries(
    entries: dict[str, dict[str, Any]],
    *,
    tags: tuple[str, ...] = (),
    group: str = "",
    match_all_tags: bool = False,
) -> dict[str, dict[str, Any]]:
    """Apply tag and group filters in sequence.

    Parameters
    ----------
    entries : dict[str, dict[str, Any]]
        Registry entries to filter.
    tags : tuple[str, ...]
        Tags to match.  Empty = no tag filter.
    group : str
        Group name.  Empty = no group filter.
    match_all_tags : bool
        Whether tag matching requires all tags.

    Returns
    -------
    dict[str, dict[str, Any]]
        Filtered entries.
    """
    result = dict(entries)

    if tags:
        result = filter_by_tags(result, tags, match_all=match_all_tags)

    if group:
        result = filter_by_group(result, group)

    return result
