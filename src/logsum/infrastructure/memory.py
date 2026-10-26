"""Peak memory of a run, measured with `tracemalloc`."""

from __future__ import annotations

import tracemalloc


class TracemallocMeter:
    """Measures the peak of Python-level allocations, which is what should stay flat as the file grows.

    Tracing slows the run by a few times, so the command-line tool measures only when asked to (`--stats`).
    """

    def start(self) -> None:
        """Start tracing and reset the peak."""
        tracemalloc.start()
        tracemalloc.reset_peak()

    def stop(self) -> int:
        """Stop tracing and return the peak, in bytes, since `start`."""
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak
