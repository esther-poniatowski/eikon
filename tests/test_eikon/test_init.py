"""Tests for eikon.__init__ — public API and convenience functions."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon import FigureSpec, load_registry, render
from eikon.config._defaults import DEFAULT_CONFIG
from eikon.config._resolver import resolve_paths
from eikon.ext._hooks import clear_hooks
from eikon.ext._plot_types import _clear_registry, register_plot_type
from eikon.spec._panel import PanelSpec

matplotlib.use("Agg")


def _noop_plot(ax: object, **kwargs: object) -> None:
    """Minimal plot function for testing."""


@pytest.fixture(autouse=True)
def _clean_state() -> None:
    _clear_registry()
    clear_hooks()
    register_plot_type("noop", _noop_plot)
    yield  # type: ignore[misc]
    plt.close("all")


class TestRenderConvenience:
    """eikon.render() convenience function."""

    def test_render_with_spec_object(self, tmp_path: Path) -> None:
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        paths.output_dir.mkdir(parents=True, exist_ok=True)
        spec = FigureSpec(
            name="test-fig",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        handle = render(spec, config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.figure is not None
        handle.close()

    def test_render_with_spec_file(self, tmp_path: Path) -> None:
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        paths.output_dir.mkdir(parents=True, exist_ok=True)
        paths.specs_dir.mkdir(parents=True, exist_ok=True)
        spec_file = tmp_path / "fig.yaml"
        spec_file.write_text(
            "name: test-fig\npanels:\n  - name: A\n    plot_type: noop\n",
            encoding="utf-8",
        )
        handle = render(str(spec_file), config=DEFAULT_CONFIG, resolved_paths=paths)
        assert handle.figure is not None
        handle.close()

    def test_render_with_formats(self, tmp_path: Path) -> None:
        paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
        paths.output_dir.mkdir(parents=True, exist_ok=True)
        spec = FigureSpec(
            name="test-fig",
            panels=(PanelSpec(name="A", plot_type="noop"),),
        )
        handle = render(spec, config=DEFAULT_CONFIG, resolved_paths=paths, formats=("pdf",))
        assert "pdf" in handle.export_paths
        handle.close()


class TestPublicAPI:
    """Verify public API exports."""

    def test_resolved_paths_exported(self) -> None:
        import eikon

        assert "ResolvedPaths" in eikon.__all__
        assert hasattr(eikon, "ResolvedPaths")


class TestLoadRegistry:
    """eikon.load_registry() convenience function."""

    def test_load_empty_registry(self, tmp_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_project)
        reg = load_registry()
        assert len(reg) == 0

    def test_load_registry_persists(self, tmp_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
        monkeypatch.chdir(tmp_project)
        reg = load_registry()
        reg.register("fig1", tags=("a",))
        reg.save()

        reg2 = load_registry()
        assert "fig1" in reg2
