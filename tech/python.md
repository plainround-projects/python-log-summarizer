# Python 3.14 (the language)

<!-- fmt:off -->

## What it is

**Python** is a programming language. A **program** is a text file of instructions; a **language** defines what the instructions mean; an **interpreter** is the program that reads the text and does what it says. You write `logsum` in `.py` files and the interpreter (`python`) runs them. Version used here: 3.14.3 for development, with the code written to run on 3.12 and newer (the tests were also run on 3.12.13).

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **terminal** is a window where you type a line of text, press Enter, and the computer runs it. The program that reads your line is the **shell** (here `zsh` or `bash`). Everything typed in a terminal is a **command**: a program's name followed by **arguments**, the words that tell it what to do.
- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A program has three channels: **standard input** (what it reads), **standard output** (what it prints normally) and **standard error** (where it prints problems and progress). They are separate so a pipe or a file can take the output while errors still show on the screen.
- A **pipe**, written `|`, sends the standard output of the command on its left into the standard input of the command on its right, for example `sort file | head -3`.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- An **environment variable** is a named piece of text that a program inherits from the program that started it, for example `PORT=9000`. Programs read them to find out their settings without a settings file. In a shell, `NAME=value command` sets a variable for that one command.
- A **process** is one running program, with its own memory and a number, its **process id** or **PID**. A program can start other processes, its **children**, and wait for them or stop them.
- A **server** is a program that waits for requests and answers them. A **client** is a program that sends requests. One program can be both.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- **JSON** is a text format for data: objects `{"name": "x", "count": 3}` (names with values), lists `[1, 2, 3]`, text in double quotes, numbers, `true`, `false` and `null`. Almost every language can read and write it, which makes it the usual way programs exchange data.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- A **decorator** is a line starting with `@` above a function or class. It passes the function to another function that wraps or registers it, for example `@pytest.fixture` or `@dataclass`.
- A **generator** is a function that uses `yield` to hand out values one at a time and pause in between, so a huge sequence never has to exist in memory all at once.
- A **context manager** is an object used in a `with` block. It does some setup when the block starts and guaranteed cleanup when it ends, even after an error: `with open(path) as f:` closes the file for you.
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- **Latency** is how long one request takes. A **percentile** says what share of requests were at least that fast: **p95** is the time that 95 out of 100 requests beat, so it shows how bad the slow tail is, which an average hides.
- A **hash** (or **digest**) is a short fixed-size fingerprint computed from data. The same data always gives the same fingerprint, and a tiny change gives a completely different one, so equal fingerprints are used to check that two results are identical.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- A **container** is a running program packaged with everything it needs, kept apart from the rest of the machine. An **image** is the frozen recipe result a container starts from. **Docker** is the tool that builds images and runs containers.
- A **cache** is a saved copy of something slow to make, kept so the next request is fast.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- A **dataclass** is a class whose fields are listed once with their types; Python then writes the constructor, the printed form and the equality check for you.
- A **protocol** is a description of the methods an object must have, without saying which class it is. In this repository's architecture a **port** is such a description of what the inner layers need, and an **adapter** is a class in the outer layer that does the real work behind it.
- A **linter** reads code without running it and reports likely mistakes and style problems. A **formatter** rewrites the layout of the code into one agreed style.
- A **seed** is the starting number of a random number generator. The same seed always produces the same 'random' sequence, which makes experiments and tests repeatable.

## Why this repository uses it

The lesson is a Python project: a typed command-line tool that reads a very large file without using much memory. The Python features that matter for that goal are generators (produce one line at a time), type hints (checked by mypy), dataclasses (small immutable records) and context managers (always close the file).

## Where it appears

| File | What it does with it |
| --- | --- |
| `src/logsum/domain/request.py` | a dataclass and a function that returns `Request | None`. |
| `src/logsum/application/summarize.py` | a generator, a small class, an orchestrating class. |
| `src/logsum/infrastructure/log_files.py` | a context manager that closes a file; `yield from`. |
| `src/logsum/application/ports.py` | `Protocol` classes: interfaces without inheritance. |
| `src/logsum/domain/tally.py` | `Counter`, a dictionary of objects, `sorted` with a key function. |
| `src/logsum/infrastructure/settings.py` | `Literal`, `__post_init__`, `classmethod`. |
| `tests/` | plain functions with `assert`. |

## How it works underneath

The interpreter reads a `.py` file, turns it into **bytecode** (a list of simple steps, cached in `__pycache__/`) and runs the bytecode one step at a time. Everything is an **object**: numbers, text, functions, and classes. A **variable** is a name attached to an object. Code is organized in **modules** (one `.py` file each) grouped in **packages** (a folder with `__init__.py`). `import logsum.domain.request` runs that file once and makes its names available.

Indentation is the syntax: a block (the body of a function, an `if`) is the lines indented under a line that ends with a colon.

Memory is managed for you. An object stays alive as long as some name or container refers to it, and is freed afterwards. A `list` holds all its elements at once in memory; a **generator** (below) produces them one at a time, which is the point of this lesson.

## Walkthrough of this repository's use

**1. Type hints.** A hint after a colon says what a parameter holds; `->` says what a function returns. Python ignores them when running; mypy checks them (see `mypy.md`).

```python
def parse(line: str) -> Request | None:
    """Read one line of `<timestamp> <METHOD> <path> <status> <latency>ms`.

    Returns None for any line that is not in that format: a missing or extra field, a timestamp without a
    time zone, a status outside 100-599, a latency that is not whole milliseconds. A bad line is routine in a
    large log, so it is a value the caller checks and not an exception.
    """
    fields = line.split()
    if len(fields) != _FIELD_COUNT:
        return None
```
(`src/logsum/domain/request.py`, lines 30 to 39)

`line: str` means the parameter is text; `-> Request | None` means "a `Request`, or `None` (nothing)". `|` between types is "or". A text in triple double quotes right below the `def` is a **docstring**: documentation attached to the function (`help(parse)` prints it). `line.split()` cuts text at every run of spaces and returns a list of words. `len(fields) != _FIELD_COUNT` compares numbers (`!=` is "not equal"); the name starting with `_` is a module-private constant by convention. `return None` ends the function with "nothing".

