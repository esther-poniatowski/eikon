"""Tests for eikon.config._resolver."""

import warnings
from pathlib import Path

import pytest

from eikon.config._resolver import discover_project_root, locate_config, resolve_paths
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

    def test_finds_config_in_config_tools(self, tmp_path: Path):
        (tmp_path / "config" / "tools").mkdir(parents=True)
        (tmp_path / "config" / "tools" / "eikon.yaml").write_text("{}\n")
        (tmp_path / "specs").mkdir()
        assert discover_project_root(tmp_path / "specs") == tmp_path.resolve()

    def test_config_tools_file_takes_precedence(self, tmp_path: Path):
        (tmp_path / "config" / "tools").mkdir(parents=True)
        (tmp_path / "config" / "tools" / "eikon.yaml").write_text("{}\n")
        (tmp_path / "eikon.yaml").write_text("{}\n")
        assert locate_config(tmp_path) == tmp_path / "config" / "tools" / "eikon.yaml"

    def test_root_file_found_alone(self, tmp_path: Path):
        (tmp_path / "eikon.yaml").write_text("{}\n")
        assert locate_config(tmp_path) == tmp_path / "eikon.yaml"

    def test_env_root_accepts_config_tools(self, tmp_path: Path, monkeypatch):
        (tmp_path / "config" / "tools").mkdir(parents=True)
        (tmp_path / "config" / "tools" / "eikon.yaml").write_text("{}\n")
        monkeypatch.delenv("EIKON_PROJECT_ROOT", raising=False)
        monkeypatch.setenv("EIKON_ROOT", str(tmp_path))
        assert discover_project_root() == tmp_path.resolve()


class TestRootEnvironment:
    """``EIKON_ROOT`` names the root; the deprecated ``EIKON_PROJECT_ROOT`` is read with a warning."""

    @staticmethod
    def _project(path: Path) -> Path:
        path.mkdir()
        (path / "eikon.yaml").write_text("{}\n")
        return path.resolve()

    def test_eikon_root(self, tmp_path: Path, monkeypatch):
        root = self._project(tmp_path / "new")
        monkeypatch.delenv("EIKON_PROJECT_ROOT", raising=False)
        monkeypatch.setenv("EIKON_ROOT", str(root))
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            assert discover_project_root(tmp_path) == root

    def test_eikon_root_wins_over_deprecated_variable(self, tmp_path: Path, monkeypatch):
        root = self._project(tmp_path / "new")
        former = self._project(tmp_path / "former")
        monkeypatch.setenv("EIKON_ROOT", str(root))
        monkeypatch.setenv("EIKON_PROJECT_ROOT", str(former))
        with warnings.catch_warnings():
            warnings.simplefilter("error")
            assert discover_project_root(tmp_path) == root

    def test_deprecated_variable_alone_works_and_warns(self, tmp_path: Path, monkeypatch):
        former = self._project(tmp_path / "former")
        monkeypatch.delenv("EIKON_ROOT", raising=False)
        monkeypatch.setenv("EIKON_PROJECT_ROOT", str(former))
        with pytest.warns(FutureWarning, match="EIKON_PROJECT_ROOT is deprecated.*EIKON_ROOT"):
            assert discover_project_root(tmp_path) == former

    def test_empty_eikon_root_falls_back_to_deprecated_variable(self, tmp_path: Path, monkeypatch):
        former = self._project(tmp_path / "former")
        monkeypatch.setenv("EIKON_ROOT", "  ")
        monkeypatch.setenv("EIKON_PROJECT_ROOT", str(former))
        with pytest.warns(FutureWarning, match="EIKON_ROOT"):
            assert discover_project_root(tmp_path) == former


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
