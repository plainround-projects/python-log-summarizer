# python-log-summarizer

`logsum`: a command-line tool that streams a web server access log and prints the requests per status code, the slowest paths by 95th-percentile latency and the number of lines it could not parse, using the same memory for a 5 GB file as for a 5 MB one.

| | |
| --- | --- |
| **Lesson** | `/prep/python/project-log-summarizer`, "A typed Python command-line tool that streams a large file" (`data-structure-explainer/src/content/tracks/python/11-project-log-summarizer.md` in the Plainround app) |
| **Planned hours** | 5 |
| **Level** | Beginner |
| **Architecture** | [ARCHITECTURE.md](ARCHITECTURE.md), decisions: [docs/adr](docs/adr) |

## Architecture

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/architecture-dark.svg">
  <img alt="The Access log is read one line at a time by the Line generator, which calls the Parser. A bad line goes to the Bad-line counter, a good Request goes to the Tally, and the Tally produces the Summary report as text or JSON." src="docs/diagrams/architecture.svg">
</picture>

Memory depends on how many distinct paths there are, not on the file, because only one line and the running Tally are ever held; the amber note is the readlines() alternative that would grow with the file.

## How one run flows

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="docs/diagrams/flow-dark.svg">
  <img alt="logsum pulls one line at a time, parses it, yields a Request or counts a bad line, tallies by status and path, then takes the 95th percentile per path and prints the top ten." src="docs/diagrams/flow.svg">
</picture>

The amber row is the bad line that is counted and skipped instead of stopping the run; the green box is what the summary prints.

## Prerequisites