**2. Tuple unpacking and early return.**

```python
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
```
(`src/logsum/domain/request.py`, lines 40 to 55)

The first line takes the five words of `fields` and gives each its own name (all five must be there, which the length check guarantees). `raw_latency.endswith(...)` is a method of text. `removesuffix` removes `ms` from the end. `str.isascii()` and `str.isdecimal()` check the text is only digits 0 to 9; the helper `_digits_to_int` exists because `int("1_000")` or `int("+5")` would be accepted by Python but are not valid in this log format. `try: ... except ValueError: return None` runs the risky line and, if it raises a `ValueError` (the error for a bad value), returns `None` instead of crashing. `timestamp.tzinfo is None` is an identity test (`is`), the right way to compare with `None`.

**3. Dataclass.**

```python
@dataclass(frozen=True, slots=True)
class Request:
    """One request from the access log. Immutable, and without a per-instance dict, since one exists per line."""

    timestamp: datetime
    method: str
    path: str
    status: int
    latency_ms: int
```
(`src/logsum/domain/request.py`, lines 14 to 22)

`@dataclass` is a **decorator** (a function applied to the class below it) that writes `__init__`, `__repr__` and `__eq__` for you from the annotated fields. `frozen=True` makes instances read-only (assigning `request.status = 500` raises `FrozenInstanceError`, so a `Request` is a value that cannot change under you). `slots=True` stores the fields in a fixed layout and no per-object dictionary, which saves memory when 500,000 of them are created.

**4. Generators: the heart of the lesson.**

```python
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
```
(`src/logsum/application/summarize.py`, lines 28 to 39)

A function with `yield` is a **generator function**. Calling it does not run the body; it returns a **generator** object. Each time something asks for the next value (a `for` loop does), the body runs until the next `yield`, hands over that value and pauses, remembering where it was. So the loop below holds one line at a time:

```python
                for request in stream_requests(lines, bad_lines):
                    tally.add(request)
```
(`src/logsum/application/summarize.py`, lines 75 to 76)

`Iterable[str]` and `Iterator[Request]` are type hints from `collections.abc`: "anything you can loop over, giving text" and "an object that gives `Request`s one at a time". `raw_line.rstrip("\r\n")` removes the line ending. `bad_lines.count += 1` adds one to a counter kept in an object, because a generator's `return` value is invisible to a `for` loop (see ADR 1 in `docs/adr`).

**5. Context managers.**

```python
    @contextmanager
    def open(self, location: str) -> Iterator[Iterator[str]]:
        """Yield the lines of the file at `location`; always close it.

        Bytes that are not valid UTF-8 are replaced and not raised: a line with them is then one more bad
        line, and one bad line never stops the run.
        """
        path = Path(location)
        try:
            handle = self._open_text(path)
        except OSError as error:
            raise UnreadableLogFileError(location, error.strerror or str(error)) from error
        with handle:
            yield self._lines(handle, location)
```
(`src/logsum/infrastructure/log_files.py`, lines 19 to 32)

`with x as y:` runs setup on entry and cleanup on exit, even if an error happens in between. `@contextmanager` builds one from a generator function: the code before `yield` is the setup, the yielded value becomes `y`, and the code after is the cleanup. Here `with handle:` closes the file when the block ends. `raise UnreadableLogFileError(...) from error` raises a new, named error and keeps the original as its cause. `yield from handle` hands out each line of the file in turn. The `Iterator[Iterator[str]]` hint reads "a generator that yields one iterator of text lines".

**6. Protocols (interfaces without inheritance).**

```python
class LineSource(Protocol):
    """Opens a log by name and hands out its lines one at a time."""

    def open(self, location: str) -> AbstractContextManager[Iterator[str]]:
        """Open `location`; the context closes it, also when reading fails.

        Raises `UnreadableLogFileError` when it cannot be opened or read.
        """
```
(`src/logsum/application/ports.py`, lines 10 to 17)

A `Protocol` class lists method signatures. Any class that has methods with those signatures counts as a `LineSource`, without saying so. mypy checks that the real class (`FileLineSource`) and the test fakes fit. The method bodies hold only a docstring, which is legal Python.

**7. Counter, sorting with a key function, and a lambda.**

```python
        ranked = sorted(
            (PathLatency(path, distribution.p95(), len(distribution)) for path, distribution in self._by_path.items()),
            key=lambda entry: (-entry.p95_ms, entry.path),
```
(`src/logsum/domain/tally.py`, lines 59 to 61)

`Counter` (from `collections`) is a dictionary that counts: `self._statuses[request.status] += 1` works even for a status not seen before, starting at 0. `sorted(iterable, key=...)` orders by the value that `key` returns for each item; `lambda entry: (-entry.p95_ms, entry.path)` is a small unnamed function returning a pair, so the slowest path comes first (the minus sign reverses the order) and ties break by path name. `(... for path, distribution in self._by_path.items())` is a **generator expression**: like a list comprehension but lazy.

**8. Validation in `__post_init__`, `Literal`, `classmethod`.**

```python
Estimator = Literal["exact", "histogram"]
ESTIMATORS: tuple[str, ...] = get_args(Estimator)
```
(`src/logsum/infrastructure/settings.py`, lines 12 to 13)

`Literal["exact", "histogram"]` is a type that allows only those two values; `get_args` pulls them back out as a tuple so the command-line parser can list them. In `Settings`, `__post_init__` runs right after the dataclass sets its fields and raises `InvalidSettingError` for a value the program cannot use; `@classmethod def from_environ(cls, environ)` is an alternative constructor that reads environment variables.

**9. The program entry.** `logsum/__main__.py` makes `python -m logsum` work, and `if __name__ == "__main__":` runs code only when a file is the program, not when it is imported. `raise SystemExit(entrypoint())` ends the process with the function's return value as its exit code.

### Every Python file of the package, one by one

