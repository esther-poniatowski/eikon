"""Sphinx configuration for the eikon documentation."""

project = "eikon"
copyright = "2026, Esther Poniatowski"
author = "Esther Poniatowski"

extensions = [
    "myst_parser",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.intersphinx",
]

autodoc_member_order = "bysource"
autodoc_typehints = "description"
napoleon_google_style = False
napoleon_numpy_style = True

myst_enable_extensions = [
    "colon_fence",
    "fieldlist",
]
myst_heading_anchors = 3

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "matplotlib": ("https://matplotlib.org/stable/", None),
}

source_suffix = {
    ".rst": "restructuredtext",
    ".md": "markdown",
}
