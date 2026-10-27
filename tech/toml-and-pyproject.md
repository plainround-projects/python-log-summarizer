# TOML and `pyproject.toml`

<!-- fmt:off -->

## What it is

**TOML** ("Tom's Obvious Minimal Language") is a plain-text format for settings: `key = value` pairs grouped under `[table]` headings. Values are strings (`"text"`), numbers, true/false, lists (`[1, 2]`) and tables. `#` starts a comment. **`pyproject.toml`** is the one file, in the root of a Python project, where the project says who it is, what it depends on, how to build it and how its tools (the linter, the type checker, the test runner) are configured. Python's standard library reads TOML with the `tomllib` module.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A **pipe**, written `|`, sends the standard output of the command on its left into the standard input of the command on its right, for example `sort file | head -3`.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- An **environment variable** is a named piece of text that a program inherits from the program that started it, for example `PORT=9000`. Programs read them to find out their settings without a settings file. In a shell, `NAME=value command` sets a variable for that one command.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- **JSON** is a text format for data: objects `{"name": "x", "count": 3}` (names with values), lists `[1, 2, 3]`, text in double quotes, numbers, `true`, `false` and `null`. Almost every language can read and write it, which makes it the usual way programs exchange data.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **virtual environment** is a private folder (here `.venv`) that holds one Python interpreter and the packages for one project, so projects with different needs do not disturb each other or the Python of the operating system.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **lock** lets only one thread at a time run a protected piece of code; the others wait. It is how threads avoid changing the same data at the same moment.
- **Latency** is how long one request takes. A **percentile** says what share of requests were at least that fast: **p95** is the time that 95 out of 100 requests beat, so it shows how bad the slow tail is, which an average hides.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- A **lock file** records the exact version and checksum of every package the project uses, so installing again gives byte-for-byte the same environment.
- A **wheel** (`.whl`) is the ready-to-install file for a Python package. A **build backend** is the program that turns the source folder into a wheel.
- An **entry point** (or **console script**) is a command, such as `logsum`, that the installer creates and that starts a named Python function.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- **Coverage** reports which lines (and which branches of `if`) were run by the tests; lines never run are lines no test can catch a mistake in.
- A **linter** reads code without running it and reports likely mistakes and style problems. A **formatter** rewrites the layout of the code into one agreed style.

## Why this repository uses it

The template for these repositories wants "one tool config file". Everything about this project that is not code lives in `pyproject.toml`: its metadata, its dependencies, its command-line commands, the build recipe and the settings of ruff, mypy, pytest, coverage and import-linter. A reader who understands this one file understands how the project is assembled.

## Where it appears

| File | What it does with it |
| --- | --- |
| `pyproject.toml` | metadata, dependencies, commands, build recipe and every tool's settings. |
| `uv.lock` | generated from `pyproject.toml`; see `uv.md`. |
| `.python-version` | not TOML: one line of text read by uv. |

## How it works underneath

A TOML file is read top to bottom. A line `[project]` opens a table named `project`; every `key = value` line below it belongs to that table until the next `[...]` heading. A name with a dot, such as `[tool.ruff.lint]`, is a table inside a table inside a table: `tool` contains `ruff`, which contains `lint`. Double brackets, `[[tool.importlinter.contracts]]`, mean "one more item in a **list of tables**": each time the heading appears, a new entry is added to the list `contracts`.

Tools find their own settings by name: ruff reads `[tool.ruff]`, mypy reads `[tool.mypy]`, pytest reads `[tool.pytest.ini_options]`. The keys `[project]`, `[build-system]` and `[dependency-groups]` are not tool-specific: they are defined by Python Enhancement Proposals (PEPs, the numbered documents that define Python standards): PEP 621 (project metadata), PEP 517/518 (build systems) and PEP 735 (dependency groups).

## Walkthrough of this repository's use

**The project table.**

```toml
[project]
name = "logsum"
version = "0.1.0"
description = "A streaming access-log summarizer: requests per status, the slowest paths by p95 latency, unparseable lines."
readme = "README.md"
requires-python = ">=3.12"
license = "MIT"
license-files = ["LICENSE"]
authors = [{ name = "Sumit Srivastava" }]
dependencies = []
```
(`pyproject.toml`, lines 5 to 14)

- `name`: the name of the package as PyPI would know it (and as `uv.lock` and the wheel file name use it).
- `version`: the version of this project. It follows semantic versioning (`major.minor.patch`); the CHANGELOG records what changed.
- `description`: one line shown by package tools.
- `readme`: the file whose text becomes the package's long description. The build fails if this file does not exist (this once broke a first `uv add` here, before a README existed).
- `requires-python`: which Python versions the code supports. Installers refuse to install on an older Python.
- `license`: the license as an SPDX identifier (`MIT`).
- `license-files`: which files hold the license text; they are copied into the wheel.
- `authors`: a list of tables, each with a `name`.
- `dependencies`: the packages needed **to run** the project. Empty means: the standard library is enough.

**What `dependencies` contains and why.**

  - none: the project runs on the standard library alone.

**Commands the package installs: `[project.scripts]`.**

```toml
[project.scripts]
logsum = "logsum.interfaces.cli:entrypoint"
logsum-make-log = "logsum.interfaces.make_log_cli:entrypoint"
```
(`pyproject.toml`, lines 16 to 18)

