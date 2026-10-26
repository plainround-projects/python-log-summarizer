"""`logsum`: summarize an access log from the command line."""

from __future__ import annotations

import argparse
import logging
import os
import sys
from collections.abc import Callable, Mapping, Sequence
from typing import TextIO

from logsum import __version__
from logsum.application.summarize import SummarizeLog
from logsum.domain.distribution import ExactLatencies, HistogramLatencies, LatencyDistribution
from logsum.domain.errors import InvalidSettingError, UnreadableLogFileError
from logsum.infrastructure.clock import SystemClock
from logsum.infrastructure.log_files import FileLineSource
from logsum.infrastructure.logging import configure_logging
from logsum.infrastructure.memory import TracemallocMeter
from logsum.infrastructure.settings import ESTIMATORS, Settings
from logsum.interfaces.render import render_json, render_text

logger = logging.getLogger(__name__)

EXIT_OK = 0
EXIT_UNREADABLE = 1
EXIT_USAGE = 2
EXIT_INTERRUPTED = 130


def distribution_factory(settings: Settings) -> Callable[[], LatencyDistribution]:
    """The distribution each path gets: every latency in a list, or fixed-size buckets."""
    if settings.estimator == "histogram":
        return lambda: HistogramLatencies(settings.bucket_ms, settings.max_latency_ms)
    return ExactLatencies


def build_parser(defaults: Settings) -> argparse.ArgumentParser:
    """The argument parser, with the environment's settings as its defaults."""
    parser = argparse.ArgumentParser(
        prog="logsum",
        description="Summarize a web server access log: requests per status, the slowest paths by 95th-percentile "
        "latency, and the lines that could not be parsed. The file is streamed one line at a time; a name ending "
        "in .gz is decompressed on the fly. Lines look like: 2026-03-14T09:26:53Z GET /orders/1234 200 87ms",
    )
    parser.add_argument("log", help="path to the access log (plain text or .gz)")
    parser.add_argument(
        "--top", type=int, default=defaults.top, help="how many slow paths to list (default: %(default)s)"
    )
    parser.add_argument("--json", action="store_true", help="print the summary as JSON (docs/summary.schema.json)")
    parser.add_argument("--stats", action="store_true", help="also report elapsed time and peak memory (slows the run)")
    parser.add_argument(
        "--estimator",
        choices=ESTIMATORS,
        default=defaults.estimator,
        help="exact keeps every latency; histogram keeps fixed-size buckets (default: %(default)s)",
    )
    parser.add_argument(
        "--bucket-ms", type=int, default=defaults.bucket_ms, help="histogram bucket width (default: %(default)s)"
    )
    parser.add_argument(
        "--max-latency-ms", type=int, default=defaults.max_latency_ms, help="histogram cap (default: %(default)s)"
    )
    parser.add_argument(
        "--log-level", default=defaults.log_level, help="log level on standard error (default: %(default)s)"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser


def main(
    argv: Sequence[str] | None = None,
    *,
    environ: Mapping[str, str] | None = None,
    stdout: TextIO | None = None,
    stderr: TextIO | None = None,
) -> int:
    """Run the command and return its exit code: 0 done, 1 unreadable file, 2 bad arguments or settings."""
    out = stdout or sys.stdout
    err = stderr or sys.stderr
    try:
        defaults = Settings.from_environ(os.environ if environ is None else environ)
        arguments = build_parser(defaults).parse_args(argv)
        settings = Settings(
            log_level=arguments.log_level,
            top=arguments.top,
            estimator=arguments.estimator,
            bucket_ms=arguments.bucket_ms,
            max_latency_ms=arguments.max_latency_ms,
        )
    except InvalidSettingError as error:
        print(f"logsum: {error}", file=err)
        return EXIT_USAGE

    configure_logging(settings.log_level, err)
    use_case = SummarizeLog(
        FileLineSource(),
        SystemClock(),
        distribution_factory(settings),
        TracemallocMeter() if arguments.stats else None,
    )
    try:
        report = use_case.run(arguments.log, top=settings.top)
    except UnreadableLogFileError as error:
        logger.error("cannot read the log", extra={"fields": {"location": error.location, "reason": error.reason}})
        print(f"logsum: {error}", file=err)
        return EXIT_UNREADABLE
    if arguments.json:
        print(render_json(report, show_stats=arguments.stats), file=out)
    else:
        print(render_text(report, top=settings.top, show_stats=arguments.stats), file=out)
    return EXIT_OK


def entrypoint() -> int:
    """The installed command: `main` plus the two ways a command-line tool ends early, Ctrl-C and a closed pipe."""
    try:
        code = main()
        sys.stdout.flush()  # in the try: a closed pipe surfaces on flush, and at interpreter exit it is code 120
        return code
    except KeyboardInterrupt:
        print("logsum: interrupted", file=sys.stderr)
        return EXIT_INTERRUPTED
    except BrokenPipeError:
        # the reader of our output (for example `head`) left; point stdout at devnull so exit does not fail again
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return EXIT_OK
