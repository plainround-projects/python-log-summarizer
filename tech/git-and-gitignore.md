# Git and `.gitignore`

<!-- fmt:off -->

## What it is

**Git** is a program that records the history of a folder as a series of **commits** (snapshots with a message and an author). A folder under git is a **repository**; the history lives in a hidden `.git/` folder inside it. `.gitignore` is a text file that lists patterns for files git must not track: generated files, local settings, secrets.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- A **redirection** sends a channel somewhere else. `> file` writes standard output to a file, `2>&1` sends standard error to wherever standard output goes, and `/dev/null` is a special file that throws away whatever is written to it.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- An **environment variable** is a named piece of text that a program inherits from the program that started it, for example `PORT=9000`. Programs read them to find out their settings without a settings file. In a shell, `NAME=value command` sets a variable for that one command.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **virtual environment** is a private folder (here `.venv`) that holds one Python interpreter and the packages for one project, so projects with different needs do not disturb each other or the Python of the operating system.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **lock** lets only one thread at a time run a protected piece of code; the others wait. It is how threads avoid changing the same data at the same moment.
- A **hash** (or **digest**) is a short fixed-size fingerprint computed from data. The same data always gives the same fingerprint, and a tiny change gives a completely different one, so equal fingerprints are used to check that two results are identical.
- **Continuous integration (CI)** means a server runs the project's checks automatically every time code is pushed, so a broken change is noticed at once.
- A **lock file** records the exact version and checksum of every package the project uses, so installing again gives byte-for-byte the same environment.
- A **wheel** (`.whl`) is the ready-to-install file for a Python package. A **build backend** is the program that turns the source folder into a wheel.
- A **container** is a running program packaged with everything it needs, kept apart from the rest of the machine. An **image** is the frozen recipe result a container starts from. **Docker** is the tool that builds images and runs containers.
- A **cache** is a saved copy of something slow to make, kept so the next request is fast.
- **Coverage** reports which lines (and which branches of `if`) were run by the tests; lines never run are lines no test can catch a mistake in.
- A **linter** reads code without running it and reports likely mistakes and style problems. A **formatter** rewrites the layout of the code into one agreed style.

## Why this repository uses it

Each project folder here is its own git repository, created with `git init`, so it can be pushed to GitHub later as a separate repository. The history is kept in meaningful commits with prefixes (`feat(domain):`, `test:`, `docs:`, `ci:`, `build:`), and the template requires that "`git status` after the final commit shows nothing untracked". The `.gitignore` is what keeps virtual environments, caches and generated data out.

## Where it appears

| File | What it does with it |
| --- | --- |
| `.gitignore` | the patterns. |
| `.git/` | the history (not part of the working files). |
| `CHANGELOG.md` | the human-written summary of what changed in each version. |

## How it works underneath

Git stores three things: file contents (as compressed objects named by their hash), trees (folders), and commits (a tree, a message, an author, a time and a parent commit). `git add` copies the current content of a file into the **staging area** (the next commit's contents); `git commit` turns the staging area into a commit. `git status` compares three views: the last commit, the staging area and the working folder. A file is **untracked** if git has never seen it and no ignore pattern matches.

A pattern in `.gitignore` matches by name: `dir/` matches a folder, `*.pyc` matches by suffix, a leading `/` anchors to the repository root, `!pattern` re-includes a file a previous line excluded. Ignoring only affects files that are not yet tracked.

## Walkthrough of this repository's use

```text
.venv/
__pycache__/
*.pyc
*.egg-info/
build/
dist/
.pytest_cache/
.mypy_cache/
.ruff_cache/
.import_linter_cache/
.coverage
coverage.xml
htmlcov/
.env
.DS_Store
logs/
*.log
!tests/data/*.log
/data/
.omc/
```
(`.gitignore`, lines 1 to 20)

Each line, in plain words:

- `.venv/`: the virtual environment (see `uv.md`); rebuilt from the lock file.
- `__pycache__/`: Python's compiled-bytecode cache folders.
- `*.pyc`: compiled bytecode files.
- `*.egg-info/`: metadata folders that older build tools leave behind (the template forbids committing them).
- `build/`: build output.
- `dist/`: wheels and archives from `uv build`.
- `.pytest_cache/`: pytest's cache (last failed tests).
- `.mypy_cache/`: mypy's cache.
- `.ruff_cache/`: ruff's cache.
- `.import_linter_cache/`: import-linter's cache.
- `.coverage`: coverage's data file.
- `coverage.xml`: a coverage report file some tools write.
- `htmlcov/`: coverage's HTML report folder.
- `.env`: a machine's real settings, never committed.
- `.DS_Store`: macOS Finder's folder-view files.
- `logs/`: log output (the template forbids committing logs).
- `*.log`: any log file.
- `!tests/data/*.log`: the exception: the small log fixtures in `tests/data` are test input and are tracked (a `!` line re-includes what an earlier line excluded).
- `/data/`: generated data at the repository root only (the leading slash keeps `tests/data/` tracked).
- `.omc/`: local state of an assistant tool.

**Commit style.** Messages begin with a type and an optional scope in parentheses: `feat(domain): ...` adds a feature in the domain layer, `fix(...)` repairs, `test:` adds tests, `build:` changes the Makefile or Dockerfile, `ci:` changes the workflow, `docs:` changes documentation, `chore:` is housekeeping. Each commit ends with a `Co-Authored-By:` line naming the assistant that helped write it. The CHANGELOG follows the "Keep a Changelog" format.

## Try it yourself

```bash
git log --oneline | head -5
```
Expected: the five newest commits, each a short hash and a message with a type prefix.

```bash
git status --short; echo "untracked/changed lines: $(git status --short | wc -l)"
```
Expected: `untracked/changed lines: 0` once everything is committed (while this `tech/` folder is still new it shows `?? tech/`).

```bash
git check-ignore -v .venv data/x.txt 2>&1 | head
```
Expected: lines that name the `.gitignore` rule responsible for ignoring each path (for a path no rule matches, nothing is printed).

```bash
git ls-files | head -10
```
Expected: the first tracked files; `uv.lock` is among the tracked files, `.venv` is not.

## Mistakes people make

- **Committing generated output** (virtual environments, `__pycache__`, coverage files). Once tracked, ignore rules no longer hide them.
- **Committing secrets.** `.env` is ignored; `.env.example` holds the variable names with harmless values.
- **A vague message** such as "fix stuff". The prefix convention makes the history readable.
- **Forgetting to commit the lock file.** `uv.lock` must be tracked: it is what makes installs reproducible.
- **`git add -A` without looking.** Check `git status` first; this repository never commits files it did not mean to.

## Check yourself

**1. What is a commit?**
A snapshot of the tracked files with a message, an author, a time and a pointer to its parent commit.

**2. Does adding a pattern to `.gitignore` untrack a file git already tracks?**
No. Ignore rules only affect untracked files; a tracked file must be removed from git (`git rm --cached`).

**3. Why is `.env` ignored but `.env.example` tracked?**
`.env` holds a machine's real settings and may hold secrets; `.env.example` documents every variable with no secret.

**4. What does a leading slash in a pattern like `/data/` mean?**
The pattern only matches at the repository root, not in a deeper folder such as `tests/data/`.

**5. What should `git status` show after the last commit?**
Nothing: no untracked and no modified files.

## Further reading

- Pro Git book (free): https://git-scm.com/book/en/v2 (chapters 2 and 7); `git help gitignore` for the pattern rules.
- Keep a Changelog: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning: https://semver.org/
