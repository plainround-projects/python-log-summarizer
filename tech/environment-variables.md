# Environment variables and the `.env.example` file

<!-- fmt:off -->

## What it is

An **environment variable** is a named piece of text that the operating system hands to every program it starts, next to the program's command-line arguments. `PORT=9000` is a variable named `PORT` whose value is the text `9000`. A program cannot see the shell's own variables unless they are **exported**; when you write `PORT=9000 some-command` the shell gives that variable to that one command only. Inside a Python program the variables arrive as `os.environ`, which behaves like a dictionary from name to text. Everything in it is text: a number such as `9000` still has to be converted.

A **`.env` file** is a plain text file of `NAME=value` lines used to collect such variables in one place. It is a convention, not a feature of the operating system: some tool has to read the file and pass the variables on. A **`.env.example`** file is the copy that is committed to git: it lists the variable names with harmless sample values, so a new person knows what can be set. The real `.env` stays out of git because it may hold secrets (the `.gitignore` of this repository ignores it).

This is the **twelve-factor** way of configuring a program: the same code runs everywhere, and settings that differ between machines (a port, a path, a mode) come from the environment instead of being written into the code.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **terminal** is a window where you type a line of text, press Enter, and the computer runs it. The program that reads your line is the **shell** (here `zsh` or `bash`). Everything typed in a terminal is a **command**: a program's name followed by **arguments**, the words that tell it what to do.
- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A program has three channels: **standard input** (what it reads), **standard output** (what it prints normally) and **standard error** (where it prints problems and progress). They are separate so a pipe or a file can take the output while errors still show on the screen.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- A **process** is one running program, with its own memory and a number, its **process id** or **PID**. A program can start other processes, its **children**, and wait for them or stop them.
- A **port** is a number (0 to 65535) that tells the computer which program on this machine should receive a network message. **localhost**, the address `127.0.0.1`, always means this same computer, so a server on port 8000 is reached at `http://localhost:8000`.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- **Latency** is how long one request takes. A **percentile** says what share of requests were at least that fast: **p95** is the time that 95 out of 100 requests beat, so it shows how bad the slow tail is, which an average hides.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- A **dataclass** is a class whose fields are listed once with their types; Python then writes the constructor, the printed form and the equality check for you.

## Why this repository uses it

`logsum` has a few tunables (how many paths to list, which percentile method, how chatty to be). They are environment variables so that a person can set them once for a whole shell session or a scheduled job without retyping flags. Reading settings in exactly one place, `src/logsum/infrastructure/settings.py`, means the rest of the program receives one validated `Settings` object. A wrong value (a port of 70000, a word that is not one of the allowed modes) stops the program at start-up with a message that names the variable, instead of failing later in a confusing way.

## Where it appears

| File | What it does with it |
| --- | --- |
| `src/logsum/infrastructure/settings.py` | the `Settings` class: every variable, its default and its validation. |
| `.env.example` | a sample of the variable names a person can set. |
| `src/logsum/interfaces/cli.py` | `main` calls `Settings.from_environ(environ)`; the flags then override the result. |
| `tests/unit/infrastructure/test_settings.py` | tests of the defaults, the conversions and the error messages. |

## How it works underneath

When a program starts, the operating system copies a table of `NAME=value` text pairs into the new process. A child process inherits its parent's table unless the parent changes it; that is why `PORT=9000 make serve` works: the shell puts `PORT` in the table of `make`, and `make` passes its table on to the programs it starts.

Python exposes the table as `os.environ`. A missing name is simply absent from it, and a name set to nothing (`PORT=`) is present with an empty text, so a careful reader treats *missing* and *empty* the same way, as this code does. Values are always `str`; a number must be converted with `int(...)` or `float(...)`, and the conversion can fail, so it needs an error message that names the variable.

**Validation at the edge.** The settings class does three jobs in a fixed order: read the text, convert it, check the ranges. Doing all three in one place means a bad value is reported once, early, with the name of the variable.

**Precedence.** The docstring of `Settings` says it: command-line flags override the environment, and the environment overrides the built-in defaults. So `LOGSUM_TOP=3 logsum access.log` lists three paths, and `LOGSUM_TOP=3 logsum access.log --top 5` lists five.