Each line has the shape `command-name = "package.module:function"`. When the project is installed, the installer writes a small launcher file named `command-name` into `.venv/bin/` (or any environment's `bin/`). Running it imports the module and calls the function, and the function's return value becomes the command's exit code.

- `logsum = "logsum.interfaces.cli:entrypoint"`: the summarizer. The function `entrypoint` in `logsum/interfaces/cli.py` runs `main`, then handles Ctrl-C (exit code 130) and a closed pipe.
- `logsum-make-log = "logsum.interfaces.make_log_cli:entrypoint"`: writes the lesson's sample logs (`make up` uses it).

**Development tools: `[dependency-groups]`.**

```toml
[dependency-groups]
dev = [
    "pytest>=8",
    "pytest-cov>=5",
    "ruff>=0.6",
    "mypy>=1.11",
    "import-linter>=2.0",
    "pip-audit>=2.7",
    "jsonschema>=4.23",
    "types-jsonschema>=4.23",
]
```
(`pyproject.toml`, lines 20 to 30)

A dependency group is a named list of packages that are not part of the project's runtime but are needed to work on it. `dev` is the name uv installs by default. The `>=` marks are *lower bounds*: the lock file decides the exact version.

  - `pytest`: the test runner (`pytest.md`).
  - `pytest-cov`: the plugin that measures coverage during a test run (`coverage.md`).
  - `ruff`: linter and formatter (`ruff.md`).
  - `mypy`: static type checker (`mypy.md`).
  - `import-linter`: checks the dependency rule between layers (`import-linter.md`).
  - `pip-audit`: checks locked versions for known vulnerabilities (`pip-audit.md`).
  - `jsonschema`: validates the `--json` output against its schema in a test (`json-and-json-schema.md`).
  - `types-jsonschema`: type information for `jsonschema`, so mypy can check calls to it.

**The build recipe: `[build-system]` and Hatch's wheel table.**

```toml
[build-system]
requires = ["hatchling>=1.25"]
build-backend = "hatchling.build"
```
(`pyproject.toml`, lines 1 to 3)

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/logsum"]
```
(`pyproject.toml`, lines 32 to 33)

`requires` lists what a build tool must install in a temporary environment before it can build this project; `build-backend` names the Python object that does the building (see `hatchling.md`). The wheel table tells Hatchling which folder of source to put in the wheel: the project's code lives in `src/<package>/`, and Hatchling cannot guess that when the package name (`logsum`) differs from the folder name.

**Tool settings.** The remaining tables, `[tool.ruff]`, `[tool.mypy]`, `[tool.pytest.ini_options]`, `[tool.coverage.*]` and `[tool.importlinter]`, are explained key by key in `ruff.md`, `mypy.md`, `pytest.md`, `coverage.md` and `import-linter.md`.

## Try it yourself

```bash
python3 -c "import tomllib; d = tomllib.load(open('pyproject.toml','rb')); print(d['project']['name'], d['project']['version'])"
```
Expected: the project name and `0.1.0`, read by the standard library's TOML parser.

```bash
python3 -c "import tomllib; d = tomllib.load(open('pyproject.toml','rb')); print(list(d['tool']))"
```
Expected: the list of tool tables, for example `['hatch', 'ruff', 'mypy', 'pytest', 'coverage', 'importlinter']`.

```bash
uv run --frozen python -c "import importlib.metadata as m; print(m.version('logsum'))"
```
Expected: `0.1.0`: the version installed into `.venv`, which came from the `version` line.

```bash
ls .venv/bin | grep -E "^(logsum|logsum-make-log)$"
```
Expected: the commands from `[project.scripts]`, each a small launcher file.

## Mistakes people make

- **Quoting.** Strings need double quotes: `name = logsum` is an error. A path or a version with dots must be quoted.
- **Mixing up `[project.dependencies]` and the dev group.** Runtime packages go in `dependencies`; tools used only during development go in `[dependency-groups]`.
- **Forgetting the wheel table** when the package folder is not named like the project: the build then fails or builds an empty wheel.
- **Editing the lock instead.** `uv.lock` is generated from this file.

## Check yourself

**1. What does a double-bracket heading such as `[[tool.importlinter.contracts]]` mean?**
One more entry in a list of tables: each occurrence adds a contract to the list `contracts`.

**2. Which table lists the packages needed to run the project, and which the packages needed to develop it?**
`[project] dependencies` lists runtime packages; `[dependency-groups] dev` lists development tools.

**3. What does `logsum = "logsum.interfaces.cli:entrypoint"`-style line under `[project.scripts]` create?**
A command of that name, installed into the environment's `bin/` folder, that imports the module and calls the function; the function's return value is the exit code.

**4. Why does the build need `[tool.hatch.build.targets.wheel] packages = [...]`?**
The code is in `src/<package>/`, and the build tool cannot guess that folder from the project name, so it must be told which folder goes into the wheel.

**5. Who reads `[tool.ruff]`?**
Ruff. Each tool reads the table named after itself under `[tool]`; other programs ignore it.

## Further reading

- TOML specification, version 1.0.0: https://toml.io/en/v1.0.0
- Python Packaging User Guide, "Writing your `pyproject.toml`": https://packaging.python.org/en/latest/guides/writing-pyproject-toml/
- PEP 621 (project metadata), PEP 517 (build backends), PEP 735 (dependency groups): https://peps.python.org/
- `tomllib` in the Python 3.14 standard library documentation: https://docs.python.org/3.14/library/tomllib.html
