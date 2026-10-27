# pytest (the test runner)

<!-- fmt:off -->

## What it is

A **test** is a small program that runs part of your code and checks the result; if a check fails, the test fails. **pytest** is the program that finds the tests, runs them, and reports which passed. A test is a function whose name starts with `test_`, in a file whose name starts with `test_`; a check is a plain `assert` statement. Version here: 9.1.1.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A program has three channels: **standard input** (what it reads), **standard output** (what it prints normally) and **standard error** (where it prints problems and progress). They are separate so a pipe or a file can take the output while errors still show on the screen.
- A **pipe**, written `|`, sends the standard output of the command on its left into the standard input of the command on its right, for example `sort file | head -3`.
- A **redirection** sends a channel somewhere else. `> file` writes standard output to a file, `2>&1` sends standard error to wherever standard output goes, and `/dev/null` is a special file that throws away whatever is written to it.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- An **environment variable** is a named piece of text that a program inherits from the program that started it, for example `PORT=9000`. Programs read them to find out their settings without a settings file. In a shell, `NAME=value command` sets a variable for that one command.
- A **process** is one running program, with its own memory and a number, its **process id** or **PID**. A program can start other processes, its **children**, and wait for them or stop them.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- **JSON** is a text format for data: objects `{"name": "x", "count": 3}` (names with values), lists `[1, 2, 3]`, text in double quotes, numbers, `true`, `false` and `null`. Almost every language can read and write it, which makes it the usual way programs exchange data.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- The **interpreter** is the program that reads Python source files and carries them out. `python` starts it. **CPython** is the standard one, written in C.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- A **decorator** is a line starting with `@` above a function or class. It passes the function to another function that wraps or registers it, for example `@pytest.fixture` or `@dataclass`.
- A **generator** is a function that uses `yield` to hand out values one at a time and pause in between, so a huge sequence never has to exist in memory all at once.
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **fake** (or **mock**, or **stub**) is a simple stand-in for a real part of the system, such as a clock that only moves when the test says so, used so a test is fast and gives the same result every time.
- **Latency** is how long one request takes. A **percentile** says what share of requests were at least that fast: **p95** is the time that 95 out of 100 requests beat, so it shows how bad the slow tail is, which an average hides.
- A **hash** (or **digest**) is a short fixed-size fingerprint computed from data. The same data always gives the same fingerprint, and a tiny change gives a completely different one, so equal fingerprints are used to check that two results are identical.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.
- A **database** stores data in **tables** of rows and columns. **SQL** is the language for asking it questions (`SELECT`) and changing it (`INSERT`, `UPDATE`). A **transaction** groups changes so that either all of them happen or none does.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- **Coverage** reports which lines (and which branches of `if`) were run by the tests; lines never run are lines no test can catch a mistake in.
- A **linter** reads code without running it and reports likely mistakes and style problems. A **formatter** rewrites the layout of the code into one agreed style.
- A **seed** is the starting number of a random number generator. The same seed always produces the same 'random' sequence, which makes experiments and tests repeatable.

## Why this repository uses it

The template asks for unit tests of the domain, integration tests against the real dependency, and one end-to-end run of the lesson's scenario, with names that read as behavior. pytest runs all three levels with one command (`make test`), labels the slower levels with markers, and reports coverage through a plugin.

## Where it appears

| File | What it does with it |
| --- | --- |
| `pyproject.toml` | `[tool.pytest.ini_options]`: the settings. |
| `tests/conftest.py` | shared fixtures: setup code that tests receive by naming it as a parameter. |
| `tests/unit/` | domain, application (with in-memory fakes), infrastructure helpers, CLI and rendering; no real services. |
| `tests/integration/` | real files, real gzip, a closed pipe and the installed command. |
| `tests/e2e/` | 500,000 lines in, a summary out, memory under 50 MB. |
| `Makefile` | `test` runs pytest with coverage; `test-unit` runs the unit folder only. |

## How it works underneath

pytest works in three steps.

1. **Collection.** pytest walks the folders in `testpaths`, imports every `test_*.py` file and lists every function named `test_*`. With `@pytest.mark.parametrize` one function becomes many tests, one per row of data.
2. **Setup.** For each test, pytest looks at the function's parameter names. A name that matches a **fixture** (a function marked `@pytest.fixture`, found in the test file or in a `conftest.py`) is replaced by that fixture's return value. This is how a test gets a fresh temporary folder (`tmp_path`, built in) or a database file (`database_path`, defined in this repository).
3. **Run and report.** pytest calls the test. Python's `assert` is rewritten by pytest so a failure prints the values on both sides. An exception that is not an `assert` failure is an *error*; `pytest.raises(SomeError)` expects one.

A **marker** is a label on a test (`@pytest.mark.integration`). The command-line option `-m integration` selects only labelled tests; a module-level `pytestmark = pytest.mark.integration` labels every test in the file.

**Plugins** add features. They are separate packages that pytest finds by name once installed.

## Walkthrough of this repository's use

```toml
[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = "-ra --strict-markers"
markers = [
    "integration: real files, real gzip and the installed command",
    "e2e: the lesson's scenario on the 500,000-line sample log",
]
```
(`pyproject.toml`, lines 58 to 64)

- `testpaths`: folders pytest searches when run with no arguments.
- `addopts`: options added to every run: `-ra` prints a one-line reason for every test that did not pass (skipped, failed, errored); `--strict-markers` makes an unregistered `@pytest.mark.xxx` an error, so a typo in a marker name cannot silently select nothing.
- `markers`: registers the marker names used to label tests, with a description each.

**Plugins pinned in this repository's development group.**

- `pytest-cov 7.1.0`: adds `--cov`, `--cov-report`; see `coverage.md`.

