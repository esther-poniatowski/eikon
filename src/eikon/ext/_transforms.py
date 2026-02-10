"""Registry and application of data transforms.

Transforms are simple callables that accept a data object and return a
transformed data object. They are addressed by string name to keep the
declarative YAML surface stable.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from eikon.exceptions import RenderError

__all__ = ["register_transform", "apply_transforms", "list_transforms"]

_TRANSFORMS: dict[str, Callable[[Any], Any]] = {}


def register_transform(name: str, fn: Callable[[Any], Any]) -> None:
    _TRANSFORMS[name] = fn


def list_transforms() -> list[str]:
    return sorted(_TRANSFORMS.keys())


def clear_transforms() -> None:
    """Remove all registered transforms (testing/cleanup helper)."""
    _TRANSFORMS.clear()


def apply_transforms(data: Any, names: tuple[str, ...]) -> Any:
    result = data
    for name in names:
        fn = _TRANSFORMS.get(name)
        if fn is None:
            raise RenderError(f"Unknown data transform: {name!r}")
        result = fn(result)
    return result
