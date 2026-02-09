"""Tests for eikon.registry._locking — advisory file locking."""

from __future__ import annotations

from pathlib import Path

from eikon.registry._locking import registry_lock


class TestRegistryLock:
    """registry_lock acquires and releases exclusive locks."""

    def test_basic_lock_unlock(self, tmp_path: Path) -> None:
        target = tmp_path / "manifest.yaml"
        target.write_text("", encoding="utf-8")
        with registry_lock(target):
            pass  # lock held, then released

    def test_creates_lock_file(self, tmp_path: Path) -> None:
        target = tmp_path / "manifest.yaml"
        target.write_text("", encoding="utf-8")
        with registry_lock(target):
            lock_file = target.with_suffix(".yaml.lock")
            assert lock_file.exists()

    def test_creates_parent_dirs(self, tmp_path: Path) -> None:
        target = tmp_path / "sub" / "dir" / "manifest.yaml"
        with registry_lock(target):
            assert target.parent.exists()

    def test_reentrant_after_release(self, tmp_path: Path) -> None:
        target = tmp_path / "manifest.yaml"
        target.write_text("", encoding="utf-8")
        with registry_lock(target):
            pass
        # Should be able to acquire again
        with registry_lock(target):
            pass