**Markers.** `integration` (real files, real gzip, the installed command) and `e2e` (the lesson's scenario on the 500,000-line sample log) are registered above. A test file labels itself with a module-level `pytestmark = pytest.mark.integration`. `make test` runs all levels; `pytest -m "not e2e"` would skip the slowest.

**Fixtures.**

```python
"""Shared fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def data_dir() -> Path:
    return ROOT / "tests" / "data"


@pytest.fixture(scope="session")
def summary_schema() -> dict[str, Any]:
    schema: dict[str, Any] = json.loads((ROOT / "docs" / "summary.schema.json").read_text(encoding="utf-8"))
    return schema
```
(`tests/conftest.py`, lines 1 to 22)

`data_dir` and `summary_schema` are fixtures with `scope="session"`: built once per run and shared. A test asks for one by writing its name as a parameter: `def test_the_small_log_prints_the_hand_checked_percentile(data_dir):`. `from __future__ import annotations` and the type hints keep mypy happy; `ROOT` is the repository folder found from the file's own location (`Path(__file__).resolve().parent.parent`).

**Parametrized tests.**

```python
@pytest.mark.parametrize(
    ("line", "why"),
    [
        ("2026-03-14T09:26:53Z GET /orders/1234 200", "a field is missing"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 87ms extra", "an extra field"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 abcms", "the latency is not a number"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 87", "the latency has no ms suffix"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 87s", "the unit is seconds"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 -5ms", "the latency is negative"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 1_0ms", "the latency uses a digit separator"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 8.5ms", "the latency is not whole milliseconds"),
        ("2026-03-14T09:26:53Z GET /orders/1234 20x 87ms", "the status is not a number"),
        ("2026-03-14T09:26:53Z GET /orders/1234 99 87ms", "the status is below 100"),
        ("2026-03-14T09:26:53Z GET /orders/1234 600 87ms", "the status is above 599"),
        ("yesterday GET /orders/1234 200 87ms", "the timestamp is not a timestamp"),
        ("2026-03-14T09:26:53 GET /orders/1234 200 87ms", "the timestamp has no time zone"),
        ("2026-03-14T09:26:53Z get /orders/1234 200 87ms", "the method is lowercase"),
        ("2026-03-14T09:26:53Z GET orders/1234 200 87ms", "the path does not start with a slash"),
        ("2026-03-14T09:26:53Z GET /orders/1234 ٢٠٠ 87ms", "the status uses non-ASCII digits"),
    ],
)
def test_a_line_not_in_the_format_is_not_a_request(line, why):
```
(`tests/unit/domain/test_request.py`, lines 18 to 39)

One function, a list of (line, reason) rows, one test per row. If the parser wrongly accepted `87s`, only that row would fail, with its line printed.

**Built-in fixtures and expected exceptions.**

```python
def test_the_sample_log_has_exactly_the_planted_number_of_bad_lines(tmp_path):
    path = tmp_path / "sample.log"
    write_sample_log(path, lines=2000, bad_lines=30, rng=random.Random(7))
    lines = path.read_text(encoding="utf-8").split("\n")[:-1]
    assert len(lines) == 2000
    assert sum(parse(line) is None for line in lines) == 30
    assert sum(line == "" for line in lines) == 10
```
(`tests/unit/infrastructure/test_sample_log.py`, lines 9 to 15)

`tmp_path` is a fresh temporary folder per test (pytest creates and deletes it). `random.Random(7)` makes the generated file the same every time. And in `tests/unit/domain/test_distribution.py`, `with pytest.raises(InvalidSettingError):` passes only if the block raises that error.

**Approximate comparison.** `assert p95(list(range(1, 21))) == pytest.approx(19.95)` allows for floating-point rounding.

**How the Makefile runs it.**

```make
test: ## all tests (unit, integration, end to end) with coverage; domain and application must stay at 95% or more
	$(RUN) pytest --cov=logsum --cov-report=term
	$(RUN) coverage report --include='src/logsum/domain/*,src/logsum/application/*' --fail-under=95
```
(`Makefile`, lines 32 to 34)

The first command runs every test (`pytest` with no path uses `testpaths`) and measures coverage of the package (`--cov=<package>`, a pytest-cov option) and prints a table (`--cov-report=term`). The second command is not pytest: it asks coverage.py to print the table again for the domain and application folders only and fails (exit code 2) if their total is below 95 percent (see `coverage.md`).

### Every test file, one by one

Generated by reading each test file with Python's parser. A test is a function whose name starts with `test_`; the repository names every test as a sentence, so the sentence is the specification. After the sentence come the decorators (marks and parametrization) and the *fixtures* the test asks for (parameters whose names match a fixture, filled in by pytest).

#### `tests/__init__.py` (0 lines)

Purpose: (no module docstring)

Imports:

This file has no imports.

What the file defines, in order:

Nothing besides imports.

This file is empty.

#### `tests/conftest.py` (22 lines)

Purpose: Shared fixtures.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import json` | Reads and writes JSON text (see `json-and-json-schema.md` or `hashlib-and-json.md`). |
| 6 | `from pathlib import Path` | a file path object |
| 7 | `from typing import Any` | any type; switches type checking off for that value |
| 9 | `import pytest` | The test library (see `pytest.md`). |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 14 | `pytest.fixture` | marks a function as a fixture |
| 21 | `json.loads` | reads JSON from text |

What the file defines, in order:

- constant `ROOT` (line 11) is set to `Path(__file__).resolve().parent.parent`.
- fixture `def data_dir() -> Path` (line 15): the folder `tests/data` that holds the small sample log files Decorators: `@pytest.fixture(scope='session')`.
- fixture `def summary_schema() -> dict[str, Any]` (line 20): reads `docs/summary.schema.json` and returns it as a dictionary, so a test can validate the program's JSON output against it Decorators: `@pytest.fixture(scope='session')`.

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Shared fixtures."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 9):

```python
from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest
```

Module-level statements (line 11):

```python
ROOT = Path(__file__).resolve().parent.parent
```

- line 11: stores `Path(__file__).resolve().parent.parent` in `ROOT`.

**`data_dir`**: the folder `tests/data` that holds the small sample log files (lines 14 to 16):

```python
@pytest.fixture(scope="session")
def data_dir() -> Path:
    return ROOT / "tests" / "data"
```

- line 14: the decorator `pytest.fixture(scope='session')` wraps or registers what is defined just below it.
- line 16: ends the function and gives back `ROOT / 'tests' / 'data'`.

**`summary_schema`**: reads `docs/summary.schema.json` and returns it as a dictionary, so a test can validate the program's JSON output against it (lines 19 to 22):

```python
@pytest.fixture(scope="session")
def summary_schema() -> dict[str, Any]:
    schema: dict[str, Any] = json.loads((ROOT / "docs" / "summary.schema.json").read_text(encoding="utf-8"))
    return schema
```

- line 19: the decorator `pytest.fixture(scope='session')` wraps or registers what is defined just below it.
- line 21: declares `schema` with the type `dict[str, Any]` and stores the result of calling `json.loads` with 1 argument(s) in it.
- line 22: ends the function and gives back `schema`.

#### `tests/e2e/__init__.py` (0 lines)

Purpose: (no module docstring)

Imports:

This file has no imports.

What the file defines, in order:

Nothing besides imports.

This file is empty.

#### `tests/e2e/test_lesson_scenario.py` (88 lines)

Purpose: The lesson's scenario, end to end through the installed commands: 500,000 lines in, a summary out.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import gzip` | Reads and writes gzip-compressed files (see `gzip.md`). |
| 6 | `import json` | Reads and writes JSON text (see `json-and-json-schema.md` or `hashlib-and-json.md`). |
| 7 | `import resource` | The operating system's accounts of a process's resource use (see `resource-getrusage.md`). |
| 8 | `import shutil` | File helpers. `which` finds a program on the path; `copyfileobj` copies one open file into another in blocks. |
| 9 | `import subprocess` | Starts other programs and collects their output (see `subprocess.md`). |
| 10 | `import sys` | Facts about the running interpreter: its command-line arguments, its standard streams, its version. |
| 11 | `from pathlib import Path` | a file path object |
| 13 | `import pytest` | The test library (see `pytest.md`). |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 15 | `pytest.mark` | attaches labels to tests (`parametrize`, `integration`, `e2e`) |
| 17 | `sys.executable` | the path of the Python program running now |
| 24 | `subprocess.run` | starts a program, waits for it, returns its result |
| 30 | `json.loads` | reads JSON from text |
| 33 | `pytest.fixture` | marks a function as a fixture |
| 34 | `pytest.TempPathFactory` | the type of the built-in fixture that creates temporary folders (used in a type hint) |
| 62 | `resource.getrusage` | reads a process's resource accounts |
| 62 | `resource.RUSAGE_CHILDREN` | asks for the accounts of finished child processes |
| 65 | `sys.platform` | the operating system's name (`darwin` for macOS) |
| 78 | `gzip.open` | opens a `.gz` file for reading or writing |
| 79 | `shutil.copyfileobj` | copies one open file into another |

What the file defines, in order:

- constant `pytestmark` (line 15) is set to `pytest.mark.e2e`.
- constant `BIN` (line 17) is set to `Path(sys.executable).parent`.
- constant `MEMORY_BUDGET_BYTES` (line 18) is set to `50 * 1024 * 1024`.
- constant `PLANTED_BAD_LINES` (line 19) is set to `300`.
- constant `LINES` (line 20) is set to `500000`.
- helper `def run(*command, **kwargs)` (line 23): runs a command as a separate process and waits for it (at most 300 seconds); turns every argument into text first; raises if the command exits with a non-zero code (`check=True`); returns the finished process with its output as text
- helper `def summary_of(path, *flags)` (line 29): runs the installed `logsum` command on a file with `--json` and returns its printed JSON as a Python dictionary
- fixture `def sample_log(tmp_path_factory: pytest.TempPathFactory) -> Path` (line 34): a fixture (computed once for the whole test session): runs `logsum-make-log` to write the sample log of the lesson into a temporary folder, checks that the command reported the expected line and bad-line counts, and returns the file's path Decorators: `@pytest.fixture(scope='module')`.
- test `test_the_summary_counts_every_line_and_exactly_the_planted_bad_ones` (line 41), plain: The summary counts every line and exactly the planted bad ones. Uses: `sample_log`.
- test `test_peak_memory_stays_under_fifty_megabytes_and_does_not_grow_with_the_file` (line 50), plain: Peak memory stays under fifty megabytes and does not grow with the file. Uses: `sample_log`, `tmp_path`.
- test `test_the_process_resident_memory_is_also_under_fifty_megabytes` (line 61), plain: The process resident memory is also under fifty megabytes. Uses: `sample_log`.
- test `test_the_hand_checked_log_prints_exactly_19_95` (line 70), plain: The hand checked log prints exactly 19 95. Uses: `tmp_path`.
- test `test_a_gzip_copy_gives_the_same_summary` (line 76), plain: A gzip copy gives the same summary. Uses: `sample_log`, `tmp_path`.
- test `test_the_histogram_estimator_agrees_with_the_exact_one_within_its_bucket_width` (line 83), plain: The histogram estimator agrees with the exact one within its bucket width. Uses: `sample_log`.

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""The lesson's scenario, end to end through the installed commands: 500,000 lines in, a summary out."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 13):

```python
from __future__ import annotations

import gzip
import json
import resource
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
```

Module-level statements (lines 15 to 20):

```python
pytestmark = pytest.mark.e2e

BIN = Path(sys.executable).parent
MEMORY_BUDGET_BYTES = 50 * 1024 * 1024
PLANTED_BAD_LINES = 300
LINES = 500_000
```

- line 15: stores `pytest.mark.e2e` in `pytestmark`.
- line 17: stores `Path(sys.executable).parent` in `BIN`.
- line 18: stores `50 * 1024 * 1024` in `MEMORY_BUDGET_BYTES`.
- line 19: stores `300` in `PLANTED_BAD_LINES`.
- line 20: stores `500000` in `LINES`.

**`run`**: runs a command as a separate process and waits for it (at most 300 seconds); turns every argument into text first; raises if the command exits with a non-zero code (`check=True`); returns the finished process with its output as text (lines 23 to 26):

```python
def run(*command, **kwargs):
    return subprocess.run(
        [str(part) for part in command], capture_output=True, text=True, check=True, timeout=300, **kwargs
    )
```

- line 24: ends the function and gives back the result of calling `subprocess.run` with 6 argument(s).

**`summary_of`**: runs the installed `logsum` command on a file with `--json` and returns its printed JSON as a Python dictionary (lines 29 to 30):

```python
def summary_of(path, *flags):
    return json.loads(run(BIN / "logsum", path, "--json", *flags).stdout)
```

- line 30: ends the function and gives back the result of calling `json.loads` with 1 argument(s).

**`sample_log`**: a fixture (computed once for the whole test session): runs `logsum-make-log` to write the sample log of the lesson into a temporary folder, checks that the command reported the expected line and bad-line counts, and returns the file's path (lines 33 to 38):

```python
@pytest.fixture(scope="module")
def sample_log(tmp_path_factory: pytest.TempPathFactory) -> Path:
    path = tmp_path_factory.mktemp("lesson") / "sample.log"
    result = run(BIN / "logsum-make-log", path)
    assert f"wrote {LINES} lines ({PLANTED_BAD_LINES} bad)" in result.stdout
    return path
```

- line 33: the decorator `pytest.fixture(scope='module')` wraps or registers what is defined just below it.
- line 35: stores `tmp_path_factory.mktemp('lesson') / 'sample.log'` in `path`.
- line 36: stores the result of calling `run` with 2 argument(s) in `result`.
- line 37: checks that `f'wrote {LINES} lines ({PLANTED_BAD_LINES} bad)' in result.stdout` is true; if it is false the program stops with an error.
- line 38: ends the function and gives back `path`.

**`test_the_summary_counts_every_line_and_exactly_the_planted_bad_ones`** (lines 41 to 47):

```python
def test_the_summary_counts_every_line_and_exactly_the_planted_bad_ones(sample_log):
    document = summary_of(sample_log)
    assert document["bad_lines"] == PLANTED_BAD_LINES
    assert document["total_requests"] == LINES - PLANTED_BAD_LINES
    assert sum(document["statuses"].values()) == LINES - PLANTED_BAD_LINES
    assert set(document["statuses"]) == {"200", "404", "500"}
    assert len(document["slowest_paths"]) == 5  # the log has five paths, fewer than the ten asked for
```

- line 42: stores the result of calling `summary_of` with 1 argument(s) in `document`.
- line 43: checks that `document['bad_lines'] == PLANTED_BAD_LINES` is true; if it is false the program stops with an error.
- line 44: checks that `document['total_requests'] == LINES - PLANTED_BAD_LINES` is true; if it is false the program stops with an error.
- line 45: checks that `sum(document['statuses'].values()) == LINES - PLANTED_BAD_LINES` is true; if it is false the program stops with an error.
- line 46: checks that `set(document['statuses']) == {'200', '404', '500'}` is true; if it is false the program stops with an error.
- line 47: checks that `len(document['slowest_paths']) == 5` is true; if it is false the program stops with an error.

**`test_peak_memory_stays_under_fifty_megabytes_and_does_not_grow_with_the_file`** (lines 50 to 58):

```python
def test_peak_memory_stays_under_fifty_megabytes_and_does_not_grow_with_the_file(sample_log, tmp_path):
    full = summary_of(sample_log, "--stats")["stats"]["peak_memory_bytes"]
    tenth = tmp_path / "tenth.log"
    with sample_log.open(encoding="utf-8") as source, tenth.open("w", encoding="utf-8") as target:
        target.writelines(line for _, line in zip(range(LINES // 10), source, strict=False))
    small = summary_of(tenth, "--stats")["stats"]["peak_memory_bytes"]
    assert full < MEMORY_BUDGET_BYTES
    # exact latencies grow by 8 bytes per request, which is the cost the lesson names; the lines themselves do not
    assert full < small + 8 * LINES + 1_000_000
```

- line 51: stores `summary_of(sample_log, '--stats')['stats']['peak_memory_bytes']` in `full`.
- line 52: stores `tmp_path / 'tenth.log'` in `tenth`.
- line 53: opens (`with`) `sample_log.open(encoding='utf-8')` as `source`; `tenth.open('w', encoding='utf-8')` as `target`; whatever it holds is released when the block ends, also after an error:
  - line 54: runs `target.writelines((line for _, line in zip(range(LINES // 10), source, strict=False)))`; the result is not kept.
- line 55: stores `summary_of(tenth, '--stats')['stats']['peak_memory_bytes']` in `small`.
- line 56: checks that `full < MEMORY_BUDGET_BYTES` is true; if it is false the program stops with an error.
- line 58: checks that `full < small + 8 * LINES + 1000000` is true; if it is false the program stops with an error.

**`test_the_process_resident_memory_is_also_under_fifty_megabytes`** (lines 61 to 67):

```python
def test_the_process_resident_memory_is_also_under_fifty_megabytes(sample_log):
    before = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    run(BIN / "logsum", sample_log)
    peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    resident = peak if sys.platform == "darwin" else peak * 1024  # bytes on macOS, kilobytes on Linux
    assert peak >= before
    assert resident < MEMORY_BUDGET_BYTES, f"resident {resident / 2**20:.1f} MB"
```

- line 62: stores `resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss` in `before`.
- line 63: runs `run(BIN / 'logsum', sample_log)`; the result is not kept.
- line 64: stores `resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss` in `peak`.
- line 65: stores `peak` if `sys.platform == 'darwin'`, otherwise `peak * 1024` in `resident`.
- line 66: checks that `peak >= before` is true; if it is false the program stops with an error.
- line 67: checks that `resident < MEMORY_BUDGET_BYTES` is true; if it is false the program stops with an error carrying the message `f'resident {resident / 2 ** 20:.1f} MB'`.

**`test_the_hand_checked_log_prints_exactly_19_95`** (lines 70 to 73):

```python
def test_the_hand_checked_log_prints_exactly_19_95(tmp_path):
    small = tmp_path / "small.log"
    run(BIN / "logsum-make-log", small, "--small")
    assert summary_of(small)["slowest_paths"] == [{"path": "/orders/1234", "p95_ms": 19.95, "requests": 20}]
```

- line 71: stores `tmp_path / 'small.log'` in `small`.
- line 72: runs `run(BIN / 'logsum-make-log', small, '--small')`; the result is not kept.
- line 73: checks that `summary_of(small)['slowest_paths'] == [{'path': '/orders/1234', 'p95_ms': 19.95, 'requests': 20}]` is true; if it is false the program stops with an error.

**`test_a_gzip_copy_gives_the_same_summary`** (lines 76 to 80):

```python
def test_a_gzip_copy_gives_the_same_summary(sample_log, tmp_path):
    compressed = tmp_path / "sample.log.gz"
    with sample_log.open("rb") as source, gzip.open(compressed, "wb", compresslevel=1) as target:
        shutil.copyfileobj(source, target)
    assert summary_of(compressed) == summary_of(sample_log)
```

- line 77: stores `tmp_path / 'sample.log.gz'` in `compressed`.
- line 78: opens (`with`) `sample_log.open('rb')` as `source`; `gzip.open(compressed, 'wb', compresslevel=1)` as `target`; whatever it holds is released when the block ends, also after an error:
  - line 79: runs `shutil.copyfileobj(source, target)`; the result is not kept.
- line 80: checks that `summary_of(compressed) == summary_of(sample_log)` is true; if it is false the program stops with an error.

**`test_the_histogram_estimator_agrees_with_the_exact_one_within_its_bucket_width`** (lines 83 to 88):

```python
def test_the_histogram_estimator_agrees_with_the_exact_one_within_its_bucket_width(sample_log):
    exact = {entry["path"]: entry["p95_ms"] for entry in summary_of(sample_log)["slowest_paths"]}
    histogram = summary_of(sample_log, "--estimator", "histogram", "--bucket-ms", "5")["slowest_paths"]
    assert len(histogram) == len(exact)
    for entry in histogram:
        assert 0 <= exact[entry["path"]] - entry["p95_ms"] < 5
```

- line 84: stores a dictionary built by going through `summary_of(sample_log)['slowest_paths']` in `exact`.
- line 85: stores `summary_of(sample_log, '--estimator', 'histogram', '--bucket-ms', '5')['slowest_paths']` in `histogram`.
- line 86: checks that `len(histogram) == len(exact)` is true; if it is false the program stops with an error.
- line 87: for each item of `histogram`, with the item called `entry`:
  - line 88: checks that `0 <= exact[entry['path']] - entry['p95_ms'] < 5` is true; if it is false the program stops with an error.

#### `tests/integration/__init__.py` (0 lines)

Purpose: (no module docstring)

Imports:

This file has no imports.

What the file defines, in order:

Nothing besides imports.

This file is empty.

#### `tests/integration/test_real_files.py` (108 lines)

Purpose: The adapters and the installed command against real files, real gzip and a real pipe.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import gzip` | Reads and writes gzip-compressed files (see `gzip.md`). |
| 6 | `import json` | Reads and writes JSON text (see `json-and-json-schema.md` or `hashlib-and-json.md`). |
| 7 | `import subprocess` | Starts other programs and collects their output (see `subprocess.md`). |
| 8 | `import sys` | Facts about the running interpreter: its command-line arguments, its standard streams, its version. |
| 9 | `from pathlib import Path` | a file path object |
| 11 | `import pytest` | The test library (see `pytest.md`). |
| 13 | `from logsum.domain.errors import UnreadableLogFileError` | this repository's class `UnreadableLogFileError` (src/logsum/domain/errors.py:8): The log file does not exist, is a directory, or cannot be opened or decompressed. |
| 14 | `from logsum.infrastructure.log_files import FileLineSource` | this repository's class `FileLineSource` (src/logsum/infrastructure/log_files.py:16): Opens files by path. A name ending in `.gz` is decompressed on the fly, still a line at a time. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 16 | `pytest.mark` | attaches labels to tests (`parametrize`, `integration`, `e2e`) |
| 18 | `sys.executable` | the path of the Python program running now |
| 46 | `pytest.raises` | passes only if the block raises the named error |
| 55 | `gzip.compress` | compresses bytes in memory |
| 77 | `subprocess.run` | starts a program, waits for it, returns its result |
| 89 | `json.loads` | reads JSON from text |
| 101 | `subprocess.Popen` | starts a program and lets the parent go on |
| 102 | `subprocess.PIPE` | asks for a stream to be connected to the parent so it can be read |

What the file defines, in order:

- constant `pytestmark` (line 16) is set to `pytest.mark.integration`.
- constant `COMMAND` (line 18) is set to `Path(sys.executable).parent / 'logsum'`.
- helper `def read_all(location)` (line 21): opens a file through the repository's `FileLineSource` and returns all its lines as a list
- test `test_a_plain_file_is_read_line_by_line` (line 26), plain: A plain file is read line by line. Uses: `data_dir`.
- test `test_a_gzip_file_gives_the_same_lines_as_the_plain_file` (line 30), plain: A gzip file gives the same lines as the plain file. Uses: `data_dir`, `tmp_path`.
- test `test_bytes_that_are_not_utf8_become_a_bad_line_and_not_a_crash` (line 36), plain: Bytes that are not utf8 become a bad line and not a crash. Uses: `tmp_path`.
- test `test_a_missing_file_and_a_directory_are_unreadable` (line 44), plain: A missing file and a directory are unreadable. Uses: `tmp_path`.
- test `test_a_truncated_gzip_file_is_reported_as_unreadable_while_reading` (line 54), plain: A truncated gzip file is reported as unreadable while reading. Uses: `data_dir`, `tmp_path`.
- test `test_a_file_that_is_not_gzip_but_named_gz_is_unreadable` (line 62), plain: A file that is not gzip but named gz is unreadable. Uses: `tmp_path`.
- test `test_the_file_is_closed_when_the_reader_stops_early` (line 69), plain: The file is closed when the reader stops early. Uses: `data_dir`.
- test `test_the_installed_command_runs_and_prints_help` (line 76), plain: The installed command runs and prints help.
- test `test_the_installed_command_summarizes_a_gzip_log_as_json` (line 82), plain: The installed command summarizes a gzip log as json. Uses: `data_dir`, `tmp_path`.
- test `test_a_missing_file_makes_the_command_exit_one_without_a_traceback` (line 92), plain: A missing file makes the command exit one without a traceback. Uses: `tmp_path`.
- test `test_a_reader_that_closes_the_pipe_early_does_not_produce_a_traceback` (line 100), plain: A reader that closes the pipe early does not produce a traceback. Uses: `data_dir`.

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""The adapters and the installed command against real files, real gzip and a real pipe."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 14):

```python
from __future__ import annotations

import gzip
import json
import subprocess
import sys
from pathlib import Path

import pytest

from logsum.domain.errors import UnreadableLogFileError
from logsum.infrastructure.log_files import FileLineSource
```

Module-level statements (lines 16 to 18):

```python
pytestmark = pytest.mark.integration

COMMAND = Path(sys.executable).parent / "logsum"
```

- line 16: stores `pytest.mark.integration` in `pytestmark`.
- line 18: stores `Path(sys.executable).parent / 'logsum'` in `COMMAND`.

**`read_all`**: opens a file through the repository's `FileLineSource` and returns all its lines as a list (lines 21 to 23):

```python
def read_all(location):
    with FileLineSource().open(str(location)) as lines:
        return list(lines)
```

- line 22: opens (`with`) `FileLineSource().open(str(location))` as `lines`; whatever it holds is released when the block ends, also after an error:
  - line 23: ends the function and gives back the result of calling `list` with 1 argument(s).

**`test_a_plain_file_is_read_line_by_line`** (lines 26 to 27):

```python
def test_a_plain_file_is_read_line_by_line(data_dir):
    assert len(read_all(data_dir / "small.log")) == 20
```

- line 27: checks that `len(read_all(data_dir / 'small.log')) == 20` is true; if it is false the program stops with an error.

**`test_a_gzip_file_gives_the_same_lines_as_the_plain_file`** (lines 30 to 33):

```python
def test_a_gzip_file_gives_the_same_lines_as_the_plain_file(data_dir, tmp_path):
    compressed = tmp_path / "small.log.gz"
    compressed.write_bytes(gzip.compress((data_dir / "small.log").read_bytes()))
    assert read_all(compressed) == read_all(data_dir / "small.log")
```

- line 31: stores `tmp_path / 'small.log.gz'` in `compressed`.
- line 32: runs `compressed.write_bytes(gzip.compress((data_dir / 'small.log').read_bytes()))`; the result is not kept.
- line 33: checks that `read_all(compressed) == read_all(data_dir / 'small.log')` is true; if it is false the program stops with an error.

**`test_bytes_that_are_not_utf8_become_a_bad_line_and_not_a_crash`** (lines 36 to 41):

```python
def test_bytes_that_are_not_utf8_become_a_bad_line_and_not_a_crash(tmp_path):
    path = tmp_path / "binary.log"
    path.write_bytes(
        b"2026-03-14T09:26:53Z GET /a 200 5ms\n\xff\xfe\x00 garbage\n2026-03-14T09:26:53Z GET /a 200 6ms\n"
    )
    assert len(read_all(path)) == 3
```

- line 37: stores `tmp_path / 'binary.log'` in `path`.
- line 38: runs `path.write_bytes(b'2026-03-14T09:26:53Z GET /a 200 5ms\n\xff\xfe\x00 garbage\n2026-03-14T09:26:53Z GET /a 200 6ms\n')`; the result is not kept.
- line 41: checks that `len(read_all(path)) == 3` is true; if it is false the program stops with an error.

**`test_a_missing_file_and_a_directory_are_unreadable`** (lines 44 to 51):

```python
def test_a_missing_file_and_a_directory_are_unreadable(tmp_path):
    with (
        pytest.raises(UnreadableLogFileError, match=r"missing\.log"),
        FileLineSource().open(str(tmp_path / "missing.log")),
    ):
        pass
    with pytest.raises(UnreadableLogFileError), FileLineSource().open(str(tmp_path)):
        pass
```

- line 45: opens (`with`) `pytest.raises(UnreadableLogFileError, match='missing\\.log')`; `FileLineSource().open(str(tmp_path / 'missing.log'))`; whatever it holds is released when the block ends, also after an error:
  - line 49: does nothing (`pass`).
- line 50: opens (`with`) `pytest.raises(UnreadableLogFileError)`; `FileLineSource().open(str(tmp_path))`; whatever it holds is released when the block ends, also after an error:
  - line 51: does nothing (`pass`).

**`test_a_truncated_gzip_file_is_reported_as_unreadable_while_reading`** (lines 54 to 59):

```python
def test_a_truncated_gzip_file_is_reported_as_unreadable_while_reading(data_dir, tmp_path):
    whole = gzip.compress((data_dir / "small.log").read_bytes() * 200)
    path = tmp_path / "cut.log.gz"
    path.write_bytes(whole[: len(whole) // 2])
    with pytest.raises(UnreadableLogFileError), FileLineSource().open(str(path)) as lines:
        list(lines)
```

- line 55: stores the result of calling `gzip.compress` with 1 argument(s) in `whole`.
- line 56: stores `tmp_path / 'cut.log.gz'` in `path`.
- line 57: runs `path.write_bytes(whole[:len(whole) // 2])`; the result is not kept.
- line 58: opens (`with`) `pytest.raises(UnreadableLogFileError)`; `FileLineSource().open(str(path))` as `lines`; whatever it holds is released when the block ends, also after an error:
  - line 59: runs `list(lines)`; the result is not kept.

**`test_a_file_that_is_not_gzip_but_named_gz_is_unreadable`** (lines 62 to 66):

```python
def test_a_file_that_is_not_gzip_but_named_gz_is_unreadable(tmp_path):
    path = tmp_path / "fake.log.gz"
    path.write_text("not compressed\n", encoding="utf-8")
    with pytest.raises(UnreadableLogFileError), FileLineSource().open(str(path)) as lines:
        list(lines)
```

- line 63: stores `tmp_path / 'fake.log.gz'` in `path`.
- line 64: runs `path.write_text('not compressed\n', encoding='utf-8')`; the result is not kept.
- line 65: opens (`with`) `pytest.raises(UnreadableLogFileError)`; `FileLineSource().open(str(path))` as `lines`; whatever it holds is released when the block ends, also after an error:
  - line 66: runs `list(lines)`; the result is not kept.

**`test_the_file_is_closed_when_the_reader_stops_early`** (lines 69 to 73):

```python
def test_the_file_is_closed_when_the_reader_stops_early(data_dir):
    with FileLineSource().open(str(data_dir / "small.log")) as lines:
        next(lines)
    # a second open of the same file works, and nothing leaks a warning (pytest turns ResourceWarning into -ra output)
    assert len(read_all(data_dir / "small.log")) == 20
```

- line 70: opens (`with`) `FileLineSource().open(str(data_dir / 'small.log'))` as `lines`; whatever it holds is released when the block ends, also after an error:
  - line 71: runs `next(lines)`; the result is not kept.
- line 73: checks that `len(read_all(data_dir / 'small.log')) == 20` is true; if it is false the program stops with an error.

**`test_the_installed_command_runs_and_prints_help`** (lines 76 to 79):

```python
def test_the_installed_command_runs_and_prints_help():
    result = subprocess.run([str(COMMAND), "--help"], capture_output=True, text=True, check=False, timeout=30)
    assert result.returncode == 0
    assert "usage: logsum" in result.stdout
```

- line 77: stores the result of calling `subprocess.run` with 5 argument(s) in `result`.
- line 78: checks that `result.returncode == 0` is true; if it is false the program stops with an error.
- line 79: checks that `'usage: logsum' in result.stdout` is true; if it is false the program stops with an error.

**`test_the_installed_command_summarizes_a_gzip_log_as_json`** (lines 82 to 89):

```python
def test_the_installed_command_summarizes_a_gzip_log_as_json(data_dir, tmp_path):
    path = tmp_path / "two.log.gz"
    path.write_bytes(gzip.compress((data_dir / "two_paths.log").read_bytes()))
    result = subprocess.run(
        [str(COMMAND), str(path), "--json"], capture_output=True, text=True, check=False, timeout=30
    )
    assert result.returncode == 0
    assert json.loads(result.stdout)["bad_lines"] == 3
```

- line 83: stores `tmp_path / 'two.log.gz'` in `path`.
- line 84: runs `path.write_bytes(gzip.compress((data_dir / 'two_paths.log').read_bytes()))`; the result is not kept.
- line 85: stores the result of calling `subprocess.run` with 5 argument(s) in `result`.
- line 88: checks that `result.returncode == 0` is true; if it is false the program stops with an error.
- line 89: checks that `json.loads(result.stdout)['bad_lines'] == 3` is true; if it is false the program stops with an error.

**`test_a_missing_file_makes_the_command_exit_one_without_a_traceback`** (lines 92 to 97):

```python
def test_a_missing_file_makes_the_command_exit_one_without_a_traceback(tmp_path):
    result = subprocess.run(
        [str(COMMAND), str(tmp_path / "nope.log")], capture_output=True, text=True, check=False, timeout=30
    )
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
```

- line 93: stores the result of calling `subprocess.run` with 5 argument(s) in `result`.
- line 96: checks that `result.returncode == 1` is true; if it is false the program stops with an error.
- line 97: checks that `'Traceback' not in result.stderr` is true; if it is false the program stops with an error.

**`test_a_reader_that_closes_the_pipe_early_does_not_produce_a_traceback`** (lines 100 to 108):

```python
def test_a_reader_that_closes_the_pipe_early_does_not_produce_a_traceback(data_dir):
    process = subprocess.Popen(
        [str(COMMAND), str(data_dir / "small.log")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    assert process.stdout is not None
    process.stdout.close()
    _, stderr = process.communicate(timeout=30)
    assert "Traceback" not in stderr
    assert process.returncode == 0
```

- line 101: stores the result of calling `subprocess.Popen` with 4 argument(s) in `process`.
- line 104: checks that `process.stdout is not None` is true; if it is false the program stops with an error.
- line 105: runs `process.stdout.close()`; the result is not kept.
- line 106: stores the result of calling `process.communicate` with 1 argument(s) in `(_, stderr)`.
- line 107: checks that `'Traceback' not in stderr` is true; if it is false the program stops with an error.
- line 108: checks that `process.returncode == 0` is true; if it is false the program stops with an error.

#### `tests/unit/__init__.py` (0 lines)

Purpose: (no module docstring)

Imports:

This file has no imports.

What the file defines, in order:

Nothing besides imports.

This file is empty.

#### `tests/unit/application/__init__.py` (0 lines)

Purpose: (no module docstring)

Imports:

This file has no imports.

What the file defines, in order:

Nothing besides imports.

This file is empty.

#### `tests/unit/application/fakes.py` (55 lines)

Purpose: In-memory stand-ins for the ports.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `from collections.abc import Iterable` | type hint for anything a `for` loop can go through |
| 5 | `from collections.abc import Iterator` | type hint for an object that hands out one value at a time (what `next()` reads) |
| 6 | `from contextlib import contextmanager` | builds a `with` object from a generator |
| 8 | `from logsum.domain.errors import UnreadableLogFileError` | this repository's class `UnreadableLogFileError` (src/logsum/domain/errors.py:8): The log file does not exist, is a directory, or cannot be opened or decompressed. |

What the file defines, in order:

- class `InMemorySource` (line 11): A LineSource over named lists of lines; records which names were opened and closed.
  - `def __init__(self, logs: dict[str, Iterable[str]]) -> None` (line 14): builds the object: stores the arguments it was given
  - `def open(self, location: str) -> Iterator[Iterator[str]]` (line 20): a stand-in for opening a log file: raises `UnreadableLogFileError` for a name it does not know; otherwise records the name in `opened`, hands out the stored lines, and records the name in `closed` when the `with` block ends (even after an error)
- class `SteppingClock` (line 30): A clock that moves forward a fixed step each time it is read.
  - `def __init__(self, step: float=2.5) -> None` (line 33): builds the object: stores the arguments it was given
  - `def monotonic(self) -> float` (line 37): returns the current fake time and then moves it forward by a fixed step, so every reading is later than the one before and elapsed times are exact numbers
- class `FixedMemoryMeter` (line 43): A MemoryMeter that reports a given peak and remembers how it was used.
  - `def __init__(self, peak: int) -> None` (line 46): builds the object: stores the arguments it was given
  - `def start(self) -> None` (line 50): records that measuring was started
  - `def stop(self) -> int` (line 53): records that measuring was stopped and returns the fixed peak-memory number given when the fake was built

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""In-memory stand-ins for the ports."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 8):

```python
from __future__ import annotations

from collections.abc import Iterable, Iterator
from contextlib import contextmanager

from logsum.domain.errors import UnreadableLogFileError
```

class `InMemorySource`: A LineSource over named lists of lines; records which names were opened and closed. (lines 11 to 12):

```python
class InMemorySource:
    """A LineSource over named lists of lines; records which names were opened and closed."""
```

- line 12: the docstring: text that describes this piece; Python keeps it but does not run it.

**`InMemorySource.__init__`**: builds the object: stores the arguments it was given (lines 14 to 17):

```python
    def __init__(self, logs: dict[str, Iterable[str]]) -> None:
        self._logs = logs
        self.opened: list[str] = []
        self.closed: list[str] = []
```

- line 15: stores `logs` in `self._logs`.
- line 16: declares `self.opened` with the type `list[str]` and stores `[]` in it.
- line 17: declares `self.closed` with the type `list[str]` and stores `[]` in it.

**`InMemorySource.open`**: a stand-in for opening a log file: raises `UnreadableLogFileError` for a name it does not know; otherwise records the name in `opened`, hands out the stored lines, and records the name in `closed` when the `with` block ends (even after an error) (lines 19 to 27):

```python
    @contextmanager
    def open(self, location: str) -> Iterator[Iterator[str]]:
        if location not in self._logs:
            raise UnreadableLogFileError(location, "no such file")
        self.opened.append(location)
        try:
            yield iter(self._logs[location])
        finally:
            self.closed.append(location)
```

- line 19: the decorator `contextmanager` wraps or registers what is defined just below it.
- line 21: if `location not in self._logs` is true:
  - line 22: raises (throws) the error `UnreadableLogFileError(location, 'no such file')`.
- line 23: runs `self.opened.append(location)`; the result is not kept.
- line 24: tries the block below; an error inside it goes to the matching `except`:
  - line 25: hands out (`yield`) and pauses until the next value is asked for: `iter(self._logs[location])`
- in every case, at the end (`finally`):
  - line 27: runs `self.closed.append(location)`; the result is not kept.

class `SteppingClock`: A clock that moves forward a fixed step each time it is read. (lines 30 to 31):

```python
class SteppingClock:
    """A clock that moves forward a fixed step each time it is read."""
```

- line 31: the docstring: text that describes this piece; Python keeps it but does not run it.

**`SteppingClock.__init__`**: builds the object: stores the arguments it was given (lines 33 to 35):

```python
    def __init__(self, step: float = 2.5) -> None:
        self._now = 100.0
        self._step = step
```

- line 34: stores `100.0` in `self._now`.
- line 35: stores `step` in `self._step`.

**`SteppingClock.monotonic`**: returns the current fake time and then moves it forward by a fixed step, so every reading is later than the one before and elapsed times are exact numbers (lines 37 to 40):

```python
    def monotonic(self) -> float:
        value = self._now
        self._now += self._step
        return value
```

- line 38: stores `self._now` in `value`.
- line 39: adds `self._step` to `self._now`.
- line 40: ends the function and gives back `value`.

class `FixedMemoryMeter`: A MemoryMeter that reports a given peak and remembers how it was used. (lines 43 to 44):

```python
class FixedMemoryMeter:
    """A MemoryMeter that reports a given peak and remembers how it was used."""
```

- line 44: the docstring: text that describes this piece; Python keeps it but does not run it.

**`FixedMemoryMeter.__init__`**: builds the object: stores the arguments it was given (lines 46 to 48):

```python
    def __init__(self, peak: int) -> None:
        self._peak = peak
        self.calls: list[str] = []
```

- line 47: stores `peak` in `self._peak`.
- line 48: declares `self.calls` with the type `list[str]` and stores `[]` in it.

**`FixedMemoryMeter.start`**: records that measuring was started (lines 50 to 51):

```python
    def start(self) -> None:
        self.calls.append("start")
```

- line 51: runs `self.calls.append('start')`; the result is not kept.

**`FixedMemoryMeter.stop`**: records that measuring was stopped and returns the fixed peak-memory number given when the fake was built (lines 53 to 55):

```python
    def stop(self) -> int:
        self.calls.append("stop")
        return self._peak
```

- line 54: runs `self.calls.append('stop')`; the result is not kept.
- line 55: ends the function and gives back `self._peak`.

#### `tests/unit/application/test_summarize.py` (72 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `import pytest` | The test library (see `pytest.md`). |
| 3 | `from logsum.application.summarize import BadLineCounter` | this repository's class `BadLineCounter` (src/logsum/application/summarize.py:17): Counts the lines the stream skipped. |
| 3 | `from logsum.application.summarize import SummarizeLog` | this repository's class `SummarizeLog` (src/logsum/application/summarize.py:51): Summarize a log file: statuses, slowest paths by 95th percentile, unreadable lines. |
| 3 | `from logsum.application.summarize import stream_requests` | this repository's function `stream_requests` (src/logsum/application/summarize.py:28): Yield the parsed request of each readable line, one at a time, and count the rest. |
| 4 | `from logsum.domain.distribution import ExactLatencies` | this repository's class `ExactLatencies` (src/logsum/domain/distribution.py:25): Every latency in a list, so the percentile is exact. |
| 5 | `from logsum.domain.errors import UnreadableLogFileError` | this repository's class `UnreadableLogFileError` (src/logsum/domain/errors.py:8): The log file does not exist, is a directory, or cannot be opened or decompressed. |
| 6 | `from tests.unit.application.fakes import FixedMemoryMeter` | this repository's class `FixedMemoryMeter` (tests/unit/application/fakes.py:43): A MemoryMeter that reports a given peak and remembers how it was used. |
| 6 | `from tests.unit.application.fakes import InMemorySource` | this repository's class `InMemorySource` (tests/unit/application/fakes.py:11): A LineSource over named lists of lines; records which names were opened and closed. |
| 6 | `from tests.unit.application.fakes import SteppingClock` | this repository's class `SteppingClock` (tests/unit/application/fakes.py:30): A clock that moves forward a fixed step each time it is read. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 39 | `pytest.approx` | compares numbers with a small tolerance |
| 58 | `pytest.raises` | passes only if the block raises the named error |

What the file defines, in order:

- constant `GOOD` (line 8) is set to `'2026-03-14T09:26:53Z GET /a 200 {}ms'`.
- test `test_stream_requests_yields_one_request_per_good_line_and_counts_the_rest` (line 11), plain: Stream requests yields one request per good line and counts the rest.
- test `test_stream_requests_reads_lazily_so_memory_does_not_depend_on_the_input` (line 18), plain: Stream requests reads lazily so memory does not depend on the input.
- test `test_run_summarizes_the_log_and_measures_time_and_memory` (line 33), plain: Run summarizes the log and measures time and memory.
- test `test_run_without_a_meter_reports_no_memory` (line 45), plain: Run without a meter reports no memory.
- test `test_run_closes_the_source_and_stops_the_meter_when_reading_fails` (line 51), plain: Run closes the source and stops the meter when reading fails.
- test `test_run_passes_an_unreadable_file_through_as_a_named_error` (line 64), plain: Run passes an unreadable file through as a named error.
- test `test_run_lists_only_the_requested_number_of_paths` (line 69), plain: Run lists only the requested number of paths.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 6):

```python
import pytest

from logsum.application.summarize import BadLineCounter, SummarizeLog, stream_requests
from logsum.domain.distribution import ExactLatencies
from logsum.domain.errors import UnreadableLogFileError
from tests.unit.application.fakes import FixedMemoryMeter, InMemorySource, SteppingClock
```

Module-level statements (line 8):

```python
GOOD = "2026-03-14T09:26:53Z GET /a 200 {}ms"
```

- line 8: stores `'2026-03-14T09:26:53Z GET /a 200 {}ms'` in `GOOD`.

**`test_stream_requests_yields_one_request_per_good_line_and_counts_the_rest`** (lines 11 to 15):

```python
def test_stream_requests_yields_one_request_per_good_line_and_counts_the_rest():
    counter = BadLineCounter()
    lines = [GOOD.format(5) + "\n", "\n", "2026-03-14T09:26:53Z GET /a 200\n", GOOD.format(7) + "\r\n", "garbage"]
    assert [request.latency_ms for request in stream_requests(lines, counter)] == [5, 7]
    assert counter.count == 3
```

- line 12: stores the result of calling `BadLineCounter` in `counter`.
- line 13: stores `[GOOD.format(5) + '\n', '\n', '2026-03-14T09:26:53Z GET /a 200\n', GOOD.format(7) + '\r\n', 'garbage']` in `lines`.
- line 14: checks that `[request.latency_ms for request in stream_requests(lines, counter)] == [5, 7]` is true; if it is false the program stops with an error.
- line 15: checks that `counter.count == 3` is true; if it is false the program stops with an error.

**`test_stream_requests_reads_lazily_so_memory_does_not_depend_on_the_input`** (lines 18 to 30):

```python
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
```

- line 19: stores `[]` in `pulled`.
- line 21: defines the function `lines()`:
  - line 22: for each item of `range(1, 1000000)`, with the item called `number`:
    - line 23: runs `pulled.append(number)`; the result is not kept.
    - line 24: hands out (`yield`) and pauses until the next value is asked for: `GOOD.format(number)`
- line 26: stores the result of calling `BadLineCounter` in `counter`.
- line 27: stores the result of calling `stream_requests` with 2 argument(s) in `stream`.
- line 28: runs `next(stream)`; the result is not kept.
- line 29: runs `next(stream)`; the result is not kept.
- line 30: checks that `pulled == [1, 2]` is true; if it is false the program stops with an error.

**`test_run_summarizes_the_log_and_measures_time_and_memory`** (lines 33 to 42):

```python
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
```

- line 34: stores the result of calling `InMemorySource` with 1 argument(s) in `source`.
- line 35: stores the result of calling `FixedMemoryMeter` with 1 argument(s) in `memory`.
- line 36: stores the result of calling `SummarizeLog(source, SteppingClock(step=2.5), ExactLatencies, memory).run` with 1 argument(s) in `report`.
- line 37: checks that `report.summary.total_requests == 20` is true; if it is false the program stops with an error.
- line 38: checks that `report.summary.bad_lines == 2` is true; if it is false the program stops with an error.
- line 39: checks that `report.summary.slowest_paths[0].p95_ms == pytest.approx(19.95)` is true; if it is false the program stops with an error.
- line 40: checks that `report.elapsed_seconds == 2.5` is true; if it is false the program stops with an error.
- line 41: checks that `report.peak_memory_bytes == 4000000` is true; if it is false the program stops with an error.
- line 42: checks that `memory.calls == ['start', 'stop']` is true; if it is false the program stops with an error.

**`test_run_without_a_meter_reports_no_memory`** (lines 45 to 48):

```python
def test_run_without_a_meter_reports_no_memory():
    report = SummarizeLog(InMemorySource({"x.log": []}), SteppingClock(), ExactLatencies).run("x.log")
    assert report.peak_memory_bytes is None
    assert report.summary.total_requests == 0
```

- line 46: stores the result of calling `SummarizeLog(InMemorySource({'x.log': []}), SteppingClock(), ExactLatencies).run` with 1 argument(s) in `report`.
- line 47: checks that `report.peak_memory_bytes is None` is true; if it is false the program stops with an error.
- line 48: checks that `report.summary.total_requests == 0` is true; if it is false the program stops with an error.

**`test_run_closes_the_source_and_stops_the_meter_when_reading_fails`** (lines 51 to 61):

```python
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
```

- line 52: defines the function `failing_lines()`:
  - line 53: hands out (`yield`) and pauses until the next value is asked for: `GOOD.format(1)`
  - line 54: raises (throws) the error `UnreadableLogFileError('x.log', 'disk went away')`.
- line 56: stores the result of calling `InMemorySource` with 1 argument(s) in `source`.
- line 57: stores the result of calling `FixedMemoryMeter` with 1 argument(s) in `memory`.
- line 58: opens (`with`) `pytest.raises(UnreadableLogFileError, match='disk went away')`; whatever it holds is released when the block ends, also after an error:
  - line 59: runs `SummarizeLog(source, SteppingClock(), ExactLatencies, memory).run('x.log')`; the result is not kept.
- line 60: checks that `source.closed == ['x.log']` is true; if it is false the program stops with an error.
- line 61: checks that `memory.calls == ['start', 'stop']` is true; if it is false the program stops with an error.

**`test_run_passes_an_unreadable_file_through_as_a_named_error`** (lines 64 to 66):

```python
def test_run_passes_an_unreadable_file_through_as_a_named_error():
    with pytest.raises(UnreadableLogFileError, match=r"missing\.log"):
        SummarizeLog(InMemorySource({}), SteppingClock(), ExactLatencies).run("missing.log")
```

- line 65: opens (`with`) `pytest.raises(UnreadableLogFileError, match='missing\\.log')`; whatever it holds is released when the block ends, also after an error:
  - line 66: runs `SummarizeLog(InMemorySource({}), SteppingClock(), ExactLatencies).run('missing.log')`; the result is not kept.

**`test_run_lists_only_the_requested_number_of_paths`** (lines 69 to 72):

```python
def test_run_lists_only_the_requested_number_of_paths():
    lines = [f"2026-03-14T09:26:53Z GET /p{number} 200 {number}ms" for number in range(1, 6)]
    report = SummarizeLog(InMemorySource({"x.log": lines}), SteppingClock(), ExactLatencies).run("x.log", top=2)
    assert [entry.path for entry in report.summary.slowest_paths] == ["/p5", "/p4"]
```

- line 70: stores a list built by going through `range(1, 6)` in `lines`.
- line 71: stores the result of calling `SummarizeLog(InMemorySource({'x.log': lines}), SteppingClock(), ExactLatencie...` with 2 argument(s) in `report`.
- line 72: checks that `[entry.path for entry in report.summary.slowest_paths] == ['/p5', '/p4']` is true; if it is false the program stops with an error.

#### `tests/unit/domain/__init__.py` (0 lines)

Purpose: (no module docstring)

Imports:

This file has no imports.

What the file defines, in order:

Nothing besides imports.

This file is empty.

#### `tests/unit/domain/test_distribution.py` (66 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `import random` | Random numbers. `random.Random(seed)` is a generator with its own state: the same seed gives the same sequence. |
| 3 | `import pytest` | The test library (see `pytest.md`). |
| 5 | `from logsum.domain.distribution import ExactLatencies` | this repository's class `ExactLatencies` (src/logsum/domain/distribution.py:25): Every latency in a list, so the percentile is exact. |
| 5 | `from logsum.domain.distribution import HistogramLatencies` | this repository's class `HistogramLatencies` (src/logsum/domain/distribution.py:48): Counts per fixed-width bucket, so memory is the same for ten requests and ten billion. |
| 6 | `from logsum.domain.errors import EmptyDistributionError` | this repository's class `EmptyDistributionError` (src/logsum/domain/errors.py:17): A percentile was asked of a distribution that holds no latencies. |
| 6 | `from logsum.domain.errors import InvalidSettingError` | this repository's class `InvalidSettingError` (src/logsum/domain/errors.py:21): A setting (environment variable or flag) has a value the program cannot use. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 14 | `pytest.approx` | compares numbers with a small tolerance |
| 18 | `pytest.raises` | passes only if the block raises the named error |
| 25 | `random.Random` | a random number generator with its own seed |
| 35 | `pytest.mark` | attaches labels to tests (`parametrize`, `integration`, `e2e`) |

What the file defines, in order:

- test `test_exact_latencies_report_the_hand_checked_percentile` (line 9), plain: Exact latencies report the hand checked percentile.
- test `test_an_empty_distribution_has_no_percentile` (line 17), plain: An empty distribution has no percentile.
- test `test_a_histogram_with_one_millisecond_buckets_matches_the_exact_percentile` (line 24), plain: A histogram with one millisecond buckets matches the exact percentile.
- test `test_a_wider_bucket_never_overstates_the_percentile_and_is_off_by_less_than_one_bucket` (line 36), plain: A wider bucket never overstates the percentile and is off by less than one bucket. Uses: `bucket_ms`. Decorators: `@pytest.mark.parametrize('bucket_ms', [2, 5, 10, 50])`.
- test `test_latencies_over_the_cap_count_as_the_cap` (line 47), plain: Latencies over the cap count as the cap.
- test `test_a_histogram_uses_the_same_memory_for_few_and_many_latencies` (line 54), plain: A histogram uses the same memory for few and many latencies.
- test `test_a_histogram_rejects_a_width_or_cap_that_makes_no_sense` (line 64), plain: A histogram rejects a width or cap that makes no sense. Uses: `bucket_ms`, `cap`. Decorators: `@pytest.mark.parametrize(('bucket_ms', 'cap'), [(0, 100), (-1, 100), (10, 5)])`.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 6):

```python
import random

import pytest

from logsum.domain.distribution import ExactLatencies, HistogramLatencies
from logsum.domain.errors import EmptyDistributionError, InvalidSettingError
```

**`test_exact_latencies_report_the_hand_checked_percentile`** (lines 9 to 14):

```python
def test_exact_latencies_report_the_hand_checked_percentile():
    distribution = ExactLatencies()
    for latency in range(1, 21):
        distribution.add(latency)
    assert len(distribution) == 20
    assert distribution.p95() == pytest.approx(19.95)
```

- line 10: stores the result of calling `ExactLatencies` in `distribution`.
- line 11: for each item of `range(1, 21)`, with the item called `latency`:
  - line 12: runs `distribution.add(latency)`; the result is not kept.
- line 13: checks that `len(distribution) == 20` is true; if it is false the program stops with an error.
- line 14: checks that `distribution.p95() == pytest.approx(19.95)` is true; if it is false the program stops with an error.

**`test_an_empty_distribution_has_no_percentile`** (lines 17 to 21):

```python
def test_an_empty_distribution_has_no_percentile():
    with pytest.raises(EmptyDistributionError):
        ExactLatencies().p95()
    with pytest.raises(EmptyDistributionError):
        HistogramLatencies().p95()
```

- line 18: opens (`with`) `pytest.raises(EmptyDistributionError)`; whatever it holds is released when the block ends, also after an error:
  - line 19: runs `ExactLatencies().p95()`; the result is not kept.
- line 20: opens (`with`) `pytest.raises(EmptyDistributionError)`; whatever it holds is released when the block ends, also after an error:
  - line 21: runs `HistogramLatencies().p95()`; the result is not kept.

**`test_a_histogram_with_one_millisecond_buckets_matches_the_exact_percentile`** (lines 24 to 32):

```python
def test_a_histogram_with_one_millisecond_buckets_matches_the_exact_percentile():
    rng = random.Random(3)
    exact, histogram = ExactLatencies(), HistogramLatencies(bucket_ms=1, max_latency_ms=1000)
    for _ in range(5000):
        latency = rng.randint(1, 400)
        exact.add(latency)
        histogram.add(latency)
    assert histogram.p95() == pytest.approx(exact.p95())
    assert len(histogram) == 5000
```

- line 25: stores the result of calling `random.Random` with 1 argument(s) in `rng`.
- line 26: stores `(ExactLatencies(), HistogramLatencies(bucket_ms=1, max_latency_ms=1000))` in `(exact, histogram)`.
- line 27: for each item of `range(5000)`, with the item called `_`:
  - line 28: stores the result of calling `rng.randint` with 2 argument(s) in `latency`.
  - line 29: runs `exact.add(latency)`; the result is not kept.
  - line 30: runs `histogram.add(latency)`; the result is not kept.
- line 31: checks that `histogram.p95() == pytest.approx(exact.p95())` is true; if it is false the program stops with an error.
- line 32: checks that `len(histogram) == 5000` is true; if it is false the program stops with an error.

**`test_a_wider_bucket_never_overstates_the_percentile_and_is_off_by_less_than_one_bucket`** (lines 35 to 44):

```python
@pytest.mark.parametrize("bucket_ms", [2, 5, 10, 50])
def test_a_wider_bucket_never_overstates_the_percentile_and_is_off_by_less_than_one_bucket(bucket_ms):
    rng = random.Random(bucket_ms)
    exact, histogram = ExactLatencies(), HistogramLatencies(bucket_ms=bucket_ms, max_latency_ms=1000)
    for _ in range(3000):
        latency = rng.randint(5, 900)
        exact.add(latency)
        histogram.add(latency)
    error = exact.p95() - histogram.p95()
    assert 0 <= error < bucket_ms
```

- line 35: the decorator `pytest.mark.parametrize('bucket_ms', [2, 5, 10, 50])` wraps or registers what is defined just below it.
- line 37: stores the result of calling `random.Random` with 1 argument(s) in `rng`.
- line 38: stores `(ExactLatencies(), HistogramLatencies(bucket_ms=bucket_ms, max_latency_ms=1000))` in `(exact, histogram)`.
- line 39: for each item of `range(3000)`, with the item called `_`:
  - line 40: stores the result of calling `rng.randint` with 2 argument(s) in `latency`.
  - line 41: runs `exact.add(latency)`; the result is not kept.
  - line 42: runs `histogram.add(latency)`; the result is not kept.
- line 43: stores `exact.p95() - histogram.p95()` in `error`.
- line 44: checks that `0 <= error < bucket_ms` is true; if it is false the program stops with an error.

**`test_latencies_over_the_cap_count_as_the_cap`** (lines 47 to 51):

```python
def test_latencies_over_the_cap_count_as_the_cap():
    histogram = HistogramLatencies(bucket_ms=10, max_latency_ms=100)
    for _ in range(20):
        histogram.add(5_000)
    assert histogram.p95() == 100.0
```

- line 48: stores the result of calling `HistogramLatencies` with 2 argument(s) in `histogram`.
- line 49: for each item of `range(20)`, with the item called `_`:
  - line 50: runs `histogram.add(5000)`; the result is not kept.
- line 51: checks that `histogram.p95() == 100.0` is true; if it is false the program stops with an error.

**`test_a_histogram_uses_the_same_memory_for_few_and_many_latencies`** (lines 54 to 60):

```python
def test_a_histogram_uses_the_same_memory_for_few_and_many_latencies():
    few, many = HistogramLatencies(), HistogramLatencies()
    for latency in range(10):
        few.add(latency)
    for latency in range(100_000):
        many.add(latency % 300)
    assert few._counts.buffer_info()[1] == many._counts.buffer_info()[1]
```

- line 55: stores `(HistogramLatencies(), HistogramLatencies())` in `(few, many)`.
- line 56: for each item of `range(10)`, with the item called `latency`:
  - line 57: runs `few.add(latency)`; the result is not kept.
- line 58: for each item of `range(100000)`, with the item called `latency`:
  - line 59: runs `many.add(latency % 300)`; the result is not kept.
- line 60: checks that `few._counts.buffer_info()[1] == many._counts.buffer_info()[1]` is true; if it is false the program stops with an error.

**`test_a_histogram_rejects_a_width_or_cap_that_makes_no_sense`** (lines 63 to 66):

```python
@pytest.mark.parametrize(("bucket_ms", "cap"), [(0, 100), (-1, 100), (10, 5)])
def test_a_histogram_rejects_a_width_or_cap_that_makes_no_sense(bucket_ms, cap):
    with pytest.raises(InvalidSettingError):
        HistogramLatencies(bucket_ms=bucket_ms, max_latency_ms=cap)
```

- line 63: the decorator `pytest.mark.parametrize(('bucket_ms', 'cap'), [(0, 100), (-1, 100), (10, 5)])` wraps or registers what is defined just below it.
- line 65: opens (`with`) `pytest.raises(InvalidSettingError)`; whatever it holds is released when the block ends, also after an error:
  - line 66: runs `HistogramLatencies(bucket_ms=bucket_ms, max_latency_ms=cap)`; the result is not kept.

#### `tests/unit/domain/test_percentile.py` (41 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `import random` | Random numbers. `random.Random(seed)` is a generator with its own state: the same seed gives the same sequence. |
| 2 | `from statistics import quantiles` | cut points that divide data into equal groups (percentiles) |
| 4 | `import pytest` | The test library (see `pytest.md`). |
| 6 | `from logsum.domain.errors import EmptyDistributionError` | this repository's class `EmptyDistributionError` (src/logsum/domain/errors.py:17): A percentile was asked of a distribution that holds no latencies. |
| 7 | `from logsum.domain.percentile import p95` | this repository's function `p95` (src/logsum/domain/percentile.py:15): The 95th percentile by the exclusive method (the `statistics.quantiles` default). |
| 7 | `from logsum.domain.percentile import p95_from_ranks` | this repository's function `p95_from_ranks` (src/logsum/domain/percentile.py:29): The same value as `p95`, computed from `count` and a lookup of the k-th smallest latency (0-based). |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 11 | `pytest.approx` | compares numbers with a small tolerance |
| 16 | `random.Random` | a random number generator with its own seed |
| 31 | `pytest.raises` | passes only if the block raises the named error |
| 37 | `pytest.mark` | attaches labels to tests (`parametrize`, `integration`, `e2e`) |

What the file defines, in order:

- test `test_the_p95_of_one_to_twenty_is_the_hand_checked_value` (line 10), plain: The p95 of one to twenty is the hand checked value.
- test `test_the_p95_does_not_depend_on_the_order_of_the_latencies` (line 14), plain: The p95 does not depend on the order of the latencies.
- test `test_a_single_latency_is_its_own_percentile` (line 20), plain: A single latency is its own percentile.
- test `test_few_latencies_never_give_a_percentile_above_the_slowest_request` (line 24), plain: Few latencies never give a percentile above the slowest request.
- test `test_an_empty_distribution_has_no_percentile` (line 30), plain: An empty distribution has no percentile.
- test `test_the_rank_based_percentile_agrees_with_the_library_for_every_sample_size` (line 38), plain: The rank based percentile agrees with the library for every sample size. Uses: `count`. Decorators: `@pytest.mark.parametrize('count', [1, 2, 3, 5, 19, 20, 21, 99, 100, 101, 1000])`.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 7):

```python
import random
from statistics import quantiles

import pytest

from logsum.domain.errors import EmptyDistributionError
from logsum.domain.percentile import p95, p95_from_ranks
```

**`test_the_p95_of_one_to_twenty_is_the_hand_checked_value`** (lines 10 to 11):

```python
def test_the_p95_of_one_to_twenty_is_the_hand_checked_value():
    assert p95(list(range(1, 21))) == pytest.approx(19.95)
```

- line 11: checks that `p95(list(range(1, 21))) == pytest.approx(19.95)` is true; if it is false the program stops with an error.

**`test_the_p95_does_not_depend_on_the_order_of_the_latencies`** (lines 14 to 17):

```python
def test_the_p95_does_not_depend_on_the_order_of_the_latencies():
    values = list(range(1, 21))
    random.Random(1).shuffle(values)
    assert p95(values) == pytest.approx(19.95)
```

- line 15: stores the result of calling `list` with 1 argument(s) in `values`.
- line 16: runs `random.Random(1).shuffle(values)`; the result is not kept.
- line 17: checks that `p95(values) == pytest.approx(19.95)` is true; if it is false the program stops with an error.

**`test_a_single_latency_is_its_own_percentile`** (lines 20 to 21):

```python
def test_a_single_latency_is_its_own_percentile():
    assert p95([42]) == 42.0
```

- line 21: checks that `p95([42]) == 42.0` is true; if it is false the program stops with an error.

**`test_few_latencies_never_give_a_percentile_above_the_slowest_request`** (lines 24 to 27):

```python
def test_few_latencies_never_give_a_percentile_above_the_slowest_request():
    assert max([10, 20, 30, 40]) == 40
    assert quantiles([10, 20, 30, 40], n=100)[94] == pytest.approx(47.5)  # what the library alone would say
    assert p95([10, 20, 30, 40]) == 40.0
```

- line 25: checks that `max([10, 20, 30, 40]) == 40` is true; if it is false the program stops with an error.
- line 26: checks that `quantiles([10, 20, 30, 40], n=100)[94] == pytest.approx(47.5)` is true; if it is false the program stops with an error.
- line 27: checks that `p95([10, 20, 30, 40]) == 40.0` is true; if it is false the program stops with an error.

**`test_an_empty_distribution_has_no_percentile`** (lines 30 to 34):

```python
def test_an_empty_distribution_has_no_percentile():
    with pytest.raises(EmptyDistributionError):
        p95([])
    with pytest.raises(EmptyDistributionError):
        p95_from_ranks(0, lambda index: index)
```

- line 31: opens (`with`) `pytest.raises(EmptyDistributionError)`; whatever it holds is released when the block ends, also after an error:
  - line 32: runs `p95([])`; the result is not kept.
- line 33: opens (`with`) `pytest.raises(EmptyDistributionError)`; whatever it holds is released when the block ends, also after an error:
  - line 34: runs `p95_from_ranks(0, lambda index: index)`; the result is not kept.

**`test_the_rank_based_percentile_agrees_with_the_library_for_every_sample_size`** (lines 37 to 41):

```python
@pytest.mark.parametrize("count", [1, 2, 3, 5, 19, 20, 21, 99, 100, 101, 1000])
def test_the_rank_based_percentile_agrees_with_the_library_for_every_sample_size(count):
    values = sorted(random.Random(count).randint(1, 500) for _ in range(count))
    expected = p95(values)
    assert p95_from_ranks(count, values.__getitem__) == pytest.approx(expected)
```

- line 37: the decorator `pytest.mark.parametrize('count', [1, 2, 3, 5, 19, 20, 21, 99, 100, 101, 1000])` wraps or registers what is defined just below it.
- line 39: stores the result of calling `sorted` with 1 argument(s) in `values`.
- line 40: stores the result of calling `p95` with 1 argument(s) in `expected`.
- line 41: checks that `p95_from_ranks(count, values.__getitem__) == pytest.approx(expected)` is true; if it is false the program stops with an error.

#### `tests/unit/domain/test_request.py` (51 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `from datetime import UTC` | the universal time zone |
| 1 | `from datetime import datetime` | a date and time |
| 3 | `import pytest` | The test library (see `pytest.md`). |
| 5 | `from logsum.domain.request import Request` | this repository's class `Request` (src/logsum/domain/request.py:15): One request from the access log. Immutable, and without a per-instance dict, since one exists per line. |
| 5 | `from logsum.domain.request import parse` | this repository's function `parse` (src/logsum/domain/request.py:30): Read one line of `<timestamp> <METHOD> <path> <status> <latency>ms`. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 18 | `pytest.mark` | attaches labels to tests (`parametrize`, `integration`, `e2e`) |
| 50 | `pytest.raises` | passes only if the block raises the named error |

What the file defines, in order:

- constant `GOOD` (line 7) is set to `'2026-03-14T09:26:53Z GET /orders/1234 200 87ms'`.
- test `test_a_good_line_becomes_a_request` (line 10), plain: A good line becomes a request.
- test `test_an_empty_line_is_not_a_request` (line 14), plain: An empty line is not a request.
- test `test_a_line_not_in_the_format_is_not_a_request` (line 39), plain: A line not in the format is not a request. Uses: `line`, `why`. Decorators: `@pytest.mark.parametrize(('line', 'why'), [('2026-03-14T09:26:53Z GET /orders/1234 200', 'a field is missing'), ('2026-03-14T09:26:53Z GET /orders/1234 200 87ms extra', 'an extra field'), ('2026-03-14T09:26:53Z GET /orders/1234 200 abcms', 'the latency is not a number'), ('2026-03-14T09:26:53Z GET /orders/1234 200 87', 'the latency has no ms suffix'), ('2026-03-14T09:26:53Z GET /orders/1234 200 87s', 'the unit is seconds'), ('2026-03-14T09:26:53Z GET /orders/1234 200 -5ms', 'the latency is negat...`.
- test `test_a_line_with_extra_whitespace_between_fields_still_parses` (line 43), plain: A line with extra whitespace between fields still parses.
- test `test_a_request_cannot_be_changed_after_it_is_made` (line 47), plain: A request cannot be changed after it is made.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 5):

```python
from datetime import UTC, datetime

import pytest

from logsum.domain.request import Request, parse
```

Module-level statements (line 7):

```python
GOOD = "2026-03-14T09:26:53Z GET /orders/1234 200 87ms"
```

- line 7: stores `'2026-03-14T09:26:53Z GET /orders/1234 200 87ms'` in `GOOD`.

**`test_a_good_line_becomes_a_request`** (lines 10 to 11):

```python
def test_a_good_line_becomes_a_request():
    assert parse(GOOD) == Request(datetime(2026, 3, 14, 9, 26, 53, tzinfo=UTC), "GET", "/orders/1234", 200, 87)
```

- line 11: checks that `parse(GOOD) == Request(datetime(2026, 3, 14, 9, 26, 53, tzinfo=UTC), 'GET', '/orders/1234', 200, 87)` is true; if it is false the program stops with an error.

**`test_an_empty_line_is_not_a_request`** (lines 14 to 15):

```python
def test_an_empty_line_is_not_a_request():
    assert parse("") is None
```

- line 15: checks that `parse('') is None` is true; if it is false the program stops with an error.

**`test_a_line_not_in_the_format_is_not_a_request`** (lines 18 to 40):

```python
@pytest.mark.parametrize(
    ("line", "why"),
    [
        ("2026-03-14T09:26:53Z GET /orders/1234 200", "a field is missing"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 87ms extra", "an extra field"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 abcms", "the latency is not a number"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 87", "the latency has no ms suffix"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 87s", "the unit is seconds"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 -5ms", "the latency is negative"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 1_0ms", "the latency uses a digit separator"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 8.5ms", "the latency is not whole milliseconds"),
        ("2026-03-14T09:26:53Z GET /orders/1234 20x 87ms", "the status is not a number"),
        ("2026-03-14T09:26:53Z GET /orders/1234 99 87ms", "the status is below 100"),
        ("2026-03-14T09:26:53Z GET /orders/1234 600 87ms", "the status is above 599"),
        ("yesterday GET /orders/1234 200 87ms", "the timestamp is not a timestamp"),
        ("2026-03-14T09:26:53 GET /orders/1234 200 87ms", "the timestamp has no time zone"),
        ("2026-03-14T09:26:53Z get /orders/1234 200 87ms", "the method is lowercase"),
        ("2026-03-14T09:26:53Z GET orders/1234 200 87ms", "the path does not start with a slash"),
        ("2026-03-14T09:26:53Z GET /orders/1234 ٢٠٠ 87ms", "the status uses non-ASCII digits"),
    ],
)
def test_a_line_not_in_the_format_is_not_a_request(line, why):
    assert parse(line) is None, why
```

- line 18: the decorator `pytest.mark.parametrize(('line', 'why'), [('2026-03-14T09:26:53Z GET /orders/1234 200', 'a field is missing'), ('2026-03-14T09:26:53Z GET /orders/1234 200 87ms extra', 'an extra field'), ('2026-03-...` wraps or registers what is defined just below it.
- line 40: checks that `parse(line) is None` is true; if it is false the program stops with an error carrying the message `why`.

**`test_a_line_with_extra_whitespace_between_fields_still_parses`** (lines 43 to 44):

```python
def test_a_line_with_extra_whitespace_between_fields_still_parses():
    assert parse("  2026-03-14T09:26:53Z   GET  /cart\t404  5ms ") is not None
```

- line 44: checks that `parse(' 2026-03-14T09:26:53Z GET /cart\t404 5ms ') is not None` is true; if it is false the program stops with an error.

**`test_a_request_cannot_be_changed_after_it_is_made`** (lines 47 to 51):

```python
def test_a_request_cannot_be_changed_after_it_is_made():
    request = parse(GOOD)
    assert request is not None
    with pytest.raises(AttributeError):
        request.status = 500  # type: ignore[misc]
```

- line 48: stores the result of calling `parse` with 1 argument(s) in `request`.
- line 49: checks that `request is not None` is true; if it is false the program stops with an error.
- line 50: opens (`with`) `pytest.raises(AttributeError)`; whatever it holds is released when the block ends, also after an error:
  - line 51: stores `500` in `request.status`.

#### `tests/unit/domain/test_tally.py` (71 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `from datetime import UTC` | the universal time zone |
| 1 | `from datetime import datetime` | a date and time |
| 3 | `import pytest` | The test library (see `pytest.md`). |
| 5 | `from logsum.domain.distribution import ExactLatencies` | this repository's class `ExactLatencies` (src/logsum/domain/distribution.py:25): Every latency in a list, so the percentile is exact. |
| 6 | `from logsum.domain.request import Request` | this repository's class `Request` (src/logsum/domain/request.py:15): One request from the access log. Immutable, and without a per-instance dict, since one exists per line. |
| 7 | `from logsum.domain.tally import LogTally` | this repository's class `LogTally` (src/logsum/domain/tally.py:32): Accumulates one request at a time; memory depends on the paths and the distribution, not the file. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 47 | `pytest.approx` | compares numbers with a small tolerance |

What the file defines, in order:

- helper `def request(path='/a', status=200, latency=10)` (line 10): builds one `Request` with the fixed date 14 March 2026 and the given path, status and latency (defaults `/a`, 200 and 10 ms), so a test states only what matters to it
- test `test_an_empty_tally_summarizes_to_nothing` (line 14), plain: An empty tally summarizes to nothing.
- test `test_statuses_are_counted_and_listed_in_order` (line 24), plain: Statuses are counted and listed in order.
- test `test_bad_lines_are_counted_apart_from_requests` (line 33), plain: Bad lines are counted apart from requests.
- test `test_each_path_keeps_its_own_distribution` (line 41), plain: Each path keeps its own distribution.
- test `test_slowest_paths_come_first_and_ties_break_by_path_name` (line 52), plain: Slowest paths come first and ties break by path name.
- test `test_the_summary_lists_at_most_top_paths` (line 59), plain: The summary lists at most top paths.
- test `test_a_path_with_one_request_is_included` (line 68), plain: A path with one request is included.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 7):

