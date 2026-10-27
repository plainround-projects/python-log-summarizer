# tracemalloc and measuring memory

<!-- fmt:off -->

## What it is

**Memory** is where a running program keeps its data. **`tracemalloc`** is a standard-library module that records every piece of memory Python allocates for objects, so a program can ask "how much did I use at the most, and which line asked for it?". The highest amount used is the **peak**.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- A **redirection** sends a channel somewhere else. `> file` writes standard output to a file, `2>&1` sends standard error to wherever standard output goes, and `/dev/null` is a special file that throws away whatever is written to it.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- A **process** is one running program, with its own memory and a number, its **process id** or **PID**. A program can start other processes, its **children**, and wait for them or stop them.
- A **port** is a number (0 to 65535) that tells the computer which program on this machine should receive a network message. **localhost**, the address `127.0.0.1`, always means this same computer, so a server on port 8000 is reached at `http://localhost:8000`.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- The **interpreter** is the program that reads Python source files and carries them out. `python` starts it. **CPython** is the standard one, written in C.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.

## Why this repository uses it

The lesson's third step: on the 500,000-line file, peak memory must stay under 50 MB, "measured with `tracemalloc` or `/usr/bin/time`". Streaming should use the same memory for 5 GB as for 5 MB; the measurement is the proof.

## Where it appears

| File | What it does with it |
| --- | --- |
| `src/logsum/infrastructure/memory.py` | `TracemallocMeter`. |
| `src/logsum/application/ports.py` | `MemoryMeter`, the interface the use case sees. |
| `src/logsum/interfaces/cli.py` | `--stats` switches the meter on. |
| `scripts/compare_memory.py` | streaming against `readlines()`. |
| `tests/e2e/test_lesson_scenario.py` | asserts the peak is under 50 MB and does not grow with the file. |

## How it works underneath

When tracing is on, Python wraps its memory allocator: each allocation is recorded with a traceback and each free removes the record. `get_traced_memory()` returns `(current, peak)` in bytes. Tracing slows the program by a few times (each allocation does extra work), so it is optional (`--stats`). It sees only memory allocated through Python's allocator, not the interpreter's own baseline (about 15 MB) or memory a C library allocates itself. That is why this repository also reports the process's **resident set size** (RSS), the memory the operating system has actually given the process, from `/usr/bin/time -l` (macOS) or `-v` (Linux), and expects it to be larger.

## Walkthrough of this repository's use

```python
"""Peak memory of a run, measured with `tracemalloc`."""

from __future__ import annotations

import tracemalloc


class TracemallocMeter:
    """Measures the peak of Python-level allocations, which is what should stay flat as the file grows.

    Tracing slows the run by a few times, so the command-line tool measures only when asked to (`--stats`).
    """

    def start(self) -> None:
        """Start tracing and reset the peak."""
        tracemalloc.start()
        tracemalloc.reset_peak()

    def stop(self) -> int:
        """Stop tracing and return the peak, in bytes, since `start`."""
        _, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return peak
```
(`src/logsum/infrastructure/memory.py`, lines 1 to 23)

- `tracemalloc.start()` begins recording; `tracemalloc.reset_peak()` sets the peak to the current level, so a second run in the same process does not inherit an earlier peak.
- `stop()` reads `(current, peak)` and keeps only `peak`, stops tracing (so the slow-down ends) and returns the peak in bytes.

```python
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
```
(`src/logsum/application/summarize.py`, lines 70 to 79)

The use case starts the meter before opening the file and stops it in `finally`, so the meter is switched off even if reading fails. The meter is optional (`None` when `--stats` is absent), and the use case only knows the `MemoryMeter` port.

```python
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
```
(`scripts/compare_memory.py`, lines 19 to 32)

`scripts/compare_memory.py` shows the failure the lesson warns about: `handle.readlines()` loads every line at once.

## Try it yourself

```bash
make demo-memory
```
Expected (after `make up`): a table with `streaming` near 0.1 MB for both a tenth of the log and the whole log, and `readlines` growing from about 4.6 MB to about 44 MB.

```bash
uv run --frozen logsum data/sample.log --stats | tail -1
```
Expected: `elapsed: ...s  peak memory: 4.0 MB`.

```bash
/usr/bin/time -l uv run --frozen logsum data/sample.log 2>&1 | grep "maximum resident"
```
Expected on macOS: a number of bytes (about 30,000,000 to 36,000,000): resident memory including the interpreter, still under 50 MB. (On Linux use `/usr/bin/time -v` and read `Maximum resident set size`.)

## Mistakes people make

- **Measuring with tracing on and reading the time as the real speed.** Tracing makes the run slower; time without `--stats`.
- **Comparing traced memory with resident memory.** They count different things.
- **Forgetting `reset_peak`** and reporting an earlier run's peak.
- **Leaving tracing on.** It slows everything after it.

## Check yourself

**1. What is a peak?**
The highest amount of memory in use at any moment of the run.

**2. Why is the memory meter optional?**
Tracing slows the program by a few times, so it only runs with `--stats`.

**3. Why can resident memory be larger than the traced peak?**
It includes the interpreter itself and memory not allocated through Python's allocator.

**4. Why does `stop` run in a `finally` block?**
So tracing is switched off even if reading the file fails.

**5. What does `make demo-memory` demonstrate?**
That streaming uses the same memory for a tenth of the file and for all of it, while `readlines()` grows with the file.

## Further reading

- `tracemalloc`: https://docs.python.org/3.14/library/tracemalloc.html
- `time(1)`: `man time` on your system.
