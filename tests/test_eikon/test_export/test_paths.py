"""Tests for eikon.export._paths — export path construction."""

from pathlib import Path

import pytest

from eikon._types import ExportFormat
from eikon.exceptions import ExportError
from eikon.export._paths import build_export_path


class TestBuildExportPath:
    """build_export_path constructs correct output paths."""

    def test_simple_path(self, tmp_path: Path) -> None:
        path = build_export_path(
            name="fig1",
            fmt=ExportFormat.PDF,
            output_dir=tmp_path,
        )
        assert path == tmp_path / "fig1.pdf"

    def test_svg_format(self, tmp_path: Path) -> None:
        path = build_export_path(
            name="fig1",
            fmt=ExportFormat.SVG,
            output_dir=tmp_path,
        )
        assert path == tmp_path / "fig1.svg"

    def test_png_format(self, tmp_path: Path) -> None:
        path = build_export_path(
            name="fig1",
            fmt=ExportFormat.PNG,
            output_dir=tmp_path,
        )
        assert path == tmp_path / "fig1.png"

    def test_with_subdirectory(self, tmp_path: Path) -> None:
        path = build_export_path(
            name="fig1",
            fmt=ExportFormat.PDF,
            output_dir=tmp_path,
            subdirectory="manuscript",
        )
        assert path == tmp_path / "manuscript" / "fig1.pdf"

    def test_filename_template(self, tmp_path: Path) -> None:
        path = build_export_path(
            name="fig1",
            fmt=ExportFormat.PDF,
            output_dir=tmp_path,
            filename_template="{name}_{group}",
            group="paper",
        )
        assert path.stem == "fig1_paper"
        assert path.suffix == ".pdf"

    def test_collision_fail_raises(self, tmp_path: Path) -> None:
        existing = tmp_path / "fig1.pdf"
        existing.write_bytes(b"")
        with pytest.raises(ExportError, match="collision='fail'"):
            build_export_path(
                name="fig1",
                fmt=ExportFormat.PDF,
                output_dir=tmp_path,
                collision="fail",
            )

    def test_collision_overwrite_allows(self, tmp_path: Path) -> None:
        existing = tmp_path / "fig1.pdf"
        existing.write_bytes(b"")
        path = build_export_path(
            name="fig1",
            fmt=ExportFormat.PDF,
            output_dir=tmp_path,
            collision="overwrite",
        )
        assert path == existing

    def test_collision_increment(self, tmp_path: Path) -> None:
        (tmp_path / "fig1.pdf").write_bytes(b"")
        path = build_export_path(
            name="fig1",
            fmt=ExportFormat.PDF,
            output_dir=tmp_path,
            collision="increment",
        )
        assert path == tmp_path / "fig1_1.pdf"

    def test_collision_increment_multiple(self, tmp_path: Path) -> None:
        (tmp_path / "fig1.pdf").write_bytes(b"")
        (tmp_path / "fig1_1.pdf").write_bytes(b"")
        path = build_export_path(
            name="fig1",
            fmt=ExportFormat.PDF,
            output_dir=tmp_path,
            collision="increment",
        )
        assert path == tmp_path / "fig1_2.pdf"

    def test_unsafe_name_sanitized(self, tmp_path: Path) -> None:
        path = build_export_path(
            name='fig<1>:"/test',
            fmt=ExportFormat.PDF,
            output_dir=tmp_path,
        )
        assert "<" not in str(path)
        assert ">" not in str(path)
        assert path.suffix == ".pdf"
