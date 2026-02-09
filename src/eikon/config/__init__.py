"""Configuration system for eikon projects.

Provides YAML-based project configuration with path resolution,
schema validation, and layered defaults.
"""

from eikon.config._loader import load_config, merge_configs
from eikon.config._resolver import ResolvedPaths, resolve_paths
from eikon.config._schema import (
    ExportDefaults,
    PathsConfig,
    ProjectConfig,
    StyleDefaults,
)
from eikon.config._validation import validate_config

__all__ = [
    "ExportDefaults",
    "PathsConfig",
    "ProjectConfig",
    "StyleDefaults",
    "ResolvedPaths",
    "load_config",
    "merge_configs",
    "resolve_paths",
    "validate_config",
]