This part is generated by reading each file with Python's own parser, so it lists every import, every constant, every class, every field and every function of the package, in the order they appear in the file. Where the source has a one-line description (a *docstring*, the text in triple quotes right under a `def` or `class`) it is quoted; otherwise the entry says what the body does. A *docstring* is ordinary text kept by Python so that tools can show it; it does not run. An **import table** says where each name comes from, and the 'What it brings in' column says in one line what that name is for.

#### `src/logsum/__init__.py` (3 lines)

Purpose: logsum: stream a web server access log and print a summary of statuses and slow paths.

Imports:

This file has no imports.

What the file defines, in order:

- constant `__version__` (line 3) is set to `'0.1.0'`.

#### `src/logsum/__main__.py` (6 lines)

Purpose: Run the command with `python -m logsum`.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from logsum.interfaces.cli import entrypoint` | this repository's function `entrypoint` (src/logsum/interfaces/cli.py:115): The installed command: `main` plus the two ways a command-line tool ends early, Ctrl-C and a closed pipe. |

What the file defines, in order:

This file defines no functions, classes or constants.

#### `src/logsum/application/__init__.py` (1 lines)

Purpose: The use case of the program and the ports it needs. Depends on the domain only.

Imports:

This file has no imports.

What the file defines, in order:

This file defines no functions, classes or constants.

#### `src/logsum/application/ports.py` (34 lines)

Purpose: What the use case needs from the outside world, as interfaces the infrastructure layer implements.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `from collections.abc import Iterator` | type hint for an object that hands out one value at a time (what `next()` reads) |
| 6 | `from contextlib import AbstractContextManager` | type hint for an object usable in `with` |
| 7 | `from typing import Protocol` | an interface named by its methods |

What the file defines, in order:

- class `LineSource(Protocol)` (line 10): Opens a log by name and hands out its lines one at a time.
  - `def open(self, location: str) -> AbstractContextManager[Iterator[str]]` (line 13): Open `location`; the context closes it, also when reading fails.
- class `Clock(Protocol)` (line 20): A monotonic clock in seconds, injected so tests control time.
  - `def monotonic(self) -> float` (line 23): Seconds from an arbitrary start; only differences mean anything.
- class `MemoryMeter(Protocol)` (line 27): Measures the peak Python memory of a run.
  - `def start(self) -> None` (line 30): Begin measuring.
  - `def stop(self) -> int` (line 33): Stop measuring and return the peak in bytes since `start`.

#### `src/logsum/application/summarize.py` (93 lines)

Purpose: The one use case: read a log as a stream and summarize it.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import logging` | Python's logging library (see `logging-and-logfmt.md`). |
| 6 | `from collections.abc import Callable` | type hint for something that can be called like a function |
| 6 | `from collections.abc import Iterable` | type hint for anything a `for` loop can go through |
| 6 | `from collections.abc import Iterator` | type hint for an object that hands out one value at a time (what `next()` reads) |
| 7 | `from dataclasses import dataclass` | writes `__init__`, `__repr__`, `__eq__` from the fields |
| 9 | `from logsum.application.ports import Clock` | this repository's class `Clock` (src/logsum/application/ports.py:20): A monotonic clock in seconds, injected so tests control time. |
| 9 | `from logsum.application.ports import LineSource` | this repository's class `LineSource` (src/logsum/application/ports.py:10): Opens a log by name and hands out its lines one at a time. |
| 9 | `from logsum.application.ports import MemoryMeter` | this repository's class `MemoryMeter` (src/logsum/application/ports.py:27): Measures the peak Python memory of a run. |
| 10 | `from logsum.domain.distribution import LatencyDistribution` | this repository's class `LatencyDistribution` (src/logsum/domain/distribution.py:12): The latencies seen for one path. |
| 11 | `from logsum.domain.request import Request` | this repository's class `Request` (src/logsum/domain/request.py:15): One request from the access log. Immutable, and without a per-instance dict, since one exists per line. |
| 11 | `from logsum.domain.request import parse` | this repository's function `parse` (src/logsum/domain/request.py:30): Read one line of `<timestamp> <METHOD> <path> <status> <latency>ms`. |
| 12 | `from logsum.domain.tally import LogTally` | this repository's class `LogTally` (src/logsum/domain/tally.py:32): Accumulates one request at a time; memory depends on the paths and the distribution, not the file. |
| 12 | `from logsum.domain.tally import Summary` | this repository's class `Summary` (src/logsum/domain/tally.py:23): What the program prints: requests per status, the slowest paths, and the lines it could not read. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 14 | `logging.getLogger` | returns the logger with a given name |

What the file defines, in order:

- constant `logger` (line 14) is set to `logging.getLogger(__name__)`.
- class `BadLineCounter` (line 17): Counts the lines the stream skipped.
  - `def __init__(self) -> None` (line 24): builds the object: stores the arguments it was given
- `def stream_requests(lines: Iterable[str], bad_lines: BadLineCounter) -> Iterator[Request]` (line 28): Yield the parsed request of each readable line, one at a time, and count the rest.
- class `RunReport` (line 43), decorated with `@dataclass(frozen=True, slots=True)`: A summary and how the run that produced it behaved.
  - field `summary: Summary` (line 46)
  - field `elapsed_seconds: float` (line 47)
  - field `peak_memory_bytes: int | None` (line 48)
- class `SummarizeLog` (line 51): Summarize a log file: statuses, slowest paths by 95th percentile, unreadable lines.
  - `def __init__(self, source: LineSource, clock: Clock, new_distribution: Callable[[], LatencyDistribution], memory: MemoryMeter | None=None) -> None` (line 54): builds the object: stores the arguments it was given
  - `def run(self, location: str, top: int=10) -> RunReport` (line 66): Stream `location` once and return its summary with the elapsed time and peak memory.

#### `src/logsum/domain/__init__.py` (4 lines)

Purpose: The rules of the problem: what a request is, what counts as a bad line, how latencies are summarized.

Imports:

This file has no imports.

What the file defines, in order:

This file defines no functions, classes or constants.

#### `src/logsum/domain/distribution.py` (86 lines)

