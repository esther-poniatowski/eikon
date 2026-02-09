"""Tests for eikon.contrib._seaborn — seaborn plot type wrappers."""

from unittest.mock import MagicMock

import pytest

from eikon.ext._plot_types import _clear_registry, get_plot_type

# Import contrib to register the plot types
import eikon.contrib  # noqa: F401


@pytest.fixture(autouse=True)
def _ensure_registered():
    import importlib

    import eikon.contrib._seaborn
    importlib.reload(eikon.contrib._seaborn)
    yield
    _clear_registry()


class TestSeabornPlotTypes:
    """Seaborn wrappers are registered and raise ImportError when seaborn is missing."""

    @pytest.mark.parametrize("name", [
        "sns.lineplot", "sns.scatterplot", "sns.heatmap",
        "sns.boxplot", "sns.violinplot",
    ])
    def test_registered(self, name: str) -> None:
        fn = get_plot_type(name)
        assert callable(fn)

    def test_lazy_import_raises_without_seaborn(self) -> None:
        from eikon.contrib._seaborn import _lazy_import_seaborn

        with pytest.raises(ImportError, match="seaborn is required"):
            _lazy_import_seaborn()

    def test_lineplot_raises_without_seaborn(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("sns.lineplot")
        with pytest.raises(ImportError):
            fn(ax)

    def test_scatterplot_raises_without_seaborn(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("sns.scatterplot")
        with pytest.raises(ImportError):
            fn(ax)

    def test_heatmap_raises_without_seaborn(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("sns.heatmap")
        with pytest.raises(ImportError):
            fn(ax)

    def test_boxplot_raises_without_seaborn(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("sns.boxplot")
        with pytest.raises(ImportError):
            fn(ax)

    def test_violinplot_raises_without_seaborn(self) -> None:
        ax = MagicMock()
        fn = get_plot_type("sns.violinplot")
        with pytest.raises(ImportError):
            fn(ax)
