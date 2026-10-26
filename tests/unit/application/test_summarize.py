import pytest

from logsum.application.summarize import BadLineCounter, SummarizeLog, stream_requests
from logsum.domain.distribution import ExactLatencies
from logsum.domain.errors import UnreadableLogFileError
from tests.unit.application.fakes import FixedMemoryMeter, InMemorySource, SteppingClock

GOOD = "2026-03-14T09:26:53Z GET /a 200 {}ms"


def test_stream_requests_yields_one_request_per_good_line_and_counts_the_rest():
    counter = BadLineCounter()
    lines = [GOOD.format(5) + "\n", "\n", "2026-03-14T09:26:53Z GET /a 200\n", GOOD.format(7) + "\r\n", "garbage"]
    assert [request.latency_ms for request in stream_requests(lines, counter)] == [5, 7]
    assert counter.count == 3


def test_stream_requests_reads_lazily_so_memory_does_not_depend_on_the_input():
    pulled = []

    def lines():
        for number in range(1, 1_000_000):
            pulled.append(number)
            yield GOOD.format(number)

    counter = BadLineCounter()
    stream = stream_requests(lines(), counter)
    next(stream)
    next(stream)
    assert pulled == [1, 2]


def test_run_summarizes_the_log_and_measures_time_and_memory():
    source = InMemorySource({"x.log": [GOOD.format(n) for n in range(1, 21)] + ["", "oops"]})
    memory = FixedMemoryMeter(peak=4_000_000)
    report = SummarizeLog(source, SteppingClock(step=2.5), ExactLatencies, memory).run("x.log")
    assert report.summary.total_requests == 20
    assert report.summary.bad_lines == 2
    assert report.summary.slowest_paths[0].p95_ms == pytest.approx(19.95)
    assert report.elapsed_seconds == 2.5
    assert report.peak_memory_bytes == 4_000_000
    assert memory.calls == ["start", "stop"]


def test_run_without_a_meter_reports_no_memory():
    report = SummarizeLog(InMemorySource({"x.log": []}), SteppingClock(), ExactLatencies).run("x.log")
    assert report.peak_memory_bytes is None
    assert report.summary.total_requests == 0


def test_run_closes_the_source_and_stops_the_meter_when_reading_fails():
    def failing_lines():
        yield GOOD.format(1)
        raise UnreadableLogFileError("x.log", "disk went away")

    source = InMemorySource({"x.log": failing_lines()})
    memory = FixedMemoryMeter(peak=1)
    with pytest.raises(UnreadableLogFileError, match="disk went away"):
        SummarizeLog(source, SteppingClock(), ExactLatencies, memory).run("x.log")
    assert source.closed == ["x.log"]
    assert memory.calls == ["start", "stop"]


def test_run_passes_an_unreadable_file_through_as_a_named_error():
    with pytest.raises(UnreadableLogFileError, match=r"missing\.log"):
        SummarizeLog(InMemorySource({}), SteppingClock(), ExactLatencies).run("missing.log")


def test_run_lists_only_the_requested_number_of_paths():
    lines = [f"2026-03-14T09:26:53Z GET /p{number} 200 {number}ms" for number in range(1, 6)]
    report = SummarizeLog(InMemorySource({"x.log": lines}), SteppingClock(), ExactLatencies).run("x.log", top=2)
    assert [entry.path for entry in report.summary.slowest_paths] == ["/p5", "/p4"]