Purpose: Where the latencies of one path are kept, and how much each choice remembers.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `from array import array` | the compact number list class |
| 6 | `from typing import Protocol` | an interface named by its methods |
| 8 | `from logsum.domain.errors import InvalidSettingError` | this repository's class `InvalidSettingError` (src/logsum/domain/errors.py:21): A setting (environment variable or flag) has a value the program cannot use. |
| 9 | `from logsum.domain.percentile import p95` | this repository's function `p95` (src/logsum/domain/percentile.py:15): The 95th percentile by the exclusive method (the `statistics.quantiles` default). |
| 9 | `from logsum.domain.percentile import p95_from_ranks` | this repository's function `p95_from_ranks` (src/logsum/domain/percentile.py:29): The same value as `p95`, computed from `count` and a lookup of the k-th smallest latency (0-based). |

What the file defines, in order:

- class `LatencyDistribution(Protocol)` (line 12): The latencies seen for one path.
  - `def add(self, latency_ms: int) -> None` (line 15): Record one latency.
  - `def p95(self) -> float` (line 18): The 95th percentile of what was recorded.
  - `def __len__(self) -> int` (line 21): How many latencies were recorded.
- class `ExactLatencies` (line 25): Every latency in a list, so the percentile is exact.
  - `def __init__(self) -> None` (line 33): builds the object: stores the arguments it was given
  - `def add(self, latency_ms: int) -> None` (line 36): Record one latency.
  - `def p95(self) -> float` (line 40): The exact 95th percentile.
  - `def __len__(self) -> int` (line 44): the number given by `len(obj)`
- class `HistogramLatencies` (line 48): Counts per fixed-width bucket, so memory is the same for ten requests and ten billion.
  - `def __init__(self, bucket_ms: int=5, max_latency_ms: int=10000) -> None` (line 58): builds the object: stores the arguments it was given
  - `def add(self, latency_ms: int) -> None` (line 68): Record one latency.
  - `def p95(self) -> float` (line 73): The 95th percentile, to within the bucket width.
  - `def _kth_smallest(self, index: int) -> int` (line 77): walks the buckets from the smallest, adding up how many values each holds, and returns the lower edge in milliseconds of the bucket that contains the value at position `index` when all values are sorted; the final `raise` can only happen if a caller asks for a position beyond the total, which the callers never do
  - `def __len__(self) -> int` (line 85): the number given by `len(obj)`

#### `src/logsum/domain/errors.py` (22 lines)

Purpose: Named errors, so callers handle a failure by what it means and not by message text.

Imports:

This file has no imports.

What the file defines, in order:

- class `LogsumError(Exception)` (line 4): Base class of every error this program raises on purpose.
- class `UnreadableLogFileError(LogsumError)` (line 8): The log file does not exist, is a directory, or cannot be opened or decompressed.
  - `def __init__(self, location: str, reason: str) -> None` (line 11): builds the object: stores the arguments it was given
- class `EmptyDistributionError(LogsumError)` (line 17): A percentile was asked of a distribution that holds no latencies.
- class `InvalidSettingError(LogsumError)` (line 21): A setting (environment variable or flag) has a value the program cannot use.

#### `src/logsum/domain/percentile.py` (43 lines)

Purpose: The 95th percentile, defined once so every distribution agrees on it.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `from collections.abc import Callable` | type hint for something that can be called like a function |
| 5 | `from collections.abc import Sequence` | type hint for an ordered, indexable collection such as a list or tuple |
| 6 | `from statistics import quantiles` | cut points that divide data into equal groups (percentiles) |
| 8 | `from logsum.domain.errors import EmptyDistributionError` | this repository's class `EmptyDistributionError` (src/logsum/domain/errors.py:17): A percentile was asked of a distribution that holds no latencies. |

What the file defines, in order:

- constant `_CUTS` (line 10) is set to `100`.
- constant `_PERCENT` (line 11) is set to `95`.
- constant `_P95_INDEX` (line 12) is set to `_PERCENT - 1`.
- `def p95(latencies: Sequence[int]) -> float` (line 15): The 95th percentile by the exclusive method (the `statistics.quantiles` default).
- `def p95_from_ranks(count: int, kth_smallest: Callable[[int], int]) -> float` (line 29): The same value as `p95`, computed from `count` and a lookup of the k-th smallest latency (0-based).

#### `src/logsum/domain/request.py` (55 lines)

Purpose: One parsed access-log line and the function that reads it.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `from dataclasses import dataclass` | writes `__init__`, `__repr__`, `__eq__` from the fields |
| 6 | `from datetime import datetime` | a date and time |

What the file defines, in order:

- constant `_FIELD_COUNT` (line 8) is set to `5`.
- constant `_LATENCY_SUFFIX` (line 9) is set to `'ms'`.
- constant `_FIRST_STATUS` (line 10) is set to `100`.
- constant `_LAST_STATUS` (line 11) is set to `599`.
- class `Request` (line 15), decorated with `@dataclass(frozen=True, slots=True)`: One request from the access log. Immutable, and without a per-instance dict, since one exists per line.
  - field `timestamp: datetime` (line 18)
  - field `method: str` (line 19)
  - field `path: str` (line 20)
  - field `status: int` (line 21)
  - field `latency_ms: int` (line 22)
- `def _digits_to_int(text: str) -> int | None` (line 25): turns text into a whole number only when it is plain ASCII digits (`int()` alone would also accept `+5`, `1_000` and digits of other alphabets); returns `None` for anything else, so a bad log field becomes a bad line, not a wrong number
- `def parse(line: str) -> Request | None` (line 30): Read one line of `<timestamp> <METHOD> <path> <status> <latency>ms`.

#### `src/logsum/domain/tally.py` (68 lines)

Purpose: The running totals of a log, and the summary they turn into.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `from collections import Counter` | a dictionary that counts the items given to it |
| 6 | `from collections.abc import Callable` | type hint for something that can be called like a function |
| 6 | `from collections.abc import Mapping` | type hint for a dictionary-like collection that is only read |
| 7 | `from dataclasses import dataclass` | writes `__init__`, `__repr__`, `__eq__` from the fields |
| 9 | `from logsum.domain.distribution import LatencyDistribution` | this repository's class `LatencyDistribution` (src/logsum/domain/distribution.py:12): The latencies seen for one path. |
| 10 | `from logsum.domain.request import Request` | this repository's class `Request` (src/logsum/domain/request.py:15): One request from the access log. Immutable, and without a per-instance dict, since one exists per line. |

