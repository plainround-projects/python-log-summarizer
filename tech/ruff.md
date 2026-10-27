# Ruff (linter and formatter)

<!-- fmt:off -->

## What it is

A **linter** reads source code without running it and reports mistakes and style problems. A **formatter** rewrites the code into one agreed layout (quotes, line breaks, spacing) so nobody argues about it. **Ruff** is both, in one fast program written in Rust. Version here: 0.17.2.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- **Continuous integration (CI)** means a server runs the project's checks automatically every time code is pushed, so a broken change is noticed at once.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.

## Why this repository uses it

The template requires "a formatter and a linter configured in the repository and run in CI". `make lint` runs Ruff first. A failing lint stops the build before the slower type check and tests run, and the same command runs in CI.

## Where it appears

| File | What it does with it |
| --- | --- |
| `pyproject.toml` | `[tool.ruff]`, `[tool.ruff.lint]` and `[tool.ruff.lint.per-file-ignores]`: the settings. |
| `Makefile` | `lint` runs `ruff check .` and `ruff format --check .`; `format` runs `ruff check --fix .` and `ruff format .`. |
| `.github/workflows/ci.yml` | runs `make lint`. |
| `tests/` | the `D` rules are switched off here by `per-file-ignores`. |

## How it works underneath

`ruff check` parses every `.py` file into a **syntax tree** (the structure of the code as a program sees it), then runs each enabled **rule** over the tree. A rule has a code (a letter prefix and a number such as `E501`). A rule that finds a problem prints the file, line, code and a message. Some problems have a **fix** that Ruff can apply (`--fix`), such as sorting imports.

`ruff format` is a separate command. It prints the code again from the tree in a fixed layout (compatible with the Black formatter). With `--check` it changes nothing and exits with code 1 if any file would change; without it, it rewrites the files.

Rules are grouped by the prefix of their code. Settings say which prefixes are on. A line can opt out of one rule with a comment `# noqa: CODE`, and Ruff reports a `noqa` that suppresses nothing (`RUF100`), so stale opt-outs do not pile up. This repository's rule (from `docs/CODE_STYLE.md` in the app) is: never weaken a check to get to green.

## Walkthrough of this repository's use

```toml
[tool.ruff]
line-length = 120
target-version = "py312"
src = ["src", "tests"]
```
(`pyproject.toml`, lines 35 to 38)

- `line-length = 120`: a line longer than this is reported (`E501`), and the formatter wraps at this width.
- `target-version = "py312"`: the oldest Python the code must run on. Rules and the formatter only use syntax that version supports, and the `UP` rules suggest what that version offers.
- `src = ['src', 'tests']`: the folders that hold this project's own code, so the import sorter knows which imports are "first party" and puts them in their own group.

```toml
[tool.ruff.lint]
select = ["E", "F", "I", "B", "UP", "SIM", "N", "C4", "RUF", "PT", "D100", "D101", "D102", "D103", "D104"]
```
(`pyproject.toml`, lines 40 to 41)

`select` is the list of rule families that are on. Everything not listed is off. Here:

  - `E`: pycodestyle errors: style problems such as lines that are too long (`E501`) or bad spacing.
  - `F`: Pyflakes: real mistakes such as an unused import (`F401`) or a name that is never defined (`F821`).
  - `I`: isort: imports must be sorted and grouped (standard library, then installed packages, then this project).
  - `B`: flake8-bugbear: code that is probably a bug, such as a mutable default argument or `raise` without `from` inside `except`.
  - `UP`: pyupgrade: syntax that the target Python version has a newer way to write.
  - `SIM`: flake8-simplify: needlessly long ways to write something simple (for example `try/except/pass`, which `contextlib.suppress` replaces).
  - `N`: pep8-naming: classes in `CapWords`, functions and variables in `snake_case`.
  - `C4`: flake8-comprehensions: unnecessary calls to `list()` or `set()` around comprehensions.
  - `RUF`: Ruff's own rules, for example unused `noqa` comments (`RUF100`) and regex patterns written without a raw string (`RUF043`).
  - `PT`: flake8-pytest-style: conventions for pytest tests, such as the form of `parametrize`.
  - `D100`: pydocstyle: a missing docstring in a public module.
  - `D101`: a missing docstring in a public class.
  - `D102`: a missing docstring in a public method.
  - `D103`: a missing docstring in a public function.
  - `D104`: a missing docstring in a public package (`__init__.py`).

