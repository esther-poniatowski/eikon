"""Render convenience function resolves specs via registry entries."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon import render, load_registry
from eikon.config._defaults import DEFAULT_CONFIG
from eikon.config._resolver import resolve_paths
from eikon.ext._hooks import clear_hooks
from eikon.ext._plot_types import _clear_registry, register_plot_type
from eikon.registry import Registry

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


def test_render_uses_registry_spec_path(tmp_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_project)
    paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_project)
    spec_path = paths.specs_dir / "by-reg.yaml"
    spec_path.write_text(
        "name: by-reg\npanels:\n  - name: A\n    plot_type: noop\n",
        encoding="utf-8",
    )

    # registry entry with spec_path
    reg = Registry(tmp_project / DEFAULT_CONFIG.registry_file)
    reg.register("by-reg", spec_path=str(spec_path))
    reg.save()

    handle = render("by-reg", config=DEFAULT_CONFIG, resolved_paths=paths)
    assert handle.figure is not None
    handle.close()


def test_render_falls_back_to_specs_dir(tmp_project: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.chdir(tmp_project)
    paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_project)
    spec_path = paths.specs_dir / "fallback.yaml"
    spec_path.write_text(
        "name: fallback\npanels:\n  - name: A\n    plot_type: noop\n",
        encoding="utf-8",
    )

    handle = render("fallback", config=DEFAULT_CONFIG, resolved_paths=paths)
    assert handle.figure is not None
    handle.close()
