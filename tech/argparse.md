# argparse (command-line arguments)

<!-- fmt:off -->

## What it is

A **command-line argument** is a word typed after a program's name: in `logsum data/sample.log --top 3`, `data/sample.log` and `--top 3` are arguments. **argparse** is the standard-library module that reads them. You describe the arguments you accept; argparse checks the typed ones, converts them (to numbers, for example), generates the `--help` text, and exits with a usage message if something is wrong.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **terminal** is a window where you type a line of text, press Enter, and the computer runs it. The program that reads your line is the **shell** (here `zsh` or `bash`). Everything typed in a terminal is a **command**: a program's name followed by **arguments**, the words that tell it what to do.
- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A program has three channels: **standard input** (what it reads), **standard output** (what it prints normally) and **standard error** (where it prints problems and progress). They are separate so a pipe or a file can take the output while errors still show on the screen.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- An **environment variable** is a named piece of text that a program inherits from the program that started it, for example `PORT=9000`. Programs read them to find out their settings without a settings file. In a shell, `NAME=value command` sets a variable for that one command.
- A **server** is a program that waits for requests and answers them. A **client** is a program that sends requests. One program can be both.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- **JSON** is a text format for data: objects `{"name": "x", "count": 3}` (names with values), lists `[1, 2, 3]`, text in double quotes, numbers, `true`, `false` and `null`. Almost every language can read and write it, which makes it the usual way programs exchange data.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- **Latency** is how long one request takes. A **percentile** says what share of requests were at least that fast: **p95** is the time that 95 out of 100 requests beat, so it shows how bad the slow tail is, which an average hides.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- A **seed** is the starting number of a random number generator. The same seed always produces the same 'random' sequence, which makes experiments and tests repeatable.

## Why this repository uses it

The lesson's first "Done when" is that `logsum --help` prints usage. argparse writes that text from the argument descriptions, so it cannot disagree with the code.

## Where it appears

| File | What it does with it |
| --- | --- |
| `src/logsum/interfaces/cli.py` | `build_parser` describes `logsum`'s arguments; `main` parses them. |
| `src/logsum/interfaces/make_log_cli.py` | the same for `logsum-make-log`. |

## How it works underneath

When a program starts, the operating system gives it the list of words typed after its name (`sys.argv`). `ArgumentParser.parse_args(argv)` walks through that list. A word that starts with `--` is an **option** (it may take a value: `--top 3`, or be a flag with none: `--json`). A word without dashes is a **positional** argument (here the log file). For each, argparse finds its description, converts the text with `type=` (for example `int`), checks `choices=`, and stores the result as an attribute of the returned `Namespace` (`arguments.top`). If anything is wrong (an unknown option, a non-number), argparse prints the usage and an error to standard error and ends the program with **exit code 2**. `--help` prints help and ends with exit code 0.

## Walkthrough of this repository's use

```python
def build_parser(defaults: Settings) -> argparse.ArgumentParser:
    """The argument parser, with the environment's settings as its defaults."""
    parser = argparse.ArgumentParser(
        prog="logsum",
        description="Summarize a web server access log: requests per status, the slowest paths by 95th-percentile "
        "latency, and the lines that could not be parsed. The file is streamed one line at a time; a name ending "
        "in .gz is decompressed on the fly. Lines look like: 2026-03-14T09:26:53Z GET /orders/1234 200 87ms",
    )
    parser.add_argument("log", help="path to the access log (plain text or .gz)")
    parser.add_argument(
        "--top", type=int, default=defaults.top, help="how many slow paths to list (default: %(default)s)"
    )
    parser.add_argument("--json", action="store_true", help="print the summary as JSON (docs/summary.schema.json)")
    parser.add_argument("--stats", action="store_true", help="also report elapsed time and peak memory (slows the run)")
    parser.add_argument(
        "--estimator",
        choices=ESTIMATORS,
        default=defaults.estimator,
        help="exact keeps every latency; histogram keeps fixed-size buckets (default: %(default)s)",
    )
    parser.add_argument(
        "--bucket-ms", type=int, default=defaults.bucket_ms, help="histogram bucket width (default: %(default)s)"
    )
    parser.add_argument(
        "--max-latency-ms", type=int, default=defaults.max_latency_ms, help="histogram cap (default: %(default)s)"
    )
    parser.add_argument(
        "--log-level", default=defaults.log_level, help="log level on standard error (default: %(default)s)"
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    return parser
```
(`src/logsum/interfaces/cli.py`, lines 38 to 68)

