"""The real clock."""

from __future__ import annotations

import time


class SystemClock:
    """A monotonic clock backed by `time.perf_counter`."""

    def monotonic(self) -> float:
        """Seconds from an arbitrary start."""
        return time.perf_counter()
