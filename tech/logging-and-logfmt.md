# Python `logging` and the logfmt format

<!-- fmt:off -->

## What it is

**Logging** is a program writing short lines about what it is doing, so a person can find out later what happened. Python's standard library has a `logging` module for this: code asks for a **logger**, calls `logger.info("message")`, and the module sends a **record** to **handlers** that decide where it goes (the screen, a file). Every record has a **level**: DEBUG, INFO, WARNING, ERROR or CRITICAL. A program shows only records at or above the level it is set to. **logfmt** is a line format of `key=value` pairs, readable by people and easy for tools to split.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- A program has three channels: **standard input** (what it reads), **standard output** (what it prints normally) and **standard error** (where it prints problems and progress). They are separate so a pipe or a file can take the output while errors still show on the screen.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- A **process** is one running program, with its own memory and a number, its **process id** or **PID**. A program can start other processes, its **children**, and wait for them or stop them.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- **JSON** is a text format for data: objects `{"name": "x", "count": 3}` (names with values), lists `[1, 2, 3]`, text in double quotes, numbers, `true`, `false` and `null`. Almost every language can read and write it, which makes it the usual way programs exchange data.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- An **entry point** (or **console script**) is a command, such as `logsum`, that the installer creates and that starts a named Python function.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- A **linter** reads code without running it and reports likely mistakes and style problems. A **formatter** rewrites the layout of the code into one agreed style.

## Why this repository uses it

The template requires "structured logging with levels and no secrets in logs". Here every operational line is one logfmt line on standard error (`ts=... level=INFO logger=... msg=... key=value`), and results go to standard output, so a pipeline such as `program | jq` stays clean.

## Where it appears

| File | What it does with it |
| --- | --- |
| `src/logsum/infrastructure/logging.py` | the formatter and `configure_logging`. |
| `src/logsum/interfaces/cli.py` | `main` calls `configure_logging(settings.log_level, err)` once, after the arguments are read. |
| `src/logsum/application/summarize.py` | logs one INFO line when a run finishes, with `extra={'fields': {...}}`. |
| `src/logsum/interfaces/cli.py` | logs an ERROR line when the file cannot be read. |
| `tests/unit/infrastructure/test_logging.py` | tests for the line format and for configuring twice. |

## How it works underneath

`logging.getLogger(__name__)` returns a logger named after the module (for example `logsum.application.summarize`). Loggers form a tree by their dotted names; a record travels up to the **root logger**, where the handlers are. A **handler** (here a `StreamHandler` that writes to standard error) uses a **formatter** to turn the record into text. The module only builds the record when the level is enabled, so disabled debug lines cost almost nothing.

Extra data is attached with the `extra` argument: `logger.info("msg", extra={"fields": {"a": 1}})` stores a dictionary on the record under the attribute name `fields`, which the formatter reads. Standard output and standard error are two separate streams of a process; log lines go to the second, results to the first.

## Walkthrough of this repository's use

```python
"""Structured logging: one logfmt line per event (`ts=... level=... logger=... msg=... key=value`)."""

from __future__ import annotations

import json
import logging
import sys
from datetime import UTC, datetime
from typing import TextIO


def _quote(value: object) -> str:
    text = str(value)
    return json.dumps(text) if not text or any(char in text for char in ' ="\n') else text


class LogfmtFormatter(logging.Formatter):
    """Format a log record as one logfmt line, with the record's `fields` extra as key=value pairs."""

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


def configure_logging(level: str, stream: TextIO | None = None) -> None:
    """Send every log record to `stream` (standard error by default) as logfmt. Safe to call twice."""
    handler = logging.StreamHandler(stream or sys.stderr)
    handler.setFormatter(LogfmtFormatter())
    root = logging.getLogger()
    root.handlers[:] = [handler]
    root.setLevel(level)
```
(`src/logsum/infrastructure/logging.py`, lines 1 to 41)