What the file defines, in order:

- class `PathLatency` (line 14), decorated with `@dataclass(frozen=True, slots=True)`: The 95th-percentile latency of one path and how many requests it is based on.
  - field `path: str` (line 17)
  - field `p95_ms: float` (line 18)
  - field `requests: int` (line 19)
- class `Summary` (line 23), decorated with `@dataclass(frozen=True, slots=True)`: What the program prints: requests per status, the slowest paths, and the lines it could not read.
  - field `total_requests: int` (line 26)
  - field `bad_lines: int` (line 27)
  - field `status_counts: Mapping[int, int]` (line 28)
  - field `slowest_paths: tuple[PathLatency, ...]` (line 29)
- class `LogTally` (line 32): Accumulates one request at a time; memory depends on the paths and the distribution, not the file.
  - `def __init__(self, new_distribution: Callable[[], LatencyDistribution]) -> None` (line 35): builds the object: stores the arguments it was given
  - `def add(self, request: Request) -> None` (line 41): Count a parsed request under its status and file its latency under its path.
  - `def add_bad_lines(self, count: int=1) -> None` (line 53): Count lines that could not be read.
  - `def summary(self, top: int=10) -> Summary` (line 57): The totals so far, with the `top` paths of highest 95th-percentile latency (ties by path name).

#### `src/logsum/infrastructure/__init__.py` (1 lines)

Purpose: Adapters to the outside world: files, the clock, memory measurement, settings, logging.

Imports:

This file has no imports.

What the file defines, in order:

This file defines no functions, classes or constants.

#### `src/logsum/infrastructure/clock.py` (13 lines)

Purpose: The real clock.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import time` | Clocks and sleeping. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 13 | `time.perf_counter` | the most precise clock for measuring durations |

What the file defines, in order:

- class `SystemClock` (line 8): A monotonic clock backed by `time.perf_counter`.
  - `def monotonic(self) -> float` (line 11): Seconds from an arbitrary start.

#### `src/logsum/infrastructure/log_files.py` (45 lines)

Purpose: Reading a log from disk, plain or gzip-compressed, one line at a time.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import gzip` | Reads and writes gzip-compressed files (see `gzip.md`). |
| 6 | `from collections.abc import Iterator` | type hint for an object that hands out one value at a time (what `next()` reads) |
| 7 | `from contextlib import contextmanager` | builds a `with` object from a generator |
| 8 | `from pathlib import Path` | a file path object |
| 9 | `from typing import TextIO` | a text stream |
| 11 | `from logsum.domain.errors import UnreadableLogFileError` | this repository's class `UnreadableLogFileError` (src/logsum/domain/errors.py:8): The log file does not exist, is a directory, or cannot be opened or decompressed. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 37 | `gzip.open` | opens a `.gz` file for reading or writing |

What the file defines, in order:

- constant `_ENCODING` (line 13) is set to `'utf-8'`.
- class `FileLineSource` (line 16): Opens files by path. A name ending in `.gz` is decompressed on the fly, still a line at a time.
  - `def open(self, location: str) -> Iterator[Iterator[str]]` (line 20): Yield the lines of the file at `location`; always close it. Decorators: `@contextmanager`.
  - `def _open_text(path: Path) -> TextIO` (line 35): opens a file for reading text: a name ending in `.gz` is opened through `gzip.open` in text mode (`"rt"`), anything else through `Path.open`; both use UTF-8 and `errors="replace"`, which puts a replacement character in place of bytes that are not valid UTF-8 instead of failing Decorators: `@staticmethod`.
  - `def _lines(handle: TextIO, location: str) -> Iterator[str]` (line 41): hands out the lines of an open file one at a time (`yield from handle`), and turns an operating-system error or a damaged gzip file (`OSError`, `EOFError`) into the repository's own `UnreadableLogFileError` that names the file Decorators: `@staticmethod`.

#### `src/logsum/infrastructure/logging.py` (41 lines)

Purpose: Structured logging: one logfmt line per event (`ts=... level=... logger=... msg=... key=value`).

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import json` | Reads and writes JSON text (see `json-and-json-schema.md` or `hashlib-and-json.md`). |
| 6 | `import logging` | Python's logging library (see `logging-and-logfmt.md`). |
| 7 | `import sys` | Facts about the running interpreter: its command-line arguments, its standard streams, its version. |
| 8 | `from datetime import UTC` | the universal time zone |
| 8 | `from datetime import datetime` | a date and time |
| 9 | `from typing import TextIO` | a text stream |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 14 | `json.dumps` | turns a Python value into JSON text |
| 17 | `logging.Formatter` | the class that turns a log record into text |
| 20 | `logging.LogRecord` | one log event with all its facts |
| 37 | `logging.StreamHandler` | a handler that writes to a stream such as standard error |
| 37 | `sys.stderr` | the standard error stream |
| 39 | `logging.getLogger` | returns the logger with a given name |

What the file defines, in order:

- `def _quote(value: object) -> str` (line 12): turns any value into text for a `key=value` log line: text that is empty or holds a space, an equals sign, a double quote or a line break is wrapped in double quotes (with JSON escapes) so a reader can split the line again; other text is left as it is
- class `LogfmtFormatter(logging.Formatter)` (line 17): Format a log record as one logfmt line, with the record's `fields` extra as key=value pairs.
  - `def format(self, record: logging.LogRecord) -> str` (line 20): Render `record` as a single line.
- `def configure_logging(level: str, stream: TextIO | None=None) -> None` (line 35): Send every log record to `stream` (standard error by default) as logfmt. Safe to call twice.

#### `src/logsum/infrastructure/memory.py` (23 lines)

Purpose: Peak memory of a run, measured with `tracemalloc`.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import tracemalloc` | Records memory allocations (see `tracemalloc.md`). |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 16 | `tracemalloc.start` | starts recording allocations |
| 17 | `tracemalloc.reset_peak` | sets the peak to the current level |
| 21 | `tracemalloc.get_traced_memory` | returns the current and peak traced memory |
| 22 | `tracemalloc.stop` | stops recording |

