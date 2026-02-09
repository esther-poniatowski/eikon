"""Tests for eikon.registry._registry — Registry class."""

from __future__ import annotations

from pathlib import Path

import pytest

from eikon.exceptions import RegistryError
from eikon.registry._registry import Registry


@pytest.fixture()
def registry(tmp_path: Path) -> Registry:
    """Create a fresh Registry backed by a temp file."""
    reg = Registry(tmp_path / "registry.yaml")
    reg.load()
    return reg


class TestRegister:
    """Registry.register adds entries with conflict handling."""

    def test_register_new(self, registry: Registry) -> None:
        registry.register("fig1", tags=("a",), group="g1")
        assert "fig1" in registry
        assert len(registry) == 1

    def test_register_sets_timestamp(self, registry: Registry) -> None:
        registry.register("fig1")
        entry = registry.get("fig1")
        assert "registered_at" in entry

    def test_on_conflict_update(self, registry: Registry) -> None:
        registry.register("fig1", group="old")
        registry.register("fig1", group="new", on_conflict="update")
        assert registry.get("fig1")["group"] == "new"

    def test_on_conflict_fail(self, registry: Registry) -> None:
        registry.register("fig1")
        with pytest.raises(RegistryError, match="already registered"):
            registry.register("fig1", on_conflict="fail")

    def test_on_conflict_skip(self, registry: Registry) -> None:
        registry.register("fig1", group="original")
        registry.register("fig1", group="ignored", on_conflict="skip")
        assert registry.get("fig1")["group"] == "original"


class TestGet:
    """Registry.get returns entry data or raises."""

    def test_get_existing(self, registry: Registry) -> None:
        registry.register("fig1", tags=("x",))
        entry = registry.get("fig1")
        assert entry["tags"] == ["x"]

    def test_get_returns_copy(self, registry: Registry) -> None:
        registry.register("fig1")
        entry = registry.get("fig1")
        entry["tags"] = ["mutated"]
        assert registry.get("fig1")["tags"] == []

    def test_get_missing_raises(self, registry: Registry) -> None:
        with pytest.raises(RegistryError, match="not registered"):
            registry.get("missing")


class TestRemove:
    """Registry.remove deletes entries or raises."""

    def test_remove_existing(self, registry: Registry) -> None:
        registry.register("fig1")
        registry.remove("fig1")
        assert "fig1" not in registry

    def test_remove_missing_raises(self, registry: Registry) -> None:
        with pytest.raises(RegistryError, match="not registered"):
            registry.remove("nonexistent")


class TestListAll:
    """Registry.list_all returns sorted names."""

    def test_empty(self, registry: Registry) -> None:
        assert registry.list_all() == []

    def test_sorted(self, registry: Registry) -> None:
        registry.register("z")
        registry.register("a")
        registry.register("m")
        assert registry.list_all() == ["a", "m", "z"]


class TestQuery:
    """Registry.query delegates to filter_entries."""

    def test_query_by_tag(self, registry: Registry) -> None:
        registry.register("fig1", tags=("neural",))
        registry.register("fig2", tags=("behavioral",))
        result = registry.query(tags=("neural",))
        assert set(result) == {"fig1"}

    def test_query_by_group(self, registry: Registry) -> None:
        registry.register("fig1", group="ms1")
        registry.register("fig2", group="ms2")
        result = registry.query(group="ms1")
        assert set(result) == {"fig1"}

    def test_query_no_filters(self, registry: Registry) -> None:
        registry.register("fig1")
        registry.register("fig2")
        result = registry.query()
        assert len(result) == 2


class TestPersistence:
    """Registry.save/load roundtrip."""

    def test_save_and_reload(self, tmp_path: Path) -> None:
        path = tmp_path / "registry.yaml"
        reg1 = Registry(path)
        reg1.load()
        reg1.register("fig1", tags=("a", "b"), group="g")
        reg1.save()

        reg2 = Registry(path)
        reg2.load()
        assert "fig1" in reg2
        assert reg2.get("fig1")["group"] == "g"
        assert reg2.get("fig1")["tags"] == ["a", "b"]
