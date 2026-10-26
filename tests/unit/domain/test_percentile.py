import random
from statistics import quantiles

import pytest

from logsum.domain.errors import EmptyDistributionError
from logsum.domain.percentile import p95, p95_from_ranks


def test_the_p95_of_one_to_twenty_is_the_hand_checked_value():
    assert p95(list(range(1, 21))) == pytest.approx(19.95)


def test_the_p95_does_not_depend_on_the_order_of_the_latencies():
    values = list(range(1, 21))
    random.Random(1).shuffle(values)
    assert p95(values) == pytest.approx(19.95)


def test_a_single_latency_is_its_own_percentile():
    assert p95([42]) == 42.0


def test_few_latencies_never_give_a_percentile_above_the_slowest_request():
    assert max([10, 20, 30, 40]) == 40
    assert quantiles([10, 20, 30, 40], n=100)[94] == pytest.approx(47.5)  # what the library alone would say
    assert p95([10, 20, 30, 40]) == 40.0


def test_an_empty_distribution_has_no_percentile():
    with pytest.raises(EmptyDistributionError):
        p95([])
    with pytest.raises(EmptyDistributionError):
        p95_from_ranks(0, lambda index: index)


@pytest.mark.parametrize("count", [1, 2, 3, 5, 19, 20, 21, 99, 100, 101, 1000])
def test_the_rank_based_percentile_agrees_with_the_library_for_every_sample_size(count):
    values = sorted(random.Random(count).randint(1, 500) for _ in range(count))
    expected = p95(values)
    assert p95_from_ranks(count, values.__getitem__) == pytest.approx(expected)
