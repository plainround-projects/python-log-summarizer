# GNU Make (the Makefile)

<!-- fmt:off -->

## What it is

**Make** is a program from the 1970s that runs commands described in a file called `Makefile`. The file is a list of **targets**: a name, then the names of other targets it **depends on** (its prerequisites), then indented lines of shell commands (the **recipe**). `make test` runs the recipe of the target `test`, after first running its prerequisites. Here Make is only a **task runner**: its job is to give every command a short, memorable name. On macOS the program is Apple's GNU Make 3.81.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **terminal** is a window where you type a line of text, press Enter, and the computer runs it. The program that reads your line is the **shell** (here `zsh` or `bash`). Everything typed in a terminal is a **command**: a program's name followed by **arguments**, the words that tell it what to do.
- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- An **environment variable** is a named piece of text that a program inherits from the program that started it, for example `PORT=9000`. Programs read them to find out their settings without a settings file. In a shell, `NAME=value command` sets a variable for that one command.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **virtual environment** is a private folder (here `.venv`) that holds one Python interpreter and the packages for one project, so projects with different needs do not disturb each other or the Python of the operating system.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- A **generator** is a function that uses `yield` to hand out values one at a time and pause in between, so a huge sequence never has to exist in memory all at once.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **lock** lets only one thread at a time run a protected piece of code; the others wait. It is how threads avoid changing the same data at the same moment.
- **Latency** is how long one request takes. A **percentile** says what share of requests were at least that fast: **p95** is the time that 95 out of 100 requests beat, so it shows how bad the slow tail is, which an average hides.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- **Continuous integration (CI)** means a server runs the project's checks automatically every time code is pushed, so a broken change is noticed at once.
- A **lock file** records the exact version and checksum of every package the project uses, so installing again gives byte-for-byte the same environment.
- A **wheel** (`.whl`) is the ready-to-install file for a Python package. A **build backend** is the program that turns the source folder into a wheel.
- A **cache** is a saved copy of something slow to make, kept so the next request is fast.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- **Coverage** reports which lines (and which branches of `if`) were run by the tests; lines never run are lines no test can catch a mistake in.
- A **linter** reads code without running it and reports likely mistakes and style problems. A **formatter** rewrites the layout of the code into one agreed style.

## Why this repository uses it

The template says: "a `Makefile` ... so `make run`, `make test` are the only commands a reader needs", with `up`, `run`, `test`, `lint` and `down` always present. The README's commands are the Makefile's targets, and CI runs the same targets, so there is one definition of "how to build and test this project".

## Where it appears

| File | What it does with it |
| --- | --- |
| `Makefile` | all targets. |
| `README.md` | tells the reader to run them. |
| `.github/workflows/ci.yml` | runs `make lint`, `make test`, `make audit` and other targets in CI. |
| `scripts/` | scripts a target calls. |

## How it works underneath

Make reads the Makefile, then looks at the target you asked for. For each prerequisite it makes that target first (recursively). Then it runs the recipe: each line is handed to the shell (`/bin/sh`) as a separate command. If a command exits with a non-zero status, Make stops and reports the error, so a failing `ruff check` stops `make lint` at once.

Normally Make compares file times: a target whose name is a file is only rebuilt if a prerequisite is newer. Targets that are only names for tasks (`test`, `lint`) are listed after `.PHONY`, which tells Make "these are not files, always run them".

**Variables.** `NAME := value` is set once, immediately. `NAME ?= value` sets only if not already set, so `make UV=/other/uv test` can override it. `NAME = value` is expanded each time it is used. Use `$(NAME)` to read one. `$$` writes a literal `$` for the shell. In a recipe, `$(shell ...)` runs a command at read time. A line starting with `#` is a comment; `##` after a target is this repository's convention for the one-line description that `make help` prints.

**Shell.** Every recipe line runs in its own shell, so `cd` in one line does not carry to the next; a line ending in `\` continues onto the next.

## Walkthrough of this repository's use

**The top of the file.**

```make
# make up | run | test | lint | down   (make help lists all)
UV ?= uv
RUN := $(UV) run --frozen
DATA := data
SAMPLE := $(DATA)/sample.log
SMALL := $(DATA)/small.log