| Tool | Version | Used for |
| --- | --- | --- |
| Python | 3.12 or newer (the lesson's `requires-python`); tested with 3.14.3 and 3.12.13, the CI runs 3.12, 3.13 and 3.14 | the tool and its tests |
| uv | 0.5 or newer (tested with 0.11.2) | the environment, the `uv.lock` lock file, building the wheel; it downloads a missing Python itself |
| GNU Make | 3.81 or newer | every command below |

No Docker (the tool reads a file; there is no service), no cloud account, no network at run time. The tool has no runtime dependencies at all, only the standard library; pytest, pytest-cov, ruff, mypy, import-linter, pip-audit and jsonschema are development dependencies, pinned in `uv.lock`.

## Setup, run, test, stop

```bash
make up                  # uv sync from uv.lock, then writes data/sample.log (500,000 lines, 300 bad) and data/small.log (20 lines)
make run                 # summarize the 500,000-line log, with elapsed time and peak memory
make run-small           # summarize the 20-line log; the p95 is 19.95
make test                # unit, integration and end-to-end tests with coverage (about 12 seconds)
make lint                # ruff check, ruff format --check, mypy --strict, import-linter
make demo-memory         # the failure mode: streaming against readlines(), peak memory on a tenth and on all of the log
make mutation-check      # step 5: change "ms" to "s" in a scratch copy of the parser; the tests must fail
make install-check       # step 6: install the built wheel into a fresh virtual environment and run logsum there
make audit               # known-vulnerability check of the locked dependencies (pip-audit)
make down                # remove the generated logs and local caches
```

`make help` lists every target. `uv run logsum --help` prints the usage. The installed commands are `logsum` and `logsum-make-log` (the lesson's log generator, with a seed). Operational log lines (structured `logfmt`) go to standard error and are off below `WARNING` unless `--log-level INFO` is given; the summary goes to standard output, so `logsum big.log --json | jq` works.

```text
$ logsum data/sample.log --stats
statuses: {200: 300250, 404: 99539, 500: 99911}
slowest paths by p95 latency in ms (top 10):
    238.00  /cart  (99747 requests)
    238.00  /health  (99947 requests)
    238.00  /orders/1234  (100025 requests)
    238.00  /search  (100091 requests)
    238.00  /users/42  (99890 requests)
bad lines: 300
elapsed: 2.50s  peak memory: 4.0 MB
```

Options: `--top N`, `--json` (described by [docs/summary.schema.json](docs/summary.schema.json)), `--stats`, `--estimator exact|histogram` with `--bucket-ms` and `--max-latency-ms`, `--log-level`. Every setting can also come from a `LOGSUM_*` environment variable ([.env.example](.env.example)); a flag beats the environment, the environment beats the default. A file whose name ends in `.gz` is decompressed on the fly. Exit codes: 0 done, 1 unreadable file, 2 bad arguments or settings, 130 interrupted.

## Done when: the lesson's checklist and the proof for each line

The lesson has a "Done when" under each of its six steps; they are listed here in step order.

| # | Done when (from the lesson) | Command | What proves it |
| --- | --- | --- | --- |
| 1 | After `uv sync`, `uv run logsum --help` prints usage, and `uv.lock` is committed. | `uv sync && uv run logsum --help` | The help text starts `usage: logsum [-h] [--top TOP] [--json] [--stats] ...`. `uv.lock` is tracked by git (`git ls-files uv.lock`). The entry point is `logsum = "logsum.interfaces.cli:entrypoint"` under `[project.scripts]` in `pyproject.toml`. |
| 2 | The type checker passes with no errors in strict mode, and `parse("")` returns `None`. | `make lint` | `mypy` (configured `strict = true` in `pyproject.toml`) prints `Success: no issues found in 47 source files`. `tests/unit/domain/test_request.py::test_an_empty_line_is_not_a_request` asserts `parse("") is None`. |
| 3 | On the 500,000-line file, peak memory stays under 50 MB, measured with `tracemalloc` or `/usr/bin/time`. | `make run` and `/usr/bin/time -l .venv/bin/logsum data/sample.log` | `peak memory: 4.0 MB` (`tracemalloc`) and `35897344 maximum resident set size` (35.9 MB, the whole interpreter included, measured with `/usr/bin/time -l` on macOS). `make demo-memory` shows the contrast: streaming 0.1 MB for a tenth of the file and for all of it, `readlines()` 4.6 MB and 44.4 MB. The e2e test `test_peak_memory_stays_under_fifty_megabytes_and_does_not_grow_with_the_file` enforces both. |
| 4 | For a hand-made 20-line log, the p95 of one path matches what you work out by hand. | `make run-small` | `19.95  /orders/1234  (20 requests)`, the value of `statistics.quantiles(range(1, 21), n=100)[94]` by the exclusive method. The hand check: rank `0.95 * 21 = 19.95`, between the 19th and 20th value, 19 + 0.95 = 19.95. |
| 5 | `uv run pytest` passes, and changing the latency suffix from `ms` to `s` makes at least one test fail. | `make test` and `make mutation-check` | `121 passed`. The mutation check edits `_LATENCY_SUFFIX = "ms"` to `"s"` in a scratch copy and runs the unit tests there: `15 failed, 89 passed`, then `mutant killed: the tests failed as they should` (the check exits nonzero if the mutant survives). |
| 6 | `logsum sample.log` works from a fresh virtual environment, with nothing installed by hand. | `make install-check` | The script builds the wheel with `uv build`, creates an empty environment in a temporary folder, installs only the wheel (`installed into a fresh environment: logsum 0.1.0;`), changes to another directory with `PYTHONPATH` unset and runs the installed `logsum` on the sample log; the output is the same summary as above. |

The lesson's six-line review checklist repeats these six lines. Besides them, `make run` shows `bad lines: 300`, the number the generator plants: 100 lines missing a field, 100 with `abcms` for a latency and 100 empty lines, and the tool counts all three and goes on (`test_the_summary_counts_every_line_and_exactly_the_planted_bad_ones` asserts 300 bad and 499,700 requests).

## The lesson's expected output against this build

The lesson shows `statuses: {200: 300241, 404: 99562, 500: 99897}` and a p95 of 238.0 for every path. With the seed this repository fixes (7) the counts are `300250 / 99539 / 99911` and the p95 is `238.00` for all five paths, because 250 is the largest latency the generator draws and each path sees about 100,000 of them, so the 95th percentile sits next to the cap. The shape agrees; the exact counts depend on the random generator and are the lesson's illustration, not a contract.

## Stretch goals

| Stretch (from the lesson) | Built? |
| --- | --- |
| Read gzip-compressed logs transparently with `gzip.open` when the file ends in `.gz`. | Yes. `FileLineSource` in `src/logsum/infrastructure/log_files.py`; tested against a real gzip file, a truncated one and a file named `.gz` that is not gzip (`tests/integration`), and the 500,000-line e2e test checks the `.gz` summary equals the plain one. |
| Replace the per-path lists with a fixed-size histogram, so memory stays flat however many requests a path gets, and state the accuracy you gave up. | Yes. `--estimator histogram`, `HistogramLatencies` in `src/logsum/domain/distribution.py`. The accuracy given up, exactly: the p95 is never above the exact one and at most `bucket_ms - 1` below it for latencies under `--max-latency-ms`; on the sample log it prints 235 against the exact 238 with 5 ms buckets. With `--bucket-ms 1` the answer is identical to the exact one (tested against `statistics.quantiles`). Unit tests check both claims. |
| Add a `--json` output and a test that checks it against a schema. | Yes. `--json`, [docs/summary.schema.json](docs/summary.schema.json), checked with `jsonschema` in `tests/unit/interfaces/test_cli.py`. |

## What is simplified for teaching

Only what the lesson scopes out, plus where this build differs from the lesson's text:

- One input file per run, no tailing of a growing log and no rotation handling.
- One fixed line format (the lesson's). Other formats (a combined log format, JSON lines) would be a second `parse` in the domain.
- Per-path state is one distribution per distinct path string, so a log whose paths carry ids (`/orders/1234`, `/orders/1235`, ...) would keep one entry per id. The lesson's log has five paths; normalizing paths is the extension noted in ARCHITECTURE.md.
- The lesson's step 4 solution leaves out paths with fewer than two requests because `statistics.quantiles` rejects them; this build lists them (a single latency is its own p95), and caps the exclusive-method percentile at the slowest observed request, because with a handful of requests the method extrapolates past the maximum (four latencies of 10 to 40 ms would give 47.5).
- The lesson's `parse` accepts anything `int()` accepts; this one rejects `+5`, `1_0` and non-ASCII digits, statuses outside 100 to 599 and timestamps without a time zone, all as bad lines.
- No network is involved, so there are no timeouts or retries to configure, no health command and no graceful shutdown beyond closing the file on Ctrl-C (exit 130) and a closed pipe (exit 0). There is no `Dockerfile` or `docker-compose.yml`: nothing here serves traffic, and `make install-check` proves the packaged form.

## Project structure

```text
src/logsum/
  domain/            Request and parse(), the p95 definition, ExactLatencies and HistogramLatencies, LogTally and
                     Summary, named errors. Depends on nothing outside the standard library, and no I/O.
  application/       the SummarizeLog use case, stream_requests (the line generator) and BadLineCounter, and the
                     ports it needs (LineSource, Clock, MemoryMeter). Depends on domain only.
  infrastructure/    adapters: FileLineSource (plain and gzip), SystemClock, TracemallocMeter, Settings from the
                     environment, logfmt logging, the sample-log writer. Depends on application and domain.
  interfaces/        the logsum and logsum-make-log programs: argument parsing, wiring, rendering, exit codes.
                     Nothing depends on it.
tests/
  unit/              domain, application (with in-memory fakes), infrastructure helpers, CLI and rendering.
  integration/       real files, real gzip, a closed pipe and the installed command.
  e2e/               the lesson's scenario: 500,000 lines in, summary out, memory under 50 MB.
  data/              small.log (the hand-checked 20 lines) and two_paths.log (a hand-checkable fixture with bad lines).
scripts/             install_check.sh, mutation_check.sh, compare_memory.py.
docs/                summary.schema.json and adr/ (decision records).
pyproject.toml       project metadata and every tool's configuration (ruff, mypy, pytest, coverage, import-linter).
uv.lock              the locked dependencies.            Makefile  the only commands a reader needs (make help).
```

The dependency rule (domain depends on nothing; application on domain; infrastructure and interfaces on both; nothing on interfaces) is enforced by `make lint` through import-linter; a second contract forbids `domain` and `application` from importing `gzip`, `argparse`, `tracemalloc`, `pathlib`, `os` or `sys`. Adding `import gzip` to `domain/tally.py` makes `lint-imports` print `BROKEN`.

## Author and license

Written by Sumit Srivastava. Released under the MIT License, see [LICENSE](LICENSE). Changes are in [CHANGELOG.md](CHANGELOG.md).