- `ArgumentParser(prog="logsum", description=...)`: the program name shown in usage, and the paragraph shown at the top of `--help`. The adjacent string literals are joined into one string.
- `parser.add_argument("log", help=...)`: no dashes, so a required **positional** argument.
- `--top`, `type=int`, `default=defaults.top`: an option whose value is converted to an integer. The **default** is not a fixed number: it is the value from the environment settings (`Settings.from_environ`), so the order of precedence is flag, then environment variable, then built-in default. `%(default)s` inside `help` is replaced by the default when help is printed.
- `--json`, `--stats`, `action="store_true"`: flags with no value; `arguments.json` is `True` if present, `False` otherwise.
- `--estimator`, `choices=ESTIMATORS`: only the listed words are accepted; anything else is a usage error (exit code 2).
- `--bucket-ms`, `--max-latency-ms`, `--log-level`: ordinary options, as above. Argparse turns `--bucket-ms` into the attribute `bucket_ms` (dashes become underscores).
- `--version`, `action="version"`: prints the text and exits with 0.

```python
        arguments = build_parser(defaults).parse_args(argv)
        settings = Settings(
            log_level=arguments.log_level,
            top=arguments.top,
            estimator=arguments.estimator,
            bucket_ms=arguments.bucket_ms,
            max_latency_ms=arguments.max_latency_ms,
```
(`src/logsum/interfaces/cli.py`, lines 83 to 89)

`parse_args(argv)` with `argv=None` reads the real command line; tests pass a list instead (`main(["--help"])`). The values are then copied into a `Settings` object, whose own checks raise `InvalidSettingError` for values argparse cannot judge (a `--top` of 0, a bucket wider than the cap). `main` catches that error and returns exit code 2, the same code argparse uses for usage errors.

### Every command-line argument of every command, from the code

Generated by reading each `add_argument` call. *Positional* arguments are given by position; options start with `--`. `type` converts the text typed into a number or a path before the program sees it; `default` is used when the option is left out; `choices` lists the only accepted words; `action` says what to do with the option (`store_true` makes a switch that is `False` unless typed).

#### `src/logsum/interfaces/cli.py`

- program name shown in help (`prog`): `logsum`
- description (`description`): Summarize a web server access log: requests per status, the slowest paths by 95th-percentile latency, and the lines that could not be parsed. The file is streamed one line at a time; a name ending in .gz is decompressed on the fly. Lines look like: 2026-03-14T09:26:53Z GET /orders/1234 200 87ms
- `log` (line 46): help = `'path to the access log (plain text or .gz)'`
- `--top` (line 47): type = `int`; default = `defaults.top`; help = `'how many slow paths to list (default: %(default)s)'`
- `--json` (line 50): action = `'store_true'`; help = `'print the summary as JSON (docs/summary.schema.json)'`
- `--stats` (line 51): action = `'store_true'`; help = `'also report elapsed time and peak memory (slows the run)'`
- `--estimator` (line 52): default = `defaults.estimator`; choices = `ESTIMATORS`; help = `'exact keeps every latency; histogram keeps fixed-size buckets (default: %(default)s)'`
- `--bucket-ms` (line 58): type = `int`; default = `defaults.bucket_ms`; help = `'histogram bucket width (default: %(default)s)'`
- `--max-latency-ms` (line 61): type = `int`; default = `defaults.max_latency_ms`; help = `'histogram cap (default: %(default)s)'`
- `--log-level` (line 64): default = `defaults.log_level`; help = `'log level on standard error (default: %(default)s)'`
- `--version` (line 67): action = `'version'`

#### `src/logsum/interfaces/make_log_cli.py`

- program name shown in help (`prog`): `logsum-make-log`
- description (`description`): Write a sample access log to practice on.
- `output` (line 17): type = `Path`; help = `'file to write'`
- `--lines` (line 18): type = `int`; default = `500000`; help = `'total lines (default: %(default)s)'`
- `--bad` (line 19): type = `int`; default = `300`; help = `'malformed lines among them (default: %(default)s)'`
- `--seed` (line 20): type = `int`; default = `7`; help = `'random seed (default: %(default)s)'`
- `--small` (line 21): action = `'store_true'`; help = `'write the 20-line log whose p95 is 19.95 instead'`