-include .env
export
```
(`Makefile`, lines 1 to 9)

- Line 1, a comment: the five targets every repository has.
- `UV ?= uv` and `RUN := $(UV) run --frozen`: the variables explained above. `DATA`, `SAMPLE` and `SMALL` name the generated folder and files so a path is written once.
- `-include .env`: read the file `.env` if it exists (the leading `-` means "no error if it is missing"). `export` on its own line then passes **every** Make variable to the commands as an environment variable. That is how `LOGSUM_TOP=5` in a `.env` file would reach the program.
- `.PHONY:` (next line): the task names that are not files.

```make
.PHONY: help up run run-small demo-memory test test-unit lint format audit check build install-check mutation-check clean down
```
(`Makefile`, line 11)

**Every target.**

**`help`**

```make
help: ## list the targets
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | sed -E 's/:.*## /\t/' | sort
```
(`Makefile`, lines 13 to 14)

Prints the list of targets. `@` before the command stops `make` from echoing the command itself. `grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST)` picks every line that starts with a target name and has a `##` comment; `sed -E 's/:.*## /\t/'` replaces the text between the colon and the comment with a tab; `sort` orders the list. `$(MAKEFILE_LIST)` is a Make variable holding the name(s) of the Makefile(s) being read.

**`up`**

```make
up: ## install the locked environment and generate data/sample.log (500,000 lines) and data/small.log (20 lines)
	$(UV) sync --frozen
	mkdir -p $(DATA)
	$(RUN) logsum-make-log $(SAMPLE)
	$(RUN) logsum-make-log $(SMALL) --small
```
(`Makefile`, lines 17 to 21)

There is no service to start, so `up` installs the locked environment (`uv sync --frozen`), makes the `data/` folder (`mkdir -p` creates it, and does nothing if it exists) and writes the two sample logs with the project's own generator command `logsum-make-log`.

**`run`**

```make
run: ## summarize the 500,000-line sample log, with elapsed time and peak memory
	$(RUN) logsum $(SAMPLE) --stats
```
(`Makefile`, lines 23 to 24)

Summarizes the 500,000-line sample, with `--stats` so elapsed time and peak memory are printed.

**`run-small`**

```make
run-small: ## summarize the 20-line log; the p95 must be 19.95
	$(RUN) logsum $(SMALL) --stats
```
(`Makefile`, lines 26 to 27)

Summarizes the 20-line log; the p95 must be 19.95.

**`demo-memory`**

```make
demo-memory: ## the failure mode: peak memory of streaming vs readlines() on a tenth of the log and on all of it
	$(RUN) python scripts/compare_memory.py $(SAMPLE)
```
(`Makefile`, lines 29 to 30)

Runs `scripts/compare_memory.py`, which prints the peak memory of streaming and of `readlines()` (see `tracemalloc.md`).

**`test`**

```make
test: ## all tests (unit, integration, end to end) with coverage; domain and application must stay at 95% or more
	$(RUN) pytest --cov=logsum --cov-report=term
	$(RUN) coverage report --include='src/logsum/domain/*,src/logsum/application/*' --fail-under=95
```
(`Makefile`, lines 32 to 34)

All tests with coverage, then the 95 percent bar on the domain and application folders (see `pytest.md`, `coverage.md`).

**`test-unit`**

```make
test-unit: ## unit tests only
	$(RUN) pytest tests/unit
```
(`Makefile`, lines 36 to 37)

Runs only `tests/unit`, which needs nothing else and is fast.

**`lint`**

```make
lint: ## ruff check, ruff format check, mypy --strict, import-linter
	$(RUN) ruff check .
	$(RUN) ruff format --check .
	$(RUN) mypy
	$(RUN) lint-imports
```
(`Makefile`, lines 39 to 43)

Ruff, formatter check, mypy and import-linter, in that order; the first failure stops `make` (see `ruff.md`, `mypy.md`, `import-linter.md`).

**`format`**

```make
format: ## apply ruff's formatting and safe fixes
	$(RUN) ruff check --fix .
	$(RUN) ruff format .
```
(`Makefile`, lines 45 to 47)

The repair target: applies Ruff's automatic fixes and rewrites the layout (see `ruff.md`).

**`audit`**

```make
audit: ## check the locked dependencies for known vulnerabilities
	$(UV) export --frozen --no-emit-project --format requirements-txt --output-file .audit-requirements.txt
	$(RUN) pip-audit --no-deps --disable-pip -r .audit-requirements.txt
	rm -f .audit-requirements.txt
```
(`Makefile`, lines 49 to 52)

Exports the lock file and checks every locked version for known vulnerabilities (see `pip-audit.md`).

**`check`**

```make
check: lint test ## lint and test
```
(`Makefile`, line 54)