```python
from datetime import UTC, datetime

import pytest

from logsum.domain.distribution import ExactLatencies
from logsum.domain.request import Request
from logsum.domain.tally import LogTally
```

**`request`**: builds one `Request` with the fixed date 14 March 2026 and the given path, status and latency (defaults `/a`, 200 and 10 ms), so a test states only what matters to it (lines 10 to 11):

```python
def request(path="/a", status=200, latency=10):
    return Request(datetime(2026, 3, 14, tzinfo=UTC), "GET", path, status, latency)
```

- line 11: ends the function and gives back the result of calling `Request` with 5 argument(s).

**`test_an_empty_tally_summarizes_to_nothing`** (lines 14 to 21):

```python
def test_an_empty_tally_summarizes_to_nothing():
    summary = LogTally(ExactLatencies).summary()
    assert (summary.total_requests, summary.bad_lines, dict(summary.status_counts), summary.slowest_paths) == (
        0,
        0,
        {},
        (),
    )
```

- line 15: stores the result of calling `LogTally(ExactLatencies).summary` in `summary`.
- line 16: checks that `(summary.total_requests, summary.bad_lines, dict(summary.status_counts), summary.slowest_paths) == (0, 0, {}, ())` is true; if it is false the program stops with an error.

**`test_statuses_are_counted_and_listed_in_order`** (lines 24 to 30):