What the file defines, in order:

- class `TracemallocMeter` (line 8): Measures the peak of Python-level allocations, which is what should stay flat as the file grows.
  - `def start(self) -> None` (line 14): Start tracing and reset the peak.
  - `def stop(self) -> int` (line 19): Stop tracing and return the peak, in bytes, since `start`.

#### `src/logsum/infrastructure/sample_log.py` (47 lines)

Purpose: Writes the sample logs the lesson asks for: 500,000 lines with a few hundred planted bad ones, and a tiny log.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import random` | Random numbers. `random.Random(seed)` is a generator with its own state: the same seed gives the same sequence. |
| 6 | `from itertools import cycle` | repeats a sequence forever |
| 7 | `from pathlib import Path` | a file path object |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 20 | `random.Random` | a random number generator with its own seed |

What the file defines, in order:

- constant `PATHS` (line 9) is set to `('/orders/1234', '/cart', '/users/42', '/health', '/search')`.
- constant `STATUSES` (line 10) is set to `(200, 200, 200, 404, 500)`.
- constant `_TIMESTAMP` (line 11) is set to `'2026-03-14T09:26:53Z'`.
- constant `_BAD_LINES_BY_KIND` (line 12) is set to `(f'{_TIMESTAMP} GET /orders/1234 200', f'{_TIMESTAMP} GET /orders/1234 200 abcms', '')`.
- constant `_FLUSH_EVERY` (line 17) is set to `10000`.
- `def write_sample_log(path: Path, *, lines: int, bad_lines: int, rng: random.Random) -> None` (line 20): Write `lines` lines to `path`, `bad_lines` of them malformed (the three kinds in turn), in one pass.
- `def write_small_log(path: Path) -> None` (line 43): Write 20 lines of one path with latencies 1ms to 20ms, whose 95th percentile (19.95) is checked by hand.

#### `src/logsum/infrastructure/settings.py` (60 lines)

Purpose: Configuration from the environment (twelve-factor), validated once, with defaults that work.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import logging` | Python's logging library (see `logging-and-logfmt.md`). |
| 6 | `from collections.abc import Mapping` | type hint for a dictionary-like collection that is only read |
| 7 | `from dataclasses import dataclass` | writes `__init__`, `__repr__`, `__eq__` from the fields |
| 8 | `from typing import Literal` | only these exact values |
| 8 | `from typing import get_args` | reads the options out of a `Literal` |
| 10 | `from logsum.domain.errors import InvalidSettingError` | this repository's class `InvalidSettingError` (src/logsum/domain/errors.py:21): A setting (environment variable or flag) has a value the program cannot use. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 37 | `logging.getLevelName` | converts between level names and numbers (also used to detect an unknown level name) |

What the file defines, in order:

- constant `Estimator` (line 12) is set to `Literal['exact', 'histogram']`.
- constant `ESTIMATORS: tuple[str, ...]` (line 13) is set to `get_args(Estimator)`.
- `def _integer(environ: Mapping[str, str], name: str, default: int) -> int` (line 16): reads one setting from the environment (a dictionary of text values) as a whole number: returns `default` when the variable is missing or empty, and raises `InvalidSettingError` (naming the variable and the bad value) when the text is not a whole number
- class `Settings` (line 27), decorated with `@dataclass(frozen=True, slots=True)`: Every tunable of the program. Command-line flags override these; these override the defaults.
  - field `log_level: str` = `'WARNING'` (line 30)
  - field `top: int` = `10` (line 31)
  - field `estimator: Estimator` = `'exact'` (line 32)
  - field `bucket_ms: int` = `5` (line 33)
  - field `max_latency_ms: int` = `10000` (line 34)
  - `def __post_init__(self) -> None` (line 36): runs right after the generated `__init__` and checks the fields
  - `def from_environ(cls, environ: Mapping[str, str]) -> Settings` (line 51): Read `LOGSUM_LOG_LEVEL`, `LOGSUM_TOP`, `LOGSUM_ESTIMATOR`, `LOGSUM_BUCKET_MS`, `LOGSUM_MAX_LATENCY_MS`. Decorators: `@classmethod`.

#### `src/logsum/interfaces/__init__.py` (1 lines)

Purpose: The command-line programs. They wire adapters into the use case and own argument parsing and exit codes.

Imports:

This file has no imports.

What the file defines, in order:

This file defines no functions, classes or constants.

#### `src/logsum/interfaces/cli.py` (127 lines)

