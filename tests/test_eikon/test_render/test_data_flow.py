"""Tests for data loading and transform flow in the render pipeline."""

from pathlib import Path

import pytest

from eikon.config._defaults import DEFAULT_CONFIG
from eikon.config._resolver import resolve_paths
from eikon.exceptions import RenderError
from eikon.ext import register_transform
from eikon.ext._plot_types import _clear_registry, register_plot_type
from eikon.render._data import resolve_data_binding
from eikon.render._pipeline import render_figure
from eikon.spec._data import DataBinding
from eikon.spec._figure import FigureSpec
from eikon.spec._panel import PanelSpec


@pytest.fixture(autouse=True)
def _clean_registry() -> None:
    _clear_registry()


def _capture_plot(calls: list[dict], ax: object, **kwargs: object) -> None:
    calls.append(kwargs)


def test_data_binding_loads_csv(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_path = data_dir / "table.csv"
    csv_path.write_text("time,value\n0,1\n1,2\n", encoding="utf-8")

    _capture_plot.calls = []  # type: ignore[attr-defined]
    register_plot_type("capture", lambda ax, **kw: _capture_plot.calls.append(kw))

    binding = DataBinding(source="table.csv", x="time", y="value")
    spec = FigureSpec(
        name="datafig",
        panels=(PanelSpec(name="A", plot_type="capture", data=binding),),
    )

    paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
    render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)

    call = _capture_plot.calls[0]  # type: ignore[attr-defined]
    x_vals = call["x"]
    y_vals = call["y"]
    x_list = x_vals.tolist() if hasattr(x_vals, "tolist") else list(x_vals)
    y_list = y_vals.tolist() if hasattr(y_vals, "tolist") else list(y_vals)
    # CSV DictReader returns strings; pandas returns numeric — normalize to float
    assert [float(v) for v in x_list] == [0.0, 1.0]
    assert [float(v) for v in y_list] == [1.0, 2.0]


def test_data_transform_applied(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    csv_path = data_dir / "table.csv"
    csv_path.write_text("time,value\n0,1\n1,2\n", encoding="utf-8")

    _capture_plot.calls = []  # type: ignore[attr-defined]
    register_plot_type("capture", lambda ax, **kw: _capture_plot.calls.append(kw))

    def double(df):
        try:
            df = df.copy()
            df["value"] = df["value"].astype(float) * 2
            return df
        except Exception:
            return [{"time": float(row["time"]), "value": float(row["value"]) * 2} for row in df]

    register_transform("double_value", double)

    binding = DataBinding(source="table.csv", x="time", y="value", transforms=("double_value",))
    spec = FigureSpec(
        name="datafig-transform",
        panels=(PanelSpec(name="A", plot_type="capture", data=binding),),
    )

    paths = resolve_paths(DEFAULT_CONFIG.paths, project_root=tmp_path)
    render_figure(spec, config=DEFAULT_CONFIG, resolved_paths=paths)

    call = _capture_plot.calls[0]  # type: ignore[attr-defined]
    y_vals = call["y"]
    y_list = y_vals.tolist() if hasattr(y_vals, "tolist") else list(y_vals)
    assert y_list == [2.0, 4.0]


class TestResolveDataBindingDirect:
    """Direct tests for resolve_data_binding covering error branches."""

    def test_empty_source_returns_empty(self, tmp_path: Path) -> None:
        binding = DataBinding(source="")
        result = resolve_data_binding(binding, tmp_path)
        assert result == {}

    def test_missing_file_raises(self, tmp_path: Path) -> None:
        binding = DataBinding(source="nonexistent.csv")
        with pytest.raises(RenderError, match="not found"):
            resolve_data_binding(binding, tmp_path)

    def test_unsupported_format_raises(self, tmp_path: Path) -> None:
        bad_file = tmp_path / "data.xlsx"
        bad_file.write_text("", encoding="utf-8")
        binding = DataBinding(source="data.xlsx")
        with pytest.raises(RenderError, match="Unsupported"):
            resolve_data_binding(binding, tmp_path)

    def test_tsv_loaded(self, tmp_path: Path) -> None:
        tsv = tmp_path / "data.tsv"
        tsv.write_text("a\tb\n1\t2\n3\t4\n", encoding="utf-8")
        binding = DataBinding(source="data.tsv", x="a", y="b")
        result = resolve_data_binding(binding, tmp_path)
        assert "x" in result
        assert "y" in result

    def test_binding_params_forwarded(self, tmp_path: Path) -> None:
        csv = tmp_path / "data.csv"
        csv.write_text("x,y\n1,2\n", encoding="utf-8")
        binding = DataBinding(source="data.csv", params={"color": "red"})
        result = resolve_data_binding(binding, tmp_path)
        assert result["color"] == "red"

    def test_hue_column_extracted(self, tmp_path: Path) -> None:
        csv = tmp_path / "data.csv"
        csv.write_text("x,y,group\n1,2,a\n3,4,b\n", encoding="utf-8")
        binding = DataBinding(source="data.csv", x="x", y="y", hue="group")
        result = resolve_data_binding(binding, tmp_path)
        assert "hue" in result
