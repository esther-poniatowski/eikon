"""Figure registry for tracking and organizing figures.

Provides persistent storage of figure metadata in a YAML manifest,
with CRUD operations, tag/group filtering, and advisory file locking
for concurrent access safety.

Public API
----------
Registry
    In-memory registry backed by a YAML manifest file.
filter_entries
    Query helper for filtering by tags and groups.
"""

from eikon.registry._query import filter_by_group, filter_by_tags, filter_entries
from eikon.registry._registry import Registry

__all__ = [
    "Registry",
    "filter_by_group",
    "filter_by_tags",
    "filter_entries",
]
