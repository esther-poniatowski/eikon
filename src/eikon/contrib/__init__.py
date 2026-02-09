"""Built-in plot type wrappers for matplotlib and seaborn.

Importing this package registers all built-in plot types in the
extension registry.  Seaborn types are registered eagerly (the
decorator fires on import) but the actual seaborn import is deferred
to first invocation.
"""

import eikon.contrib._matplotlib as _matplotlib  # noqa: F401
import eikon.contrib._seaborn as _seaborn  # noqa: F401
