"""Where the latencies of one path are kept, and how much each choice remembers."""

from __future__ import annotations

from array import array
from typing import Protocol

from logsum.domain.errors import InvalidSettingError
from logsum.domain.percentile import p95, p95_from_ranks


class LatencyDistribution(Protocol):
    """The latencies seen for one path."""

    def add(self, latency_ms: int) -> None:
        """Record one latency."""

    def p95(self) -> float:
        """The 95th percentile of what was recorded."""

    def __len__(self) -> int:
        """How many latencies were recorded."""


class ExactLatencies:
    """Every latency in a list, so the percentile is exact.

    The list grows with the number of requests to the path, with no bound: a hot path with tens of millions of
    requests holds tens of millions of integers. That is fine for a summary of one file and wrong for a long
    running service, which is what `HistogramLatencies` is for.
    """

    def __init__(self) -> None:
        self._values: list[int] = []

    def add(self, latency_ms: int) -> None:
        """Record one latency."""
        self._values.append(latency_ms)

    def p95(self) -> float:
        """The exact 95th percentile."""
        return p95(self._values)

    def __len__(self) -> int:
        return len(self._values)


class HistogramLatencies:
    """Counts per fixed-width bucket, so memory is the same for ten requests and ten billion.

    Accuracy given up, stated exactly: a latency is remembered as the lower edge of its bucket, so the
    percentile is never above the exact one and at most `bucket_ms - 1` below it, for whole-millisecond
    latencies under `max_latency_ms`. A latency at or over `max_latency_ms` counts as `max_latency_ms`, so
    the percentile is wrong only when more than 5 percent of requests exceed that cap. With `bucket_ms=1` the
    answer is identical to `ExactLatencies` below the cap.
    """

    def __init__(self, bucket_ms: int = 5, max_latency_ms: int = 10_000) -> None:
        if bucket_ms < 1 or max_latency_ms < bucket_ms:
            raise InvalidSettingError(
                f"need 1 <= bucket_ms <= max_latency_ms, got bucket_ms={bucket_ms}, max_latency_ms={max_latency_ms}"
            )
        self._bucket_ms = bucket_ms
        self._last_bucket = max_latency_ms // bucket_ms
        self._counts = array("Q", bytes(8 * (self._last_bucket + 1)))
        self._total = 0

    def add(self, latency_ms: int) -> None:
        """Record one latency."""
        self._counts[min(latency_ms // self._bucket_ms, self._last_bucket)] += 1
        self._total += 1

    def p95(self) -> float:
        """The 95th percentile, to within the bucket width."""
        return p95_from_ranks(self._total, self._kth_smallest)

    def _kth_smallest(self, index: int) -> int:
        seen = 0
        for bucket, count in enumerate(self._counts):
            seen += count
            if index < seen:
                return bucket * self._bucket_ms
        raise IndexError(index)  # pragma: no cover - callers stay below the total

    def __len__(self) -> int:
        return self._total
