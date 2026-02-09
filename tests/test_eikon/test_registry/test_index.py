"""Tests for eikon.registry._index — YAML manifest I/O."""

from __future__ import annotations

from pathlib import Path

import pytest
import yaml

from eikon.exceptions import RegistryError
from eikon.registry._index import load_manifest, save_manifest


class TestLoadManifest:
    """load_manifest reads YAML and returns entry dict."""

    def test_missing_file_returns_empty(self, tmp_path: Path) -> None:
        result = load_manifest(tmp_path / "missing.yaml")
        assert result == {}

    def test_empty_file_returns_empty(self, tmp_path: Path) -> None:
        manifest = tmp_path / "empty.yaml"
        manifest.write_text("", encoding="utf-8")
        result = load_manifest(manifest)
        assert result == {}

    def test_valid_manifest(self, tmp_path: Path) -> None:
        manifest = tmp_path / "registry.yaml"
        data = {
            "fig1": {"tags": ["a"], "group": "g1", "metadata": {}},
        }
        manifest.write_text(yaml.dump(data), encoding="utf-8")
        result = load_manifest(manifest)
        assert "fig1" in result
        assert result["fig1"]["tags"] == ["a"]

    def test_non_mapping_raises(self, tmp_path: Path) -> None:
        manifest = tmp_path / "bad.yaml"
        manifest.write_text("- item1\n- item2\n", encoding="utf-8")
        with pytest.raises(RegistryError, match="not a YAML mapping"):
            load_manifest(manifest)


class TestSaveManifest:
    """save_manifest writes YAML to disk."""

    def test_creates_file(self, tmp_path: Path) -> None:
        manifest = tmp_path / "sub" / "registry.yaml"
        entries = {"fig1": {"tags": ["a"], "group": "g1", "metadata": {}}}
        save_manifest(manifest, entries)
        assert manifest.exists()
        loaded = yaml.safe_load(manifest.read_text(encoding="utf-8"))
        assert loaded["fig1"]["tags"] == ["a"]

    def test_roundtrip(self, tmp_path: Path) -> None:
        manifest = tmp_path / "registry.yaml"
        entries = {
            "x": {"tags": ["t1", "t2"], "group": "g", "metadata": {"k": "v"}},
            "y": {"tags": [], "group": "", "metadata": {}},
        }
        save_manifest(manifest, entries)
        loaded = load_manifest(manifest)
        assert set(loaded) == {"x", "y"}
        assert loaded["x"]["tags"] == ["t1", "t2"]
