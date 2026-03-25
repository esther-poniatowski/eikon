"""Registry and application of data transforms.

Transforms are simple callables that accept a data object and return a
transformed data object. They are addressed by string name to keep the
declarative YAML surface stable.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from eikon.ext._registry import get_default_registry

__all__ = ["register_transform", "apply_transforms", "list_transforms"]


def register_transform(name: str, fn: Callable[[Any], Any]) -> None:
    get_default_registry().register_transform(name, fn)


def list_transforms() -> list[str]:
    return get_default_registry().list_transforms()


def clear_transforms() -> None:
    """Remove all registered transforms (testing/cleanup helper)."""
    get_default_registry().clear_transforms()


def apply_transforms(data: Any, names: tuple[str, ...]) -> Any:
    return get_default_registry().apply_transforms(data, names)