```python
def test_statuses_are_counted_and_listed_in_order():
    tally = LogTally(ExactLatencies)
    for status in (500, 200, 404, 200, 200):
        tally.add(request(status=status))
    assert dict(tally.summary().status_counts) == {200: 3, 404: 1, 500: 1}
    assert list(tally.summary().status_counts) == [200, 404, 500]
    assert tally.summary().total_requests == 5
```

- line 25: stores the result of calling `LogTally` with 1 argument(s) in `tally`.
- line 26: for each item of `(500, 200, 404, 200, 200)`, with the item called `status`:
  - line 27: runs `tally.add(request(status=status))`; the result is not kept.
- line 28: checks that `dict(tally.summary().status_counts) == {200: 3, 404: 1, 500: 1}` is true; if it is false the program stops with an error.
- line 29: checks that `list(tally.summary().status_counts) == [200, 404, 500]` is true; if it is false the program stops with an error.
- line 30: checks that `tally.summary().total_requests == 5` is true; if it is false the program stops with an error.

**`test_bad_lines_are_counted_apart_from_requests`** (lines 33 to 38):

```python
def test_bad_lines_are_counted_apart_from_requests():
    tally = LogTally(ExactLatencies)
    tally.add_bad_lines()
    tally.add_bad_lines(4)
    assert tally.summary().bad_lines == 5
    assert tally.summary().total_requests == 0
```

