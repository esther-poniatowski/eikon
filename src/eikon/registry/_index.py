"""YAML manifest I/O for the figure registry.

The manifest is a YAML file (default ``eikon-registry.yaml``) that
persists registry entries across sessions.  Each entry stores the
figure name, tags, group, and the timestamp of last registration.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

from eikon.exceptions import RegistryError
from eikon.registry._locking import registry_lock

__all__ = ["load_manifest", "save_manifest"]


def load_manifest(path: Path) -> dict[str, dict[str, Any]]:
    """Load the registry manifest from a YAML file.

    Parameters
    ----------
    path : Path
        Path to the manifest file.

    Returns
    -------
    dict[str, dict[str, Any]]
        Mapping of figure names to their registry entries.

    Raises
    ------
    RegistryError
        If the file exists but is not a valid YAML mapping.
    """
    if not path.exists():
        return {}

    with registry_lock(path):
        text = path.read_text(encoding="utf-8")

    if not text.strip():
        return {}

    data = yaml.safe_load(text)
    if data is None:
        return {}
    if not isinstance(data, dict):
        msg = f"Registry manifest is not a YAML mapping: {path}"
        raise RegistryError(msg)

    return dict(data)


def save_manifest(path: Path, entries: dict[str, dict[str, Any]]) -> None:
    """Save the registry manifest to a YAML file.

    Parameters
    ----------
    path : Path
        Path to the manifest file.
    entries : dict[str, dict[str, Any]]
        Mapping of figure names to their registry entries.
    """
    path.parent.mkdir(parents=True, exist_ok=True)

    with registry_lock(path):
        path.write_text(
            yaml.dump(
                entries,
                default_flow_style=False,
                sort_keys=True,
                allow_unicode=True,
            ),
            encoding="utf-8",
        )
