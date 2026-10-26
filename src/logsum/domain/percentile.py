"""The 95th percentile, defined once so every distribution agrees on it."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from statistics import quantiles

from logsum.domain.errors import EmptyDistributionError

_CUTS = 100
_PERCENT = 95
_P95_INDEX = _PERCENT - 1  # quantiles(..., n=100) returns 99 cut points; the 95th is at index 94


def p95(latencies: Sequence[int]) -> float:
    """The 95th percentile by the exclusive method (the `statistics.quantiles` default).

    A single latency is its own percentile. For the integers 1 to 20 the answer is 19.95. The exclusive method
    extrapolates past the largest value when there are few data points (four latencies give 47.5 for a maximum of
    40), so the answer is capped at the largest latency: no request was slower than that.
    """
    if not latencies:
        raise EmptyDistributionError("no latencies to take a percentile of")
    if len(latencies) == 1:
        return float(latencies[0])
    return min(quantiles(latencies, n=_CUTS)[_P95_INDEX], float(max(latencies)))


def p95_from_ranks(count: int, kth_smallest: Callable[[int], int]) -> float:
    """The same value as `p95`, computed from `count` and a lookup of the k-th smallest latency (0-based).

    This lets a histogram answer without expanding itself into a sorted list. The arithmetic is the one in
    `statistics.quantiles`: scale the cut point to the rank space, clamp it, interpolate between neighbors.
    """
    if count == 0:
        raise EmptyDistributionError("no latencies to take a percentile of")
    if count == 1:
        return float(kth_smallest(0))
    spacing = count + 1
    rank = min(max(_PERCENT * spacing // _CUTS, 1), count - 1)
    delta = _PERCENT * spacing - rank * _CUTS
    interpolated = (kth_smallest(rank - 1) * (_CUTS - delta) + kth_smallest(rank) * delta) / _CUTS
    return min(interpolated, float(kth_smallest(count - 1)))
