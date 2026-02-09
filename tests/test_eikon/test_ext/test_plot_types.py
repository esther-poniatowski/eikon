"""Tests for eikon.ext._plot_types — plot type registry."""

from typing import Any

import pytest

from eikon.exceptions import UnknownPlotTypeError
from eikon.ext._plot_types import (
    _clear_registry,
    get_plot_type,
    list_plot_types,
    plot_type,
    register_plot_type,
)


@pytest.fixture(autouse=True)
def _clean_registry() -> Any:
    """Clear the registry before and after each test."""
    _clear_registry()
    yield
    _clear_registry()


class TestRegisterAndGet:
    """Registration and lookup."""

    def test_register_and_get(self) -> None:
        def my_plot(ax: Any, /, **kwargs: Any) -> None:
            pass

        register_plot_type("myplot", my_plot)
        assert get_plot_type("myplot") is my_plot

    def test_get_unregistered_raises(self) -> None:
        with pytest.raises(UnknownPlotTypeError, match="nope"):
            get_plot_type("nope")

    def test_list_plot_types(self) -> None:
        register_plot_type("b", lambda ax, /, **kw: None)
        register_plot_type("a", lambda ax, /, **kw: None)
        assert list_plot_types() == ["a", "b"]

    def test_overwrite(self) -> None:
        fn1 = lambda ax, /, **kw: None  # noqa: E731
        fn2 = lambda ax, /, **kw: None  # noqa: E731
        register_plot_type("x", fn1)
        register_plot_type("x", fn2)
        assert get_plot_type("x") is fn2


class TestDecorator:
    """@plot_type decorator."""

    def test_decorator_registers(self) -> None:
        @plot_type("decorated")
        def draw(ax: Any, /, **kwargs: Any) -> None:
            pass

        assert get_plot_type("decorated") is draw

    def test_decorator_returns_original(self) -> None:
        @plot_type("original")
        def draw(ax: Any, /, **kwargs: Any) -> None:
            pass

        # The function is returned unmodified
        assert callable(draw)
