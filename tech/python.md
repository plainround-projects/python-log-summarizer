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
- An **enumeration** (`enum`) is a fixed set of named values, such as the report modes, so a typo is an error instead of a silent new value.
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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (lines 1 to 3):

```python
"""logsum: stream a web server access log and print a summary of statuses and slow paths."""

__version__ = "0.1.0"
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 3: stores `'0.1.0'` in `__version__`.

#### `src/logsum/__main__.py` (6 lines)

Purpose: Run the command with `python -m logsum`.

Imports:

| Line | Statement | What it brings in |
|---|---|---|
| 3 | `from logsum.interfaces.cli import entrypoint` | this repository's function `entrypoint` (src/logsum/interfaces/cli.py:115): The installed command: `main` plus the two ways a command-line tool ends early, Ctrl-C and a closed pipe. |

What the file defines, in order:

This file defines no functions, classes or constants.

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Run the command with `python -m logsum`."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (line 3):

```python
from logsum.interfaces.cli import entrypoint
```

Module-level statements (lines 5 to 6):

```python
if __name__ == "__main__":
    raise SystemExit(entrypoint())
```

- line 5: if `__name__ == '__main__'` is true:
  - line 6: raises (throws) the error `SystemExit(entrypoint())`.

#### `src/logsum/application/__init__.py` (1 lines)

Purpose: The use case of the program and the ports it needs. Depends on the domain only.

Imports:

This file has no imports.

What the file defines, in order:

This file defines no functions, classes or constants.

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""The use case of the program and the ports it needs. Depends on the domain only."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""What the use case needs from the outside world, as interfaces the infrastructure layer implements."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 7):

```python
from __future__ import annotations

from collections.abc import Iterator
from contextlib import AbstractContextManager
from typing import Protocol
```

class `LineSource`: Opens a log by name and hands out its lines one at a time. (lines 10 to 11):

```python
class LineSource(Protocol):
    """Opens a log by name and hands out its lines one at a time."""
```

- line 11: the docstring: text that describes this piece; Python keeps it but does not run it.

**`LineSource.open`**: Open `location`; the context closes it, also when reading fails. (lines 13 to 17):

```python
    def open(self, location: str) -> AbstractContextManager[Iterator[str]]:
        """Open `location`; the context closes it, also when reading fails.

        Raises `UnreadableLogFileError` when it cannot be opened or read.
        """
```

- line 14: the docstring: text that describes this piece; Python keeps it but does not run it.

class `Clock`: A monotonic clock in seconds, injected so tests control time. (lines 20 to 21):

```python
class Clock(Protocol):
    """A monotonic clock in seconds, injected so tests control time."""
```

- line 21: the docstring: text that describes this piece; Python keeps it but does not run it.

**`Clock.monotonic`**: Seconds from an arbitrary start; only differences mean anything. (lines 23 to 24):

```python
    def monotonic(self) -> float:
        """Seconds from an arbitrary start; only differences mean anything."""
```

- line 24: the docstring: text that describes this piece; Python keeps it but does not run it.

class `MemoryMeter`: Measures the peak Python memory of a run. (lines 27 to 28):

```python
class MemoryMeter(Protocol):
    """Measures the peak Python memory of a run."""
```

- line 28: the docstring: text that describes this piece; Python keeps it but does not run it.

**`MemoryMeter.start`**: Begin measuring. (lines 30 to 31):

```python
    def start(self) -> None:
        """Begin measuring."""
```

- line 31: the docstring: text that describes this piece; Python keeps it but does not run it.

**`MemoryMeter.stop`**: Stop measuring and return the peak in bytes since `start`. (lines 33 to 34):

```python
    def stop(self) -> int:
        """Stop measuring and return the peak in bytes since `start`."""
```

- line 34: the docstring: text that describes this piece; Python keeps it but does not run it.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""The one use case: read a log as a stream and summarize it."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 12):

```python
from __future__ import annotations

import logging
from collections.abc import Callable, Iterable, Iterator
from dataclasses import dataclass

from logsum.application.ports import Clock, LineSource, MemoryMeter
from logsum.domain.distribution import LatencyDistribution
from logsum.domain.request import Request, parse
from logsum.domain.tally import LogTally, Summary
```

Module-level statements (line 14):

```python
logger = logging.getLogger(__name__)
```

- line 14: stores the result of calling `logging.getLogger` with 1 argument(s) in `logger`.

class `BadLineCounter`: Counts the lines the stream skipped. (lines 17 to 22):

```python
class BadLineCounter:
    """Counts the lines the stream skipped.

    A generator's `return` value is invisible to a plain `for` loop, so the count lives in an object the
    caller passes in and reads afterwards.
    """
```

- line 18: the docstring: text that describes this piece; Python keeps it but does not run it.

**`BadLineCounter.__init__`**: builds the object: stores the arguments it was given (lines 24 to 25):

```python
    def __init__(self) -> None:
        self.count = 0
```

- line 25: stores `0` in `self.count`.

**`stream_requests`**: Yield the parsed request of each readable line, one at a time, and count the rest. (lines 28 to 39):

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

- line 29: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 34: for each item of `lines`, with the item called `raw_line`:
  - line 35: stores the result of calling `parse` with 1 argument(s) in `request`.
  - line 36: if `request is None` is true:
    - line 37: adds `1` to `bad_lines.count`.
  - otherwise:
    - line 39: hands out (`yield`) and pauses until the next value is asked for: `request`

class `RunReport`: A summary and how the run that produced it behaved. (lines 42 to 48):

```python
@dataclass(frozen=True, slots=True)
class RunReport:
    """A summary and how the run that produced it behaved."""

    summary: Summary
    elapsed_seconds: float
    peak_memory_bytes: int | None
```

- line 42: the decorator `dataclass(frozen=True, slots=True)` wraps or registers what is defined just below it.
- line 44: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 46: declares `summary` with the type `Summary` (no value yet).
- line 47: declares `elapsed_seconds` with the type `float` (no value yet).
- line 48: declares `peak_memory_bytes` with the type `int | None` (no value yet).

class `SummarizeLog`: Summarize a log file: statuses, slowest paths by 95th percentile, unreadable lines. (lines 51 to 52):

```python
class SummarizeLog:
    """Summarize a log file: statuses, slowest paths by 95th percentile, unreadable lines."""
```

- line 52: the docstring: text that describes this piece; Python keeps it but does not run it.

**`SummarizeLog.__init__`**: builds the object: stores the arguments it was given (lines 54 to 64):

```python
    def __init__(
        self,
        source: LineSource,
        clock: Clock,
        new_distribution: Callable[[], LatencyDistribution],
        memory: MemoryMeter | None = None,
    ) -> None:
        self._source = source
        self._clock = clock
        self._new_distribution = new_distribution
        self._memory = memory
```

- line 61: stores `source` in `self._source`.
- line 62: stores `clock` in `self._clock`.
- line 63: stores `new_distribution` in `self._new_distribution`.
- line 64: stores `memory` in `self._memory`.

**`SummarizeLog.run`**: Stream `location` once and return its summary with the elapsed time and peak memory. (lines 66 to 93):

```python
    def run(self, location: str, top: int = 10) -> RunReport:
        """Stream `location` once and return its summary with the elapsed time and peak memory."""
        tally = LogTally(self._new_distribution)
        bad_lines = BadLineCounter()
        if self._memory:
            self._memory.start()
        started = self._clock.monotonic()
        try:
            with self._source.open(location) as lines:
                for request in stream_requests(lines, bad_lines):
                    tally.add(request)
        finally:
            elapsed = self._clock.monotonic() - started
            peak = self._memory.stop() if self._memory else None
        tally.add_bad_lines(bad_lines.count)
        report = RunReport(tally.summary(top), elapsed, peak)
        logger.info(
            "summarized log",
            extra={
                "fields": {
                    "location": location,
                    "requests": report.summary.total_requests,
                    "bad_lines": bad_lines.count,
                    "elapsed_seconds": round(elapsed, 3),
                }
            },
        )
        return report
