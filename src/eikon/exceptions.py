"""Exception hierarchy for the eikon package.

All eikon exceptions inherit from :class:`EikonError`, allowing users to catch
the entire family with a single ``except EikonError`` clause.
"""

__all__ = [
    "EikonError",
    "ConfigError",
    "ConfigNotFoundError",
    "ConfigValidationError",
    "SpecError",
    "SpecValidationError",
    "StyleError",
    "StyleNotFoundError",
    "LayoutError",
    "PanelOverlapError",
    "RenderError",
    "UnknownPlotTypeError",
    "ExportError",
    "RegistryError",
]


class EikonError(Exception):
    """Base exception for all eikon errors."""


# --- Configuration ---


class ConfigError(EikonError):
    """Configuration loading or validation error."""


class ConfigNotFoundError(ConfigError):
    """No ``eikon.yaml`` found in the project hierarchy."""

    def __init__(self, search_root: str = ".") -> None:
        super().__init__(
            f"No eikon.yaml found searching upward from {search_root!r}. "
            "Run 'eikon init' to create a project configuration."
        )


class ConfigValidationError(ConfigError):
    """Schema validation failure with detailed messages.

    Parameters
    ----------
    errors : list[str]
        Individual validation error messages.
    """

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        bullet_list = "\n  - ".join(errors)
        super().__init__(f"Configuration validation failed:\n  - {bullet_list}")


# --- Specification ---


class SpecError(EikonError):
    """Figure specification error."""


class SpecValidationError(SpecError):
    """Invalid figure specification.

    Parameters
    ----------
    errors : list[str]
        Individual validation error messages.
    """

    def __init__(self, errors: list[str]) -> None:
        self.errors = errors
        bullet_list = "\n  - ".join(errors)
        super().__init__(f"Figure spec validation failed:\n  - {bullet_list}")


# --- Style ---


class StyleError(EikonError):
    """Style loading or composition error."""


class StyleNotFoundError(StyleError):
    """Referenced style could not be found.

    Parameters
    ----------
    name : str
        The style name or path that was not found.
    """

    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(f"Style not found: {name!r}")


# --- Layout ---


class LayoutError(EikonError):
    """Layout building or validation error."""


class PanelOverlapError(LayoutError):
    """Two panels occupy the same grid cells.

    Parameters
    ----------
    panel_a : str
        Name of the first overlapping panel.
    panel_b : str
        Name of the second overlapping panel.
    """

    def __init__(self, panel_a: str, panel_b: str) -> None:
        self.panel_a = panel_a
        self.panel_b = panel_b
        super().__init__(f"Panels {panel_a!r} and {panel_b!r} overlap in the grid layout.")


# --- Rendering ---


class RenderError(EikonError):
    """Error during rendering."""


class UnknownPlotTypeError(RenderError):
    """Referenced plot type is not registered.

    Parameters
    ----------
    name : str
        The unrecognized plot type name.
    available : list[str]
        Currently registered plot type names.
    """

    def __init__(self, name: str, available: list[str]) -> None:
        self.name = name
        self.available = available
        avail_str = ", ".join(sorted(available)) if available else "(none)"
        super().__init__(
            f"Unknown plot type {name!r}. Available types: {avail_str}"
        )


# --- Export ---


class ExportError(EikonError):
    """Error during figure export."""


# --- Registry ---


class RegistryError(EikonError):
    """Error in the figure registry."""