Purpose: `logsum`: summarize an access log from the command line.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import argparse` | Reads the words typed after a program's name on the command line (see `argparse.md`). |
| 6 | `import logging` | Python's logging library (see `logging-and-logfmt.md`). |
| 7 | `import os` | Access to the operating system: environment variables, process ids, low-level file operations. |
| 8 | `import sys` | Facts about the running interpreter: its command-line arguments, its standard streams, its version. |
| 9 | `from collections.abc import Callable` | type hint for something that can be called like a function |
| 9 | `from collections.abc import Mapping` | type hint for a dictionary-like collection that is only read |
| 9 | `from collections.abc import Sequence` | type hint for an ordered, indexable collection such as a list or tuple |
| 10 | `from typing import TextIO` | a text stream |
| 12 | `from logsum import __version__` | this repository's constant `__version__` (src/logsum/__init__.py:3) |
| 13 | `from logsum.application.summarize import SummarizeLog` | this repository's class `SummarizeLog` (src/logsum/application/summarize.py:51): Summarize a log file: statuses, slowest paths by 95th percentile, unreadable lines. |
| 14 | `from logsum.domain.distribution import ExactLatencies` | this repository's class `ExactLatencies` (src/logsum/domain/distribution.py:25): Every latency in a list, so the percentile is exact. |
| 14 | `from logsum.domain.distribution import HistogramLatencies` | this repository's class `HistogramLatencies` (src/logsum/domain/distribution.py:48): Counts per fixed-width bucket, so memory is the same for ten requests and ten billion. |
| 14 | `from logsum.domain.distribution import LatencyDistribution` | this repository's class `LatencyDistribution` (src/logsum/domain/distribution.py:12): The latencies seen for one path. |
| 15 | `from logsum.domain.errors import InvalidSettingError` | this repository's class `InvalidSettingError` (src/logsum/domain/errors.py:21): A setting (environment variable or flag) has a value the program cannot use. |
| 15 | `from logsum.domain.errors import UnreadableLogFileError` | this repository's class `UnreadableLogFileError` (src/logsum/domain/errors.py:8): The log file does not exist, is a directory, or cannot be opened or decompressed. |
| 16 | `from logsum.infrastructure.clock import SystemClock` | this repository's class `SystemClock` (src/logsum/infrastructure/clock.py:8): A monotonic clock backed by `time.perf_counter`. |
| 17 | `from logsum.infrastructure.log_files import FileLineSource` | this repository's class `FileLineSource` (src/logsum/infrastructure/log_files.py:16): Opens files by path. A name ending in `.gz` is decompressed on the fly, still a line at a time. |
| 18 | `from logsum.infrastructure.logging import configure_logging` | this repository's function `configure_logging` (src/logsum/infrastructure/logging.py:35): Send every log record to `stream` (standard error by default) as logfmt. Safe to call twice. |
| 19 | `from logsum.infrastructure.memory import TracemallocMeter` | this repository's class `TracemallocMeter` (src/logsum/infrastructure/memory.py:8): Measures the peak of Python-level allocations, which is what should stay flat as the file grows. |
| 20 | `from logsum.infrastructure.settings import ESTIMATORS` | this repository's constant `ESTIMATORS` (src/logsum/infrastructure/settings.py:13) |
| 20 | `from logsum.infrastructure.settings import Settings` | this repository's class `Settings` (src/logsum/infrastructure/settings.py:27): Every tunable of the program. Command-line flags override these; these override the defaults. |
| 21 | `from logsum.interfaces.render import render_json` | this repository's function `render_json` (src/logsum/interfaces/render.py:26): The same summary as JSON, described by docs/summary.schema.json. |
| 21 | `from logsum.interfaces.render import render_text` | this repository's function `render_text` (src/logsum/interfaces/render.py:12): The human-readable summary: statuses, the slowest paths, the bad-line count, and optionally the run's cost. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 23 | `logging.getLogger` | returns the logger with a given name |
| 38 | `argparse.ArgumentParser` | the object that holds the argument descriptions and reads the command line |
| 79 | `sys.stdout` | the standard output stream |
| 80 | `sys.stderr` | the standard error stream |
| 82 | `os.environ` | the process's environment variables as a dictionary |
| 126 | `os.dup2` | makes one file descriptor (a number naming an open file) point at the same file as another |
| 126 | `os.open` | opens a file at the lowest level and returns a file descriptor |
| 126 | `os.devnull` | the name of the null device, `/dev/null`, which discards what is written to it |
| 126 | `os.O_WRONLY` | the flag for opening a file for writing only |

What the file defines, in order:

- constant `logger` (line 23) is set to `logging.getLogger(__name__)`.
- constant `EXIT_OK` (line 25) is set to `0`.
- constant `EXIT_UNREADABLE` (line 26) is set to `1`.
- constant `EXIT_USAGE` (line 27) is set to `2`.
- constant `EXIT_INTERRUPTED` (line 28) is set to `130`.
- `def distribution_factory(settings: Settings) -> Callable[[], LatencyDistribution]` (line 31): The distribution each path gets: every latency in a list, or fixed-size buckets.
- `def build_parser(defaults: Settings) -> argparse.ArgumentParser` (line 38): The argument parser, with the environment's settings as its defaults.
- `def main(argv: Sequence[str] | None=None, *, environ: Mapping[str, str] | None=None, stdout: TextIO | None=None, stderr: TextIO | None=None) -> int` (line 71): Run the command and return its exit code: 0 done, 1 unreadable file, 2 bad arguments or settings.
- `def entrypoint() -> int` (line 115): The installed command: `main` plus the two ways a command-line tool ends early, Ctrl-C and a closed pipe.

#### `src/logsum/interfaces/make_log_cli.py` (40 lines)

Purpose: `logsum-make-log`: write the sample logs the lesson starts from.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import argparse` | Reads the words typed after a program's name on the command line (see `argparse.md`). |
| 6 | `import random` | Random numbers. `random.Random(seed)` is a generator with its own state: the same seed gives the same sequence. |
| 7 | `import sys` | Facts about the running interpreter: its command-line arguments, its standard streams, its version. |
| 8 | `from collections.abc import Sequence` | type hint for an ordered, indexable collection such as a list or tuple |
| 9 | `from pathlib import Path` | a file path object |
| 11 | `from logsum.infrastructure.sample_log import write_sample_log` | this repository's function `write_sample_log` (src/logsum/infrastructure/sample_log.py:20): Write `lines` lines to `path`, `bad_lines` of them malformed (the three kinds in turn), in one pass. |
| 11 | `from logsum.infrastructure.sample_log import write_small_log` | this repository's function `write_small_log` (src/logsum/infrastructure/sample_log.py:43): Write 20 lines of one path with latencies 1ms to 20ms, whose 95th percentile (19.95) is checked by hand. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 16 | `argparse.ArgumentParser` | the object that holds the argument descriptions and reads the command line |
| 29 | `random.Random` | a random number generator with its own seed |
| 32 | `sys.stderr` | the standard error stream |

What the file defines, in order:

- `def main(argv: Sequence[str] | None=None) -> int` (line 14): Write a sample log and report what it holds. The same seed always gives the same file.
- `def entrypoint() -> int` (line 38): The installed command.

#### `src/logsum/interfaces/render.py` (48 lines)

