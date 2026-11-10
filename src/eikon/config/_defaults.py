"""Built-in default values for project configuration.

These defaults are used when no ``eikon.yaml`` is found or when fields are
omitted from the user's configuration file.
"""

from pathlib import Path
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

CONFIG_LOCATIONS = (Path("config") / "tools" / CONFIG_FILENAME, Path(CONFIG_FILENAME))
"""Places of the configuration file below a project root, in the order of their precedence:
``config/tools/``, where a project keeps the settings of its tools off its root, then the root
itself."""
