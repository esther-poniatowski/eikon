"""Built-in default values for project configuration.

These defaults are used when a project holds no ``eikon.yml`` or when fields are
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

CONFIG_FILENAME = "eikon.yml"
"""Standard name for the project configuration file."""

CONFIG_LOCATIONS = (Path("config") / "tools" / CONFIG_FILENAME, Path(CONFIG_FILENAME))
"""Places of the configuration file below a project root: ``config/tools/``, where a project keeps
the settings of its tools off its root, and the root itself.  A root holding both is an error."""
