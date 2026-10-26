"""`logsum-make-log`: write the sample logs the lesson starts from."""

from __future__ import annotations

import argparse
import random
import sys
from collections.abc import Sequence
from pathlib import Path

from logsum.infrastructure.sample_log import write_sample_log, write_small_log


def main(argv: Sequence[str] | None = None) -> int:
    """Write a sample log and report what it holds. The same seed always gives the same file."""
    parser = argparse.ArgumentParser(prog="logsum-make-log", description="Write a sample access log to practice on.")
    parser.add_argument("output", type=Path, help="file to write")
    parser.add_argument("--lines", type=int, default=500_000, help="total lines (default: %(default)s)")
    parser.add_argument("--bad", type=int, default=300, help="malformed lines among them (default: %(default)s)")
    parser.add_argument("--seed", type=int, default=7, help="random seed (default: %(default)s)")
    parser.add_argument("--small", action="store_true", help="write the 20-line log whose p95 is 19.95 instead")
    arguments = parser.parse_args(argv)
    if arguments.small:
        write_small_log(arguments.output)
        print(f"wrote 20 lines (0 bad) to {arguments.output}")
        return 0
    try:
        write_sample_log(
            arguments.output, lines=arguments.lines, bad_lines=arguments.bad, rng=random.Random(arguments.seed)
        )
    except ValueError as error:
        print(f"logsum-make-log: {error}", file=sys.stderr)
        return 2
    print(f"wrote {arguments.lines} lines ({arguments.bad} bad) to {arguments.output}")
    return 0


def entrypoint() -> int:
    """The installed command."""
    return main()