```

- line 67: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 68: stores the result of calling `LogTally` with 1 argument(s) in `tally`.
- line 69: stores the result of calling `BadLineCounter` in `bad_lines`.
- line 70: if `self._memory` is true:
  - line 71: runs `self._memory.start()`; the result is not kept.
- line 72: stores the result of calling `self._clock.monotonic` in `started`.
- line 73: tries the block below; an error inside it goes to the matching `except`:
  - line 74: opens (`with`) `self._source.open(location)` as `lines`; whatever it holds is released when the block ends, also after an error:
    - line 75: for each item of `stream_requests(lines, bad_lines)`, with the item called `request`:
      - line 76: runs `tally.add(request)`; the result is not kept.
- in every case, at the end (`finally`):
  - line 78: stores `self._clock.monotonic() - started` in `elapsed`.
  - line 79: stores `self._memory.stop()` if `self._memory`, otherwise `None` in `peak`.
- line 80: runs `tally.add_bad_lines(bad_lines.count)`; the result is not kept.
- line 81: stores the result of calling `RunReport` with 3 argument(s) in `report`.
- line 82: runs `logger.info('summarized log', extra={'fields': {'location': location, 'requests': report.summary.total_requests, 'bad_lines': bad_lines.count, 'ela...`; the result is not kept.
- line 93: ends the function and gives back `report`.

#### `src/logsum/domain/__init__.py` (4 lines)

Purpose: The rules of the problem: what a request is, what counts as a bad line, how latencies are summarized.

Imports:

This file has no imports.

What the file defines, in order:

This file defines no functions, classes or constants.

Source in full, in pieces, each followed by what its statements do:

Module-level statements (lines 1 to 4):

```python
"""The rules of the problem: what a request is, what counts as a bad line, how latencies are summarized.

Depends on nothing outside the standard library.
"""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Where the latencies of one path are kept, and how much each choice remembers."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 9):

```python
from __future__ import annotations

from array import array
from typing import Protocol

from logsum.domain.errors import InvalidSettingError
from logsum.domain.percentile import p95, p95_from_ranks
```

class `LatencyDistribution`: The latencies seen for one path. (lines 12 to 13):

```python
class LatencyDistribution(Protocol):
    """The latencies seen for one path."""
```

- line 13: the docstring: text that describes this piece; Python keeps it but does not run it.

**`LatencyDistribution.add`**: Record one latency. (lines 15 to 16):

```python
    def add(self, latency_ms: int) -> None:
        """Record one latency."""
```

- line 16: the docstring: text that describes this piece; Python keeps it but does not run it.

**`LatencyDistribution.p95`**: The 95th percentile of what was recorded. (lines 18 to 19):

```python
    def p95(self) -> float:
        """The 95th percentile of what was recorded."""
```

- line 19: the docstring: text that describes this piece; Python keeps it but does not run it.

**`LatencyDistribution.__len__`**: How many latencies were recorded. (lines 21 to 22):

```python
    def __len__(self) -> int:
        """How many latencies were recorded."""
```

- line 22: the docstring: text that describes this piece; Python keeps it but does not run it.

class `ExactLatencies`: Every latency in a list, so the percentile is exact. (lines 25 to 31):

```python
class ExactLatencies:
    """Every latency in a list, so the percentile is exact.

    The list grows with the number of requests to the path, with no bound: a hot path with tens of millions of
    requests holds tens of millions of integers. That is fine for a summary of one file and wrong for a long
    running service, which is what `HistogramLatencies` is for.
    """
```

- line 26: the docstring: text that describes this piece; Python keeps it but does not run it.

**`ExactLatencies.__init__`**: builds the object: stores the arguments it was given (lines 33 to 34):

```python
    def __init__(self) -> None:
        self._values: list[int] = []
```

- line 34: declares `self._values` with the type `list[int]` and stores `[]` in it.

**`ExactLatencies.add`**: Record one latency. (lines 36 to 38):

```python
    def add(self, latency_ms: int) -> None:
        """Record one latency."""
        self._values.append(latency_ms)
```

- line 37: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 38: runs `self._values.append(latency_ms)`; the result is not kept.

**`ExactLatencies.p95`**: The exact 95th percentile. (lines 40 to 42):

```python
    def p95(self) -> float:
        """The exact 95th percentile."""
        return p95(self._values)
```

- line 41: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 42: ends the function and gives back the result of calling `p95` with 1 argument(s).

**`ExactLatencies.__len__`**: the number given by `len(obj)` (lines 44 to 45):

```python
    def __len__(self) -> int:
        return len(self._values)
```

- line 45: ends the function and gives back the result of calling `len` with 1 argument(s).

class `HistogramLatencies`: Counts per fixed-width bucket, so memory is the same for ten requests and ten billion. (lines 48 to 56):

```python
class HistogramLatencies:
    """Counts per fixed-width bucket, so memory is the same for ten requests and ten billion.

    Accuracy given up, stated exactly: a latency is remembered as the lower edge of its bucket, so the
    percentile is never above the exact one and at most `bucket_ms - 1` below it, for whole-millisecond
    latencies under `max_latency_ms`. A latency at or over `max_latency_ms` counts as `max_latency_ms`, so
    the percentile is wrong only when more than 5 percent of requests exceed that cap. With `bucket_ms=1` the
    answer is identical to `ExactLatencies` below the cap.
    """
```

- line 49: the docstring: text that describes this piece; Python keeps it but does not run it.

**`HistogramLatencies.__init__`**: builds the object: stores the arguments it was given (lines 58 to 66):

```python
    def __init__(self, bucket_ms: int = 5, max_latency_ms: int = 10_000) -> None:
        if bucket_ms < 1 or max_latency_ms < bucket_ms:
            raise InvalidSettingError(
                f"need 1 <= bucket_ms <= max_latency_ms, got bucket_ms={bucket_ms}, max_latency_ms={max_latency_ms}"
            )
        self._bucket_ms = bucket_ms
        self._last_bucket = max_latency_ms // bucket_ms
        self._counts = array("Q", bytes(8 * (self._last_bucket + 1)))
        self._total = 0
```

- line 59: if `bucket_ms < 1 or max_latency_ms < bucket_ms` is true:
  - line 60: raises (throws) the error `InvalidSettingError(f'need 1 <= bucket_ms <= max_latency_ms, got bucket_ms={bucket_ms}, max_latency_ms={max_latency_ms}')`.
- line 63: stores `bucket_ms` in `self._bucket_ms`.
- line 64: stores `max_latency_ms // bucket_ms` in `self._last_bucket`.
- line 65: stores the result of calling `array` with 2 argument(s) in `self._counts`.
- line 66: stores `0` in `self._total`.

**`HistogramLatencies.add`**: Record one latency. (lines 68 to 71):

```python
    def add(self, latency_ms: int) -> None:
        """Record one latency."""
        self._counts[min(latency_ms // self._bucket_ms, self._last_bucket)] += 1
        self._total += 1
```

- line 69: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 70: adds `1` to `self._counts[min(latency_ms // self._bucket_ms, self._last_bucket)]`.
- line 71: adds `1` to `self._total`.

**`HistogramLatencies.p95`**: The 95th percentile, to within the bucket width. (lines 73 to 75):

```python
    def p95(self) -> float:
        """The 95th percentile, to within the bucket width."""
        return p95_from_ranks(self._total, self._kth_smallest)
```

- line 74: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 75: ends the function and gives back the result of calling `p95_from_ranks` with 2 argument(s).

**`HistogramLatencies._kth_smallest`**: walks the buckets from the smallest, adding up how many values each holds, and returns the lower edge in milliseconds of the bucket that contains the value at position `index` when all values are sorted; the final `raise` can only happen if a caller asks for a position beyond the total, which the callers never do (lines 77 to 83):

```python
    def _kth_smallest(self, index: int) -> int:
        seen = 0
        for bucket, count in enumerate(self._counts):
            seen += count
            if index < seen:
                return bucket * self._bucket_ms
        raise IndexError(index)  # pragma: no cover - callers stay below the total
```

- line 78: stores `0` in `seen`.
- line 79: for each item of `enumerate(self._counts)`, with the item called `(bucket, count)`:
  - line 80: adds `count` to `seen`.
  - line 81: if `index < seen` is true:
    - line 82: ends the function and gives back `bucket * self._bucket_ms`.
- line 83: raises (throws) the error `IndexError(index)`.

**`HistogramLatencies.__len__`**: the number given by `len(obj)` (lines 85 to 86):

```python
    def __len__(self) -> int:
        return self._total
```

- line 86: ends the function and gives back `self._total`.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Named errors, so callers handle a failure by what it means and not by message text."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

class `LogsumError`: Base class of every error this program raises on purpose. (lines 4 to 5):

```python
class LogsumError(Exception):
    """Base class of every error this program raises on purpose."""
```

- line 5: the docstring: text that describes this piece; Python keeps it but does not run it.

class `UnreadableLogFileError`: The log file does not exist, is a directory, or cannot be opened or decompressed. (lines 8 to 9):

```python
class UnreadableLogFileError(LogsumError):
    """The log file does not exist, is a directory, or cannot be opened or decompressed."""
```

- line 9: the docstring: text that describes this piece; Python keeps it but does not run it.

**`UnreadableLogFileError.__init__`**: builds the object: stores the arguments it was given (lines 11 to 14):

```python
    def __init__(self, location: str, reason: str) -> None:
        super().__init__(f"cannot read {location}: {reason}")
        self.location = location
        self.reason = reason
```

- line 12: runs `super().__init__(f'cannot read {location}: {reason}')`; the result is not kept.
- line 13: stores `location` in `self.location`.
- line 14: stores `reason` in `self.reason`.

class `EmptyDistributionError`: A percentile was asked of a distribution that holds no latencies. (lines 17 to 18):

```python
class EmptyDistributionError(LogsumError):
    """A percentile was asked of a distribution that holds no latencies."""
```

- line 18: the docstring: text that describes this piece; Python keeps it but does not run it.

class `InvalidSettingError`: A setting (environment variable or flag) has a value the program cannot use. (lines 21 to 22):

```python
class InvalidSettingError(LogsumError):
    """A setting (environment variable or flag) has a value the program cannot use."""
```

- line 22: the docstring: text that describes this piece; Python keeps it but does not run it.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""The 95th percentile, defined once so every distribution agrees on it."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 8):

```python
from __future__ import annotations

from collections.abc import Callable, Sequence
from statistics import quantiles

from logsum.domain.errors import EmptyDistributionError
```

Module-level statements (lines 10 to 12):

```python
_CUTS = 100
_PERCENT = 95
_P95_INDEX = _PERCENT - 1  # quantiles(..., n=100) returns 99 cut points; the 95th is at index 94
```

- line 10: stores `100` in `_CUTS`.
- line 11: stores `95` in `_PERCENT`.
- line 12: stores `_PERCENT - 1` in `_P95_INDEX`.

**`p95`**: The 95th percentile by the exclusive method (the `statistics.quantiles` default). (lines 15 to 26):

```python
def p95(latencies: Sequence[int]) -> float:
    """The 95th percentile by the exclusive method (the `statistics.quantiles` default).

    A single latency is its own percentile. For the integers 1 to 20 the answer is 19.95. The exclusive method
    extrapolates past the largest value when there are few data points (four latencies give 47.5 for a maximum of
    40), so the answer is capped at the largest latency: no request was slower than that.
    """
    if not latencies:
        raise EmptyDistributionError("no latencies to take a percentile of")
    if len(latencies) == 1:
        return float(latencies[0])
    return min(quantiles(latencies, n=_CUTS)[_P95_INDEX], float(max(latencies)))
```

- line 16: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 22: if `not latencies` is true:
  - line 23: raises (throws) the error `EmptyDistributionError('no latencies to take a percentile of')`.
- line 24: if `len(latencies) == 1` is true:
  - line 25: ends the function and gives back the result of calling `float` with 1 argument(s).
- line 26: ends the function and gives back the result of calling `min` with 2 argument(s).

**`p95_from_ranks`**: The same value as `p95`, computed from `count` and a lookup of the k-th smallest latency (0-based). (lines 29 to 43):

```python
def p95_from_ranks(count: int, kth_smallest: Callable[[int], int]) -> float:
    """The same value as `p95`, computed from `count` and a lookup of the k-th smallest latency (0-based).

    This lets a histogram answer without expanding itself into a sorted list. The arithmetic is the one in
    `statistics.quantiles`: scale the cut point to the rank space, clamp it, interpolate between neighbors.
    """
    if count == 0:
        raise EmptyDistributionError("no latencies to take a percentile of")
    if count == 1:
        return float(kth_smallest(0))
    spacing = count + 1
    rank = min(max(_PERCENT * spacing // _CUTS, 1), count - 1)
    delta = _PERCENT * spacing - rank * _CUTS
    interpolated = (kth_smallest(rank - 1) * (_CUTS - delta) + kth_smallest(rank) * delta) / _CUTS
    return min(interpolated, float(kth_smallest(count - 1)))
```

- line 30: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 35: if `count == 0` is true:
  - line 36: raises (throws) the error `EmptyDistributionError('no latencies to take a percentile of')`.
- line 37: if `count == 1` is true:
  - line 38: ends the function and gives back the result of calling `float` with 1 argument(s).
- line 39: stores `count + 1` in `spacing`.
- line 40: stores the result of calling `min` with 2 argument(s) in `rank`.
- line 41: stores `_PERCENT * spacing - rank * _CUTS` in `delta`.
- line 42: stores `(kth_smallest(rank - 1) * (_CUTS - delta) + kth_smallest(rank) * delta) / _CUTS` in `interpolated`.
- line 43: ends the function and gives back the result of calling `min` with 2 argument(s).

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""One parsed access-log line and the function that reads it."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 6):

```python
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
```

Module-level statements (lines 8 to 11):

```python
_FIELD_COUNT = 5
_LATENCY_SUFFIX = "ms"
_FIRST_STATUS = 100
_LAST_STATUS = 599
```

- line 8: stores `5` in `_FIELD_COUNT`.
- line 9: stores `'ms'` in `_LATENCY_SUFFIX`.
- line 10: stores `100` in `_FIRST_STATUS`.
- line 11: stores `599` in `_LAST_STATUS`.

class `Request`: One request from the access log. Immutable, and without a per-instance dict, since one exists per line. (lines 14 to 22):

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

- line 14: the decorator `dataclass(frozen=True, slots=True)` wraps or registers what is defined just below it.
- line 16: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 18: declares `timestamp` with the type `datetime` (no value yet).
- line 19: declares `method` with the type `str` (no value yet).
- line 20: declares `path` with the type `str` (no value yet).
- line 21: declares `status` with the type `int` (no value yet).
- line 22: declares `latency_ms` with the type `int` (no value yet).

**`_digits_to_int`**: turns text into a whole number only when it is plain ASCII digits (`int()` alone would also accept `+5`, `1_000` and digits of other alphabets); returns `None` for anything else, so a bad log field becomes a bad line, not a wrong number (lines 25 to 27):

```python
def _digits_to_int(text: str) -> int | None:
    # int() also accepts "+5", "1_000" and non-ASCII digits; a log field is plain ASCII digits or it is bad.
    return int(text) if text.isascii() and text.isdecimal() else None
```

- line 27: ends the function and gives back `int(text)` if `text.isascii() and text.isdecimal()`, otherwise `None`.

**`parse`**: Read one line of `<timestamp> <METHOD> <path> <status> <latency>ms`. (lines 30 to 55):

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

- line 31: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 37: stores the result of calling `line.split` in `fields`.
- line 38: if `len(fields) != _FIELD_COUNT` is true:
  - line 39: ends the function and gives back `None`.
- line 40: stores `fields` in `(raw_timestamp, method, path, raw_status, raw_latency)`.
- line 41: if `not raw_latency.endswith(_LATENCY_SUFFIX)` is true:
  - line 42: ends the function and gives back `None`.
- line 43: stores the result of calling `_digits_to_int` with 1 argument(s) in `status`.
- line 44: stores the result of calling `_digits_to_int` with 1 argument(s) in `latency_ms`.
- line 45: if `status is None or latency_ms is None or (not _FIRST_STATUS <= status <= _LAST_STATUS)` is true:
  - line 46: ends the function and gives back `None`.
- line 47: if `not (method.isascii() and method.isalpha() and method.isupper() and path.startswith('/'))` is true:
  - line 48: ends the function and gives back `None`.
- line 49: tries the block below; an error inside it goes to the matching `except`:
  - line 50: stores the result of calling `datetime.fromisoformat` with 1 argument(s) in `timestamp`.
- line 51: if the error is `ValueError`:
  - line 52: ends the function and gives back `None`.
- line 53: if `timestamp.tzinfo is None` is true:
  - line 54: ends the function and gives back `None`.
- line 55: ends the function and gives back the result of calling `Request` with 5 argument(s).

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""The running totals of a log, and the summary they turn into."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 10):

```python
from __future__ import annotations

from collections import Counter
from collections.abc import Callable, Mapping
from dataclasses import dataclass

from logsum.domain.distribution import LatencyDistribution
from logsum.domain.request import Request
```

class `PathLatency`: The 95th-percentile latency of one path and how many requests it is based on. (lines 13 to 19):

```python
@dataclass(frozen=True, slots=True)
class PathLatency:
    """The 95th-percentile latency of one path and how many requests it is based on."""

    path: str
    p95_ms: float
    requests: int
```

- line 13: the decorator `dataclass(frozen=True, slots=True)` wraps or registers what is defined just below it.
- line 15: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 17: declares `path` with the type `str` (no value yet).
- line 18: declares `p95_ms` with the type `float` (no value yet).
- line 19: declares `requests` with the type `int` (no value yet).

class `Summary`: What the program prints: requests per status, the slowest paths, and the lines it could not read. (lines 22 to 29):

```python
@dataclass(frozen=True, slots=True)
class Summary:
    """What the program prints: requests per status, the slowest paths, and the lines it could not read."""

    total_requests: int
    bad_lines: int
    status_counts: Mapping[int, int]
    slowest_paths: tuple[PathLatency, ...]
```

- line 22: the decorator `dataclass(frozen=True, slots=True)` wraps or registers what is defined just below it.
- line 24: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 26: declares `total_requests` with the type `int` (no value yet).
- line 27: declares `bad_lines` with the type `int` (no value yet).
- line 28: declares `status_counts` with the type `Mapping[int, int]` (no value yet).
- line 29: declares `slowest_paths` with the type `tuple[PathLatency, ...]` (no value yet).

class `LogTally`: Accumulates one request at a time; memory depends on the paths and the distribution, not the file. (lines 32 to 33):

```python
class LogTally:
    """Accumulates one request at a time; memory depends on the paths and the distribution, not the file."""
```

- line 33: the docstring: text that describes this piece; Python keeps it but does not run it.

**`LogTally.__init__`**: builds the object: stores the arguments it was given (lines 35 to 39):

```python
    def __init__(self, new_distribution: Callable[[], LatencyDistribution]) -> None:
        self._new_distribution = new_distribution
        self._statuses: Counter[int] = Counter()
        self._by_path: dict[str, LatencyDistribution] = {}
        self._bad_lines = 0
```

- line 36: stores `new_distribution` in `self._new_distribution`.
- line 37: declares `self._statuses` with the type `Counter[int]` and stores the result of calling `Counter` in it.
- line 38: declares `self._by_path` with the type `dict[str, LatencyDistribution]` and stores `{}` in it.
- line 39: stores `0` in `self._bad_lines`.

**`LogTally.add`**: Count a parsed request under its status and file its latency under its path. (lines 41 to 51):

```python
    def add(self, request: Request) -> None:
        """Count a parsed request under its status and file its latency under its path.

        One distribution per path, because the ten slowest paths are compared with each other and a
        percentile over all latencies mixed together says nothing about any one path.
        """
        self._statuses[request.status] += 1
        distribution = self._by_path.get(request.path)
        if distribution is None:
            distribution = self._by_path[request.path] = self._new_distribution()
        distribution.add(request.latency_ms)
```

- line 42: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 47: adds `1` to `self._statuses[request.status]`.
- line 48: stores the result of calling `self._by_path.get` with 1 argument(s) in `distribution`.
- line 49: if `distribution is None` is true:
  - line 50: stores the result of calling `self._new_distribution` in `distribution`, `self._by_path[request.path]`.
- line 51: runs `distribution.add(request.latency_ms)`; the result is not kept.

**`LogTally.add_bad_lines`**: Count lines that could not be read. (lines 53 to 55):

```python
    def add_bad_lines(self, count: int = 1) -> None:
        """Count lines that could not be read."""
        self._bad_lines += count
```

- line 54: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 55: adds `count` to `self._bad_lines`.

**`LogTally.summary`**: The totals so far, with the `top` paths of highest 95th-percentile latency (ties by path name). (lines 57 to 68):

```python
    def summary(self, top: int = 10) -> Summary:
        """The totals so far, with the `top` paths of highest 95th-percentile latency (ties by path name)."""
        ranked = sorted(
            (PathLatency(path, distribution.p95(), len(distribution)) for path, distribution in self._by_path.items()),
            key=lambda entry: (-entry.p95_ms, entry.path),
        )
        return Summary(
            total_requests=self._statuses.total(),
            bad_lines=self._bad_lines,
            status_counts=dict(sorted(self._statuses.items())),
            slowest_paths=tuple(ranked[:top]),
        )
```

- line 58: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 59: stores the result of calling `sorted` with 2 argument(s) in `ranked`.
- line 63: ends the function and gives back the result of calling `Summary` with 4 argument(s).

#### `src/logsum/infrastructure/__init__.py` (1 lines)

Purpose: Adapters to the outside world: files, the clock, memory measurement, settings, logging.

Imports:

This file has no imports.

What the file defines, in order:

This file defines no functions, classes or constants.

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Adapters to the outside world: files, the clock, memory measurement, settings, logging."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""The real clock."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 5):

```python
from __future__ import annotations

import time
```

class `SystemClock`: A monotonic clock backed by `time.perf_counter`. (lines 8 to 9):

```python
class SystemClock:
    """A monotonic clock backed by `time.perf_counter`."""
```

- line 9: the docstring: text that describes this piece; Python keeps it but does not run it.

**`SystemClock.monotonic`**: Seconds from an arbitrary start. (lines 11 to 13):

```python
    def monotonic(self) -> float:
        """Seconds from an arbitrary start."""
        return time.perf_counter()
```

- line 12: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 13: ends the function and gives back the result of calling `time.perf_counter`.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Reading a log from disk, plain or gzip-compressed, one line at a time."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 11):

```python
from __future__ import annotations

import gzip
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO

from logsum.domain.errors import UnreadableLogFileError
```

Module-level statements (line 13):

```python
_ENCODING = "utf-8"
```

- line 13: stores `'utf-8'` in `_ENCODING`.

class `FileLineSource`: Opens files by path. A name ending in `.gz` is decompressed on the fly, still a line at a time. (lines 16 to 17):

```python
class FileLineSource:
    """Opens files by path. A name ending in `.gz` is decompressed on the fly, still a line at a time."""
```

- line 17: the docstring: text that describes this piece; Python keeps it but does not run it.

**`FileLineSource.open`**: Yield the lines of the file at `location`; always close it. (lines 19 to 32):

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

- line 19: the decorator `contextmanager` wraps or registers what is defined just below it.
- line 21: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 26: stores the result of calling `Path` with 1 argument(s) in `path`.
- line 27: tries the block below; an error inside it goes to the matching `except`:
  - line 28: stores the result of calling `self._open_text` with 1 argument(s) in `handle`.
- line 29: if the error is `OSError` (the error is called `error`):
  - line 30: raises (throws) the error `UnreadableLogFileError(location, error.strerror or str(error))`, chained to `error`.
- line 31: opens (`with`) `handle`; whatever it holds is released when the block ends, also after an error:
  - line 32: hands out (`yield`) and pauses until the next value is asked for: `self._lines(handle, location)`

**`FileLineSource._open_text`**: opens a file for reading text: a name ending in `.gz` is opened through `gzip.open` in text mode (`"rt"`), anything else through `Path.open`; both use UTF-8 and `errors="replace"`, which puts a replacement character in place of bytes that are not valid UTF-8 instead of failing (lines 34 to 38):

```python
    @staticmethod
    def _open_text(path: Path) -> TextIO:
        if path.suffix == ".gz":
            return gzip.open(path, "rt", encoding=_ENCODING, errors="replace")
        return path.open(encoding=_ENCODING, errors="replace")
```

- line 34: the decorator `staticmethod` wraps or registers what is defined just below it.
- line 36: if `path.suffix == '.gz'` is true:
  - line 37: ends the function and gives back the result of calling `gzip.open` with 4 argument(s).
- line 38: ends the function and gives back the result of calling `path.open` with 2 argument(s).

**`FileLineSource._lines`**: hands out the lines of an open file one at a time (`yield from handle`), and turns an operating-system error or a damaged gzip file (`OSError`, `EOFError`) into the repository's own `UnreadableLogFileError` that names the file (lines 40 to 45):

```python
    @staticmethod
    def _lines(handle: TextIO, location: str) -> Iterator[str]:
        try:
            yield from handle
        except (OSError, EOFError) as error:
            raise UnreadableLogFileError(location, str(error)) from error
```

- line 40: the decorator `staticmethod` wraps or registers what is defined just below it.
- line 42: tries the block below; an error inside it goes to the matching `except`:
  - line 43: hands out every value of `handle`
- line 44: if the error is `(OSError, EOFError)` (the error is called `error`):
  - line 45: raises (throws) the error `UnreadableLogFileError(location, str(error))`, chained to `error`.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Structured logging: one logfmt line per event (`ts=... level=... logger=... msg=... key=value`)."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 9):

```python
from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime
from typing import TextIO
```

**`_quote`**: turns any value into text for a `key=value` log line: text that is empty or holds a space, an equals sign, a double quote or a line break is wrapped in double quotes (with JSON escapes) so a reader can split the line again; other text is left as it is (lines 12 to 14):

```python
def _quote(value: object) -> str:
    text = str(value)
    return json.dumps(text) if not text or any(char in text for char in ' ="\n') else text
```

- line 13: stores the result of calling `str` with 1 argument(s) in `text`.
- line 14: ends the function and gives back `json.dumps(text)` if `not text or any((char in text for char in ' ="\n'))`, otherwise `text`.

class `LogfmtFormatter`: Format a log record as one logfmt line, with the record's `fields` extra as key=value pairs. (lines 17 to 18):

```python
class LogfmtFormatter(logging.Formatter):
    """Format a log record as one logfmt line, with the record's `fields` extra as key=value pairs."""
```

- line 18: the docstring: text that describes this piece; Python keeps it but does not run it.

**`LogfmtFormatter.format`**: Render `record` as a single line. (lines 20 to 32):

```python
    def format(self, record: logging.LogRecord) -> str:
        """Render `record` as a single line."""
        timestamp = datetime.fromtimestamp(record.created, tz=UTC).isoformat(timespec="milliseconds")
        parts = [
            f"ts={timestamp}",
            f"level={record.levelname}",
            f"logger={record.name}",
            f"msg={_quote(record.getMessage())}",
        ]
        parts.extend(f"{key}={_quote(value)}" for key, value in getattr(record, "fields", {}).items())
        if record.exc_info:
            parts.append(f"exc={_quote(self.formatException(record.exc_info))}")
        return " ".join(parts)
```

- line 21: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 22: stores the result of calling `datetime.fromtimestamp(record.created, tz=UTC).isoformat` with 1 argument(s) in `timestamp`.
- line 23: stores `[f'ts={timestamp}', f'level={record.levelname}', f'logger={record.name}', f'msg={_quote(record.getMessage())}']` in `parts`.
- line 29: runs `parts.extend((f'{key}={_quote(value)}' for key, value in getattr(record, 'fields', {}).items()))`; the result is not kept.
- line 30: if `record.exc_info` is true:
  - line 31: runs `parts.append(f'exc={_quote(self.formatException(record.exc_info))}')`; the result is not kept.
- line 32: ends the function and gives back the result of calling `' '.join` with 1 argument(s).

**`configure_logging`**: Send every log record to `stream` (standard error by default) as logfmt. Safe to call twice. (lines 35 to 41):

```python
def configure_logging(level: str, stream: TextIO | None = None) -> None:
    """Send every log record to `stream` (standard error by default) as logfmt. Safe to call twice."""
    handler = logging.StreamHandler(stream or sys.stderr)
    handler.setFormatter(LogfmtFormatter())
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)
```

- line 36: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 37: stores the result of calling `logging.StreamHandler` with 1 argument(s) in `handler`.
- line 38: runs `handler.setFormatter(LogfmtFormatter())`; the result is not kept.
- line 39: stores the result of calling `logging.getLogger` in `root`.
- line 40: stores `[handler]` in `root.handlers[:]`.
- line 41: runs `root.setLevel(level)`; the result is not kept.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Peak memory of a run, measured with `tracemalloc`."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 5):

```python
from __future__ import annotations

import tracemalloc
```

class `TracemallocMeter`: Measures the peak of Python-level allocations, which is what should stay flat as the file grows. (lines 8 to 12):

```python
class TracemallocMeter:
    """Measures the peak of Python-level allocations, which is what should stay flat as the file grows.

    Tracing slows the run by a few times, so the command-line tool measures only when asked to (`--stats`).
    """
```

- line 9: the docstring: text that describes this piece; Python keeps it but does not run it.

**`TracemallocMeter.start`**: Start tracing and reset the peak. (lines 14 to 17):

```python
    def start(self) -> None:
        """Start tracing and reset the peak."""
        tracemalloc.start()
        tracemalloc.reset_peak()
```

- line 15: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 16: runs `tracemalloc.start()`; the result is not kept.
- line 17: runs `tracemalloc.reset_peak()`; the result is not kept.

**`TracemallocMeter.stop`**: Stop tracing and return the peak, in bytes, since `start`. (lines 19 to 23):

```python
    def stop(self) -> int:
        """Stop tracing and return the peak, in bytes, since `start`."""
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak
```

- line 20: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 21: stores the result of calling `tracemalloc.get_traced_memory` in `(_, peak)`.
- line 22: runs `tracemalloc.stop()`; the result is not kept.
- line 23: ends the function and gives back `peak`.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Writes the sample logs the lesson asks for: 500,000 lines with a few hundred planted bad ones, and a tiny log."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 7):

```python
from __future__ import annotations

import random
from itertools import cycle
from pathlib import Path
```

Module-level statements (lines 9 to 17):

```python
PATHS = ("/orders/1234", "/cart", "/users/42", "/health", "/search")
STATUSES = (200, 200, 200, 404, 500)
_TIMESTAMP = "2026-03-14T09:26:53Z"
_BAD_LINES_BY_KIND = (
    f"{_TIMESTAMP} GET /orders/1234 200",  # one field short
    f"{_TIMESTAMP} GET /orders/1234 200 abcms",  # latency that is not a number
    "",  # an empty line
)
_FLUSH_EVERY = 10_000
```

- line 9: stores `('/orders/1234', '/cart', '/users/42', '/health', '/search')` in `PATHS`.
- line 10: stores `(200, 200, 200, 404, 500)` in `STATUSES`.
- line 11: stores `'2026-03-14T09:26:53Z'` in `_TIMESTAMP`.
- line 12: stores `(f'{_TIMESTAMP} GET /orders/1234 200', f'{_TIMESTAMP} GET /orders/1234 200 abcms', '')` in `_BAD_LINES_BY_KIND`.
- line 17: stores `10000` in `_FLUSH_EVERY`.

**`write_sample_log`**: Write `lines` lines to `path`, `bad_lines` of them malformed (the three kinds in turn), in one pass. (lines 20 to 40):

```python
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
```

- line 21: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 25: if `not 0 <= bad_lines <= lines` is true:
  - line 26: raises (throws) the error `ValueError(f'bad_lines must be between 0 and lines, got {bad_lines} of {lines}')`.
- line 27: stores the result of calling `dict` with 1 argument(s) in `bad_at`.
- line 28: opens (`with`) `path.open('w', encoding='utf-8')` as `handle`; whatever it holds is released when the block ends, also after an error:
  - line 29: declares `batch` with the type `list[str]` and stores `[]` in it.
  - line 30: for each item of `range(lines)`, with the item called `index`:
    - line 31: if `index in bad_at` is true:
      - line 32: runs `batch.append(bad_at[index])`; the result is not kept.
    - otherwise:
      - line 34: stores the result of calling `rng.randint` with 2 argument(s) in `latency`.
      - line 35: runs `batch.append(f'{_TIMESTAMP} GET {rng.choice(PATHS)} {rng.choice(STATUSES)} {latency}ms')`; the result is not kept.
    - line 36: if `len(batch) == _FLUSH_EVERY` is true:
      - line 37: runs `handle.write('\n'.join(batch) + '\n')`; the result is not kept.
      - line 38: runs `batch.clear()`; the result is not kept.
  - line 39: if `batch` is true:
    - line 40: runs `handle.write('\n'.join(batch) + '\n')`; the result is not kept.

**`write_small_log`**: Write 20 lines of one path with latencies 1ms to 20ms, whose 95th percentile (19.95) is checked by hand. (lines 43 to 47):

```python
def write_small_log(path: Path) -> None:
    """Write 20 lines of one path with latencies 1ms to 20ms, whose 95th percentile (19.95) is checked by hand."""
    path.write_text(
        "".join(f"{_TIMESTAMP} GET /orders/1234 200 {latency}ms\n" for latency in range(1, 21)), encoding="utf-8"
    )
```

- line 44: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 45: runs `path.write_text(''.join((f'{_TIMESTAMP} GET /orders/1234 200 {latency}ms\n' for latency in range(1, 21))), encoding='utf-8')`; the result is not kept.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Configuration from the environment (twelve-factor), validated once, with defaults that work."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 10):

```python
from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, get_args

from logsum.domain.errors import InvalidSettingError
```

Module-level statements (lines 12 to 13):

```python
Estimator = Literal["exact", "histogram"]
ESTIMATORS: tuple[str, ...] = get_args(Estimator)
```

- line 12: stores `Literal['exact', 'histogram']` in `Estimator`.
- line 13: declares `ESTIMATORS` with the type `tuple[str, ...]` and stores the result of calling `get_args` with 1 argument(s) in it.

**`_integer`**: reads one setting from the environment (a dictionary of text values) as a whole number: returns `default` when the variable is missing or empty, and raises `InvalidSettingError` (naming the variable and the bad value) when the text is not a whole number (lines 16 to 23):

```python
def _integer(environ: Mapping[str, str], name: str, default: int) -> int:
    raw = environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        raise InvalidSettingError(f"{name} must be a whole number, got {raw!r}") from None
```

- line 17: stores the result of calling `environ.get` with 1 argument(s) in `raw`.
- line 18: if `raw is None or raw == ''` is true:
  - line 19: ends the function and gives back `default`.
- line 20: tries the block below; an error inside it goes to the matching `except`:
  - line 21: ends the function and gives back the result of calling `int` with 1 argument(s).
- line 22: if the error is `ValueError`:
  - line 23: raises (throws) the error `InvalidSettingError(f'{name} must be a whole number, got {raw!r}')`, with the earlier error hidden (`from None`).

class `Settings`: Every tunable of the program. Command-line flags override these; these override the defaults. (lines 26 to 34):

```python
@dataclass(frozen=True, slots=True)
class Settings:
    """Every tunable of the program. Command-line flags override these; these override the defaults."""

    log_level: str = "WARNING"
    top: int = 10
    estimator: Estimator = "exact"
    bucket_ms: int = 5
    max_latency_ms: int = 10_000
```

- line 26: the decorator `dataclass(frozen=True, slots=True)` wraps or registers what is defined just below it.
- line 28: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 30: declares `log_level` with the type `str` and stores `'WARNING'` in it.
- line 31: declares `top` with the type `int` and stores `10` in it.
- line 32: declares `estimator` with the type `Estimator` and stores `'exact'` in it.
- line 33: declares `bucket_ms` with the type `int` and stores `5` in it.
- line 34: declares `max_latency_ms` with the type `int` and stores `10000` in it.

**`Settings.__post_init__`**: runs right after the generated `__init__` and checks the fields (lines 36 to 48):

```python
    def __post_init__(self) -> None:
        if logging.getLevelName(self.log_level.upper()) == f"Level {self.log_level.upper()}":
            raise InvalidSettingError(
                f"log level must be DEBUG, INFO, WARNING, ERROR or CRITICAL, got {self.log_level!r}"
            )
        if self.top < 1:
            raise InvalidSettingError(f"top must be at least 1, got {self.top}")
        if self.estimator not in ESTIMATORS:
            raise InvalidSettingError(f"estimator must be one of {', '.join(ESTIMATORS)}, got {self.estimator!r}")
        if self.bucket_ms < 1 or self.max_latency_ms < self.bucket_ms:
            raise InvalidSettingError(
                f"need 1 <= bucket_ms <= max_latency_ms, got {self.bucket_ms} and {self.max_latency_ms}"
            )
```

- line 37: if `logging.getLevelName(self.log_level.upper()) == f'Level {self.log_level.upper()}'` is true:
  - line 38: raises (throws) the error `InvalidSettingError(f'log level must be DEBUG, INFO, WARNING, ERROR or CRITICAL, got {self.log_level!r}')`.
- line 41: if `self.top < 1` is true:
  - line 42: raises (throws) the error `InvalidSettingError(f'top must be at least 1, got {self.top}')`.
- line 43: if `self.estimator not in ESTIMATORS` is true:
  - line 44: raises (throws) the error `InvalidSettingError(f"estimator must be one of {', '.join(ESTIMATORS)}, got {self.estimator!r}")`.
- line 45: if `self.bucket_ms < 1 or self.max_latency_ms < self.bucket_ms` is true:
  - line 46: raises (throws) the error `InvalidSettingError(f'need 1 <= bucket_ms <= max_latency_ms, got {self.bucket_ms} and {self.max_latency_ms}')`.

**`Settings.from_environ`**: Read `LOGSUM_LOG_LEVEL`, `LOGSUM_TOP`, `LOGSUM_ESTIMATOR`, `LOGSUM_BUCKET_MS`, `LOGSUM_MAX_LATENCY_MS`. (lines 50 to 60):

```python
    @classmethod
    def from_environ(cls, environ: Mapping[str, str]) -> Settings:
        """Read `LOGSUM_LOG_LEVEL`, `LOGSUM_TOP`, `LOGSUM_ESTIMATOR`, `LOGSUM_BUCKET_MS`, `LOGSUM_MAX_LATENCY_MS`."""
        defaults = cls()
        return cls(
            log_level=environ.get("LOGSUM_LOG_LEVEL") or defaults.log_level,
            top=_integer(environ, "LOGSUM_TOP", defaults.top),
            estimator=environ.get("LOGSUM_ESTIMATOR") or defaults.estimator,  # type: ignore[arg-type]
            bucket_ms=_integer(environ, "LOGSUM_BUCKET_MS", defaults.bucket_ms),
            max_latency_ms=_integer(environ, "LOGSUM_MAX_LATENCY_MS", defaults.max_latency_ms),
        )
```

- line 50: the decorator `classmethod` wraps or registers what is defined just below it.
- line 52: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 53: stores the result of calling `cls` in `defaults`.
- line 54: ends the function and gives back the result of calling `cls` with 5 argument(s).

#### `src/logsum/interfaces/__init__.py` (1 lines)

Purpose: The command-line programs. They wire adapters into the use case and own argument parsing and exit codes.

Imports:

This file has no imports.

What the file defines, in order:

This file defines no functions, classes or constants.

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""The command-line programs. They wire adapters into the use case and own argument parsing and exit codes."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""`logsum`: summarize an access log from the command line."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 21):

```python
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
```

Module-level statements (lines 23 to 28):

```python
logger = logging.getLogger(__name__)

EXIT_OK = 0
EXIT_UNREADABLE = 1
EXIT_USAGE = 2
EXIT_INTERRUPTED = 130
```

- line 23: stores the result of calling `logging.getLogger` with 1 argument(s) in `logger`.
- line 25: stores `0` in `EXIT_OK`.
- line 26: stores `1` in `EXIT_UNREADABLE`.
- line 27: stores `2` in `EXIT_USAGE`.
- line 28: stores `130` in `EXIT_INTERRUPTED`.

**`distribution_factory`**: The distribution each path gets: every latency in a list, or fixed-size buckets. (lines 31 to 35):

```python
def distribution_factory(settings: Settings) -> Callable[[], LatencyDistribution]:
    """The distribution each path gets: every latency in a list, or fixed-size buckets."""
    if settings.estimator == "histogram":
        return lambda: HistogramLatencies(settings.bucket_ms, settings.max_latency_ms)
    return ExactLatencies
```

- line 32: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 33: if `settings.estimator == 'histogram'` is true:
  - line 34: ends the function and gives back a small unnamed function (`lambda`).
- line 35: ends the function and gives back `ExactLatencies`.

**`build_parser`**: The argument parser, with the environment's settings as its defaults. (lines 38 to 68):

```python
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
```

- line 39: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 40: stores the result of calling `argparse.ArgumentParser` with 2 argument(s) in `parser`.
- line 46: runs `parser.add_argument('log', help='path to the access log (plain text or .gz)')`; the result is not kept.
- line 47: runs `parser.add_argument('--top', type=int, default=defaults.top, help='how many slow paths to list (default: %(default)s)')`; the result is not kept.
- line 50: runs `parser.add_argument('--json', action='store_true', help='print the summary as JSON (docs/summary.schema.json)')`; the result is not kept.
- line 51: runs `parser.add_argument('--stats', action='store_true', help='also report elapsed time and peak memory (slows the run)')`; the result is not kept.
- line 52: runs `parser.add_argument('--estimator', choices=ESTIMATORS, default=defaults.estimator, help='exact keeps every latency; histogram keeps fixed-size buck...`; the result is not kept.
- line 58: runs `parser.add_argument('--bucket-ms', type=int, default=defaults.bucket_ms, help='histogram bucket width (default: %(default)s)')`; the result is not kept.
- line 61: runs `parser.add_argument('--max-latency-ms', type=int, default=defaults.max_latency_ms, help='histogram cap (default: %(default)s)')`; the result is not kept.
- line 64: runs `parser.add_argument('--log-level', default=defaults.log_level, help='log level on standard error (default: %(default)s)')`; the result is not kept.
- line 67: runs `parser.add_argument('--version', action='version', version=f'%(prog)s {__version__}')`; the result is not kept.
- line 68: ends the function and gives back `parser`.

**`main`**: Run the command and return its exit code: 0 done, 1 unreadable file, 2 bad arguments or settings. (lines 71 to 112):

```python
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
```

- line 78: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 79: stores `stdout or sys.stdout` in `out`.
- line 80: stores `stderr or sys.stderr` in `err`.
- line 81: tries the block below; an error inside it goes to the matching `except`:
  - line 82: stores the result of calling `Settings.from_environ` with 1 argument(s) in `defaults`.
  - line 83: stores the result of calling `build_parser(defaults).parse_args` with 1 argument(s) in `arguments`.
  - line 84: stores the result of calling `Settings` with 5 argument(s) in `settings`.
- line 91: if the error is `InvalidSettingError` (the error is called `error`):
  - line 92: runs `print(f'logsum: {error}', file=err)`; the result is not kept.
  - line 93: ends the function and gives back `EXIT_USAGE`.
- line 95: runs `configure_logging(settings.log_level, err)`; the result is not kept.
- line 96: stores the result of calling `SummarizeLog` with 4 argument(s) in `use_case`.
- line 102: tries the block below; an error inside it goes to the matching `except`:
  - line 103: stores the result of calling `use_case.run` with 2 argument(s) in `report`.
- line 104: if the error is `UnreadableLogFileError` (the error is called `error`):
  - line 105: runs `logger.error('cannot read the log', extra={'fields': {'location': error.location, 'reason': error.reason}})`; the result is not kept.
  - line 106: runs `print(f'logsum: {error}', file=err)`; the result is not kept.
  - line 107: ends the function and gives back `EXIT_UNREADABLE`.
- line 108: if `arguments.json` is true:
  - line 109: runs `print(render_json(report, show_stats=arguments.stats), file=out)`; the result is not kept.
- otherwise:
  - line 111: runs `print(render_text(report, top=settings.top, show_stats=arguments.stats), file=out)`; the result is not kept.
- line 112: ends the function and gives back `EXIT_OK`.

**`entrypoint`**: The installed command: `main` plus the two ways a command-line tool ends early, Ctrl-C and a closed pipe. (lines 115 to 127):

```python
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
```

- line 116: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 117: tries the block below; an error inside it goes to the matching `except`:
  - line 118: stores the result of calling `main` in `code`.
  - line 119: runs `sys.stdout.flush()`; the result is not kept.
  - line 120: ends the function and gives back `code`.
- line 121: if the error is `KeyboardInterrupt`:
  - line 122: runs `print('logsum: interrupted', file=sys.stderr)`; the result is not kept.
  - line 123: ends the function and gives back `EXIT_INTERRUPTED`.
- line 124: if the error is `BrokenPipeError`:
  - line 126: runs `os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())`; the result is not kept.
  - line 127: ends the function and gives back `EXIT_OK`.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""`logsum-make-log`: write the sample logs the lesson starts from."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 11):

```python
from __future__ import annotations

import argparse
import random
import sys
from collections.abc import Sequence
from pathlib import Path

from logsum.infrastructure.sample_log import write_sample_log, write_small_log
```

**`main`**: Write a sample log and report what it holds. The same seed always gives the same file. (lines 14 to 35):

```python
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
```

- line 15: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 16: stores the result of calling `argparse.ArgumentParser` with 2 argument(s) in `parser`.
- line 17: runs `parser.add_argument('output', type=Path, help='file to write')`; the result is not kept.
- line 18: runs `parser.add_argument('--lines', type=int, default=500000, help='total lines (default: %(default)s)')`; the result is not kept.
- line 19: runs `parser.add_argument('--bad', type=int, default=300, help='malformed lines among them (default: %(default)s)')`; the result is not kept.
- line 20: runs `parser.add_argument('--seed', type=int, default=7, help='random seed (default: %(default)s)')`; the result is not kept.
- line 21: runs `parser.add_argument('--small', action='store_true', help='write the 20-line log whose p95 is 19.95 instead')`; the result is not kept.
- line 22: stores the result of calling `parser.parse_args` with 1 argument(s) in `arguments`.
- line 23: if `arguments.small` is true:
  - line 24: runs `write_small_log(arguments.output)`; the result is not kept.
  - line 25: runs `print(f'wrote 20 lines (0 bad) to {arguments.output}')`; the result is not kept.
  - line 26: ends the function and gives back `0`.
- line 27: tries the block below; an error inside it goes to the matching `except`:
  - line 28: runs `write_sample_log(arguments.output, lines=arguments.lines, bad_lines=arguments.bad, rng=random.Random(arguments.seed))`; the result is not kept.
- line 31: if the error is `ValueError` (the error is called `error`):
  - line 32: runs `print(f'logsum-make-log: {error}', file=sys.stderr)`; the result is not kept.
  - line 33: ends the function and gives back `2`.
- line 34: runs `print(f'wrote {arguments.lines} lines ({arguments.bad} bad) to {arguments.output}')`; the result is not kept.
- line 35: ends the function and gives back `0`.

**`entrypoint`**: The installed command. (lines 38 to 40):

```python
def entrypoint() -> int:
    """The installed command."""
    return main()
```

- line 39: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 40: ends the function and gives back the result of calling `main`.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (line 1):

```python
"""Turns a run report into text or JSON. Output goes to standard output; logs go to standard error."""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 3 to 7):

```python
from __future__ import annotations

import json

from logsum.application.summarize import RunReport
```

Module-level statements (line 9):

```python
_BYTES_PER_MEGABYTE = 1024 * 1024
```

- line 9: stores `1024 * 1024` in `_BYTES_PER_MEGABYTE`.

**`render_text`**: The human-readable summary: statuses, the slowest paths, the bad-line count, and optionally the run's cost. (lines 12 to 23):

```python
def render_text(report: RunReport, *, top: int, show_stats: bool) -> str:
    """The human-readable summary: statuses, the slowest paths, the bad-line count, and optionally the run's cost."""
    summary = report.summary
    statuses = ", ".join(f"{status}: {count}" for status, count in summary.status_counts.items())
    lines = [f"statuses: {{{statuses}}}", f"slowest paths by p95 latency in ms (top {top}):"]
    lines.extend(
        f"  {entry.p95_ms:>8.2f}  {entry.path}  ({entry.requests} requests)" for entry in summary.slowest_paths
    )
    lines.append(f"bad lines: {summary.bad_lines}")
    if show_stats:
        lines.append(_stats_line(report))
    return "\n".join(lines)
```

- line 13: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 14: stores `report.summary` in `summary`.
- line 15: stores the result of calling `', '.join` with 1 argument(s) in `statuses`.
- line 16: stores `[f'statuses: {{{statuses}}}', f'slowest paths by p95 latency in ms (top {top}):']` in `lines`.
- line 17: runs `lines.extend((f' {entry.p95_ms:>8.2f} {entry.path} ({entry.requests} requests)' for entry in summary.slowest_paths))`; the result is not kept.
- line 20: runs `lines.append(f'bad lines: {summary.bad_lines}')`; the result is not kept.
- line 21: if `show_stats` is true:
  - line 22: runs `lines.append(_stats_line(report))`; the result is not kept.
- line 23: ends the function and gives back the result of calling `'\n'.join` with 1 argument(s).

**`render_json`**: The same summary as JSON, described by docs/summary.schema.json. (lines 26 to 43):

```python
def render_json(report: RunReport, *, show_stats: bool) -> str:
    """The same summary as JSON, described by docs/summary.schema.json."""
    summary = report.summary
    document: dict[str, object] = {
        "total_requests": summary.total_requests,
        "bad_lines": summary.bad_lines,
        "statuses": {str(status): count for status, count in summary.status_counts.items()},
        "slowest_paths": [
            {"path": entry.path, "p95_ms": round(entry.p95_ms, 2), "requests": entry.requests}
            for entry in summary.slowest_paths
        ],
    }
    if show_stats:
        document["stats"] = {
            "elapsed_seconds": round(report.elapsed_seconds, 3),
            "peak_memory_bytes": report.peak_memory_bytes,
        }
    return json.dumps(document, indent=2)
```

- line 27: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 28: stores `report.summary` in `summary`.
- line 29: declares `document` with the type `dict[str, object]` and stores `{'total_requests': summary.total_requests, 'bad_lines': summary.bad_lines, 'statuses': {str(status): count for status, count in summary.status_coun...` in it.
- line 38: if `show_stats` is true:
  - line 39: stores `{'elapsed_seconds': round(report.elapsed_seconds, 3), 'peak_memory_bytes': report.peak_memory_bytes}` in `document['stats']`.
- line 43: ends the function and gives back the result of calling `json.dumps` with 2 argument(s).

**`_stats_line`**: builds the last line of the text report: the elapsed seconds with two decimals and the peak memory in megabytes with one decimal, or `n/a` when memory was not measured (lines 46 to 48):

```python
def _stats_line(report: RunReport) -> str:
    peak = "n/a" if report.peak_memory_bytes is None else f"{report.peak_memory_bytes / _BYTES_PER_MEGABYTE:.1f} MB"
    return f"elapsed: {report.elapsed_seconds:.2f}s  peak memory: {peak}"
```

- line 47: stores `'n/a'` if `report.peak_memory_bytes is None`, otherwise `f'{report.peak_memory_bytes / _BYTES_PER_MEGABYTE:.1f} MB'` in `peak`.
- line 48: ends the function and gives back an f-string: text with the values inside `{}` filled in.

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

Source in full, in pieces, each followed by what its statements do:

Module-level statements (lines 1 to 5):

```python
"""The failure mode the lesson names: reading the whole file into a list.

Prints the peak memory of summarizing a log by streaming it and by loading every line first, for the whole
file and for a tenth of it. Streaming stays flat; loading grows with the file.
"""
```

- line 1: the docstring: text that describes this piece; Python keeps it but does not run it.

The imports (each one is explained in the import table above) (lines 7 to 16):

```python
from __future__ import annotations

import sys
import tempfile
import tracemalloc
from collections.abc import Callable
from itertools import islice
from pathlib import Path

from logsum.application.summarize import BadLineCounter, stream_requests
```

**`streaming`**: Count the requests, holding one line at a time. (lines 19 to 22):

```python
def streaming(path: Path) -> int:
    """Count the requests, holding one line at a time."""
    with path.open(encoding="utf-8") as handle:
        return sum(1 for _ in stream_requests(handle, BadLineCounter()))
```

- line 20: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 21: opens (`with`) `path.open(encoding='utf-8')` as `handle`; whatever it holds is released when the block ends, also after an error:
  - line 22: ends the function and gives back the result of calling `sum` with 1 argument(s).

**`loading_everything`**: Count the requests after loading every line into a list. (lines 25 to 29):

```python
def loading_everything(path: Path) -> int:
    """Count the requests after loading every line into a list."""
    with path.open(encoding="utf-8") as handle:
        lines = handle.readlines()  # every line held at once: the mistake
    return sum(1 for _ in stream_requests(lines, BadLineCounter()))
```

- line 26: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 27: opens (`with`) `path.open(encoding='utf-8')` as `handle`; whatever it holds is released when the block ends, also after an error:
  - line 28: stores the result of calling `handle.readlines` in `lines`.
- line 29: ends the function and gives back the result of calling `sum` with 1 argument(s).

**`peak_megabytes`**: Peak traced memory of `work(path)`, in megabytes. (lines 32 to 38):

```python
def peak_megabytes(work: Callable[[Path], int], path: Path) -> float:
    """Peak traced memory of `work(path)`, in megabytes."""
    tracemalloc.start()
    work(path)
    _, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak / (1024 * 1024)
```

- line 33: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 34: runs `tracemalloc.start()`; the result is not kept.
- line 35: runs `work(path)`; the result is not kept.
- line 36: stores the result of calling `tracemalloc.get_traced_memory` in `(_, peak)`.
- line 37: runs `tracemalloc.stop()`; the result is not kept.
- line 38: ends the function and gives back `peak / (1024 * 1024)`.

**`main`**: Print the comparison for the whole log and for a tenth of it. (lines 41 to 52):

```python
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
```

- line 42: the docstring: text that describes this piece; Python keeps it but does not run it.
- line 43: opens (`with`) `log.open(encoding='utf-8')` as `source`; whatever it holds is released when the block ends, also after an error:
  - line 44: stores the result of calling `sum` with 1 argument(s) in `total`.
- line 45: opens (`with`) `tempfile.TemporaryDirectory()` as `folder`; whatever it holds is released when the block ends, also after an error:
  - line 46: stores `Path(folder) / 'tenth.log'` in `tenth`.
  - line 47: opens (`with`) `log.open(encoding='utf-8')` as `source`; whatever it holds is released when the block ends, also after an error:
    - line 48: runs `tenth.write_text(''.join(islice(source, total // 10)), encoding='utf-8')`; the result is not kept.
  - line 49: runs `print(f"{'lines':>10} {'streaming':>10} {'readlines':>10} (peak traced memory, MB)")`; the result is not kept.
  - line 50: for each item of `((tenth, total // 10), (log, total))`, with the item called `(path, lines)`:
    - line 51: stores `(peak_megabytes(streaming, path), peak_megabytes(loading_everything, path))` in `(streamed, loaded)`.
    - line 52: runs `print(f'{lines:>10} {streamed:>10.1f} {loaded:>10.1f}')`; the result is not kept.

Module-level statements (lines 55 to 56):

```python
if __name__ == "__main__":
    main(Path(sys.argv[1]))
```

- line 55: if `__name__ == '__main__'` is true:
  - line 56: runs `main(Path(sys.argv[1]))`; the result is not kept.

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
