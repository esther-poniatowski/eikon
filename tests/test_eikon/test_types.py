"""Tests for eikon._types."""

import pytest

from eikon._types import ExportFormat


class TestExportFormat:
    def test_values(self):
        assert ExportFormat.PDF.value == "pdf"
        assert ExportFormat.SVG.value == "svg"
        assert ExportFormat.PNG.value == "png"

    def test_from_string_lowercase(self):
        assert ExportFormat.from_string("pdf") == ExportFormat.PDF
        assert ExportFormat.from_string("svg") == ExportFormat.SVG
        assert ExportFormat.from_string("png") == ExportFormat.PNG

    def test_from_string_uppercase(self):
        assert ExportFormat.from_string("PDF") == ExportFormat.PDF

    def test_from_string_mixed_case(self):
        assert ExportFormat.from_string("Svg") == ExportFormat.SVG

    def test_from_string_invalid(self):
        with pytest.raises(ValueError, match="Unknown export format"):
            ExportFormat.from_string("bmp")
