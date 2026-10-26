"""The running totals of a log, and the summary they turn into."""

from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Mapping
from dataclasses import dataclass

from logsum.domain.distribution import LatencyDistribution
from logsum.domain.request import Request


@dataclass(frozen=True, slots=True)
class PathLatency:
    """The 95th-percentile latency of one path and how many requests it is based on."""

    path: str
    p95_ms: float
    requests: int


@dataclass(frozen=True, slots=True)
class Summary:
    """What the program prints: requests per status, the slowest paths, and the lines it could not read."""

    total_requests: int
    bad_lines: int
    status_counts: Mapping[int, int]
    slowest_paths: tuple[PathLatency, ...]


class LogTally:
    """Accumulates one request at a time; memory depends on the paths and the distribution, not the file."""

    def __init__(self, new_distribution: Callable[[], LatencyDistribution]) -> None:
        self._new_distribution = new_distribution
        self._statuses: Counter[int] = Counter()
        self._by_path: dict[str, LatencyDistribution] = {}
        self._bad_lines = 0

    def add(self, request: Request) -> None:
        """Count a parsed request under its status and file its latency under its path.

        One distribution per path, because the ten slowest paths are compared with each other and a
        percentile over all latencies mixed together says nothing about any one path.
        """
        self._statuses[request.status] += 1
        distribution = self._by_path.get(request.path)
        if distribution is None:
            distribution = self._by_path[request.path] = self._new_distribution()
        distribution.add(request.latency_ms)

    def add_bad_lines(self, count: int = 1) -> None:
        """Count lines that could not be read."""
        self._bad_lines += count

    def summary(self, top: int = 10) -> Summary:
        """The totals so far, with the `top` paths of highest 95th-percentile latency (ties by path name)."""
        ranked = sorted(
            (PathLatency(path, distribution.p95(), len(distribution)) for path, distribution in self._by_path.items()),
            key=lambda entry: (-entry.p95_ms, entry.path),
        )
        return Summary(
            total_requests=self._statuses.total(),
            bad_lines=self._bad_lines,
            status_counts=dict(sorted(self._statuses.items())),
            slowest_paths=tuple(ranked[:top]),
        )