A target with no recipe of its own: its prerequisites `lint test` run, in that order. It is the one command that proves the repository is healthy.

**`build`**

```make
build: ## build the wheel and source archive into dist/
	$(UV) build
```
(`Makefile`, lines 56 to 57)

Builds the sdist and the wheel into `dist/` with `uv build` (see `hatchling.md`).

**`install-check`**

```make
install-check: ## step 6: install the wheel into a fresh virtual environment and run logsum there
	./scripts/install_check.sh $(SAMPLE)
```
(`Makefile`, lines 59 to 60)

Calls `scripts/install_check.sh` with the sample log; see `bash.md`.

**`mutation-check`**

```make
mutation-check: ## step 5: change the latency suffix from ms to s in a scratch copy; the tests must fail
	./scripts/mutation_check.sh
```
(`Makefile`, lines 62 to 63)

Calls `scripts/mutation_check.sh`; see `bash.md`.

**`down`**

```make
down: ## remove the generated logs and local build output
	rm -rf $(DATA) dist .pytest_cache .mypy_cache .ruff_cache .import_linter_cache .coverage .audit-requirements.txt
```
(`Makefile`, lines 65 to 66)

Deletes the generated logs and the caches (`rm -rf` removes folders without asking). There is no service to stop.

**`clean`**

```make
clean: down
	rm -rf .venv
```
(`Makefile`, lines 68 to 69)

`down` and then also removes `.venv`: the whole environment goes.

### The shell commands inside the recipes, one by one

A recipe line is handed to the shell. These are all the shell commands the recipes use, with every option they are given.

- `grep -E 'pattern' files` prints the lines of the files that match the pattern. `-E` switches on *extended regular expressions* (patterns such as `[a-z-]+` with `+` and `|`).
- `sed -E 's/old/new/'` is the *stream editor*: it reads lines and applies the command. `s/old/new/` means substitute: replace the text that matches `old` (a pattern) with `new`. `-E` again means extended patterns. `\t` in the replacement is a tab.
- `sort` orders its input lines alphabetically.
- `mkdir -p folder` makes a folder. `-p` also makes missing parent folders and does not complain if the folder already exists.
- `rm -f file` removes a file. `-f` (force) makes it silent and successful when the file is already gone.
- `rm -rf folder` removes a folder with everything in it. `-r` means recursive (go into folders) and `-f` means do not ask and do not complain. It cannot be undone, so the recipes only name generated folders.
- `./scripts/name.sh argument` runs a script file in the `scripts` folder (the file has the executable permission) and passes it one argument.

## Try it yourself

```bash
make help
```
Expected: a sorted list of `target<TAB>description` lines.

```bash
make -n lint
```
Expected: `-n` (dry run) prints the commands `lint` would run, without running them.

```bash
make lint; echo "exit code $?"
```
Expected: the four tools' output and `exit code 0`.

```bash
make nonsense; echo "exit code $?"
```
Expected: `make: *** No rule to make target `nonsense'.  Stop.` and a non-zero exit code.

## Mistakes people make

- **Spaces instead of a tab** before a recipe line: `*** missing separator. Stop.` (the `.editorconfig` forces tabs).
- **Forgetting `.PHONY`** for a task target: if a file or folder with that name exists, Make decides there is nothing to do.
- **Expecting `cd` or variables set in one recipe line to apply to the next.** Each line is its own shell.
- **Writing `$VAR` for a Make variable.** Make needs `$(VAR)`; `$VAR` is read as `$V` followed by `AR`. In recipes, a shell variable needs `$$VAR`.
- **Ignoring failures with a leading `-`.** A `-` before a command tells Make to continue if it fails; it is used here once, on purpose, for an optional install.

## Check yourself

**1. What is a target's prerequisite, and when does it run?**
Another target listed after the colon; Make runs it before the target's own recipe.

**2. What does `.PHONY` mean?**
The listed names are tasks, not files, so Make always runs them.

**3. What does the `@` in front of a recipe line do?**
Stops Make printing the command before running it.

**4. What happens when one command of a recipe exits with a non-zero status?**
Make stops and reports an error (unless the line starts with `-`).

**5. Why does `$(RUN)` appear in so many recipes?**
It is a variable that expands to `uv run --frozen`, so every tool runs inside the locked project environment.

## Further reading

- GNU Make manual: https://www.gnu.org/software/make/manual/make.html ("Rules", "Phony targets", "How to use variables", "Recipe execution"). The Apple build is GNU Make 3.81; everything used here is in that version.
