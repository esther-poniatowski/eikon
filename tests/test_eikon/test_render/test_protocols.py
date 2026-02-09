"""Tests for eikon.render._protocols — protocol definitions."""

from typing import Any

from eikon.render._protocols import DataTransform, FigurePostProcessor, PlotFunction


class TestProtocols:
    """Protocol structural subtyping checks."""

    def test_plot_function_matches(self) -> None:
        def draw(ax: Any, /, **kwargs: Any) -> None:
            pass

        assert isinstance(draw, PlotFunction)

    def test_figure_post_processor_matches(self) -> None:
        def process(figure: Any, axes: dict[str, Any], /) -> None:
            pass

        assert isinstance(process, FigurePostProcessor)

    def test_data_transform_matches(self) -> None:
        def transform(data: Any, /) -> Any:
            return data

        assert isinstance(transform, DataTransform)