#### The help text exactly as each program prints it

Captured by running `<command> --help` in this repository's environment (width 88). Here the defaults and choices that the code above writes as expressions such as `Strategy.INDEX.value` appear as the words a person types.

```text
$ logsum --help
usage: logsum [-h] [--top TOP] [--json] [--stats] [--estimator {exact,histogram}]
              [--bucket-ms BUCKET_MS] [--max-latency-ms MAX_LATENCY_MS]
              [--log-level LOG_LEVEL] [--version]
              log

Summarize a web server access log: requests per status, the slowest paths by 95th-
percentile latency, and the lines that could not be parsed. The file is streamed one
line at a time; a name ending in .gz is decompressed on the fly. Lines look like:
2026-03-14T09:26:53Z GET /orders/1234 200 87ms

positional arguments:
  log                   path to the access log (plain text or .gz)

options:
  -h, --help            show this help message and exit
  --top TOP             how many slow paths to list (default: 10)
  --json                print the summary as JSON (docs/summary.schema.json)
  --stats               also report elapsed time and peak memory (slows the run)
  --estimator {exact,histogram}
                        exact keeps every latency; histogram keeps fixed-size buckets
                        (default: exact)
  --bucket-ms BUCKET_MS
                        histogram bucket width (default: 5)
  --max-latency-ms MAX_LATENCY_MS
                        histogram cap (default: 10000)
  --log-level LOG_LEVEL
                        log level on standard error (default: WARNING)
  --version             show program's version number and exit
```

```text
$ logsum-make-log --help
usage: logsum-make-log [-h] [--lines LINES] [--bad BAD] [--seed SEED] [--small] output

Write a sample access log to practice on.

positional arguments:
  output         file to write

options:
  -h, --help     show this help message and exit
  --lines LINES  total lines (default: 500000)
  --bad BAD      malformed lines among them (default: 300)
  --seed SEED    random seed (default: 7)
  --small        write the 20-line log whose p95 is 19.95 instead
```

## Try it yourself

```bash
uv run --frozen logsum --help | head -12
```
Expected: `usage: logsum [-h] [--top TOP] [--json] [--stats] ...`, then the description paragraph.

```bash
uv run --frozen logsum; echo "exit code $?"
```
Expected: `usage: logsum ...` and `logsum: error: the following arguments are required: log`, then `exit code 2`.

```bash
uv run --frozen logsum data/small.log --top many; echo "exit code $?"
```
Expected (after `make up` has made `data/small.log`): `logsum: error: argument --top: invalid int value: 'many'` and `exit code 2`.

```bash
uv run --frozen logsum data/small.log --estimator median; echo "exit code $?"
```
Expected: `argument --estimator: invalid choice: 'median' (choose from exact, histogram)` and `exit code 2`.

## Mistakes people make

- **Reading `sys.argv` by hand.** You lose conversion, checking and `--help`.
- **Printing usage errors to standard output.** argparse writes them to standard error.
- **A default that disagrees with the real behavior.** Here the default comes from the same `Settings` the program uses.
- **Forgetting that dashes become underscores** in attribute names.
- **Letting two layers both judge a value.** argparse checks the type; `Settings` checks the meaning; each does its own part.

## Check yourself

**1. What is the exit code when argparse rejects an argument?**
2, and the usage and error go to standard error.

**2. What does `action="store_true"` mean?**
The option is a flag with no value: the attribute is `True` if it was given and `False` otherwise.

**3. What does `choices=` do?**
Accepts only the listed values; anything else is a usage error.

**4. Why does `main(argv)` take the argument list as a parameter?**
So tests can call it with a list instead of the real command line.

**5. Where does the default of `--top` come from?**
From the `Settings` read from the environment (`LOGSUM_TOP`), falling back to 10, so flag beats environment beats default.

## Further reading

- `argparse` in the Python 3.14 documentation: https://docs.python.org/3.14/library/argparse.html and the tutorial https://docs.python.org/3.14/howto/argparse.html
