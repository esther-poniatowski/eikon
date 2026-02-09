"""Tests for eikon.ext._discovery — entry-point plugin discovery."""

from unittest.mock import MagicMock, patch

from eikon.ext._discovery import discover_plugins


class TestDiscoverPlugins:
    """Plugin discovery via entry points."""

    def test_no_plugins_returns_zero(self) -> None:
        # There are no plugins installed in the test environment
        count = discover_plugins("eikon.test_nonexistent_group")
        assert count == 0

    def test_default_group(self) -> None:
        # Should not raise even if nothing is registered
        count = discover_plugins()
        assert isinstance(count, int)

    def test_loads_entry_points(self) -> None:
        ep = MagicMock()
        ep.name = "test-plugin"
        ep.value = "test.module"
        with patch("eikon.ext._discovery.importlib.metadata.entry_points", return_value=[ep]):
            count = discover_plugins("eikon.plot_types")
        assert count == 1
        ep.load.assert_called_once()

    def test_handles_failing_plugin(self) -> None:
        ep = MagicMock()
        ep.name = "bad-plugin"
        ep.value = "bad.module"
        ep.load.side_effect = ImportError("no module")
        with patch("eikon.ext._discovery.importlib.metadata.entry_points", return_value=[ep]):
            count = discover_plugins("eikon.plot_types")
        assert count == 0
