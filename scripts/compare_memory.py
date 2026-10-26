"""The failure mode the lesson names: reading the whole file into a list.

Prints the peak memory of summarizing a log by streaming it and by loading every line first, for the whole
file and for a tenth of it. Streaming stays flat; loading grows with the file.
"""

from __future__ import annotations

import sys
import tempfile
import tracemalloc
from collections.abc import Callable
from itertools import islice
from pathlib import Path

from logsum.application.summarize import BadLineCounter, stream_requests


def streaming(path: Path) -> int:
    """Count the requests, holding one line at a time."""
    with path.open(encoding="utf-8") as handle:
        return sum(1 for _ in stream_requests(handle, BadLineCounter()))


def loading_everything(path: Path) -> int:
    """Count the requests after loading every line into a list."""
    with path.open(encoding="utf-8") as handle:
        lines = handle.readlines()  # every line held at once: the mistake
    return sum(1 for _ in stream_requests(lines, BadLineCounter()))


def peak_megabytes(work: Callable[[Path], int], path: Path) -> float:
    """Peak traced memory of `work(path)`, in megabytes."""
    tracemalloc.start()
    work(path)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / (1024 * 1024)


def main(log: Path) -> None:
    """Print the comparison for the whole log and for a tenth of it."""
    with log.open(encoding="utf-8") as source:
        total = sum(1 for _ in source)
    with tempfile.TemporaryDirectory() as folder:
        tenth = Path(folder) / "tenth.log"
        with log.open(encoding="utf-8") as source:
            tenth.write_text("".join(islice(source, total // 10)), encoding="utf-8")
        print(f"{'lines':>10}  {'streaming':>10}  {'readlines':>10}   (peak traced memory, MB)")
        for path, lines in ((tenth, total // 10), (log, total)):
            streamed, loaded = peak_megabytes(streaming, path), peak_megabytes(loading_everything, path)
            print(f"{lines:>10}  {streamed:>10.1f}  {loaded:>10.1f}")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