- line 34: stores the result of calling `LogTally` with 1 argument(s) in `tally`.
- line 35: runs `tally.add_bad_lines()`; the result is not kept.
- line 36: runs `tally.add_bad_lines(4)`; the result is not kept.
- line 37: checks that `tally.summary().bad_lines == 5` is true; if it is false the program stops with an error.
- line 38: checks that `tally.summary().total_requests == 0` is true; if it is false the program stops with an error.

**`test_each_path_keeps_its_own_distribution`** (lines 41 to 49):

```python
def test_each_path_keeps_its_own_distribution():
    tally = LogTally(ExactLatencies)
    for latency in range(1, 21):
        tally.add(request("/fast", latency=latency))
        tally.add(request("/slow", latency=latency * 10))
    by_path = {entry.path: entry for entry in tally.summary().slowest_paths}
    assert by_path["/fast"].p95_ms == pytest.approx(19.95)
    assert by_path["/slow"].p95_ms == pytest.approx(199.5)
    assert by_path["/fast"].requests == 20
```

- line 42: stores the result of calling `LogTally` with 1 argument(s) in `tally`.
- line 43: for each item of `range(1, 21)`, with the item called `latency`:
  - line 44: runs `tally.add(request('/fast', latency=latency))`; the result is not kept.
  - line 45: runs `tally.add(request('/slow', latency=latency * 10))`; the result is not kept.