**How the file is used here.** `logsum` does not read `.env` by itself. To use the sample, copy it to `.env` and export the variables in your shell (for example `set -a; . ./.env; set +a`, where `set -a` marks every variable assigned afterwards for export and `.` runs the file's lines in the current shell), or set a variable in front of one command.

## Walkthrough of this repository's use

The whole settings module:

```python
"""Configuration from the environment (twelve-factor), validated once, with defaults that work."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, get_args

from logsum.domain.errors import InvalidSettingError

Estimator = Literal["exact", "histogram"]
ESTIMATORS: tuple[str, ...] = get_args(Estimator)


def _integer(environ: Mapping[str, str], name: str, default: int) -> int:
    raw = environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        raise InvalidSettingError(f"{name} must be a whole number, got {raw!r}") from None


@dataclass(frozen=True, slots=True)
class Settings:
    """Every tunable of the program. Command-line flags override these; these override the defaults."""

    log_level: str = "WARNING"
    top: int = 10
    estimator: Estimator = "exact"
    bucket_ms: int = 5
    max_latency_ms: int = 10_000

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
(`src/logsum/infrastructure/settings.py`, lines 1 to 60)

- `Estimator = Literal["exact", "histogram"]` and `ESTIMATORS = get_args(Estimator)`: a *literal type* names the only allowed values; `get_args` reads them back as a tuple so the error message can list them.
- `_integer(environ, name, default)`: `environ.get(name)` is the text or `None`; a missing or empty value gives `default`; otherwise `int(raw)` converts, and a `ValueError` becomes `InvalidSettingError` that names the variable and shows the bad text with `!r` (the quoted form, so `'abc'` is visibly text). `from None` hides the original traceback, which would only repeat the same fact.
- `@dataclass(frozen=True, slots=True) class Settings`: five fields with their defaults. `frozen=True` makes the object unchangeable after creation; `slots=True` stores the fields compactly and rejects misspelled new attributes.
- `__post_init__`: runs after the generated constructor and refuses impossible combinations. `logging.getLevelName("FOO")` returns the text `Level FOO` for an unknown name, which is how the code detects a bad level; `top` must be at least 1; the estimator must be listed; and `1 <= bucket_ms <= max_latency_ms`.
- `from_environ(cls, environ)`: a *class method* (it receives the class, not an object) that builds a `Settings`. `defaults = cls()` creates an object with all defaults, so each default is written once, in the field list. `environ.get("LOGSUM_LOG_LEVEL") or defaults.log_level` uses the default when the variable is missing or empty. The `# type: ignore[arg-type]` on the estimator line tells mypy that a plain `str` is accepted there on purpose: the value is checked at run time in `__post_init__`.

The variables, found by reading `from_environ` with Python's own parser, so none is left out:

| Variable | Settings field | Read as | Default | What it controls |
| --- | --- | --- | --- | --- |
| `LOGSUM_LOG_LEVEL` | `log_level` | text (then checked in `__post_init__`) | `'WARNING'` | how much the program says about itself on standard error: `DEBUG`, `INFO`, `WARNING`, `ERROR` or `CRITICAL`; only records at or above this level are shown. |
| `LOGSUM_TOP` | `top` | whole number | `10` | how many slowest paths the report lists (at least 1). |
| `LOGSUM_ESTIMATOR` | `estimator` | text (then checked in `__post_init__`) | `'exact'` | how percentiles are computed: `exact` keeps every latency in memory; `histogram` counts latencies in fixed-size buckets and uses constant memory (see `statistics-percentiles.md`). |
| `LOGSUM_BUCKET_MS` | `bucket_ms` | whole number | `5` | the width in milliseconds of one histogram bucket (at least 1); used only by the `histogram` estimator. |
| `LOGSUM_MAX_LATENCY_MS` | `max_latency_ms` | whole number | `10000` | the largest latency the histogram tracks, in milliseconds (at least the bucket width); used only by the `histogram` estimator. |

## Try it yourself

```bash
LOGSUM_TOP=3 uv run --frozen logsum data/small.log | head -12
```
Expected: the report lists only three slowest paths instead of ten (the default).

```bash
LOGSUM_TOP=abc uv run --frozen logsum data/small.log; echo "exit code $?"
```
Expected: `logsum: LOGSUM_TOP must be a whole number, got 'abc'` and `exit code 2`.

```bash
uv run --frozen python - <<'EOF'
from logsum.infrastructure.settings import Settings
print(Settings.from_environ({"LOGSUM_TOP": "3", "LOGSUM_ESTIMATOR": "histogram"}))
try:
    Settings.from_environ({"LOGSUM_ESTIMATOR": "fast"})
except Exception as error:
    print(type(error).__name__, error)
EOF
```
Expected: `Settings(log_level='WARNING', top=3, estimator='histogram', bucket_ms=5, max_latency_ms=10000)` and then `InvalidSettingError estimator must be one of exact, histogram, got 'fast'`.

```bash
uv run --frozen pytest tests/unit/infrastructure/test_settings.py -q
```
Expected: all tests pass (`N passed`).

## Mistakes people make

- **Treating the value as a number.** `os.environ["PORT"]` is the text `"9000"`. Without conversion, `PORT + 1` is an error and `PORT == 9000` is false.
- **Forgetting that empty means missing here.** `PORT=` sets an empty value; this code uses the default, as if the variable were not set.
- **Reading `os.environ` all over the program.** Settings then become impossible to list and to test. Here only `Settings.from_environ` reads them, and tests pass an ordinary dictionary instead.
- **Committing `.env`.** It is ignored by git on purpose; only `.env.example` is committed.
- **Putting a real secret in `.env.example`.** The example file must contain only harmless sample values.
- **Expecting a change to apply to a running program.** The table is copied when a process starts; changing the variable later does not reach a process that is already running.

## Check yourself

**1. What is an environment variable?**
A named piece of text that a program inherits from the process that started it; Python reads it through `os.environ`.

**2. Why does `_integer` treat an empty value like a missing one?**
`LOGSUM_TOP=` in a shell sets an empty text. Using the default for it is friendlier than failing, and it matches how `or` is used for the text settings.

**3. Which wins when both `LOGSUM_TOP=3` and `--top 5` are given?**
The flag, `--top 5`: flags override the environment, and the environment overrides the defaults.

**4. Why check the settings once in `__post_init__` instead of where each is used?**
A bad value stops the program at start-up with one clear message that names it, instead of failing later somewhere unrelated.

**5. Why is `.env.example` committed but `.env` is not?**
The example documents the names with harmless values; the real file may hold secrets, so git ignores it.

## Further reading

- The `os.environ` mapping, Python 3.14: https://docs.python.org/3.14/library/os.html#os.environ
- The twelve-factor app, factor III, Config: https://12factor.net/config
- `dataclasses`, Python 3.14: https://docs.python.org/3.14/library/dataclasses.html
