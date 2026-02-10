"""Shared fixtures for the eikon test suite."""

from pathlib import Path

import pytest

from eikon.ext import clear_transforms


@pytest.fixture()
def tmp_project(tmp_path: Path) -> Path:
    """Create a minimal eikon project directory with ``eikon.yaml``."""
    config = tmp_path / "eikon.yaml"
    config.write_text(
        """\
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
""",
        encoding="utf-8",
    )
    for dirname in ("figures", "styles", "specs", "data"):
        (tmp_path / dirname).mkdir()
    return tmp_path


@pytest.fixture(autouse=True)
def _clear_transforms() -> None:
    """Reset registered data transforms between tests."""
    clear_transforms()


@pytest.fixture()
def sample_spec_dict() -> dict:
    """A minimal valid figure specification dictionary."""
    return {
        "name": "test-figure",
        "title": "Test Figure",
        "tags": ["test", "unit"],
        "group": "tests",
        "panels": [
            {
                "name": "A",
                "plot_type": "line",
                "row": 0,
                "col": 0,
                "params": {"color": "blue"},
            },
            {
                "name": "B",
                "plot_type": "scatter",
                "row": 0,
                "col": 1,
            },
        ],
        "layout": {"rows": 1, "cols": 2},
    }