- line 46: stores a dictionary built by going through `tally.summary().slowest_paths` in `by_path`.
- line 47: checks that `by_path['/fast'].p95_ms == pytest.approx(19.95)` is true; if it is false the program stops with an error.
- line 48: checks that `by_path['/slow'].p95_ms == pytest.approx(199.5)` is true; if it is false the program stops with an error.
- line 49: checks that `by_path['/fast'].requests == 20` is true; if it is false the program stops with an error.

**`test_slowest_paths_come_first_and_ties_break_by_path_name`** (lines 52 to 56):

```python
def test_slowest_paths_come_first_and_ties_break_by_path_name():
    tally = LogTally(ExactLatencies)
    for path, latency in (("/b", 50), ("/a", 50), ("/c", 90), ("/d", 10)):
        tally.add(request(path, latency=latency))
    assert [entry.path for entry in tally.summary().slowest_paths] == ["/c", "/a", "/b", "/d"]
```

- line 53: stores the result of calling `LogTally` with 1 argument(s) in `tally`.
- line 54: for each item of `(('/b', 50), ('/a', 50), ('/c', 90), ('/d', 10))`, with the item called `(path, latency)`:
  - line 55: runs `tally.add(request(path, latency=latency))`; the result is not kept.
- line 56: checks that `[entry.path for entry in tally.summary().slowest_paths] == ['/c', '/a', '/b', '/d']` is true; if it is false the program stops with an error.

**`test_the_summary_lists_at_most_top_paths`** (lines 59 to 65):

```python
def test_the_summary_lists_at_most_top_paths():
    tally = LogTally(ExactLatencies)
    for number in range(15):
        tally.add(request(f"/p{number:02d}", latency=number + 1))
    assert len(tally.summary().slowest_paths) == 10
    assert len(tally.summary(top=3).slowest_paths) == 3
    assert tally.summary(top=3).slowest_paths[0].path == "/p14"
```

- line 60: stores the result of calling `LogTally` with 1 argument(s) in `tally`.
- line 61: for each item of `range(15)`, with the item called `number`:
  - line 62: runs `tally.add(request(f'/p{number:02d}', latency=number + 1))`; the result is not kept.
- line 63: checks that `len(tally.summary().slowest_paths) == 10` is true; if it is false the program stops with an error.
- line 64: checks that `len(tally.summary(top=3).slowest_paths) == 3` is true; if it is false the program stops with an error.
- line 65: checks that `tally.summary(top=3).slowest_paths[0].path == '/p14'` is true; if it is false the program stops with an error.

**`test_a_path_with_one_request_is_included`** (lines 68 to 71):

```python
def test_a_path_with_one_request_is_included():
    tally = LogTally(ExactLatencies)
    tally.add(request("/once", latency=77))
    assert tally.summary().slowest_paths[0].p95_ms == 77.0
```

- line 69: stores the result of calling `LogTally` with 1 argument(s) in `tally`.
- line 70: runs `tally.add(request('/once', latency=77))`; the result is not kept.
- line 71: checks that `tally.summary().slowest_paths[0].p95_ms == 77.0` is true; if it is false the program stops with an error.

#### `tests/unit/infrastructure/__init__.py` (0 lines)

Purpose: (no module docstring)

Imports:

This file has no imports.

What the file defines, in order:

Nothing besides imports.

This file is empty.

#### `tests/unit/infrastructure/test_clock_and_memory.py` (30 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `from logsum.infrastructure.clock import SystemClock` | this repository's class `SystemClock` (src/logsum/infrastructure/clock.py:8): A monotonic clock backed by `time.perf_counter`. |
| 2 | `from logsum.infrastructure.memory import TracemallocMeter` | this repository's class `TracemallocMeter` (src/logsum/infrastructure/memory.py:8): Measures the peak of Python-level allocations, which is what should stay flat as the file grows. |

What the file defines, in order:

- test `test_the_system_clock_never_goes_backwards` (line 5), plain: The system clock never goes backwards.
- test `test_the_meter_reports_a_peak_that_covers_a_large_allocation` (line 11), plain: The meter reports a peak that covers a large allocation.
- test `test_the_meter_can_be_used_twice_and_forgets_the_first_run` (line 20), plain: The meter can be used twice and forgets the first run.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 2):

```python
from logsum.infrastructure.clock import SystemClock
from logsum.infrastructure.memory import TracemallocMeter
```

**`test_the_system_clock_never_goes_backwards`** (lines 5 to 8):

```python
def test_the_system_clock_never_goes_backwards():
    clock = SystemClock()
    first = clock.monotonic()
    assert clock.monotonic() >= first
```

- line 6: stores the result of calling `SystemClock` in `clock`.
- line 7: stores the result of calling `clock.monotonic` in `first`.
- line 8: checks that `clock.monotonic() >= first` is true; if it is false the program stops with an error.

**`test_the_meter_reports_a_peak_that_covers_a_large_allocation`** (lines 11 to 17):

```python
def test_the_meter_reports_a_peak_that_covers_a_large_allocation():
    meter = TracemallocMeter()
    meter.start()
    block = bytearray(5_000_000)
    del block
    peak = meter.stop()
    assert peak >= 5_000_000
```

- line 12: stores the result of calling `TracemallocMeter` in `meter`.
- line 13: runs `meter.start()`; the result is not kept.
- line 14: stores the result of calling `bytearray` with 1 argument(s) in `block`.
- line 15: deletes `block`.
- line 16: stores the result of calling `meter.stop` in `peak`.
- line 17: checks that `peak >= 5000000` is true; if it is false the program stops with an error.

**`test_the_meter_can_be_used_twice_and_forgets_the_first_run`** (lines 20 to 30):

```python
def test_the_meter_can_be_used_twice_and_forgets_the_first_run():
    meter = TracemallocMeter()
    meter.start()
    big = bytearray(5_000_000)
    del big
    meter.stop()
    meter.start()
    small = bytearray(1000)
    peak = meter.stop()
    assert len(small) == 1000
    assert peak < 1_000_000
```

- line 21: stores the result of calling `TracemallocMeter` in `meter`.
- line 22: runs `meter.start()`; the result is not kept.
- line 23: stores the result of calling `bytearray` with 1 argument(s) in `big`.
- line 24: deletes `big`.
- line 25: runs `meter.stop()`; the result is not kept.
- line 26: runs `meter.start()`; the result is not kept.
- line 27: stores the result of calling `bytearray` with 1 argument(s) in `small`.
- line 28: stores the result of calling `meter.stop` in `peak`.
- line 29: checks that `len(small) == 1000` is true; if it is false the program stops with an error.
- line 30: checks that `peak < 1000000` is true; if it is false the program stops with an error.

#### `tests/unit/infrastructure/test_logging.py` (38 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `import io` | In-memory streams. `io.StringIO` is a text buffer that behaves like a file, used by tests to capture what a program prints. |
| 2 | `import logging` | Python's logging library (see `logging-and-logfmt.md`). |
| 4 | `from logsum.infrastructure.logging import LogfmtFormatter` | this repository's class `LogfmtFormatter` (src/logsum/infrastructure/logging.py:17): Format a log record as one logfmt line, with the record's `fields` extra as key=value pairs. |
| 4 | `from logsum.infrastructure.logging import configure_logging` | this repository's function `configure_logging` (src/logsum/infrastructure/logging.py:35): Send every log record to `stream` (standard error by default) as logfmt. Safe to call twice. |
| 24 | `import sys` | Facts about the running interpreter: its command-line arguments, its standard streams, its version. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 8 | `logging.LogRecord` | one log event with all its facts |
| 8 | `logging.INFO` | the number of the INFO level |
| 26 | `logging.ERROR` | the number of the ERROR level |
| 26 | `sys.exc_info` | the exception being handled |
| 33 | `io.StringIO` | a text buffer that acts like a file |
| 36 | `logging.getLogger` | returns the logger with a given name |

What the file defines, in order:

- helper `def record(message='hello', **fields)` (line 7): builds a log record named `dedupe.test` at INFO level with the given message and attaches the extra `fields`
- test `test_a_record_becomes_one_logfmt_line_with_its_fields` (line 13), plain: A record becomes one logfmt line with its fields.
- test `test_an_exception_is_kept_on_the_same_line` (line 20), plain: An exception is kept on the same line.
- test `test_configure_logging_replaces_handlers_and_sets_the_level` (line 32), plain: Configure logging replaces handlers and sets the level.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 4):

```python
import io
import logging

from logsum.infrastructure.logging import LogfmtFormatter, configure_logging
```

**`record`**: builds a log record named `dedupe.test` at INFO level with the given message and attaches the extra `fields` (lines 7 to 10):

```python
def record(message="hello", **fields):
    made = logging.LogRecord("logsum.test", logging.INFO, __file__, 1, message, None, None)
    made.fields = fields
    return made
```

- line 8: stores the result of calling `logging.LogRecord` with 7 argument(s) in `made`.
- line 9: stores `fields` in `made.fields`.
- line 10: ends the function and gives back `made`.

**`test_a_record_becomes_one_logfmt_line_with_its_fields`** (lines 13 to 17):

```python
def test_a_record_becomes_one_logfmt_line_with_its_fields():
    line = LogfmtFormatter().format(record("summarized log", location="a b.log", requests=5))
    assert line.startswith("ts=")
    assert 'level=INFO logger=logsum.test msg="summarized log" location="a b.log" requests=5' in line
    assert "\n" not in line
```

- line 14: stores the result of calling `LogfmtFormatter().format` with 1 argument(s) in `line`.
- line 15: checks that `line.startswith('ts=')` is true; if it is false the program stops with an error.
- line 16: checks that `'level=INFO logger=logsum.test msg="summarized log" location="a b.log" requests=5' in line` is true; if it is false the program stops with an error.
- line 17: checks that `'\n' not in line` is true; if it is false the program stops with an error.

**`test_an_exception_is_kept_on_the_same_line`** (lines 20 to 29):

```python
def test_an_exception_is_kept_on_the_same_line():
    try:
        raise ValueError("boom")
    except ValueError:
        import sys

        made = logging.LogRecord("x", logging.ERROR, __file__, 1, "failed", None, sys.exc_info())
    line = LogfmtFormatter().format(made)
    assert "exc=" in line
    assert "\n" not in line.replace("\\n", "")
```

- line 21: tries the block below; an error inside it goes to the matching `except`:
  - line 22: raises (throws) the error `ValueError('boom')`.
- line 23: if the error is `ValueError`:
  - line 24: imports `import sys` (here, inside the function, so it only happens when the function runs).
  - line 26: stores the result of calling `logging.LogRecord` with 7 argument(s) in `made`.
- line 27: stores the result of calling `LogfmtFormatter().format` with 1 argument(s) in `line`.
- line 28: checks that `'exc=' in line` is true; if it is false the program stops with an error.
- line 29: checks that `'\n' not in line.replace('\\n', '')` is true; if it is false the program stops with an error.

**`test_configure_logging_replaces_handlers_and_sets_the_level`** (lines 32 to 38):

```python
def test_configure_logging_replaces_handlers_and_sets_the_level():
    stream = io.StringIO()
    configure_logging("INFO", stream)
    configure_logging("INFO", stream)
    logging.getLogger("logsum.test").info("one", extra={"fields": {"n": 1}})
    assert stream.getvalue().count("msg=one") == 1
    assert len(logging.getLogger().handlers) == 1
```

- line 33: stores the result of calling `io.StringIO` in `stream`.
- line 34: runs `configure_logging('INFO', stream)`; the result is not kept.
- line 35: runs `configure_logging('INFO', stream)`; the result is not kept.
- line 36: runs `logging.getLogger('logsum.test').info('one', extra={'fields': {'n': 1}})`; the result is not kept.
- line 37: checks that `stream.getvalue().count('msg=one') == 1` is true; if it is false the program stops with an error.
- line 38: checks that `len(logging.getLogger().handlers) == 1` is true; if it is false the program stops with an error.

#### `tests/unit/infrastructure/test_sample_log.py` (42 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `import random` | Random numbers. `random.Random(seed)` is a generator with its own state: the same seed gives the same sequence. |
| 3 | `import pytest` | The test library (see `pytest.md`). |
| 5 | `from logsum.domain.request import parse` | this repository's function `parse` (src/logsum/domain/request.py:30): Read one line of `<timestamp> <METHOD> <path> <status> <latency>ms`. |
| 6 | `from logsum.infrastructure.sample_log import write_sample_log` | this repository's function `write_sample_log` (src/logsum/infrastructure/sample_log.py:20): Write `lines` lines to `path`, `bad_lines` of them malformed (the three kinds in turn), in one pass. |
| 6 | `from logsum.infrastructure.sample_log import write_small_log` | this repository's function `write_small_log` (src/logsum/infrastructure/sample_log.py:43): Write 20 lines of one path with latencies 1ms to 20ms, whose 95th percentile (19.95) is checked by hand. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 11 | `random.Random` | a random number generator with its own seed |
| 32 | `pytest.mark` | attaches labels to tests (`parametrize`, `integration`, `e2e`) |
| 34 | `pytest.raises` | passes only if the block raises the named error |

What the file defines, in order:

- test `test_the_sample_log_has_exactly_the_planted_number_of_bad_lines` (line 9), plain: The sample log has exactly the planted number of bad lines. Uses: `tmp_path`.
- test `test_the_same_seed_gives_the_same_file_and_another_seed_a_different_one` (line 18), plain: The same seed gives the same file and another seed a different one. Uses: `tmp_path`.
- test `test_a_file_longer_than_one_write_batch_is_complete` (line 26), plain: A file longer than one write batch is complete. Uses: `tmp_path`.
- test `test_more_bad_lines_than_lines_is_refused` (line 33), plain: More bad lines than lines is refused. Uses: `tmp_path`, `lines`, `bad`. Decorators: `@pytest.mark.parametrize(('lines', 'bad'), [(10, 11), (10, -1)])`.
- test `test_the_small_log_has_twenty_lines_of_one_to_twenty_milliseconds` (line 38), plain: The small log has twenty lines of one to twenty milliseconds. Uses: `tmp_path`.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 6):

```python
import random

import pytest

from logsum.domain.request import parse
from logsum.infrastructure.sample_log import write_sample_log, write_small_log
```

**`test_the_sample_log_has_exactly_the_planted_number_of_bad_lines`** (lines 9 to 15):

```python
def test_the_sample_log_has_exactly_the_planted_number_of_bad_lines(tmp_path):
    path = tmp_path / "sample.log"
    write_sample_log(path, lines=2000, bad_lines=30, rng=random.Random(7))
    lines = path.read_text(encoding="utf-8").split("\n")[:-1]
    assert len(lines) == 2000
    assert sum(parse(line) is None for line in lines) == 30
    assert sum(line == "" for line in lines) == 10
```

- line 10: stores `tmp_path / 'sample.log'` in `path`.
- line 11: runs `write_sample_log(path, lines=2000, bad_lines=30, rng=random.Random(7))`; the result is not kept.
- line 12: stores `path.read_text(encoding='utf-8').split('\n')[:-1]` in `lines`.
- line 13: checks that `len(lines) == 2000` is true; if it is false the program stops with an error.
- line 14: checks that `sum((parse(line) is None for line in lines)) == 30` is true; if it is false the program stops with an error.
- line 15: checks that `sum((line == '' for line in lines)) == 10` is true; if it is false the program stops with an error.

**`test_the_same_seed_gives_the_same_file_and_another_seed_a_different_one`** (lines 18 to 23):

```python
def test_the_same_seed_gives_the_same_file_and_another_seed_a_different_one(tmp_path):
    first, second, third = (tmp_path / name for name in ("a.log", "b.log", "c.log"))
    write_sample_log(first, lines=500, bad_lines=5, rng=random.Random(7))
    write_sample_log(second, lines=500, bad_lines=5, rng=random.Random(7))
    write_sample_log(third, lines=500, bad_lines=5, rng=random.Random(8))
    assert first.read_bytes() == second.read_bytes() != third.read_bytes()
```

