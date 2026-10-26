"""Writes the sample logs the lesson asks for: 500,000 lines with a few hundred planted bad ones, and a tiny log."""

from __future__ import annotations

import random
from itertools import cycle
from pathlib import Path

PATHS = ("/orders/1234", "/cart", "/users/42", "/health", "/search")
STATUSES = (200, 200, 200, 404, 500)
_TIMESTAMP = "2026-03-14T09:26:53Z"
_BAD_LINES_BY_KIND = (
    f"{_TIMESTAMP} GET /orders/1234 200",  # one field short
    f"{_TIMESTAMP} GET /orders/1234 200 abcms",  # latency that is not a number
    "",  # an empty line
)
_FLUSH_EVERY = 10_000


def write_sample_log(path: Path, *, lines: int, bad_lines: int, rng: random.Random) -> None:
    """Write `lines` lines to `path`, `bad_lines` of them malformed (the three kinds in turn), in one pass.

    The random generator is passed in so the same seed gives the same file.
    """
    if not 0 <= bad_lines <= lines:
        raise ValueError(f"bad_lines must be between 0 and lines, got {bad_lines} of {lines}")
    bad_at = dict(zip(rng.sample(range(lines), bad_lines), cycle(_BAD_LINES_BY_KIND), strict=False))
    with path.open("w", encoding="utf-8") as handle:
        batch: list[str] = []
        for index in range(lines):
            if index in bad_at:
                batch.append(bad_at[index])
            else:
                latency = rng.randint(5, 250)
                batch.append(f"{_TIMESTAMP} GET {rng.choice(PATHS)} {rng.choice(STATUSES)} {latency}ms")
            if len(batch) == _FLUSH_EVERY:
                handle.write("\n".join(batch) + "\n")
                batch.clear()
        if batch:
            handle.write("\n".join(batch) + "\n")


def write_small_log(path: Path) -> None:
    """Write 20 lines of one path with latencies 1ms to 20ms, whose 95th percentile (19.95) is checked by hand."""
    path.write_text(
        "".join(f"{_TIMESTAMP} GET /orders/1234 200 {latency}ms\n" for latency in range(1, 21)), encoding="utf-8"
    )
