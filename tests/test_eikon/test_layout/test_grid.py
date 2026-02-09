"""Tests for eikon.layout._grid — LayoutSpec dataclass."""

from dataclasses import FrozenInstanceError

import pytest

from eikon.layout import LayoutSpec


class TestLayoutSpec:
    """LayoutSpec construction and immutability."""

    def test_defaults(self) -> None:
        spec = LayoutSpec()
        assert spec.rows == 1
        assert spec.cols == 1
        assert spec.width_ratios is None
        assert spec.height_ratios is None
        assert spec.wspace is None
        assert spec.hspace is None
        assert spec.constrained_layout is True

    def test_full_construction(self) -> None:
        spec = LayoutSpec(
            rows=2,
            cols=3,
            width_ratios=(1.0, 2.0, 1.0),
            height_ratios=(1.0, 3.0),
            wspace=0.3,
            hspace=0.4,
            constrained_layout=False,
        )
        assert spec.rows == 2
        assert spec.cols == 3
        assert spec.width_ratios == (1.0, 2.0, 1.0)
        assert spec.height_ratios == (1.0, 3.0)
        assert spec.wspace == 0.3
        assert spec.hspace == 0.4
        assert spec.constrained_layout is False

    def test_frozen(self) -> None:
        spec = LayoutSpec()
        with pytest.raises(FrozenInstanceError):
            spec.rows = 5  # type: ignore[misc]

    def test_equality(self) -> None:
        a = LayoutSpec(rows=2, cols=2)
        b = LayoutSpec(rows=2, cols=2)
        assert a == b