- line 19: stores a generator (values produced one at a time) built by going through `('a.log', 'b.log', 'c.log')` in `(first, second, third)`.
- line 20: runs `write_sample_log(first, lines=500, bad_lines=5, rng=random.Random(7))`; the result is not kept.
- line 21: runs `write_sample_log(second, lines=500, bad_lines=5, rng=random.Random(7))`; the result is not kept.
- line 22: runs `write_sample_log(third, lines=500, bad_lines=5, rng=random.Random(8))`; the result is not kept.
- line 23: checks that `first.read_bytes() == second.read_bytes() != third.read_bytes()` is true; if it is false the program stops with an error.

**`test_a_file_longer_than_one_write_batch_is_complete`** (lines 26 to 29):

```python
def test_a_file_longer_than_one_write_batch_is_complete(tmp_path):
    path = tmp_path / "long.log"
    write_sample_log(path, lines=25_000, bad_lines=0, rng=random.Random(1))
    assert path.read_text(encoding="utf-8").count("\n") == 25_000
```

- line 27: stores `tmp_path / 'long.log'` in `path`.
- line 28: runs `write_sample_log(path, lines=25000, bad_lines=0, rng=random.Random(1))`; the result is not kept.
- line 29: checks that `path.read_text(encoding='utf-8').count('\n') == 25000` is true; if it is false the program stops with an error.

**`test_more_bad_lines_than_lines_is_refused`** (lines 32 to 35):

```python
@pytest.mark.parametrize(("lines", "bad"), [(10, 11), (10, -1)])
def test_more_bad_lines_than_lines_is_refused(tmp_path, lines, bad):
    with pytest.raises(ValueError, match="bad_lines"):
        write_sample_log(tmp_path / "x.log", lines=lines, bad_lines=bad, rng=random.Random(1))
```

- line 32: the decorator `pytest.mark.parametrize(('lines', 'bad'), [(10, 11), (10, -1)])` wraps or registers what is defined just below it.
- line 34: opens (`with`) `pytest.raises(ValueError, match='bad_lines')`; whatever it holds is released when the block ends, also after an error:
  - line 35: runs `write_sample_log(tmp_path / 'x.log', lines=lines, bad_lines=bad, rng=random.Random(1))`; the result is not kept.

**`test_the_small_log_has_twenty_lines_of_one_to_twenty_milliseconds`** (lines 38 to 42):

```python
def test_the_small_log_has_twenty_lines_of_one_to_twenty_milliseconds(tmp_path):
    path = tmp_path / "small.log"
    write_small_log(path)
    requests = [parse(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert [request.latency_ms for request in requests if request] == list(range(1, 21))
```

- line 39: stores `tmp_path / 'small.log'` in `path`.
- line 40: runs `write_small_log(path)`; the result is not kept.
- line 41: stores a list built by going through `path.read_text(encoding='utf-8').splitlines()` in `requests`.
- line 42: checks that `[request.latency_ms for request in requests if request] == list(range(1, 21))` is true; if it is false the program stops with an error.

#### `tests/unit/infrastructure/test_settings.py` (49 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `import pytest` | The test library (see `pytest.md`). |
| 3 | `from logsum.domain.errors import InvalidSettingError` | this repository's class `InvalidSettingError` (src/logsum/domain/errors.py:21): A setting (environment variable or flag) has a value the program cannot use. |
| 4 | `from logsum.infrastructure.settings import Settings` | this repository's class `Settings` (src/logsum/infrastructure/settings.py:27): Every tunable of the program. Command-line flags override these; these override the defaults. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 36 | `pytest.mark` | attaches labels to tests (`parametrize`, `integration`, `e2e`) |
| 48 | `pytest.raises` | passes only if the block raises the named error |

What the file defines, in order:

- test `test_no_environment_gives_the_defaults` (line 7), plain: No environment gives the defaults.
- test `test_every_variable_is_read` (line 13), plain: Every variable is read.
- test `test_an_empty_variable_means_the_default` (line 32), plain: An empty variable means the default.
- test `test_a_value_the_program_cannot_use_is_rejected_by_name` (line 47), plain: A value the program cannot use is rejected by name. Uses: `environ`. Decorators: `@pytest.mark.parametrize('environ', [{'LOGSUM_TOP': 'many'}, {'LOGSUM_TOP': '0'}, {'LOGSUM_ESTIMATOR': 'median'}, {'LOGSUM_LOG_LEVEL': 'LOUD'}, {'LOGSUM_BUCKET_MS': '0'}, {'LOGSUM_BUCKET_MS': '50', 'LOGSUM_MAX_LATENCY_MS': '10'}])`.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 4):

```python
import pytest

from logsum.domain.errors import InvalidSettingError
from logsum.infrastructure.settings import Settings
```

**`test_no_environment_gives_the_defaults`** (lines 7 to 10):

```python
def test_no_environment_gives_the_defaults():
    assert Settings.from_environ({}) == Settings(
        log_level="WARNING", top=10, estimator="exact", bucket_ms=5, max_latency_ms=10_000
    )
```

- line 8: checks that `Settings.from_environ({}) == Settings(log_level='WARNING', top=10, estimator='exact', bucket_ms=5, max_latency_ms=10000)` is true; if it is false the program stops with an error.

**`test_every_variable_is_read`** (lines 13 to 29):

```python
def test_every_variable_is_read():
    settings = Settings.from_environ(
        {
            "LOGSUM_LOG_LEVEL": "debug",
            "LOGSUM_TOP": "3",
            "LOGSUM_ESTIMATOR": "histogram",
            "LOGSUM_BUCKET_MS": "2",
            "LOGSUM_MAX_LATENCY_MS": "500",
        }
    )
    assert (settings.log_level, settings.top, settings.estimator, settings.bucket_ms, settings.max_latency_ms) == (
        "debug",
        3,
        "histogram",
        2,
        500,
    )
```

- line 14: stores the result of calling `Settings.from_environ` with 1 argument(s) in `settings`.
- line 23: checks that `(settings.log_level, settings.top, settings.estimator, settings.bucket_ms, settings.max_latency_ms) == ('debug', 3, 'histogram', 2, 500)` is true; if it is false the program stops with an error.

**`test_an_empty_variable_means_the_default`** (lines 32 to 33):

```python
def test_an_empty_variable_means_the_default():
    assert Settings.from_environ({"LOGSUM_TOP": "", "LOGSUM_ESTIMATOR": ""}) == Settings()
```

- line 33: checks that `Settings.from_environ({'LOGSUM_TOP': '', 'LOGSUM_ESTIMATOR': ''}) == Settings()` is true; if it is false the program stops with an error.

**`test_a_value_the_program_cannot_use_is_rejected_by_name`** (lines 36 to 49):

```python
@pytest.mark.parametrize(
    "environ",
    [
        {"LOGSUM_TOP": "many"},
        {"LOGSUM_TOP": "0"},
        {"LOGSUM_ESTIMATOR": "median"},
        {"LOGSUM_LOG_LEVEL": "LOUD"},
        {"LOGSUM_BUCKET_MS": "0"},
        {"LOGSUM_BUCKET_MS": "50", "LOGSUM_MAX_LATENCY_MS": "10"},
    ],
)
def test_a_value_the_program_cannot_use_is_rejected_by_name(environ):
    with pytest.raises(InvalidSettingError):
        Settings.from_environ(environ)
```

- line 36: the decorator `pytest.mark.parametrize('environ', [{'LOGSUM_TOP': 'many'}, {'LOGSUM_TOP': '0'}, {'LOGSUM_ESTIMATOR': 'median'}, {'LOGSUM_LOG_LEVEL': 'LOUD'}, {'LOGSUM_BUCKET_MS': '0'}, {'LOGSUM_BUCKET_MS': '50', ...` wraps or registers what is defined just below it.
- line 48: opens (`with`) `pytest.raises(InvalidSettingError)`; whatever it holds is released when the block ends, also after an error:
  - line 49: runs `Settings.from_environ(environ)`; the result is not kept.

#### `tests/unit/interfaces/__init__.py` (0 lines)

Purpose: (no module docstring)

Imports:

This file has no imports.

What the file defines, in order:

Nothing besides imports.

This file is empty.

#### `tests/unit/interfaces/test_cli.py` (131 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `import io` | In-memory streams. `io.StringIO` is a text buffer that behaves like a file, used by tests to capture what a program prints. |
| 2 | `import json` | Reads and writes JSON text (see `json-and-json-schema.md` or `hashlib-and-json.md`). |
| 4 | `import pytest` | The test library (see `pytest.md`). |
| 5 | `from jsonschema import validate` | checks a document against a schema |
| 7 | `from logsum.infrastructure.settings import Settings` | this repository's class `Settings` (src/logsum/infrastructure/settings.py:27): Every tunable of the program. Command-line flags override these; these override the defaults. |
| 8 | `from logsum.interfaces.cli import distribution_factory` | this repository's function `distribution_factory` (src/logsum/interfaces/cli.py:31): The distribution each path gets: every latency in a list, or fixed-size buckets. |
| 8 | `from logsum.interfaces.cli import entrypoint` | this repository's function `entrypoint` (src/logsum/interfaces/cli.py:115): The installed command: `main` plus the two ways a command-line tool ends early, Ctrl-C and a closed pipe. |
| 8 | `from logsum.interfaces.cli import main` | this repository's function `main` (src/logsum/interfaces/cli.py:71): Run the command and return its exit code: 0 done, 1 unreadable file, 2 bad arguments or settings. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 12 | `io.StringIO` | a text buffer that acts like a file |
| 18 | `pytest.raises` | passes only if the block raises the named error |
| 43 | `json.loads` | reads JSON from text |

What the file defines, in order:

- helper `def run(*argv, environ=None)` (line 11): calls the program's `main` function directly with the given arguments and environment, collects what it printed to standard output and standard error in two in-memory buffers, and returns the exit code and both texts
- test `test_help_prints_usage_and_exits_zero` (line 17), plain: Help prints usage and exits zero. Uses: `capsys`.
- test `test_the_small_log_prints_the_hand_checked_percentile` (line 24), plain: The small log prints the hand checked percentile. Uses: `data_dir`.
- test `test_the_two_path_fixture_counts_statuses_bad_lines_and_orders_paths` (line 32), plain: The two path fixture counts statuses bad lines and orders paths. Uses: `data_dir`.
- test `test_json_output_follows_the_published_schema` (line 40), plain: Json output follows the published schema. Uses: `data_dir`, `summary_schema`.
- test `test_json_output_without_stats_has_no_stats_key_and_still_validates` (line 49), plain: Json output without stats has no stats key and still validates. Uses: `data_dir`, `summary_schema`.
- test `test_stats_adds_elapsed_time_and_peak_memory_to_the_text` (line 55), plain: Stats adds elapsed time and peak memory to the text. Uses: `data_dir`.
- test `test_top_limits_the_paths_listed` (line 61), plain: Top limits the paths listed. Uses: `data_dir`.
- test `test_the_histogram_estimator_is_selectable_and_close_to_exact` (line 67), plain: The histogram estimator is selectable and close to exact. Uses: `data_dir`.
- test `test_the_environment_supplies_defaults_and_flags_override_them` (line 73), plain: The environment supplies defaults and flags override them. Uses: `data_dir`.
- test `test_a_missing_file_exits_one_with_a_message_and_a_structured_log_line` (line 80), plain: A missing file exits one with a message and a structured log line. Uses: `tmp_path`.
- test `test_a_bad_setting_in_the_environment_exits_two` (line 88), plain: A bad setting in the environment exits two.
- test `test_a_bad_flag_value_exits_two` (line 94), plain: A bad flag value exits two.
- test `test_the_distribution_factory_follows_the_estimator_setting` (line 100), plain: The distribution factory follows the estimator setting.
- test `test_entrypoint_returns_the_exit_code_of_main` (line 105), plain: Entrypoint returns the exit code of main. Uses: `data_dir`, `monkeypatch`.
- test `test_ctrl_c_exits_with_130_and_a_one_line_message` (line 110), plain: Ctrl c exits with 130 and a one line message. Uses: `monkeypatch`, `capsys`.
- test `test_a_closed_pipe_exits_zero_and_points_stdout_at_devnull` (line 119), plain: A closed pipe exits zero and points stdout at devnull. Uses: `monkeypatch`, `tmp_path`.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 8):

```python
import io
import json

import pytest
from jsonschema import validate

from logsum.infrastructure.settings import Settings
from logsum.interfaces.cli import distribution_factory, entrypoint, main
```

**`run`**: calls the program's `main` function directly with the given arguments and environment, collects what it printed to standard output and standard error in two in-memory buffers, and returns the exit code and both texts (lines 11 to 14):

```python
def run(*argv, environ=None):
    out, err = io.StringIO(), io.StringIO()
    code = main(list(argv), environ=environ or {}, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()
```

- line 12: stores `(io.StringIO(), io.StringIO())` in `(out, err)`.
- line 13: stores the result of calling `main` with 4 argument(s) in `code`.
- line 14: ends the function and gives back `(code, out.getvalue(), err.getvalue())`.

**`test_help_prints_usage_and_exits_zero`** (lines 17 to 21):

```python
def test_help_prints_usage_and_exits_zero(capsys):
    with pytest.raises(SystemExit) as stop:
        main(["--help"], environ={})
    assert stop.value.code == 0
    assert "usage: logsum" in capsys.readouterr().out
```

- line 18: opens (`with`) `pytest.raises(SystemExit)` as `stop`; whatever it holds is released when the block ends, also after an error:
  - line 19: runs `main(['--help'], environ={})`; the result is not kept.
- line 20: checks that `stop.value.code == 0` is true; if it is false the program stops with an error.
- line 21: checks that `'usage: logsum' in capsys.readouterr().out` is true; if it is false the program stops with an error.

**`test_the_small_log_prints_the_hand_checked_percentile`** (lines 24 to 29):

```python
def test_the_small_log_prints_the_hand_checked_percentile(data_dir):
    code, out, _ = run(str(data_dir / "small.log"))
    assert code == 0
    assert "statuses: {200: 20}" in out
    assert "19.95  /orders/1234  (20 requests)" in out
    assert "bad lines: 0" in out
```

- line 25: stores the result of calling `run` with 1 argument(s) in `(code, out, _)`.
- line 26: checks that `code == 0` is true; if it is false the program stops with an error.
- line 27: checks that `'statuses: {200: 20}' in out` is true; if it is false the program stops with an error.
- line 28: checks that `'19.95 /orders/1234 (20 requests)' in out` is true; if it is false the program stops with an error.
- line 29: checks that `'bad lines: 0' in out` is true; if it is false the program stops with an error.

**`test_the_two_path_fixture_counts_statuses_bad_lines_and_orders_paths`** (lines 32 to 37):

```python
def test_the_two_path_fixture_counts_statuses_bad_lines_and_orders_paths(data_dir):
    code, out, _ = run(str(data_dir / "two_paths.log"))
    assert code == 0
    assert "statuses: {200: 4, 404: 1, 500: 1}" in out
    assert "bad lines: 3" in out
    assert out.index("/b") < out.index("/a")  # /b is slower
```

- line 33: stores the result of calling `run` with 1 argument(s) in `(code, out, _)`.
- line 34: checks that `code == 0` is true; if it is false the program stops with an error.
- line 35: checks that `'statuses: {200: 4, 404: 1, 500: 1}' in out` is true; if it is false the program stops with an error.
- line 36: checks that `'bad lines: 3' in out` is true; if it is false the program stops with an error.
- line 37: checks that `out.index('/b') < out.index('/a')` is true; if it is false the program stops with an error.

**`test_json_output_follows_the_published_schema`** (lines 40 to 46):

```python
def test_json_output_follows_the_published_schema(data_dir, summary_schema):
    code, out, _ = run(str(data_dir / "two_paths.log"), "--json", "--stats")
    assert code == 0
    document = json.loads(out)
    validate(document, summary_schema)
    assert document["bad_lines"] == 3
    assert document["stats"]["peak_memory_bytes"] > 0
```

- line 41: stores the result of calling `run` with 3 argument(s) in `(code, out, _)`.
- line 42: checks that `code == 0` is true; if it is false the program stops with an error.
- line 43: stores the result of calling `json.loads` with 1 argument(s) in `document`.
- line 44: runs `validate(document, summary_schema)`; the result is not kept.
- line 45: checks that `document['bad_lines'] == 3` is true; if it is false the program stops with an error.
- line 46: checks that `document['stats']['peak_memory_bytes'] > 0` is true; if it is false the program stops with an error.

**`test_json_output_without_stats_has_no_stats_key_and_still_validates`** (lines 49 to 52):

```python
def test_json_output_without_stats_has_no_stats_key_and_still_validates(data_dir, summary_schema):
    _, out, _ = run(str(data_dir / "small.log"), "--json")
    validate(json.loads(out), summary_schema)
    assert "stats" not in json.loads(out)
```

