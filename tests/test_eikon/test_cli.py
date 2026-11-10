"""Tests for eikon.cli."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest
from typer.testing import CliRunner

from eikon.cli import app
from eikon.ext._hooks import clear_hooks
from eikon.ext._plot_types import _clear_registry, register_plot_type

matplotlib.use("Agg")
runner = CliRunner()

_EIKON_YAML = """\
paths:
  output_dir: figures
  styles_dir: styles
  specs_dir: specs
  data_dir: data

export:
  formats: [pdf]
  dpi: 300
  transparent: false

style:
  base_style: default
  font_family: serif
  font_size: 10.0
  figure_size: [6.4, 4.8]

registry_file: eikon-registry.yaml
"""


def _noop_plot(ax: object, **kwargs: object) -> None:
    """Minimal plot function for testing."""


class TestCliInfo:
    def test_info_runs(self):
        result = runner.invoke(app, ["info"])
        assert result.exit_code == 0
        assert "eikon" in result.output


class TestCliVersion:
    def test_version_flag(self):
        result = runner.invoke(app, ["--version"])
        assert result.exit_code == 0


class TestCliInit:
    def test_creates_project(self, tmp_path: Path):
        result = runner.invoke(app, ["init", str(tmp_path)])
        assert result.exit_code == 0
        assert (tmp_path / "eikon.yml").is_file()
        assert (tmp_path / "figures").is_dir()
        assert (tmp_path / "styles").is_dir()
        assert (tmp_path / "specs").is_dir()
        assert (tmp_path / "data").is_dir()

    def test_refuses_if_exists(self, tmp_path: Path):
        (tmp_path / "eikon.yml").write_text("", encoding="utf-8")
        result = runner.invoke(app, ["init", str(tmp_path)])
        assert result.exit_code == 2
        assert str(tmp_path / "eikon.yml") in result.stderr
        assert (tmp_path / "eikon.yml").read_text(encoding="utf-8") == ""

    def test_refuses_to_overwrite_edited_example_spec(self, tmp_path: Path):
        (tmp_path / "specs").mkdir()
        edited = tmp_path / "specs" / "example.yaml"
        edited.write_text("name: edited\n", encoding="utf-8")
        result = runner.invoke(app, ["init", str(tmp_path)])
        assert result.exit_code == 2
        assert str(edited) in result.stderr
        assert edited.read_text(encoding="utf-8") == "name: edited\n"
        assert not (tmp_path / "eikon.yml").exists()

    def test_force_overwrites_settings_in_config_tools(self, tmp_path: Path):
        (tmp_path / "config" / "tools").mkdir(parents=True)
        settings = tmp_path / "config" / "tools" / "eikon.yml"
        settings.write_text("", encoding="utf-8")
        result = runner.invoke(app, ["init", str(tmp_path), "--force"])
        assert result.exit_code == 0
        assert "config_version: 1" in settings.read_text(encoding="utf-8")
        assert not (tmp_path / "eikon.yml").exists()

    def test_generates_example_spec(self, tmp_path: Path):
        runner.invoke(app, ["init", str(tmp_path)])
        example = tmp_path / "specs" / "example.yaml"
        assert example.is_file()
        content = example.read_text(encoding="utf-8")
        assert "spec_version: 1" in content
        assert "plot_type: line" in content

    def test_generates_multi_panel_example(self, tmp_path: Path):
        runner.invoke(app, ["init", str(tmp_path)])
        example = tmp_path / "specs" / "multi-panel-example.yaml"
        assert example.is_file()
        content = example.read_text(encoding="utf-8")
        assert "rows: 2" in content
        assert "cols: 2" in content
        assert "shared_legend:" in content
        assert "hide_spines:" in content

    def test_config_version_in_template(self, tmp_path: Path):
        runner.invoke(app, ["init", str(tmp_path)])
        content = (tmp_path / "eikon.yml").read_text(encoding="utf-8")
        assert "config_version: 1" in content


class TestCliValidate:
    def test_valid_config(self, tmp_project: Path):
        result = runner.invoke(app, ["validate", str(tmp_project / "eikon.yml")])
        assert result.exit_code == 0
        assert "valid" in result.output.lower()

    def test_invalid_config(self, tmp_path: Path):
        cfg = tmp_path / "eikon.yml"
        cfg.write_text("export:\n  dpi: -1\n", encoding="utf-8")
        result = runner.invoke(app, ["validate", str(cfg)])
        assert result.exit_code == 1

    def test_missing_file(self, tmp_path: Path):
        result = runner.invoke(app, ["validate", str(tmp_path / "missing.yaml")])
        assert result.exit_code == 2

    def test_valid_figure_spec(self, tmp_path: Path):
        spec = tmp_path / "fig.yaml"
        spec.write_text("name: test-fig\n", encoding="utf-8")
        result = runner.invoke(app, ["validate", str(spec)])
        assert result.exit_code == 0
        assert "valid" in result.output.lower()

    def test_invalid_config_rich_output(self, tmp_path: Path):
        cfg = tmp_path / "eikon.yml"
        cfg.write_text("export:\n  dpi: -1\n", encoding="utf-8")
        result = runner.invoke(app, ["validate", str(cfg)])
        assert result.exit_code == 1
        assert "validation failed" in result.output.lower()


class TestCliRoot:
    """--root global option threads the root through ctx.obj."""

    def test_root_option(self, tmp_project: Path, monkeypatch):
        monkeypatch.chdir(tmp_project)
        result = runner.invoke(
            app, ["--root", str(tmp_project), "registry", "list"]
        )
        assert result.exit_code == 0
        assert "deprecated" not in result.output

    def test_render_uses_root_option(self, tmp_project: Path, tmp_path: Path, monkeypatch):
        spec_path = tmp_project / "specs" / "rooted.yaml"
        spec_path.write_text(
            "name: rooted\npanels:\n  - name: A\n    plot_type: line\n",
            encoding="utf-8",
        )
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        monkeypatch.chdir(elsewhere)
        result = runner.invoke(
            app,
            ["--root", str(tmp_project), "render", str(spec_path), "-f", "pdf"],
        )

        assert result.exit_code == 0
        assert (tmp_project / "figures" / "rooted.pdf").exists()

    def test_batch_uses_root_option(self, tmp_project: Path, tmp_path: Path, monkeypatch):
        spec_path = tmp_project / "specs" / "b1.yaml"
        spec_path.write_text(
            "name: b1\npanels:\n  - name: A\n    plot_type: line\n", encoding="utf-8"
        )
        elsewhere = tmp_path / "elsewhere-batch"
        elsewhere.mkdir()
        monkeypatch.chdir(elsewhere)
        result = runner.invoke(
            app,
            ["--root", str(tmp_project), "batch", "-f", "pdf"],
        )
        assert result.exit_code == 0
        assert (tmp_project / "figures" / "b1.pdf").exists()

    def test_registry_with_root_option(self, tmp_project: Path, tmp_path: Path, monkeypatch):
        elsewhere = tmp_path / "elsewhere-reg"
        elsewhere.mkdir()
        monkeypatch.chdir(elsewhere)
        result = runner.invoke(
            app,
            ["--root", str(tmp_project), "registry", "list"],
        )
        assert result.exit_code == 0

    def test_short_root_option(self, tmp_project: Path, tmp_path: Path, monkeypatch):
        elsewhere = tmp_path / "elsewhere-short"
        elsewhere.mkdir()
        monkeypatch.chdir(elsewhere)
        result = runner.invoke(app, ["-r", str(tmp_project), "registry", "add", "short"])
        assert result.exit_code == 0
        assert (tmp_project / "eikon-registry.yaml").is_file()

    def test_retired_project_root_is_rejected(self, tmp_project: Path):
        result = runner.invoke(
            app, ["--project-root", str(tmp_project), "registry", "list"]
        )
        assert result.exit_code == 2
        assert "No such option" in result.output

    def test_help_lists_root_and_config(self):
        result = runner.invoke(app, ["--help"])
        assert result.exit_code == 0
        assert "--root" in result.output
        assert "--config" in result.output
        assert "--project-root" not in result.output


class TestCliSettings:
    """--config names the settings file; without one, eikon runs on its built-in defaults."""

    def test_config_option_relative_to_current_folder(self, tmp_path: Path, monkeypatch):
        root = tmp_path / "root"
        root.mkdir()
        elsewhere = tmp_path / "elsewhere"
        elsewhere.mkdir()
        (elsewhere / "custom.yml").write_text(
            "registry_file: custom-registry.yaml\n", encoding="utf-8"
        )
        monkeypatch.chdir(elsewhere)
        result = runner.invoke(
            app, ["-r", str(root), "-c", "custom.yml", "registry", "add", "fig"]
        )
        assert result.exit_code == 0
        assert (root / "custom-registry.yaml").is_file()

    def test_absent_config_option_is_an_error(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["--config", "absent.yml", "registry", "list"])
        assert result.exit_code == 2
        assert "absent.yml" in result.stderr

    def test_no_settings_file_runs_on_defaults(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["registry", "add", "fig"])
        assert result.exit_code == 0
        assert (tmp_path / "eikon-registry.yaml").is_file()

    def test_conflicting_settings_files_name_both(self, tmp_path: Path, monkeypatch):
        (tmp_path / "config" / "tools").mkdir(parents=True)
        (tmp_path / "config" / "tools" / "eikon.yml").write_text("{}\n", encoding="utf-8")
        (tmp_path / "eikon.yml").write_text("{}\n", encoding="utf-8")
        monkeypatch.chdir(tmp_path)
        result = runner.invoke(app, ["registry", "list"])
        assert result.exit_code == 2
        assert str(tmp_path / "config" / "tools" / "eikon.yml") in result.stderr
        assert str(tmp_path / "eikon.yml") in result.stderr

    def test_retired_root_variable_is_ignored(self, tmp_path: Path, monkeypatch):
        former = tmp_path / "former"
        former.mkdir()
        (former / "eikon.yml").write_text(_EIKON_YAML, encoding="utf-8")
        start = tmp_path / "start"
        start.mkdir()
        monkeypatch.chdir(start)
        monkeypatch.setenv("EIKON_PROJECT_ROOT", str(former))
        result = runner.invoke(app, ["registry", "add", "fig"])
        assert result.exit_code == 0
        assert (start / "eikon-registry.yaml").is_file()
        assert not (former / "eikon-registry.yaml").exists()


class TestCliRegistry:
    """CLI registry subcommands (list, add, remove, show)."""

    def test_add_and_list(self, tmp_project: Path, monkeypatch):
        monkeypatch.chdir(tmp_project)
        result = runner.invoke(app, ["registry", "add", "fig1", "--tag", "a"])
        assert result.exit_code == 0
        assert "Registered" in result.output

        result = runner.invoke(app, ["registry", "list"])
        assert result.exit_code == 0
        assert "fig1" in result.output

    def test_show(self, tmp_project: Path, monkeypatch):
        monkeypatch.chdir(tmp_project)
        runner.invoke(app, ["registry", "add", "fig1", "--group", "g1"])
        result = runner.invoke(app, ["registry", "show", "fig1"])
        assert result.exit_code == 0
        assert "g1" in result.output

    def test_show_missing(self, tmp_project: Path, monkeypatch):
        monkeypatch.chdir(tmp_project)
        result = runner.invoke(app, ["registry", "show", "nope"])
        assert result.exit_code == 1

    def test_remove(self, tmp_project: Path, monkeypatch):
        monkeypatch.chdir(tmp_project)
        runner.invoke(app, ["registry", "add", "fig1"])
        result = runner.invoke(app, ["registry", "remove", "fig1"])
        assert result.exit_code == 0
        assert "Removed" in result.output

    def test_remove_missing(self, tmp_project: Path, monkeypatch):
        monkeypatch.chdir(tmp_project)
        result = runner.invoke(app, ["registry", "remove", "nope"])
        assert result.exit_code == 1

    def test_list_empty(self, tmp_project: Path, monkeypatch):
        monkeypatch.chdir(tmp_project)
        result = runner.invoke(app, ["registry", "list"])
        assert result.exit_code == 0
        assert "No figures" in result.output

    def test_list_with_tag_filter(self, tmp_project: Path, monkeypatch):
        monkeypatch.chdir(tmp_project)
        runner.invoke(app, ["registry", "add", "fig1", "--tag", "neural"])
        runner.invoke(app, ["registry", "add", "fig2", "--tag", "behavioral"])
        result = runner.invoke(app, ["registry", "list", "--tag", "neural"])
        assert result.exit_code == 0
        assert "fig1" in result.output
        assert "fig2" not in result.output

    def test_add_conflict_fail(self, tmp_project: Path, monkeypatch):
        monkeypatch.chdir(tmp_project)
        runner.invoke(app, ["registry", "add", "fig1"])
        result = runner.invoke(
            app, ["registry", "add", "fig1", "--on-conflict", "fail"]
        )
        assert result.exit_code == 1


class TestCliRenderRegistry:
    """CLI render-registry command renders a figure by registry name."""

    @pytest.fixture(autouse=True)
    def _clean_state(self) -> None:
        _clear_registry()
        clear_hooks()
        register_plot_type("noop", _noop_plot)
        yield  # type: ignore[misc]
        plt.close("all")

    def test_render_by_name(self, tmp_project: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_project)
        spec = tmp_project / "specs" / "myfig.yaml"
        spec.write_text(
            "name: myfig\npanels:\n  - name: A\n    plot_type: noop\n",
            encoding="utf-8",
        )
        # Register the figure with a spec_path
        runner.invoke(app, ["registry", "add", "myfig", "--spec-path", str(spec)])
        result = runner.invoke(app, ["render-registry", "myfig"])
        assert result.exit_code == 0
        assert "Rendered" in result.output

    def test_spec_path_stored_relative_to_root(self, tmp_project: Path, monkeypatch) -> None:
        spec = tmp_project / "specs" / "sub.yaml"
        spec.write_text(
            "name: sub\npanels:\n  - name: A\n    plot_type: noop\n",
            encoding="utf-8",
        )
        monkeypatch.chdir(tmp_project / "specs")
        result = runner.invoke(app, ["registry", "add", "sub", "--spec-path", "sub.yaml"])
        assert result.exit_code == 0
        content = (tmp_project / "eikon-registry.yaml").read_text(encoding="utf-8")
        assert "specs/sub.yaml" in content
        assert str(tmp_project) not in content
        monkeypatch.chdir(tmp_project / "data")
        result = runner.invoke(app, ["render-registry", "sub"])
        assert result.exit_code == 0
        assert "Rendered" in result.output

    def test_render_by_name_fallback_to_specs_dir(self, tmp_project: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_project)
        spec = tmp_project / "specs" / "fallback.yaml"
        spec.write_text(
            "name: fallback\npanels:\n  - name: A\n    plot_type: noop\n",
            encoding="utf-8",
        )
        # Register without spec_path — should fall back to specs_dir
        runner.invoke(app, ["registry", "add", "fallback"])
        result = runner.invoke(app, ["render-registry", "fallback"])
        assert result.exit_code == 0
        assert "Rendered" in result.output

    def test_render_by_name_missing_spec(self, tmp_project: Path, monkeypatch) -> None:
        monkeypatch.chdir(tmp_project)
        runner.invoke(app, ["registry", "add", "ghost"])
        result = runner.invoke(app, ["render-registry", "ghost"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()


def _write_spec(path: Path, name: str, tags: list[str] | None = None, group: str = "") -> Path:
    """Write a minimal figure spec YAML file."""
    import yaml

    spec = {
        "name": name,
        "panels": [{"name": "A", "plot_type": "noop"}],
    }
    if tags:
        spec["tags"] = tags
    if group:
        spec["group"] = group
    path.write_text(yaml.dump(spec), encoding="utf-8")
    return path


class TestCliBatch:
    """CLI batch command renders multiple figures."""

    @pytest.fixture(autouse=True)
    def _clean_state(self) -> None:
        _clear_registry()
        clear_hooks()
        register_plot_type("noop", _noop_plot)
        yield  # type: ignore[misc]
        plt.close("all")

    def test_batch_explicit_specs(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "eikon.yml").write_text(_EIKON_YAML, encoding="utf-8")
        (tmp_path / "figures").mkdir()
        s1 = _write_spec(tmp_path / "a.yaml", "fig-a")
        s2 = _write_spec(tmp_path / "b.yaml", "fig-b")
        result = runner.invoke(app, ["batch", str(s1), str(s2), "-f", "pdf"])
        assert result.exit_code == 0
        assert "2 rendered" in result.output

    def test_batch_scans_specs_dir(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "eikon.yml").write_text(_EIKON_YAML, encoding="utf-8")
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        (tmp_path / "figures").mkdir()
        _write_spec(specs_dir / "fig1.yaml", "fig1")
        _write_spec(specs_dir / "fig2.yaml", "fig2")
        result = runner.invoke(app, ["batch", "-f", "pdf"])
        assert result.exit_code == 0
        assert "2 rendered" in result.output

    def test_batch_no_specs_dir_fails(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "eikon.yml").write_text(_EIKON_YAML, encoding="utf-8")
        result = runner.invoke(app, ["batch"])
        assert result.exit_code == 1
        assert "not found" in result.output.lower()

    def test_batch_tag_filter(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "eikon.yml").write_text(_EIKON_YAML, encoding="utf-8")
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        (tmp_path / "figures").mkdir()
        _write_spec(specs_dir / "a.yaml", "a", tags=["neural"])
        _write_spec(specs_dir / "b.yaml", "b", tags=["behavioral"])
        result = runner.invoke(app, ["batch", "--tag", "neural", "-f", "pdf"])
        assert result.exit_code == 0
        assert "1 rendered" in result.output

    def test_batch_group_filter(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "eikon.yml").write_text(_EIKON_YAML, encoding="utf-8")
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        (tmp_path / "figures").mkdir()
        _write_spec(specs_dir / "a.yaml", "a", group="ms1")
        _write_spec(specs_dir / "b.yaml", "b", group="ms2")
        result = runner.invoke(app, ["batch", "--group", "ms1", "-f", "pdf"])
        assert result.exit_code == 0
        assert "1 rendered" in result.output

    def test_batch_no_matches(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "eikon.yml").write_text(_EIKON_YAML, encoding="utf-8")
        specs_dir = tmp_path / "specs"
        specs_dir.mkdir()
        _write_spec(specs_dir / "a.yaml", "a", tags=["x"])
        result = runner.invoke(app, ["batch", "--tag", "nonexistent"])
        assert result.exit_code == 0
        assert "No matching" in result.output

    def test_batch_continue_on_error(self, tmp_path: Path, monkeypatch):
        monkeypatch.chdir(tmp_path)
        (tmp_path / "eikon.yml").write_text(_EIKON_YAML, encoding="utf-8")
        (tmp_path / "figures").mkdir()
        good = _write_spec(tmp_path / "good.yaml", "good")
        bad = tmp_path / "bad.yaml"
        bad.write_text("name: bad\npanels:\n  - name: A\n    plot_type: nonexistent\n", encoding="utf-8")
        result = runner.invoke(
            app, ["batch", str(good), str(bad), "-f", "pdf", "--continue-on-error"]
        )
        assert "1 rendered" in result.output
        assert "1 failed" in result.output
