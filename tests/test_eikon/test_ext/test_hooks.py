"""Tests for eikon.ext._hooks — lifecycle hook system."""

from typing import Any

import pytest

from eikon.ext._hooks import HookName, clear_hooks, fire_hook, register_hook


@pytest.fixture(autouse=True)
def _clean_hooks() -> Any:
    """Clear hooks before and after each test."""
    clear_hooks()
    yield
    clear_hooks()


class TestHooks:
    """Hook registration and firing."""

    def test_register_and_fire(self) -> None:
        calls: list[str] = []
        register_hook(HookName.PRE_RENDER, lambda **kw: calls.append("fired"))
        fire_hook(HookName.PRE_RENDER)
        assert calls == ["fired"]

    def test_fire_passes_kwargs(self) -> None:
        received: dict[str, Any] = {}

        def capture(**kwargs: Any) -> None:
            received.update(kwargs)

        register_hook(HookName.POST_RENDER, capture)
        fire_hook(HookName.POST_RENDER, spec="test", layout="mock")
        assert received == {"spec": "test", "layout": "mock"}

    def test_multiple_hooks(self) -> None:
        order: list[int] = []
        register_hook(HookName.PRE_EXPORT, lambda **kw: order.append(1))
        register_hook(HookName.PRE_EXPORT, lambda **kw: order.append(2))
        fire_hook(HookName.PRE_EXPORT)
        assert order == [1, 2]

    def test_no_hooks_is_noop(self) -> None:
        fire_hook(HookName.POST_EXPORT)  # should not raise

    def test_clear_hooks(self) -> None:
        calls: list[str] = []
        register_hook(HookName.PRE_RENDER, lambda **kw: calls.append("x"))
        clear_hooks()
        fire_hook(HookName.PRE_RENDER)
        assert calls == []

    def test_all_hook_names_exist(self) -> None:
        assert len(HookName) == 4
        names = {h.value for h in HookName}
        assert names == {"pre_render", "post_render", "pre_export", "post_export"}
