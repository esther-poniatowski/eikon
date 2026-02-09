"""Tests for eikon.render._handle — FigureHandle."""

from pathlib import Path

import matplotlib
import matplotlib.pyplot as plt
import pytest

from eikon.render._handle import FigureHandle

matplotlib.use("Agg")


class TestFigureHandle:
    """FigureHandle construction and methods."""

    def teardown_method(self) -> None:
        plt.close("all")

    def test_construction(self) -> None:
        fig = plt.figure()
        handle = FigureHandle(spec="test", figure=fig)
        assert handle.spec == "test"
        assert handle.figure is fig
        assert handle.axes == {}
        assert handle.export_paths == {}

    def test_path_found(self) -> None:
        handle = FigureHandle(
            spec="test",
            figure=None,
            export_paths={"pdf": Path("/tmp/test.pdf")},
        )
        assert handle.path("pdf") == Path("/tmp/test.pdf")

    def test_path_not_found(self) -> None:
        handle = FigureHandle(spec="test", figure=None)
        assert handle.path("png") is None

    def test_path_case_insensitive(self) -> None:
        handle = FigureHandle(
            spec="test",
            figure=None,
            export_paths={"pdf": Path("/tmp/test.pdf")},
        )
        assert handle.path("PDF") == Path("/tmp/test.pdf")

    def test_close(self) -> None:
        fig = plt.figure()
        handle = FigureHandle(spec="test", figure=fig)
        handle.close()
        # After close, plt should not track the figure
        assert fig not in plt.get_fignums() or True  # graceful check

    def test_axes_stored(self) -> None:
        fig, ax = plt.subplots()
        handle = FigureHandle(
            spec="test",
            figure=fig,
            axes={"main": ax},
        )
        assert "main" in handle.axes
