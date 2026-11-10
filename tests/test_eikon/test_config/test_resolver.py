"""Tests for eikon.config._resolver."""

from pathlib import Path

import pytest

from eikon.config._resolver import discover_project_root, locate_config, resolve_paths
from eikon.config._schema import PathsConfig
from eikon.exceptions import ConfigConflictError


class TestDiscoverProjectRoot:
    def test_finds_eikon_yml(self, tmp_project: Path):
        root = discover_project_root(tmp_project)
        assert root == tmp_project

    def test_finds_from_subdirectory(self, tmp_project: Path):
        sub = tmp_project / "specs"
        root = discover_project_root(sub)
        assert root == tmp_project

    def test_current_folder_when_no_settings_file(self, tmp_path: Path):
        assert discover_project_root(tmp_path) == tmp_path.resolve()

    def test_finds_config_in_config_tools(self, tmp_path: Path):
        (tmp_path / "config" / "tools").mkdir(parents=True)
        (tmp_path / "config" / "tools" / "eikon.yml").write_text("{}\n")
        (tmp_path / "specs").mkdir()
        assert discover_project_root(tmp_path / "specs") == tmp_path.resolve()

    def test_retired_settings_name_is_not_found(self, tmp_path: Path):
        (tmp_path / "eikon.yaml").write_text("{}\n")
        (tmp_path / "specs").mkdir()
        assert discover_project_root(tmp_path / "specs") == (tmp_path / "specs").resolve()

    def test_env_root_accepts_config_tools(self, tmp_path: Path, monkeypatch):
        (tmp_path / "config" / "tools").mkdir(parents=True)
        (tmp_path / "config" / "tools" / "eikon.yml").write_text("{}\n")
        monkeypatch.setenv("EIKON_ROOT", str(tmp_path))
        assert discover_project_root() == tmp_path.resolve()


class TestLocateConfig:
    def test_config_tools_file_found_alone(self, tmp_path: Path):
        (tmp_path / "config" / "tools").mkdir(parents=True)
        (tmp_path / "config" / "tools" / "eikon.yml").write_text("{}\n")
        assert locate_config(tmp_path) == tmp_path / "config" / "tools" / "eikon.yml"

    def test_root_file_found_alone(self, tmp_path: Path):
        (tmp_path / "eikon.yml").write_text("{}\n")
        assert locate_config(tmp_path) == tmp_path / "eikon.yml"

    def test_none_without_settings_file(self, tmp_path: Path):
        assert locate_config(tmp_path) is None

    def test_both_files_are_an_error_naming_both(self, tmp_path: Path):
        (tmp_path / "config" / "tools").mkdir(parents=True)
        (tmp_path / "config" / "tools" / "eikon.yml").write_text("{}\n")
        (tmp_path / "eikon.yml").write_text("{}\n")
        with pytest.raises(ConfigConflictError) as info:
            locate_config(tmp_path)
        message = str(info.value)
        assert str(tmp_path / "config" / "tools" / "eikon.yml") in message
        assert str(tmp_path / "eikon.yml") in message


class TestRootEnvironment:
    """``EIKON_ROOT`` names the root; the retired ``EIKON_PROJECT_ROOT`` is ignored."""

    def test_eikon_root(self, tmp_path: Path, monkeypatch):
        root = tmp_path / "named"
        root.mkdir()
        (root / "eikon.yml").write_text("{}\n")
        monkeypatch.setenv("EIKON_ROOT", str(root))
        assert discover_project_root(tmp_path) == root.resolve()

    def test_eikon_root_without_settings_file(self, tmp_path: Path, monkeypatch):
        root = tmp_path / "bare"
        root.mkdir()
        monkeypatch.setenv("EIKON_ROOT", str(root))
        assert discover_project_root(tmp_path) == root.resolve()

    def test_retired_variable_is_ignored(self, tmp_path: Path, monkeypatch):
        former = tmp_path / "former"
        former.mkdir()
        (former / "eikon.yml").write_text("{}\n")
        start = tmp_path / "start"
        start.mkdir()
        monkeypatch.setenv("EIKON_PROJECT_ROOT", str(former))
        assert discover_project_root(start) == start.resolve()


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
