"""The one use case: read a log as a stream and summarize it."""

from __future__ import annotations

import logging
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass

from logsum.application.ports import Clock, LineSource, MemoryMeter
from logsum.domain.distribution import LatencyDistribution
from logsum.domain.request import Request, parse
from logsum.domain.tally import LogTally, Summary

logger = logging.getLogger(__name__)


class BadLineCounter:
    """Counts the lines the stream skipped.

    A generator's `return` value is invisible to a plain `for` loop, so the count lives in an object the
    caller passes in and reads afterwards.
    """

    def __init__(self) -> None:
        self.count = 0


def stream_requests(lines: Iterable[str], bad_lines: BadLineCounter) -> Iterator[Request]:
    """Yield the parsed request of each readable line, one at a time, and count the rest.

    At any moment this holds one line, so memory does not depend on how many lines there are. An empty line
    is a bad line like any other.
    """
    for raw_line in lines:
        request = parse(raw_line.rstrip("\r\n"))
        if request is None:
            bad_lines.count += 1
        else:
            yield request


@dataclass(frozen=True, slots=True)
class RunReport:
    """A summary and how the run that produced it behaved."""

    summary: Summary
    elapsed_seconds: float
    peak_memory_bytes: int | None


class SummarizeLog:
    """Summarize a log file: statuses, slowest paths by 95th percentile, unreadable lines."""

    def __init__(
        self,
        source: LineSource,
        clock: Clock,
        new_distribution: Callable[[], LatencyDistribution],
        memory: MemoryMeter | None = None,
    ) -> None:
        self._source = source
        self._clock = clock
        self._new_distribution = new_distribution
        self._memory = memory

    def run(self, location: str, top: int = 10) -> RunReport:
        """Stream `location` once and return its summary with the elapsed time and peak memory."""
        tally = LogTally(self._new_distribution)
        bad_lines = BadLineCounter()
        if self._memory:
            self._memory.start()
        started = self._clock.monotonic()
        try:
            with self._source.open(location) as lines:
                for request in stream_requests(lines, bad_lines):
                    tally.add(request)
        finally:
            elapsed = self._clock.monotonic() - started
            peak = self._memory.stop() if self._memory else None
        tally.add_bad_lines(bad_lines.count)
        report = RunReport(tally.summary(top), elapsed, peak)
        logger.info(
            "summarized log",
            extra={
                "fields": {
                    "location": location,
                    "requests": report.summary.total_requests,
                    "bad_lines": bad_lines.count,
                    "elapsed_seconds": round(elapsed, 3),
                }
            },
        )
        return report
