"""Built-in default values for project configuration.

These defaults are used when no ``eikon.yaml`` is found or when fields are
omitted from the user's configuration file.
"""

from eikon.config._schema import (
    ExportDefaults,
    PathsConfig,
    ProjectConfig,
    StyleDefaults,
)

DEFAULT_PATHS = PathsConfig()
DEFAULT_EXPORT = ExportDefaults()
DEFAULT_STYLE = StyleDefaults()
DEFAULT_CONFIG = ProjectConfig()

CONFIG_FILENAME = "eikon.yaml"
"""Standard name for the project configuration file."""
