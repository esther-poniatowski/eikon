"""Advisory file locking for concurrent registry access.

Provides a context manager that acquires an exclusive lock on the
registry manifest file, preventing partial reads or lost writes when
multiple processes access the same manifest concurrently.

Uses ``fcntl.flock`` (Unix/macOS) when available, with a no-op
fallback on platforms that lack ``fcntl`` (e.g. Windows).
"""

from __future__ import annotations

import time
from collections.abc import Generator
from contextlib import contextmanager
from pathlib import Path

from eikon.exceptions import RegistryError

try:
    import fcntl

    _HAS_FCNTL = True
except ImportError:
    _HAS_FCNTL = False

__all__ = ["registry_lock"]

_DEFAULT_TIMEOUT: float = 5.0
_POLL_INTERVAL: float = 0.1


@contextmanager
def registry_lock(
    path: Path,
    *,
    timeout: float = _DEFAULT_TIMEOUT,
) -> Generator[None]:
    """Acquire an exclusive advisory lock on a file.

    Parameters
    ----------
    path : Path
        Path to the file to lock.  A ``.lock`` sibling file is used.
    timeout : float
        Maximum seconds to wait for the lock.  Defaults to 5.

    Yields
    ------
    None
        Control while the lock is held.

    Raises
    ------
    RegistryError
        If the lock cannot be acquired within *timeout*.
    """
    if not _HAS_FCNTL:
        yield
        return

    lock_path = path.with_suffix(path.suffix + ".lock")
    lock_path.parent.mkdir(parents=True, exist_ok=True)

    fd = lock_path.open("w")
    deadline = time.monotonic() + timeout

    while True:
        try:
            fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
            break
        except OSError:
            if time.monotonic() >= deadline:
                fd.close()
                msg = (
                    f"Could not acquire registry lock on {lock_path} "
                    f"within {timeout}s.  Another process may be writing "
                    f"the registry manifest."
                )
                raise RegistryError(msg)
            time.sleep(_POLL_INTERVAL)

    try:
        yield
    finally:
        fcntl.flock(fd, fcntl.LOCK_UN)
        fd.close()
