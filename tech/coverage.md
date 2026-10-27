# coverage.py and pytest-cov

<!-- fmt:off -->

## What it is

**Test coverage** is the share of your code's lines (and decision branches) that ran while the tests ran. **coverage.py** measures it; **pytest-cov** is the pytest plugin that starts coverage.py around a test run (`--cov`). Versions: coverage.py 7.17.0, pytest-cov 7.1.0. A line that never ran has no test that could have caught a bug in it; a line that ran is not proven correct, but at least it was executed.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **terminal** is a window where you type a line of text, press Enter, and the computer runs it. The program that reads your line is the **shell** (here `zsh` or `bash`). Everything typed in a terminal is a **command**: a program's name followed by **arguments**, the words that tell it what to do.
- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- A **process** is one running program, with its own memory and a number, its **process id** or **PID**. A program can start other processes, its **children**, and wait for them or stop them.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- **Continuous integration (CI)** means a server runs the project's checks automatically every time code is pushed, so a broken change is noticed at once.
- An **entry point** (or **console script**) is a command, such as `logsum`, that the installer creates and that starts a named Python function.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- **Coverage** reports which lines (and which branches of `if`) were run by the tests; lines never run are lines no test can catch a mistake in.

## Why this repository uses it

The template says: "coverage reported, with the domain at or near full coverage". `make test` prints the table for the whole package and then fails the build if the domain and application layers (the logic) fall under 95 percent. Wiring code at the edges (command-line entry points, subprocess launchers) is covered by integration and end-to-end tests but may leave a few lines.

## Where it appears

| File | What it does with it |
| --- | --- |
| `pyproject.toml` | `[tool.coverage.run]` and `[tool.coverage.report]`. |
| `Makefile` | `test` runs pytest with `--cov=...` and then `coverage report --fail-under=95` for two folders. |
| `.github/workflows/ci.yml` | runs `make test`. |

## How it works underneath

Python can call a function each time it runs a line (a *trace* hook). coverage.py installs that hook, records every (file, line) that ran into a data file called `.coverage`, and, with **branch** measurement, also records each jump (which side of an `if` was taken). After the run, `coverage report` compares the recorded lines with the lines that *could* run in each file and prints percentages and the numbers of the lines that did not run.

pytest-cov starts coverage before the tests import the code, so module-level lines (class and function definitions) count as run. Because the data goes to a file, a second command (`coverage report --include=...`) can report on a subset without running the tests again.

## Walkthrough of this repository's use

```toml
[tool.coverage.run]
source = ["logsum"]
branch = true
```
(`pyproject.toml`, lines 66 to 68)

- `source = ['logsum']`: measure only this package (not the tests, not installed libraries).
- `branch = true`: also measure branches. A line with an `if` counts as fully covered only when the test run took both the true and the false side.


```toml
[tool.coverage.report]
show_missing = true
skip_covered = false
```
(`pyproject.toml`, lines 70 to 72)

- `show_missing = true`: print the line numbers that did not run, in a `Missing` column.
- `skip_covered = false`: list files that are 100 percent covered too (so the whole package is visible).

**How the table reads.** Columns: `Stmts` (statements), `Miss` (statements that never ran), `Branch` (decision branches), `BrPart` (branches only partly taken), `Cover` (percent) and `Missing` (the lines). For example `scoring.py 59 0 22 0 100%` means no statement was missed and every branch was taken.

```make
	$(RUN) coverage report --include='src/logsum/domain/*,src/logsum/application/*' --fail-under=95
```
(`Makefile`, line 34)

`--include='...'` limits the report to the domain and application folders (shell-style patterns in quotes so the shell does not expand them); `--fail-under=95` makes the command exit with status 2 when the total is below 95 percent.

## Try it yourself

```bash
uv run --frozen pytest tests/unit -q --cov=logsum --cov-report=term | tail -8
```
Expected: the coverage table ending in a `TOTAL` row with a percentage.

```bash
uv run --frozen coverage report --include='src/*/domain/*' | tail -4
```
Expected: the table for the domain folder only (the data from the run above is still in `.coverage`).

```bash
uv run --frozen coverage report --include='src/*/domain/*' --fail-under=100; echo "exit code $?"
```
Expected: `exit code 0` when the domain is fully covered; a number below the bar prints `FAIL Required test coverage of 100% not reached` and exit code 2.

## Mistakes people make

- **Chasing 100 percent everywhere.** Coverage says which code ran, not that it is right. The bar is on the logic layers, where a missed line is a missed rule.
- **Measuring the tests themselves.** `source` limits the report to the package.
- **Reading branch partials as noise.** `BrPart` shows an `if` whose other side no test took.
- **A stale `.coverage` file.** The report reads whatever the last run left; the `down` target deletes it.
- **Forgetting that subprocess code is invisible.** Code that only runs in another process is not measured unless coverage is configured to follow it, which is why wiring code can show lines as missed although end-to-end tests run them.

## Check yourself

**1. What does the `Miss` column count?**
Statements that never ran during the measured run.

**2. What does `branch = true` add?**
It also checks that both sides of each decision (the true and the false side of an `if`) were taken.

**3. What does `--fail-under=95` do?**
Makes `coverage report` exit with a non-zero status (and `make` stop) if the total is under 95 percent.

**4. Why is the report restricted with `--include` for the 95 percent check?**
The bar applies to the domain and application layers, the logic; edge code is covered mostly by integration tests.

**5. What is `.coverage`?**
A data file the run writes; reports are produced from it later.

## Further reading

- coverage.py documentation: https://coverage.readthedocs.io/en/7.17.0/ ("Configuration reference", "Branch coverage measurement", "Command line usage").
- pytest-cov documentation: https://pytest-cov.readthedocs.io/en/v7.1.0/
