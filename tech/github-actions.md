# GitHub Actions (the CI workflow)

<!-- fmt:off -->

## What it is

**Continuous integration (CI)** means: every time someone pushes code, a server automatically builds the project and runs the checks, and reports pass or fail. **GitHub Actions** is GitHub's CI service. A **workflow** is a YAML file in `.github/workflows/`; GitHub runs it on its own machines (**runners**) when the events it names happen. **YAML** is a text format for nested data that uses indentation (two spaces here) instead of brackets: `key: value` pairs, and lists as lines that begin with `- `.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **terminal** is a window where you type a line of text, press Enter, and the computer runs it. The program that reads your line is the **shell** (here `zsh` or `bash`). Everything typed in a terminal is a **command**: a program's name followed by **arguments**, the words that tell it what to do.
- A **server** is a program that waits for requests and answers them. A **client** is a program that sends requests. One program can be both.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **hash** (or **digest**) is a short fixed-size fingerprint computed from data. The same data always gives the same fingerprint, and a tiny change gives a completely different one, so equal fingerprints are used to check that two results are identical.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- A **wheel** (`.whl`) is the ready-to-install file for a Python package. A **build backend** is the program that turns the source folder into a wheel.
- A **cache** is a saved copy of something slow to make, kept so the next request is fast.
- **Coverage** reports which lines (and which branches of `if`) were run by the tests; lines never run are lines no test can catch a mistake in.

## Why this repository uses it

The template says the CI "runs format, lint, type check, tests and `pip-audit` on every push", and that the CI file mirrors the one test command. This repository has not been pushed to GitHub yet (the owner pushes later), so the workflow has not run on GitHub; everything it runs was run locally through the same `make` targets.

## Where it appears

| File | What it does with it |
| --- | --- |
| `.github/workflows/ci.yml` | the whole workflow. |
| `Makefile` | every `run:` step is a `make` target. |

## How it works underneath

GitHub reads each file in `.github/workflows/` and watches for the events in `on:`. For each trigger it starts a **job** on a fresh runner: a virtual machine with a clean disk. The job's **steps** run one after another. A step is either `uses:` (run a published action, a packaged bit of automation such as "check out the code") or `run:` (a shell command). If any step exits with a non-zero status, the job fails and the pull request or commit shows a red mark. Nothing carries over from one run to the next except what a cache action stores.

YAML rules that matter: indentation is meaningful (spaces, never tabs); `key: value` needs a space after the colon; a list item starts with `- `; text with a colon or `${{ }}` inside is safer in quotes.

## Walkthrough of this repository's use

```yaml
name: ci

on: [push, pull_request]

jobs:
  check:
    name: Format, lint, types, import rules, tests with coverage, dependency audit, wheel install
    runs-on: ubuntu-latest
    strategy:
      fail-fast: false
      matrix:
        python-version: ["3.12", "3.13", "3.14"]
    steps:
      - uses: actions/checkout@v4
      - uses: astral-sh/setup-uv@v6
        with:
          enable-cache: true
          python-version: ${{ matrix.python-version }}
      - run: make up
      - run: make lint
      - run: make test
      - run: make audit
      - run: make install-check
```
(`.github/workflows/ci.yml`, lines 1 to 23)

- `name: ci`: the name of the workflow, shown in GitHub's Actions tab.
- `on: [push, pull_request]`: when it runs: on every push to any branch and on every pull request.
- `jobs:`: the workflow's jobs. Jobs run in parallel unless one declares `needs`.
- `check:`: the id of a job (any name).
- `name:`: the job's display name.
- `runs-on: ubuntu-latest`: the kind of machine: a fresh virtual machine with a current Ubuntu Linux, thrown away when the job ends.
- `strategy:`: run this job once for every combination in `matrix`.
- `fail-fast: false`: do not cancel the other matrix runs when one fails, so every Python version reports.
- `python-version: [`: the matrix: three runs, one per Python version. `${{ matrix.python-version }}` reads the current value.
- `steps:`: the list of steps of a job, run in order on the same machine; a failing step stops the job.
- `uses: actions/checkout@v4`: a ready-made step (an *action*) that downloads this repository's code onto the machine. `@v4` pins its major version.
- `uses: astral-sh/setup-uv@v6`: installs uv. `with:` passes it inputs: `enable-cache: true` caches uv's downloads between runs, and `python-version` makes uv install that Python.
- `- run:`: a step that runs a shell command. Here every command is a `make` target, so CI runs exactly what a developer runs.

The commands the job runs, in order:

  - `make up`
  - `make lint`
  - `make test`
  - `make audit`
  - `make install-check`

## Try it yourself

GitHub is not needed to read the workflow, and the commands can be run by hand:

```bash
grep "run:" .github/workflows/ci.yml
```
Expected: the `make` targets the workflow runs.

```bash
python3 -c "import re,sys; t=open('.github/workflows/ci.yml').read(); print('tabs:', '\t' in t)"
```
Expected: `tabs: False` (YAML forbids tab indentation).

```bash
make lint && echo "the lint step would pass"
```
Expected: the lint output and the final message.

## Mistakes people make

- **A step that works only on your machine** (a tool you installed by hand). CI starts empty; every needed tool is installed by a step.
- **Using different commands in CI and locally.** Here both use `make`.
- **Unpinned actions.** `@v4` pins the major version; pinning to a commit hash is stricter.
- **Tab characters** in YAML.
- **Putting secrets in the file.** Secrets belong in the repository's encrypted settings, never in the workflow.

## Check yourself

**1. What triggers this workflow?**
A push to any branch and any pull request (`on: [push, pull_request]`).

**2. What does `uses:` do compared to `run:`?**
`uses:` runs a published action; `run:` runs a shell command.

**3. What happens when a step fails?**
The job stops and is marked failed; later steps do not run.

**4. Why do the steps call `make` targets?**
So CI and developers run exactly the same commands.

**5. Why has this workflow not run on GitHub yet?**
The repository has not been pushed; the owner pushes it later. Its commands were run locally.

## Further reading

- GitHub Actions documentation: https://docs.github.com/en/actions ("Workflow syntax for GitHub Actions", "Understanding GitHub Actions").
- `actions/checkout`: https://github.com/actions/checkout ; `astral-sh/setup-uv`: https://github.com/astral-sh/setup-uv
- YAML 1.2 specification: https://yaml.org/spec/1.2.2/
