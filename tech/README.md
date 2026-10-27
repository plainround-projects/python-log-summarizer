# Technology notes

<!-- fmt:off -->

This folder teaches every technology the `python-log-summarizer` repository uses, from zero, through the repository's own files. The repository is a command-line tool, `logsum`, that reads a web server access log without loading it into memory and prints a summary. You do not need to know any of the technologies in advance.

Every file has the same nine parts: what the technology is, why this repository uses it, where it appears, how it works underneath, a walkthrough of this repository's own files, commands to try, common mistakes, five questions with answers, and the official documentation to read next. Versions are the ones this repository pins. Commands are meant to be run from the repository folder. Each file starts with the everyday words it uses, defined once. The files for Python, pytest, argparse, make and uv end their walkthrough with a part generated from the repository itself: every Python file with its imports and definitions, every test, every command-line argument, every shell command of the recipes and every uv command, so nothing the repository contains is left unexplained.

## Reading order

The language first, then the build and packaging tools, then the runtime pieces, then the quality tools and the tests, then automation.

1. [`python`](python.md): the language: generators, dataclasses, type hints, context managers, protocols; the code is read through it
2. [`uv`](uv.md): creates the environment and the lock file, runs every command
3. [`toml-and-pyproject`](toml-and-pyproject.md): the one settings file: metadata, dependencies, commands, tool settings
4. [`hatchling`](hatchling.md): the build backend that turns the source into an installable wheel
5. [`argparse`](argparse.md): reads the command line and writes `--help`
6. [`environment-variables`](environment-variables.md): every setting read from the environment, with its default, and the `.env.example` file
7. [`gzip`](gzip.md): reads compressed logs while streaming
8. [`statistics-percentiles`](statistics-percentiles.md): what p95 is and how 19.95 comes out
9. [`tracemalloc`](tracemalloc.md): measures peak memory, the lesson's proof of streaming
10. [`json-and-json-schema`](json-and-json-schema.md): the `--json` output and the schema test
11. [`logging-and-logfmt`](logging-and-logfmt.md): one-line structured log records on standard error
12. [`pytest`](pytest.md): the test runner, fixtures, parametrized tests
13. [`coverage`](coverage.md): which lines the tests ran; the 95 percent bar
14. [`ruff`](ruff.md): linter and formatter
15. [`mypy`](mypy.md): the strict static type checker
16. [`import-linter`](import-linter.md): makes the layer rule a failing check
17. [`pip-audit`](pip-audit.md): checks locked versions for known vulnerabilities
18. [`make`](make.md): short names for every command: `make test`, `make lint`
19. [`bash`](bash.md): the two scripts under `scripts/`: install check and mutation check
20. [`github-actions`](github-actions.md): the CI workflow that runs the same make targets
21. [`git-and-gitignore`](git-and-gitignore.md): history, commit style, and what is never committed
22. [`markdown`](markdown.md): the README, ARCHITECTURE, CHANGELOG, decision records and result tables
23. [`editorconfig`](editorconfig.md): tabs, spaces and line endings for every editor

## If you have ten minutes

- [`python`](python.md)
- [`uv`](uv.md)
- [`make`](make.md)

Together these show how the code reads, how every command is run, and the one-word entry points; then read `pytest` and `statistics-percentiles` to see how the lesson's answers are checked.

There are 23 technology files in this folder.
