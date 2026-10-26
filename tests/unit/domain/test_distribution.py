import random

import pytest

from logsum.domain.distribution import ExactLatencies, HistogramLatencies
from logsum.domain.errors import EmptyDistributionError, InvalidSettingError


def test_exact_latencies_report_the_hand_checked_percentile():
    distribution = ExactLatencies()
    for latency in range(1, 21):
        distribution.add(latency)
    assert len(distribution) == 20
    assert distribution.p95() == pytest.approx(19.95)


def test_an_empty_distribution_has_no_percentile():
    with pytest.raises(EmptyDistributionError):
        ExactLatencies().p95()
    with pytest.raises(EmptyDistributionError):
        HistogramLatencies().p95()


def test_a_histogram_with_one_millisecond_buckets_matches_the_exact_percentile():
    rng = random.Random(3)
    exact, histogram = ExactLatencies(), HistogramLatencies(bucket_ms=1, max_latency_ms=1000)
    for _ in range(5000):
        latency = rng.randint(1, 400)
        exact.add(latency)
        histogram.add(latency)
    assert histogram.p95() == pytest.approx(exact.p95())
    assert len(histogram) == 5000


@pytest.mark.parametrize("bucket_ms", [2, 5, 10, 50])
def test_a_wider_bucket_never_overstates_the_percentile_and_is_off_by_less_than_one_bucket(bucket_ms):
    rng = random.Random(bucket_ms)
    exact, histogram = ExactLatencies(), HistogramLatencies(bucket_ms=bucket_ms, max_latency_ms=1000)
    for _ in range(3000):
        latency = rng.randint(5, 900)
        exact.add(latency)
        histogram.add(latency)
    error = exact.p95() - histogram.p95()
    assert 0 <= error < bucket_ms


def test_latencies_over_the_cap_count_as_the_cap():
    histogram = HistogramLatencies(bucket_ms=10, max_latency_ms=100)
    for _ in range(20):
        histogram.add(5_000)
    assert histogram.p95() == 100.0


def test_a_histogram_uses_the_same_memory_for_few_and_many_latencies():
    few, many = HistogramLatencies(), HistogramLatencies()
    for latency in range(10):
        few.add(latency)
    for latency in range(100_000):
        many.add(latency % 300)
    assert few._counts.buffer_info()[1] == many._counts.buffer_info()[1]


@pytest.mark.parametrize(("bucket_ms", "cap"), [(0, 100), (-1, 100), (10, 5)])
def test_a_histogram_rejects_a_width_or_cap_that_makes_no_sense(bucket_ms, cap):
    with pytest.raises(InvalidSettingError):
        HistogramLatencies(bucket_ms=bucket_ms, max_latency_ms=cap)
