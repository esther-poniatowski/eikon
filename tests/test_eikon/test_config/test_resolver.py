"""Tests for eikon.config._resolver."""

from pathlib import Path

import pytest

from eikon.config._resolver import discover_project_root, resolve_paths
from eikon.config._schema import PathsConfig
from eikon.exceptions import ConfigNotFoundError


class TestDiscoverProjectRoot:
    def test_finds_eikon_yaml(self, tmp_project: Path):
        root = discover_project_root(tmp_project)
        assert root == tmp_project

    def test_finds_from_subdirectory(self, tmp_project: Path):
        sub = tmp_project / "specs"
        root = discover_project_root(sub)
        assert root == tmp_project

    def test_raises_when_not_found(self, tmp_path: Path):
        with pytest.raises(ConfigNotFoundError):
            discover_project_root(tmp_path)


class TestResolvePaths:
    def test_resolves_relative_to_root(self, tmp_project: Path):
        config = PathsConfig(output_dir=Path("figures"))
        resolved = resolve_paths(config, project_root=tmp_project)
        assert resolved.project_root == tmp_project
        assert resolved.output_dir == tmp_project / "figures"

    def test_all_paths_absolute(self, tmp_project: Path):
        config = PathsConfig()
        resolved = resolve_paths(config, project_root=tmp_project)
        assert resolved.project_root.is_absolute()
        assert resolved.output_dir.is_absolute()
        assert resolved.styles_dir.is_absolute()
        assert resolved.specs_dir.is_absolute()
        assert resolved.data_dir.is_absolute()
