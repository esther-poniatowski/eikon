"""Explicit extension registry and runtime bootstrap helpers."""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from eikon.exceptions import RenderError, UnknownPlotTypeError

__all__ = [
    "ExtensionRegistry",
    "build_runtime_registry",
    "get_default_registry",
]


class ExtensionRegistry:
    """Container for plot types, hooks, and transforms."""

    def __init__(
        self,
        *,
        plot_types: dict[str, Callable[..., None]] | None = None,
        hooks: dict[Any, list[Callable[..., Any]]] | None = None,
        transforms: dict[str, Callable[[Any], Any]] | None = None,
    ) -> None:
        self.plot_types = dict(plot_types or {})
        self.hooks = {hook: list(callbacks) for hook, callbacks in (hooks or {}).items()}
        self.transforms = dict(transforms or {})

    def clone(self) -> "ExtensionRegistry":
        return ExtensionRegistry(
            plot_types=self.plot_types,
            hooks=self.hooks,
            transforms=self.transforms,
        )

    def register_plot_type(self, name: str, fn: Callable[..., None]) -> None:
        self.plot_types[name] = fn

    def get_plot_type(self, name: str) -> Callable[..., None]:
        fn = self.plot_types.get(name)
        if fn is None:
            raise UnknownPlotTypeError(name, list(self.plot_types.keys()))
        return fn

    def list_plot_types(self) -> list[str]:
        return sorted(self.plot_types.keys())

    def clear_plot_types(self) -> None:
        self.plot_types.clear()

    def register_hook(self, hook: Any, fn: Callable[..., Any]) -> None:
        self.hooks.setdefault(hook, []).append(fn)

    def fire_hook(self, hook: Any, **kwargs: Any) -> None:
        for fn in self.hooks.get(hook, []):
            fn(**kwargs)

    def clear_hooks(self) -> None:
        for hook in list(self.hooks):
            self.hooks[hook] = []

    def register_transform(self, name: str, fn: Callable[[Any], Any]) -> None:
        self.transforms[name] = fn

    def list_transforms(self) -> list[str]:
        return sorted(self.transforms.keys())

    def clear_transforms(self) -> None:
        self.transforms.clear()

    def apply_transforms(self, data: Any, names: tuple[str, ...]) -> Any:
        result = data
        for name in names:
            fn = self.transforms.get(name)
            if fn is None:
                raise RenderError(f"Unknown data transform: {name!r}")
            result = fn(result)
        return result


_DEFAULT_REGISTRY = ExtensionRegistry()
_BOOTSTRAPPED = False


def get_default_registry() -> ExtensionRegistry:
    """Return the mutable process-local default registry."""
    return _DEFAULT_REGISTRY


def build_runtime_registry() -> ExtensionRegistry:
    """Return a bootstrapped snapshot for one render/runtime session."""
    _bootstrap_default_registry()
    return _DEFAULT_REGISTRY.clone()


def _bootstrap_default_registry() -> None:
    global _BOOTSTRAPPED
    if _BOOTSTRAPPED:
        return
    import eikon.contrib  # noqa: F401
    from eikon.ext._discovery import discover_plugins

    discover_plugins()
    _BOOTSTRAPPED = True
