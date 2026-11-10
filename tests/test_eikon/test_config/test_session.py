"""Tests for eikon.config._session."""

from pathlib import Path

import pytest

from eikon.config._session import ProjectSession
from eikon.exceptions import ConfigNotFoundError


class TestFromConfig:
    def test_settings_paths_are_relative_to_root(self, tmp_path: Path):
        (tmp_path / "config" / "tools").mkdir(parents=True)
        (tmp_path / "config" / "tools" / "eikon.yml").write_text(
            "paths:\n  output_dir: out\n", encoding="utf-8"
        )
        session = ProjectSession.from_config(project_root=tmp_path)
        assert session.paths.output_dir == (tmp_path / "out").resolve()

    def test_explicit_config_path_is_relative_to_current_folder(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        root = tmp_path / "root"
        root.mkdir()
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        (elsewhere / "other.yml").write_text("paths:\n  output_dir: out\n", encoding="utf-8")
        monkeypatch.chdir(elsewhere)
        session = ProjectSession.from_config(project_root=root, config_path=Path("other.yml"))
        assert session.paths.output_dir == (root / "out").resolve()

    def test_absent_explicit_config_path_raises(self, tmp_path: Path):
        with pytest.raises(ConfigNotFoundError):
            ProjectSession.from_config(project_root=tmp_path, config_path=tmp_path / "absent.yml")

    def test_no_settings_file_runs_on_defaults_in_current_folder(
        self, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
    ):
        monkeypatch.chdir(tmp_path)
        session = ProjectSession.from_config()
        assert session.paths.project_root == tmp_path.resolve()
        assert session.paths.output_dir == (tmp_path / "figures").resolve()
