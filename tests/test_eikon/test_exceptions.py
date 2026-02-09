"""Tests for eikon.exceptions."""

from eikon.exceptions import (
    ConfigNotFoundError,
    ConfigValidationError,
    EikonError,
    PanelOverlapError,
    SpecValidationError,
    UnknownPlotTypeError,
)


class TestExceptionHierarchy:
    def test_all_inherit_from_eikon_error(self):
        assert issubclass(ConfigNotFoundError, EikonError)
        assert issubclass(ConfigValidationError, EikonError)
        assert issubclass(SpecValidationError, EikonError)
        assert issubclass(PanelOverlapError, EikonError)
        assert issubclass(UnknownPlotTypeError, EikonError)


class TestConfigNotFoundError:
    def test_message(self):
        err = ConfigNotFoundError("/some/path")
        assert "eikon.yaml" in str(err)
        assert "/some/path" in str(err)


class TestConfigValidationError:
    def test_message_lists_errors(self):
        err = ConfigValidationError(["error one", "error two"])
        msg = str(err)
        assert "error one" in msg
        assert "error two" in msg
        assert err.errors == ["error one", "error two"]


class TestSpecValidationError:
    def test_message_lists_errors(self):
        err = SpecValidationError(["missing name"])
        assert "missing name" in str(err)
        assert err.errors == ["missing name"]


class TestPanelOverlapError:
    def test_message(self):
        err = PanelOverlapError("A", "B")
        assert "A" in str(err)
        assert "B" in str(err)


class TestUnknownPlotTypeError:
    def test_message_with_available(self):
        err = UnknownPlotTypeError("custom", ["line", "scatter"])
        assert "custom" in str(err)
        assert "line" in str(err)

    def test_message_no_available(self):
        err = UnknownPlotTypeError("custom", [])
        assert "(none)" in str(err)