```toml
[tool.ruff.lint.per-file-ignores]
"tests/**" = ["D"]
```
(`pyproject.toml`, lines 43 to 44)

`per-file-ignores` turns rules off for files that match a pattern. `"tests/**" = ["D"]` switches off every docstring rule in the tests: the tests are named as sentences (`test_a_missing_file_is_a_named_error`), which already says what they check.

**How the Makefile calls it.**

```make
lint: ## ruff check, ruff format check, mypy --strict, import-linter
	$(RUN) ruff check .
	$(RUN) ruff format --check .
	$(RUN) mypy
	$(RUN) lint-imports
```
(`Makefile`, lines 39 to 43)

`ruff check .` lints the whole folder (`.` is the current folder); `ruff format --check .` checks the layout without changing files; the last two lines are the type checker and the import rules (see `mypy.md`, `import-linter.md`). `make` stops at the first command that fails (exit code not 0).

```make
format: ## apply ruff's formatting and safe fixes
	$(RUN) ruff check --fix .
	$(RUN) ruff format .
```
(`Makefile`, lines 45 to 47)

`format` is the repair target: `ruff check --fix .` applies the automatic fixes, then `ruff format .` rewrites the layout.

## Try it yourself

```bash
uv run --frozen ruff --version
```
Expected: `ruff 0.17.2`.

```bash
uv run --frozen ruff check .
```
Expected: `All checks passed!`

```bash
uv run --frozen ruff format --check .
```
Expected: a line such as `NN files already formatted`.

```bash
printf 'import os\nx=1\n' > /tmp/demo_ruff.py && uv run --frozen ruff check --isolated --select F,E,I /tmp/demo_ruff.py; rm /tmp/demo_ruff.py
```
Expected: two reports, ``I001 [*] Import block is un-sorted or un-formatted`` and ``F401 [*] `os` imported but unused``, each with a small picture of the line and a `help:` line; then `Found 2 errors.` and `[*] 2 fixable with `--fix``. The exit code is 1. `--isolated` ignores the repository's settings so the demo file is judged alone.

## Mistakes people make

- **Running only `ruff check`.** Layout is checked by `ruff format --check`; both are in `make lint`.
- **Silencing a rule with `# noqa` instead of fixing it.** `RUF100` complains when the comment is not needed; this repository has no `noqa` comments in the source.
- **Letting two tools format the same code** (for example an editor plugin with different settings). The `.editorconfig` and Ruff agree on indentation and line endings.
- **Forgetting that `select` is an allow list.** A rule that is not in the list is silently off.
- **Reading a docstring rule as a demand for long text.** One accurate sentence satisfies `D10x`.

## Check yourself

**1. What is the difference between `ruff check` and `ruff format`?**
`check` is the linter: it reports mistakes and style problems by rule. `format` is the formatter: it rewrites the layout. `format --check` only reports whether a rewrite would change anything.

**2. What does the `src` setting tell Ruff?**
Which folders hold the project's own code, so the import sorter can tell first-party imports from installed packages.

**3. Why are the `D` rules ignored under `tests/`?**
Test names already read as sentences that say what they check, so a docstring on each would repeat them.

**4. What happens if a line has `# noqa: E501` but is short enough?**
Ruff reports the unused suppression as `RUF100`, because `RUF` is selected.

**5. Which command does CI run for linting?**
`make lint`, which runs ruff check, ruff format --check, mypy and import-linter in that order.

## Further reading

- Ruff documentation: https://docs.astral.sh/ruff/ (version 0.17.2 here): "Rules" lists every code; "Configuration" explains `select`, `src` and `per-file-ignores`; "Formatter" explains `format`.
- `uv run ruff check --help` and `uv run ruff rule E501` print the installed version's own text.
