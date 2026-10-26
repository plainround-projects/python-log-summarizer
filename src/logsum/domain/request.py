"""One parsed access-log line and the function that reads it."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

_FIELD_COUNT = 5
_LATENCY_SUFFIX = "ms"
_FIRST_STATUS = 100
_LAST_STATUS = 599


@dataclass(frozen=True, slots=True)
class Request:
    """One request from the access log. Immutable, and without a per-instance dict, since one exists per line."""

    timestamp: datetime
    method: str
    path: str
    status: int
    latency_ms: int


def _digits_to_int(text: str) -> int | None:
    # int() also accepts "+5", "1_000" and non-ASCII digits; a log field is plain ASCII digits or it is bad.
    return int(text) if text.isascii() and text.isdecimal() else None


def parse(line: str) -> Request | None:
    """Read one line of `<timestamp> <METHOD> <path> <status> <latency>ms`.

    Returns None for any line that is not in that format: a missing or extra field, a timestamp without a
    time zone, a status outside 100-599, a latency that is not whole milliseconds. A bad line is routine in a
    large log, so it is a value the caller checks and not an exception.
    """
    fields = line.split()
    if len(fields) != _FIELD_COUNT:
        return None
    raw_timestamp, method, path, raw_status, raw_latency = fields
    if not raw_latency.endswith(_LATENCY_SUFFIX):
        return None
    status = _digits_to_int(raw_status)
    latency_ms = _digits_to_int(raw_latency.removesuffix(_LATENCY_SUFFIX))
    if status is None or latency_ms is None or not _FIRST_STATUS <= status <= _LAST_STATUS:
        return None
    if not (method.isascii() and method.isalpha() and method.isupper() and path.startswith("/")):
        return None
    try:
        timestamp = datetime.fromisoformat(raw_timestamp)
    except ValueError:
        return None
    if timestamp.tzinfo is None:
        return None
    return Request(timestamp, method, path, status, latency_ms)
