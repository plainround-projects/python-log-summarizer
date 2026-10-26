from datetime import UTC, datetime

import pytest

from logsum.domain.distribution import ExactLatencies
from logsum.domain.request import Request
from logsum.domain.tally import LogTally


def request(path="/a", status=200, latency=10):
    return Request(datetime(2026, 3, 14, tzinfo=UTC), "GET", path, status, latency)


def test_an_empty_tally_summarizes_to_nothing():
    summary = LogTally(ExactLatencies).summary()
    assert (summary.total_requests, summary.bad_lines, dict(summary.status_counts), summary.slowest_paths) == (
        0,
        0,
        {},
        (),
    )


def test_statuses_are_counted_and_listed_in_order():
    tally = LogTally(ExactLatencies)
    for status in (500, 200, 404, 200, 200):
        tally.add(request(status=status))
    assert dict(tally.summary().status_counts) == {200: 3, 404: 1, 500: 1}
    assert list(tally.summary().status_counts) == [200, 404, 500]
    assert tally.summary().total_requests == 5


def test_bad_lines_are_counted_apart_from_requests():
    tally = LogTally(ExactLatencies)
    tally.add_bad_lines()
    tally.add_bad_lines(4)
    assert tally.summary().bad_lines == 5
    assert tally.summary().total_requests == 0


def test_each_path_keeps_its_own_distribution():
    tally = LogTally(ExactLatencies)
    for latency in range(1, 21):
        tally.add(request("/fast", latency=latency))
        tally.add(request("/slow", latency=latency * 10))
    by_path = {entry.path: entry for entry in tally.summary().slowest_paths}
    assert by_path["/fast"].p95_ms == pytest.approx(19.95)
    assert by_path["/slow"].p95_ms == pytest.approx(199.5)
    assert by_path["/fast"].requests == 20


def test_slowest_paths_come_first_and_ties_break_by_path_name():
    tally = LogTally(ExactLatencies)
    for path, latency in (("/b", 50), ("/a", 50), ("/c", 90), ("/d", 10)):
        tally.add(request(path, latency=latency))
    assert [entry.path for entry in tally.summary().slowest_paths] == ["/c", "/a", "/b", "/d"]


def test_the_summary_lists_at_most_top_paths():
    tally = LogTally(ExactLatencies)
    for number in range(15):
        tally.add(request(f"/p{number:02d}", latency=number + 1))
    assert len(tally.summary().slowest_paths) == 10
    assert len(tally.summary(top=3).slowest_paths) == 3
    assert tally.summary(top=3).slowest_paths[0].path == "/p14"


def test_a_path_with_one_request_is_included():
    tally = LogTally(ExactLatencies)
    tally.add(request("/once", latency=77))
    assert tally.summary().slowest_paths[0].p95_ms == 77.0