Purpose: Turns a run report into text or JSON. Output goes to standard output; logs go to standard error.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 5 | `import json` | Reads and writes JSON text (see `json-and-json-schema.md` or `hashlib-and-json.md`). |
| 7 | `from logsum.application.summarize import RunReport` | this repository's class `RunReport` (src/logsum/application/summarize.py:43): A summary and how the run that produced it behaved. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 43 | `json.dumps` | turns a Python value into JSON text |

What the file defines, in order:

- constant `_BYTES_PER_MEGABYTE` (line 9) is set to `1024 * 1024`.
- `def render_text(report: RunReport, *, top: int, show_stats: bool) -> str` (line 12): The human-readable summary: statuses, the slowest paths, the bad-line count, and optionally the run's cost.
- `def render_json(report: RunReport, *, show_stats: bool) -> str` (line 26): The same summary as JSON, described by docs/summary.schema.json.
- `def _stats_line(report: RunReport) -> str` (line 46): builds the last line of the text report: the elapsed seconds with two decimals and the peak memory in megabytes with one decimal, or `n/a` when memory was not measured

#### `scripts/compare_memory.py` (56 lines)

Purpose: The failure mode the lesson names: reading the whole file into a list.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 7 | `from __future__ import annotations` | A special module that switches on language behaviors. `from __future__ import annotations` makes every type hint in the file a piece of text that is read later, so a hint can name a class defined further down the file. |
| 9 | `import sys` | Facts about the running interpreter: its command-line arguments, its standard streams, its version. |
| 10 | `import tempfile` | Temporary files and folders that are removed afterwards. |
| 11 | `import tracemalloc` | Records memory allocations (see `tracemalloc.md`). |
| 12 | `from collections.abc import Callable` | type hint for something that can be called like a function |
| 13 | `from itertools import islice` | takes the first N items of an iterable |
| 14 | `from pathlib import Path` | a file path object |
| 16 | `from logsum.application.summarize import BadLineCounter` | this repository's class `BadLineCounter` (src/logsum/application/summarize.py:17): Counts the lines the stream skipped. |
| 16 | `from logsum.application.summarize import stream_requests` | this repository's function `stream_requests` (src/logsum/application/summarize.py:28): Yield the parsed request of each readable line, one at a time, and count the rest. |

Names used through an imported module:

| Line | Name | What it does |
|---|---|---|
| 34 | `tracemalloc.start` | starts recording allocations |
| 36 | `tracemalloc.get_traced_memory` | returns the current and peak traced memory |
| 37 | `tracemalloc.stop` | stops recording |
| 45 | `tempfile.TemporaryDirectory` | a folder that is deleted when the `with` block ends |
| 56 | `sys.argv` | the list of command-line words |

What the file defines, in order:

- `def streaming(path: Path) -> int` (line 19): Count the requests, holding one line at a time.
- `def loading_everything(path: Path) -> int` (line 25): Count the requests after loading every line into a list.
- `def peak_megabytes(work: Callable[[Path], int], path: Path) -> float` (line 32): Peak traced memory of `work(path)`, in megabytes.
- `def main(log: Path) -> None` (line 41): Print the comparison for the whole log and for a tenth of it.

## Try it yourself

```bash
uv run --frozen python --version
```
Expected: `Python 3.14.3`.

```bash
uv run --frozen python -c "
from logsum.domain.request import parse
print(parse('2026-03-14T09:26:53Z GET /orders/1234 200 87ms'))
print(parse(''))
print(parse('2026-03-14T09:26:53Z GET /orders/1234 200 abcms'))
"
```
Expected: a `Request(timestamp=datetime.datetime(2026, 3, 14, 9, 26, 53, tzinfo=datetime.timezone.utc), method='GET', path='/orders/1234', status=200, latency_ms=87)` and then `None` twice.

```bash
uv run --frozen python -c "
def numbers():
    for n in (1, 2, 3):
        print('making', n)
        yield n
for n in numbers():
    print('got', n)
"
```
Expected: `making 1`, `got 1`, `making 2`, `got 2`, `making 3`, `got 3`: each value is made only when the loop asks for it.

```bash
uv run --frozen python -c "
from logsum.domain.request import parse
request = parse('2026-03-14T09:26:53Z GET /a 200 5ms')
try:
    request.status = 500
except Exception as error:
    print(type(error).__name__)
"
```
Expected: `FrozenInstanceError`.

## Mistakes people make

- **Reading a whole file into a list** (`.readlines()`): memory grows with the file. Iterate the file object, as `FileLineSource` does.
- **Comparing with `None` using `==`.** Use `is None`.
- **Mutable default arguments** such as `def f(x=[])`: the same list is shared by every call. This code uses `None` or immutable defaults.
- **Catching everything** (`except Exception:` and moving on). This code catches the specific error it expects.
- **Believing type hints stop bad data at run time.** They do not; `parse` checks its input by hand.

## Check yourself

**1. What does the `yield` keyword do?**
It makes the function a generator: each `yield` hands out one value and pauses the function until the next value is asked for.

**2. What do `frozen=True` and `slots=True` do in `@dataclass(frozen=True, slots=True)`?**
`frozen` makes instances read-only; `slots` stores fields in a fixed layout without a per-object dictionary, saving memory.

**3. Why does `parse` return `None` instead of raising an exception for a bad line?**
A bad line is routine in a large log, so it is a value the caller must check; mypy forces the check.

**4. What does `with open(...) as f:` guarantee?**
The file is closed when the block ends, also if an error happens inside.

**5. What is `Protocol` for?**
To name an interface by its methods; any class with matching methods fits it without inheriting, and mypy checks the fit.

## Further reading

- The Python 3.14 tutorial and language reference: https://docs.python.org/3.14/tutorial/ and https://docs.python.org/3.14/reference/
- `dataclasses`: https://docs.python.org/3.14/library/dataclasses.html ; `contextlib`: https://docs.python.org/3.14/library/contextlib.html ; `typing.Protocol`: https://docs.python.org/3.14/library/typing.html#typing.Protocol
- Generators: https://docs.python.org/3.14/howto/functional.html#generators