- `from __future__ import annotations`: write type hints as text so forward references work (see `python.md`).
- `_quote(value)`: turns any value into text; a value that is empty or contains a space, `=`, a double quote or a newline is wrapped in JSON quotes (`json.dumps`), so `msg="two words"` stays one field and a line never breaks.
- `class LogfmtFormatter(logging.Formatter)`: a formatter that overrides `format`, which receives a `LogRecord` and returns the text.
- `record.created`: when the record was made, as seconds since 1970; `datetime.fromtimestamp(..., tz=UTC).isoformat(timespec="milliseconds")` makes `2026-10-27T03:11:25.135+00:00`.
- `parts`: the fixed fields in order: `ts`, `level`, `logger` (the logger's name), `msg` (`record.getMessage()` fills in any `%s` placeholders).
- `getattr(record, "fields", {})`: the `extra` data from the call, or an empty dictionary if none was given; every key becomes `key=value`.
- `record.exc_info`: set when an exception was logged; the traceback is added as one more field, with its newlines quoted, so the record stays one line.
- `configure_logging(level, stream)`: builds one `StreamHandler` writing to `stream` (default standard error), sets the formatter, then `root.handlers[:] = [handler]` replaces any existing handlers (so calling it twice does not print everything twice) and `root.setLevel(level)` sets the threshold.

Where it is called and with what default level (`WARNING`):
- `src/logsum/interfaces/cli.py`: `main` calls `configure_logging(settings.log_level, err)` once, after the arguments are read.
- `src/logsum/application/summarize.py`: logs one INFO line when a run finishes, with `extra={'fields': {...}}`.
- `src/logsum/interfaces/cli.py`: logs an ERROR line when the file cannot be read.

**Rules this module follows:** logs never contain secrets or personal data (only counts, paths, durations, names); a library function does not configure logging, the program's entry point does.

## Try it yourself

```bash
uv run --frozen python - <<'EOF'
import logging
from logsum.infrastructure.logging import configure_logging
configure_logging("INFO")
logging.getLogger("demo").info("hello world", extra={"fields": {"count": 3, "path": "a b"}})
EOF
```
Expected: one line on standard error like `ts=2026-... level=INFO logger=demo msg="hello world" count=3 path="a b"`.

```bash
uv run --frozen python -c "
import logging
from logsum.infrastructure.logging import configure_logging
configure_logging('WARNING')
logging.getLogger('demo').info('hidden')
logging.getLogger('demo').warning('shown')
"
```
Expected: only the `shown` line; the INFO record is below the threshold.

```bash
uv run --frozen pytest tests/unit/infrastructure/test_logging.py -q
```
Expected: `3 passed` (three tests).

## Mistakes people make

- **`print` for operational messages.** It cannot be filtered by level and mixes with the program's real output.
- **Configuring logging inside library code.** Only the entry point decides where logs go.
- **Building the message with an f-string in the call** (`logger.info(f"x={x}")`) when the level may be off: the string is built anyway. Use `extra` fields or `%s` placeholders.
- **Logging secrets or whole payloads.** Only identifiers and counts are logged here.
- **Adding a handler on every call.** `configure_logging` replaces the handlers instead of adding.

## Check yourself

**1. What is a log level for?**
To decide which records are shown: only records at or above the configured level.

**2. Why does this code put logs on standard error and results on standard output?**
So a program's results can be piped into another tool without log lines mixed in.

**3. What does `extra={"fields": {...}}` do?**
Attaches a dictionary to the record under the name `fields`; the formatter prints each key as `key=value`.

**4. Why does `_quote` wrap some values in quotes?**
A value with a space, `=`, a quote or a newline would break the one-line `key=value` format.

**5. Why does `configure_logging` assign `root.handlers[:] = [handler]` instead of calling `addHandler`?**
To replace existing handlers, so calling it twice does not print every line twice.

## Further reading

- Python 3.14 `logging` module: https://docs.python.org/3.14/library/logging.html and the Logging HOWTO https://docs.python.org/3.14/howto/logging.html
- logfmt, as described by the Brandur and Heroku logging conventions: https://brandur.org/logfmt
