# uv

<!-- fmt:off -->

## What it is

`uv` is a command-line program that manages Python for a project. It finds or downloads a Python interpreter, creates a **virtual environment** (a private folder, here `.venv/`, that holds the project's own copy of every package, so projects on one computer do not disturb each other), installs packages into it, and writes a **lock file** (`uv.lock`) that records the exact version of every package. It is written in Rust and is much faster than `pip`, the older tool.

Version in this repository: uv 0.11.2 (run `uv --version`).

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- An **environment variable** is a named piece of text that a program inherits from the program that started it, for example `PORT=9000`. Programs read them to find out their settings without a settings file. In a shell, `NAME=value command` sets a variable for that one command.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- The **interpreter** is the program that reads Python source files and carries them out. `python` starts it. **CPython** is the standard one, written in C.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **lock** lets only one thread at a time run a protected piece of code; the others wait. It is how threads avoid changing the same data at the same moment.
- Work is **CPU-bound** when the processor is the limit (counting, comparing, hashing) and **I/O-bound** when the program mostly waits for **input/output**: the disk, the network or a database.
- A **hash** (or **digest**) is a short fixed-size fingerprint computed from data. The same data always gives the same fingerprint, and a tiny change gives a completely different one, so equal fingerprints are used to check that two results are identical.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- **Continuous integration (CI)** means a server runs the project's checks automatically every time code is pushed, so a broken change is noticed at once.
- A **wheel** (`.whl`) is the ready-to-install file for a Python package. A **build backend** is the program that turns the source folder into a wheel.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.
- A **cache** is a saved copy of something slow to make, kept so the next request is fast.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- A **linter** reads code without running it and reports likely mistakes and style problems. A **formatter** rewrites the layout of the code into one agreed style.

## Why this repository uses it

The lesson asks for a project that "installs the same way on every machine". A `pyproject.toml` alone only says "any version of this library in a range"; `uv.lock` says exactly which version, with a hash of each file, so two computers install the same thing. uv also runs every command in this repository (`uv run ...`), so a reader never activates a virtual environment by hand.

## Where it appears

| File | What it does with it |
| --- | --- |
| `uv.lock` | the lock file: the exact version and hash of every package, written by uv. |
| `pyproject.toml` | the list of what the project wants (`[project]`, `[dependency-groups]`); uv reads it to make the lock file. |
| `.python-version` | one line, `3.14`: the Python minor version uv uses when it makes `.venv`. |
| `Makefile` | every command goes through `uv` (`$(UV)` is `uv`; `$(RUN)` is `uv run --frozen`). |
| `.github/workflows/ci.yml` | installs uv in CI with the `astral-sh/setup-uv` action and runs the same `make` targets. |

## How it works underneath

Three files and one folder matter.

1. **`pyproject.toml`** lists what the project wants, with loose rules such as `>=1.25`.
2. **`uv.lock`** is generated from it. `uv lock` (or any `uv sync` without `--frozen`) asks the package index (PyPI) for the newest versions that satisfy the rules and writes the winners, with the SHA-256 hash of each downloadable file, into the lock. Nobody edits it by hand.
3. **`.venv/`** is built from the lock by `uv sync`. It holds a copy of (or a link to) a Python interpreter and a `site-packages` folder with the installed packages. It is not committed; it can be deleted and rebuilt at any time.
4. **uv's cache** (`~/.cache/uv`) keeps downloaded files, so the second install is almost instant.

Two modes matter in this repository's commands:

- **Normal** (`uv sync`, `uv run x`): uv first checks that `uv.lock` still matches `pyproject.toml` and updates it if not, then syncs `.venv`.
- **Frozen** (`--frozen`): uv trusts the lock file as it is, never touches it, and never contacts the index to re-resolve. This is what the `Makefile` uses, so a build cannot silently change the versions.

`uv run <command>` runs the command with `.venv/bin` first on the path. It is the same as activating the environment, running the command and deactivating.

## Walkthrough of this repository's use

**The lock file's first lines.**

```text
version = 1
revision = 3
requires-python = ">=3.12"
resolution-markers = [
    "python_full_version >= '3.15'",
    "python_full_version < '3.15'",
]
```
(`uv.lock`, lines 1 to 8)

`version = 1` and `revision = 3` are the lock file format's own version numbers. `requires-python = ">=3.12"` is copied from `pyproject.toml`: the lock is valid for every Python from 3.12 up. `resolution-markers` records that the resolver found different answers for Python 3.15 and above than for older ones, so the file holds both. After that, each package is a `[[package]]` block with its `name`, `version`, where it came from (`source`), and one `{ url, hash }` entry per downloadable file (`sdist` is the source archive, `wheels` are the ready-to-install builds for each operating system and Python version). When uv installs, it checks every downloaded file against its hash; a different file with the same version number is refused.

**The commands the Makefile gives to uv.**

```make
	$(UV) sync --frozen
```
(`Makefile`, line 18)

`$(UV)` is a Makefile variable that expands to `uv` (it is defined at the top of the file as `UV ?= uv`, so it can be overridden). `sync` makes `.venv` match the lock. `--frozen` is explained above. The default dependency groups are included, which is why the development tools (pytest, ruff, mypy) land in `.venv` without a flag: uv installs the `dev` group by default.

`RUN := $(UV) run --frozen` (near the top of the Makefile) makes every other target say `$(RUN) pytest`, `$(RUN) ruff check .`, `$(RUN) mypy`: each is `uv run --frozen` followed by the tool, so `$(RUN) pytest` expands to `uv run --frozen pytest`. Every tool runs inside the project environment, from the locked versions.



**`uv build`** (the `build` target) builds a source archive (`.tar.gz`) and a wheel (`.whl`, the install-ready package) into `dist/`. The build is done by the project's build backend, Hatchling (see `hatchling.md`).

**`.python-version`** holds a single line. uv reads it to choose the interpreter when it creates `.venv`; the lesson allows Python 3.12 and newer, and the line pins the one used for development.

### Every uv command this repository uses, with its options

Found by reading the Makefile, the scripts, the Dockerfile, the CI file and the tests. The option descriptions follow `uv --help` of version 0.11.2, the pinned one.

- `uv sync --frozen`: make `.venv` match `uv.lock` exactly. `--frozen` means 'sync without updating the `uv.lock` file': uv trusts the lock file as it is and does not look for newer versions.
- `uv run --frozen <command>`: run a command inside the project's environment without updating `uv.lock` first. Everything the Makefile runs goes through it.
- `uv export --frozen --no-emit-project --format requirements-txt --output-file FILE`: write the locked packages in the older `requirements.txt` format (name, exact version and file hashes). `--no-emit-project` leaves this project itself out ('Do not emit the current project'), `--format` picks the file format, `--output-file` names the file.
- `uv build --out-dir DIR` (short form `-o DIR`): build the source archive and the wheel and write them to `DIR` ('the output directory to which distributions should be written').
- `uv venv --quiet PATH`: create an empty virtual environment at `PATH`. `--quiet` (short `-q`) prints less.
- `uv pip install --quiet --python PYTHON FILE`: install a package file into the environment of the given interpreter. `--python` (short `-p`) names the interpreter whose environment is changed; this is the pip-compatible interface of uv, used to prove the wheel installs on its own.
- `uv pip list --python PYTHON`: list what is installed in that interpreter's environment.

### The `.python-version` file

The file `.python-version` holds one line:

```text
3.14
```
(`.python-version`, line 1)

It names the Python version this project wants. When uv creates `.venv` it looks for an interpreter that matches `3.14` (a request for the minor version 3.14: any 3.14.x), and it tells other tools, such as editors and pyenv, which Python to use here. `requires-python` in `pyproject.toml` is the wider promise (the versions the code runs on); `.python-version` is the one version used day to day.

## Try it yourself

Run these from the repository folder.

```bash
uv --version
```
Expected: `uv 0.11.2 (...)`.

```bash
uv sync --frozen && ls .venv
```
Expected: one line from uv, `Checked NN packages in NNms`, then the folder listing `CACHEDIR.TAG  bin  lib  pyvenv.cfg` (a hidden `.gitignore` too). Nothing was downloaded: the environment already matched the lock.

```bash
uv run --frozen python -c "import sys; print(sys.prefix)"
```
Expected: a path that ends in `/python-log-summarizer/.venv`. The command ran with the project's interpreter, without activating anything.

```bash
grep -c '^\[\[package\]\]' uv.lock
```
Expected: a number: the packages the lock file pins, plus the project's own entry. It changes whenever `uv.lock` changes (it was 46 in `python-cpu-bound-job` and 65 in `python-blocked-event-loop` when this note was written).

```bash
uv export --frozen --no-emit-project --format requirements-txt --output-file /tmp/req-demo.txt && head -6 /tmp/req-demo.txt | cut -c1-90; rm /tmp/req-demo.txt
```
Expected: two comment lines saying the file was generated by uv, then the first package as `name==version \` followed by indented `--hash=sha256:...` lines: the lock file rewritten in the older `requirements.txt` format, which is what the audit tool reads.

## Mistakes people make

- **Editing `uv.lock` by hand.** It is generated. Change `pyproject.toml` and run `uv lock`.
- **Forgetting `--frozen` in CI or scripts.** Without it, uv may re-resolve and change versions on the build machine, which defeats the lock. This repository's Makefile always passes it.
- **Committing `.venv/`.** It is machine-specific. The `.gitignore` lists it.
- **Running `pip install` inside the project.** It bypasses the lock. Use `uv add <package>` (which edits `pyproject.toml` and the lock) or edit `pyproject.toml` and run `uv lock`.
- **Assuming `uv sync` installs only what the project needs to run.** The default also installs the `dev` group; use `--no-dev` for a runtime-only environment.

## Check yourself

**1. What does the `--frozen` flag change?**
uv uses `uv.lock` exactly as it is: it does not check that it matches `pyproject.toml`, does not re-resolve and does not rewrite it.

**2. Why is `.venv/` not committed to git?**
It is built from the lock file and is specific to the machine (paths, operating system, Python build). Anyone can rebuild it with `uv sync`.

**3. What does the hash next to each package in `uv.lock` protect against?**
A downloaded file that is not the one that was locked (a changed or tampered package with the same version number): uv refuses it.

**4. What is the difference between `uv sync` and `uv run`?**
`uv sync` only makes `.venv` match the lock. `uv run` does that (unless told not to) and then runs a command inside the environment.

**5. Where does the choice of Python 3.14 come from?**
From the `.python-version` file, which uv reads when it creates `.venv`; `requires-python` in `pyproject.toml` only says which versions are allowed.

## Further reading

- uv documentation: https://docs.astral.sh/uv/ (this repository uses 0.11.2; see "Projects", "Locking and syncing" and "The lockfile").
- `uv sync --help`, `uv run --help` and `uv export --help` print the flags of the installed version.
- PEP 735, dependency groups: https://peps.python.org/pep-0735/
