"""
Entry point for the `eikon` package, invoked as a module.

Usage
-----
To launch the command-line interface, execute::

    python -m eikon


See Also
--------
eikon.cli: Module implementing the application's command-line interface.
"""
from .cli import app

app()
