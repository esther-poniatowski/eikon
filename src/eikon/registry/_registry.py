"""Registry class — CRUD operations on the figure registry.

The :class:`Registry` provides a high-level API for managing figure
entries: registering, querying, removing, and persisting to YAML.
"""

from __future__ import annotations

import datetime
from pathlib import Path
from typing import Any, Literal

from eikon.exceptions import RegistryError
from eikon.registry._index import load_manifest, save_manifest
from eikon.registry._query import filter_entries

__all__ = ["Registry"]


class Registry:
    """In-memory figure registry backed by a YAML manifest.

    Parameters
    ----------
    path : Path
        Path to the YAML manifest file.

    Attributes
    ----------
    path : Path
        Manifest file path.
    """

    def __init__(self, path: Path) -> None:
        self.path = path
        self._entries: dict[str, dict[str, Any]] = {}

    def load(self) -> None:
        """Load entries from the manifest file.

        If the file does not exist, the registry starts empty.
        """
        self._entries = load_manifest(self.path)

    def save(self) -> None:
        """Persist current entries to the manifest file."""
        save_manifest(self.path, self._entries)

    def register(
        self,
        name: str,
        *,
        tags: tuple[str, ...] = (),
        group: str = "",
        metadata: dict[str, str] | None = None,
        on_conflict: Literal["update", "fail", "skip"] = "update",
        spec_path: str | None = None,
    ) -> None:
        """Register a figure in the registry.

        Parameters
        ----------
        name : str
            Figure name (unique identifier).
        tags : tuple[str, ...]
            Organizational tags.
        group : str
            Grouping key (e.g. ``"manuscript-1"``).
            metadata : dict[str, str], optional
                Arbitrary metadata fields.
            on_conflict : {"update", "fail", "skip"}
                How to handle duplicate names.
                - ``"update"`` (default) — replace the existing entry.
                - ``"fail"`` — raise ``RegistryError``.
                - ``"skip"`` — keep the existing entry.
            spec_path : str, optional
                Path to the figure specification YAML file (relative or absolute).

        Raises
        ------
        RegistryError
            If ``on_conflict="fail"`` and the name already exists.
        """
        if name in self._entries:
            if on_conflict == "fail":
                msg = f"Figure {name!r} is already registered."
                raise RegistryError(msg)
            if on_conflict == "skip":
                return

        self._entries[name] = {
            "tags": list(tags),
            "group": group,
            "metadata": dict(metadata) if metadata else {},
            "spec_path": spec_path or "",
            "registered_at": datetime.datetime.now(tz=datetime.UTC).isoformat(),
        }

    def get(self, name: str) -> dict[str, Any]:
        """Get a registry entry by name.

        Parameters
        ----------
        name : str
            Figure name.

        Returns
        -------
        dict[str, Any]
            The entry data.

        Raises
        ------
        RegistryError
            If the name is not registered.
        """
        entry = self._entries.get(name)
        if entry is None:
            msg = f"Figure {name!r} is not registered."
            raise RegistryError(msg)
        return dict(entry)

    def remove(self, name: str) -> None:
        """Remove a figure from the registry.

        Parameters
        ----------
        name : str
            Figure name.

        Raises
        ------
        RegistryError
            If the name is not registered.
        """
        if name not in self._entries:
            msg = f"Figure {name!r} is not registered."
            raise RegistryError(msg)
        del self._entries[name]

    def list_all(self) -> list[str]:
        """Return a sorted list of all registered figure names."""
        return sorted(self._entries.keys())

    def query(
        self,
        *,
        tags: tuple[str, ...] = (),
        group: str = "",
        match_all_tags: bool = False,
    ) -> dict[str, dict[str, Any]]:
        """Query the registry with optional tag and group filters.

        Parameters
        ----------
        tags : tuple[str, ...]
            Tags to match.  Empty = no tag filter.
        group : str
            Group to match.  Empty = no group filter.
        match_all_tags : bool
            If ``True``, entries must have **all** tags.

        Returns
        -------
        dict[str, dict[str, Any]]
            Matching entries.
        """
        return filter_entries(
            self._entries,
            tags=tags,
            group=group,
            match_all_tags=match_all_tags,
        )

    def __len__(self) -> int:
        return len(self._entries)

    def __contains__(self, name: str) -> bool:
        return name in self._entries
