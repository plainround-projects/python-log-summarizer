"""What the use case needs from the outside world, as interfaces the infrastructure layer implements."""

from __future__ import annotations

from collections.abc import Iterator
from contextlib import AbstractContextManager
from typing import Protocol


class LineSource(Protocol):
    """Opens a log by name and hands out its lines one at a time."""

    def open(self, location: str) -> AbstractContextManager[Iterator[str]]:
        """Open `location`; the context closes it, also when reading fails.

        Raises `UnreadableLogFileError` when it cannot be opened or read.
        """


class Clock(Protocol):
    """A monotonic clock in seconds, injected so tests control time."""

    def monotonic(self) -> float:
        """Seconds from an arbitrary start; only differences mean anything."""


class MemoryMeter(Protocol):
    """Measures the peak Python memory of a run."""

    def start(self) -> None:
        """Begin measuring."""

    def stop(self) -> int:
        """Stop measuring and return the peak in bytes since `start`."""
