"""In-memory stand-ins for the ports."""

from __future__ import annotations

from collections.abc import Iterable, Iterator
from contextlib import contextmanager

from logsum.domain.errors import UnreadableLogFileError


class InMemorySource:
    """A LineSource over named lists of lines; records which names were opened and closed."""

    def __init__(self, logs: dict[str, Iterable[str]]) -> None:
        self._logs = logs
        self.opened: list[str] = []
        self.closed: list[str] = []

    @contextmanager
    def open(self, location: str) -> Iterator[Iterator[str]]:
        if location not in self._logs:
            raise UnreadableLogFileError(location, "no such file")
        self.opened.append(location)
        try:
            yield iter(self._logs[location])
        finally:
            self.closed.append(location)


class SteppingClock:
    """A clock that moves forward a fixed step each time it is read."""

    def __init__(self, step: float = 2.5) -> None:
        self._now = 100.0
        self._step = step

    def monotonic(self) -> float:
        value = self._now
        self._now += self._step
        return value


class FixedMemoryMeter:
    """A MemoryMeter that reports a given peak and remembers how it was used."""

    def __init__(self, peak: int) -> None:
        self._peak = peak
        self.calls: list[str] = []

    def start(self) -> None:
        self.calls.append("start")

    def stop(self) -> int:
        self.calls.append("stop")
        return self._peak