- line 50: stores the result of calling `run` with 2 argument(s) in `(_, out, _)`.
- line 51: runs `validate(json.loads(out), summary_schema)`; the result is not kept.
- line 52: checks that `'stats' not in json.loads(out)` is true; if it is false the program stops with an error.

**`test_stats_adds_elapsed_time_and_peak_memory_to_the_text`** (lines 55 to 58):

```python
def test_stats_adds_elapsed_time_and_peak_memory_to_the_text(data_dir):
    _, out, _ = run(str(data_dir / "small.log"), "--stats")
    assert "elapsed: " in out
    assert "peak memory: " in out
```

- line 56: stores the result of calling `run` with 2 argument(s) in `(_, out, _)`.
- line 57: checks that `'elapsed: ' in out` is true; if it is false the program stops with an error.
- line 58: checks that `'peak memory: ' in out` is true; if it is false the program stops with an error.

**`test_top_limits_the_paths_listed`** (lines 61 to 64):

```python
def test_top_limits_the_paths_listed(data_dir):
    _, out, _ = run(str(data_dir / "two_paths.log"), "--top", "1")
    assert "(top 1)" in out
    assert "/a" not in out.split("bad lines")[0].split("(top 1):")[1]
```

- line 62: stores the result of calling `run` with 3 argument(s) in `(_, out, _)`.
- line 63: checks that `'(top 1)' in out` is true; if it is false the program stops with an error.
- line 64: checks that `'/a' not in out.split('bad lines')[0].split('(top 1):')[1]` is true; if it is false the program stops with an error.

**`test_the_histogram_estimator_is_selectable_and_close_to_exact`** (lines 67 to 70):

```python
def test_the_histogram_estimator_is_selectable_and_close_to_exact(data_dir):
    _, exact, _ = run(str(data_dir / "small.log"), "--json")
    _, histogram, _ = run(str(data_dir / "small.log"), "--json", "--estimator", "histogram", "--bucket-ms", "1")
    assert json.loads(histogram)["slowest_paths"] == json.loads(exact)["slowest_paths"]
```

- line 68: stores the result of calling `run` with 2 argument(s) in `(_, exact, _)`.
- line 69: stores the result of calling `run` with 6 argument(s) in `(_, histogram, _)`.
- line 70: checks that `json.loads(histogram)['slowest_paths'] == json.loads(exact)['slowest_paths']` is true; if it is false the program stops with an error.

**`test_the_environment_supplies_defaults_and_flags_override_them`** (lines 73 to 77):

```python
def test_the_environment_supplies_defaults_and_flags_override_them(data_dir):
    _, out, _ = run(str(data_dir / "two_paths.log"), environ={"LOGSUM_TOP": "1"})
    assert "(top 1)" in out
    _, out, _ = run(str(data_dir / "two_paths.log"), "--top", "2", environ={"LOGSUM_TOP": "1"})
    assert "(top 2)" in out
```

- line 74: stores the result of calling `run` with 2 argument(s) in `(_, out, _)`.
- line 75: checks that `'(top 1)' in out` is true; if it is false the program stops with an error.
- line 76: stores the result of calling `run` with 4 argument(s) in `(_, out, _)`.
- line 77: checks that `'(top 2)' in out` is true; if it is false the program stops with an error.

**`test_a_missing_file_exits_one_with_a_message_and_a_structured_log_line`** (lines 80 to 85):

```python
def test_a_missing_file_exits_one_with_a_message_and_a_structured_log_line(tmp_path):
    code, out, err = run(str(tmp_path / "missing.log"), "--log-level", "ERROR")
    assert code == 1
    assert out == ""
    assert "logsum: cannot read" in err
    assert "level=ERROR" in err
```

- line 81: stores the result of calling `run` with 3 argument(s) in `(code, out, err)`.
- line 82: checks that `code == 1` is true; if it is false the program stops with an error.
- line 83: checks that `out == ''` is true; if it is false the program stops with an error.
- line 84: checks that `'logsum: cannot read' in err` is true; if it is false the program stops with an error.
- line 85: checks that `'level=ERROR' in err` is true; if it is false the program stops with an error.

**`test_a_bad_setting_in_the_environment_exits_two`** (lines 88 to 91):

```python
def test_a_bad_setting_in_the_environment_exits_two():
    code, _, err = run("x.log", environ={"LOGSUM_TOP": "lots"})
    assert code == 2
    assert "LOGSUM_TOP" in err
```

- line 89: stores the result of calling `run` with 2 argument(s) in `(code, _, err)`.
- line 90: checks that `code == 2` is true; if it is false the program stops with an error.
- line 91: checks that `'LOGSUM_TOP' in err` is true; if it is false the program stops with an error.

**`test_a_bad_flag_value_exits_two`** (lines 94 to 97):

```python
def test_a_bad_flag_value_exits_two():
    code, _, err = run("x.log", "--top", "0")
    assert code == 2
    assert "top must be at least 1" in err
```

- line 95: stores the result of calling `run` with 3 argument(s) in `(code, _, err)`.
- line 96: checks that `code == 2` is true; if it is false the program stops with an error.
- line 97: checks that `'top must be at least 1' in err` is true; if it is false the program stops with an error.

**`test_the_distribution_factory_follows_the_estimator_setting`** (lines 100 to 102):

```python
def test_the_distribution_factory_follows_the_estimator_setting():
    assert type(distribution_factory(Settings())()).__name__ == "ExactLatencies"
    assert type(distribution_factory(Settings(estimator="histogram"))()).__name__ == "HistogramLatencies"
```

- line 101: checks that `type(distribution_factory(Settings())()).__name__ == 'ExactLatencies'` is true; if it is false the program stops with an error.
- line 102: checks that `type(distribution_factory(Settings(estimator='histogram'))()).__name__ == 'HistogramLatencies'` is true; if it is false the program stops with an error.

**`test_entrypoint_returns_the_exit_code_of_main`** (lines 105 to 107):

```python
def test_entrypoint_returns_the_exit_code_of_main(data_dir, monkeypatch):
    monkeypatch.setattr("sys.argv", ["logsum", str(data_dir / "small.log")])
    assert entrypoint() == 0
```

- line 106: runs `monkeypatch.setattr('sys.argv', ['logsum', str(data_dir / 'small.log')])`; the result is not kept.
- line 107: checks that `entrypoint() == 0` is true; if it is false the program stops with an error.

**`test_ctrl_c_exits_with_130_and_a_one_line_message`** (lines 110 to 116):

```python
def test_ctrl_c_exits_with_130_and_a_one_line_message(monkeypatch, capsys):
    def interrupted(*_args, **_kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr("logsum.interfaces.cli.main", interrupted)
    assert entrypoint() == 130
    assert capsys.readouterr().err.strip() == "logsum: interrupted"
```

- line 111: defines the function `interrupted(*_args, **_kwargs)`:
  - line 112: raises (throws) the error `KeyboardInterrupt`.
- line 114: runs `monkeypatch.setattr('logsum.interfaces.cli.main', interrupted)`; the result is not kept.
- line 115: checks that `entrypoint() == 130` is true; if it is false the program stops with an error.
- line 116: checks that `capsys.readouterr().err.strip() == 'logsum: interrupted'` is true; if it is false the program stops with an error.

**`test_a_closed_pipe_exits_zero_and_points_stdout_at_devnull`** (lines 119 to 131):

```python
def test_a_closed_pipe_exits_zero_and_points_stdout_at_devnull(monkeypatch, tmp_path):
    redirected = []

    def pipe_closed(*_args, **_kwargs):
        raise BrokenPipeError

    stand_in = (tmp_path / "stdout").open("w", encoding="utf-8")
    monkeypatch.setattr("logsum.interfaces.cli.main", pipe_closed)
    monkeypatch.setattr("os.dup2", lambda source, target: redirected.append(target))
    monkeypatch.setattr("sys.stdout", stand_in)
    assert entrypoint() == 0
    assert redirected == [stand_in.fileno()]
    stand_in.close()
```

- line 120: stores `[]` in `redirected`.
- line 122: defines the function `pipe_closed(*_args, **_kwargs)`:
  - line 123: raises (throws) the error `BrokenPipeError`.
- line 125: stores the result of calling `(tmp_path / 'stdout').open` with 2 argument(s) in `stand_in`.
- line 126: runs `monkeypatch.setattr('logsum.interfaces.cli.main', pipe_closed)`; the result is not kept.
- line 127: runs `monkeypatch.setattr('os.dup2', lambda source, target: redirected.append(target))`; the result is not kept.
- line 128: runs `monkeypatch.setattr('sys.stdout', stand_in)`; the result is not kept.
- line 129: checks that `entrypoint() == 0` is true; if it is false the program stops with an error.
- line 130: checks that `redirected == [stand_in.fileno()]` is true; if it is false the program stops with an error.
- line 131: runs `stand_in.close()`; the result is not kept.

#### `tests/unit/interfaces/test_make_log_cli.py` (26 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `from logsum.domain.request import parse` | this repository's function `parse` (src/logsum/domain/request.py:30): Read one line of `<timestamp> <METHOD> <path> <status> <latency>ms`. |
| 2 | `from logsum.interfaces.make_log_cli import entrypoint` | this repository's function `entrypoint` (src/logsum/interfaces/make_log_cli.py:38): The installed command. |
| 2 | `from logsum.interfaces.make_log_cli import main` | this repository's function `main` (src/logsum/interfaces/make_log_cli.py:14): Write a sample log and report what it holds. The same seed always gives the same file. |

What the file defines, in order:

- test `test_it_writes_the_requested_log_and_says_so` (line 5), plain: It writes the requested log and says so. Uses: `tmp_path`, `capsys`.
- test `test_small_writes_the_twenty_line_log` (line 12), plain: Small writes the twenty line log. Uses: `tmp_path`, `capsys`.
- test `test_more_bad_lines_than_lines_exits_two` (line 19), plain: More bad lines than lines exits two. Uses: `tmp_path`, `capsys`.
- test `test_entrypoint_reads_the_process_arguments` (line 24), plain: Entrypoint reads the process arguments. Uses: `tmp_path`, `monkeypatch`.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 2):

```python
from logsum.domain.request import parse
from logsum.interfaces.make_log_cli import entrypoint, main
```

**`test_it_writes_the_requested_log_and_says_so`** (lines 5 to 9):

```python
def test_it_writes_the_requested_log_and_says_so(tmp_path, capsys):
    path = tmp_path / "sample.log"
    assert main([str(path), "--lines", "300", "--bad", "6", "--seed", "1"]) == 0
    assert "wrote 300 lines (6 bad)" in capsys.readouterr().out
    assert sum(parse(line) is None for line in path.read_text(encoding="utf-8").splitlines()) == 6
```

- line 6: stores `tmp_path / 'sample.log'` in `path`.
- line 7: checks that `main([str(path), '--lines', '300', '--bad', '6', '--seed', '1']) == 0` is true; if it is false the program stops with an error.
- line 8: checks that `'wrote 300 lines (6 bad)' in capsys.readouterr().out` is true; if it is false the program stops with an error.
- line 9: checks that `sum((parse(line) is None for line in path.read_text(encoding='utf-8').splitlines())) == 6` is true; if it is false the program stops with an error.

**`test_small_writes_the_twenty_line_log`** (lines 12 to 16):

```python
def test_small_writes_the_twenty_line_log(tmp_path, capsys):
    path = tmp_path / "small.log"
    assert main([str(path), "--small"]) == 0
    assert len(path.read_text(encoding="utf-8").splitlines()) == 20
    assert "wrote 20 lines" in capsys.readouterr().out
```

- line 13: stores `tmp_path / 'small.log'` in `path`.
- line 14: checks that `main([str(path), '--small']) == 0` is true; if it is false the program stops with an error.
- line 15: checks that `len(path.read_text(encoding='utf-8').splitlines()) == 20` is true; if it is false the program stops with an error.
- line 16: checks that `'wrote 20 lines' in capsys.readouterr().out` is true; if it is false the program stops with an error.

**`test_more_bad_lines_than_lines_exits_two`** (lines 19 to 21):

```python
def test_more_bad_lines_than_lines_exits_two(tmp_path, capsys):
    assert main([str(tmp_path / "x.log"), "--lines", "5", "--bad", "9"]) == 2
    assert "bad_lines" in capsys.readouterr().err
```

- line 20: checks that `main([str(tmp_path / 'x.log'), '--lines', '5', '--bad', '9']) == 2` is true; if it is false the program stops with an error.
- line 21: checks that `'bad_lines' in capsys.readouterr().err` is true; if it is false the program stops with an error.

**`test_entrypoint_reads_the_process_arguments`** (lines 24 to 26):

```python
def test_entrypoint_reads_the_process_arguments(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["logsum-make-log", str(tmp_path / "x.log"), "--small"])
    assert entrypoint() == 0
```

- line 25: runs `monkeypatch.setattr('sys.argv', ['logsum-make-log', str(tmp_path / 'x.log'), '--small'])`; the result is not kept.
- line 26: checks that `entrypoint() == 0` is true; if it is false the program stops with an error.

#### `tests/unit/interfaces/test_module_main.py` (11 lines)

Purpose: (no module docstring)

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 1 | `import runpy` | Runs a module the way `python -m` does; a test uses it to run `python -m` inside the test process. |
| 3 | `import pytest` | The test library (see `pytest.md`). |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 8 | `pytest.raises` | passes only if the block raises the named error |
| 9 | `runpy.run_module` | runs a module as `python -m` would |

What the file defines, in order:

- test `test_python_dash_m_logsum_runs_the_command` (line 6), plain: Python dash m logsum runs the command. Uses: `data_dir`, `monkeypatch`, `capsys`.

Source in full, in pieces, each followed by what its statements do:

The imports (each one is explained in the import table above) (lines 1 to 3):

```python
import runpy

import pytest
```

**`test_python_dash_m_logsum_runs_the_command`** (lines 6 to 11):

```python
def test_python_dash_m_logsum_runs_the_command(data_dir, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["logsum", str(data_dir / "small.log")])
    with pytest.raises(SystemExit) as stop:
        runpy.run_module("logsum", run_name="__main__")
    assert stop.value.code == 0
    assert "19.95" in capsys.readouterr().out
```

- line 7: runs `monkeypatch.setattr('sys.argv', ['logsum', str(data_dir / 'small.log')])`; the result is not kept.
- line 8: opens (`with`) `pytest.raises(SystemExit)` as `stop`; whatever it holds is released when the block ends, also after an error:
  - line 9: runs `runpy.run_module('logsum', run_name='__main__')`; the result is not kept.
- line 10: checks that `stop.value.code == 0` is true; if it is false the program stops with an error.
- line 11: checks that `'19.95' in capsys.readouterr().out` is true; if it is false the program stops with an error.

## Try it yourself

```bash
uv run --frozen pytest --version
```
Expected: `pytest 9.1.1` (plus plugin lines).

```bash
uv run --frozen pytest tests/unit -q
```
Expected: dots for passing tests and a last line `NNN passed in N.NNs`.

```bash
uv run --frozen pytest tests/unit -q --collect-only | tail -3
```
Expected: the last lines show how many tests were collected, without running any.

```bash
uv run --frozen pytest tests/unit -q -k "empty" -v
```
Expected: only tests whose name contains `empty`, each printed with `PASSED`.

```bash
uv run --frozen pytest -m integration -q
```
Expected: only the tests labelled `integration`, `NN passed`, `NNN deselected`.

## Mistakes people make

- **A test with no `assert`.** It passes whatever the code does. Every test here asserts something or uses `pytest.raises`.
- **Depending on the order of tests.** Each test must create its own data (this repository uses `tmp_path` and fixtures for that).
- **Typing a marker wrong.** Without `--strict-markers` the typo silently selects nothing; with it, pytest stops.
- **Comparing floats with `==`.** Use `pytest.approx(19.95)`, as the percentile tests here do.
- **Tests that talk to the network or the clock.** Time and randomness are injected in this repository so tests are deterministic.

## Check yourself

**1. How does pytest decide a function is a test?**
Its name starts with `test_`, in a file named `test_*.py` that is under `testpaths`.

**2. What is a fixture, and how does a test receive one?**
A function marked `@pytest.fixture` that builds something a test needs; a test receives it by naming it as a parameter.

**3. What does `--strict-markers` prevent?**
A misspelled or unregistered marker name silently doing nothing: pytest stops with an error.

**4. What does `@pytest.mark.parametrize` do?**
Runs one test function once per row of data, reporting each row as its own test.

**5. What is the difference between a failure and an error?**
A failure is a failed `assert`; an error is any other exception in the test or in its setup.

## Further reading

- pytest documentation: https://docs.pytest.org/en/stable/ (version 9.1.1 here): "Get started", "How to use fixtures", "How to parametrize", "Configuration".
- `pytest --help` prints the options of the installed version.
