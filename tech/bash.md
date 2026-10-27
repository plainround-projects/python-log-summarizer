# Bash (the scripts in `scripts/`)

<!-- fmt:off -->

## What it is

**Bash** is a shell: a program that reads commands you type (or that a file contains) and runs other programs. A **shell script** is a text file of such commands; the first line `#!/usr/bin/env bash` (the **shebang**) tells the operating system to run the file with bash. A command is a program name followed by arguments; `|` (a **pipe**) sends one command's output into the next command's input; `$(...)` runs a command and substitutes its output; `$name` is a variable. Every command ends with an **exit status**, a number: 0 means success, anything else means failure.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **terminal** is a window where you type a line of text, press Enter, and the computer runs it. The program that reads your line is the **shell** (here `zsh` or `bash`). Everything typed in a terminal is a **command**: a program's name followed by **arguments**, the words that tell it what to do.
- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A program has three channels: **standard input** (what it reads), **standard output** (what it prints normally) and **standard error** (where it prints problems and progress). They are separate so a pipe or a file can take the output while errors still show on the screen.
- A **redirection** sends a channel somewhere else. `> file` writes standard output to a file, `2>&1` sends standard error to wherever standard output goes, and `/dev/null` is a special file that throws away whatever is written to it.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- An **environment variable** is a named piece of text that a program inherits from the program that started it, for example `PORT=9000`. Programs read them to find out their settings without a settings file. In a shell, `NAME=value command` sets a variable for that one command.
- A **process** is one running program, with its own memory and a number, its **process id** or **PID**. A program can start other processes, its **children**, and wait for them or stop them.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **virtual environment** is a private folder (here `.venv`) that holds one Python interpreter and the packages for one project, so projects with different needs do not disturb each other or the Python of the operating system.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- **Latency** is how long one request takes. A **percentile** says what share of requests were at least that fast: **p95** is the time that 95 out of 100 requests beat, so it shows how bad the slow tail is, which an average hides.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- A **wheel** (`.whl`) is the ready-to-install file for a Python package. A **build backend** is the program that turns the source folder into a wheel.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.
- A **cache** is a saved copy of something slow to make, kept so the next request is fast.

## Why this repository uses it

Two of the lesson's "Done when" lines are about things that are awkward to prove inside Python: that the project installs from a built wheel into a brand-new environment (step 6), and that changing the latency suffix from `ms` to `s` makes a test fail (step 5). Each is a few commands in sequence, which a shell script says directly.

## Where it appears

| File | What it does with it |
| --- | --- |
| `scripts/install_check.sh` | build the wheel, install it into a fresh environment, run the command from another folder. |
| `scripts/mutation_check.sh` | break the parser on purpose in a scratch copy and require that the tests fail. |
| `Makefile` | `install-check` and `mutation-check` call the two scripts. |

## How it works underneath

When bash runs a script it reads it one line at a time. For each line it expands variables and `$(...)`, splits the line into words, finds the program (searching the folders in `PATH`), starts it as a **process**, waits, and records the exit status in `$?`. Environment variables are copied into each child process; changing one in a child never changes the parent. `set -euo pipefail` changes the defaults for the safer: `-e` stops the script at the first command that fails; `-u` makes using an unset variable an error; `-o pipefail` makes a pipeline fail if any command in it fails, not only the last. A `trap '...' EXIT` registers a command to run when the script ends, whether it succeeded or failed: the usual way to clean up temporary files.

## Walkthrough of this repository's use

### `scripts/install_check.sh`

```bash
#!/usr/bin/env bash
# Build the wheel, install it into a brand-new virtual environment with nothing else, and run the command
# from a different directory with PYTHONPATH unset, so success means the packaged wheel works and not that
# Python found this source tree by accident.
set -euo pipefail

log=$(cd "$(dirname "${1:?usage: install_check.sh LOG_FILE}")" && pwd)/$(basename "$1")
root=$(cd "$(dirname "$0")/.." && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

cd "$root"
uv build --out-dir "$work/dist" >/dev/null
uv venv --quiet "$work/venv"
uv pip install --quiet --python "$work/venv/bin/python" "$work"/dist/*.whl
echo "installed into a fresh environment: $(uv pip list --python "$work/venv/bin/python" 2>/dev/null | tail -n +3 | tr -s ' ' | tr '\n' ';')"

cd "$work"
env -u PYTHONPATH "$work/venv/bin/logsum" --help | head -1
env -u PYTHONPATH "$work/venv/bin/logsum" "$log"
```
(`scripts/install_check.sh`, lines 1 to 20)

- Line 1, the shebang. Lines 2 to 4 are comments (`#`).
- Line 5, `set -euo pipefail`: stop at the first failing command, treat unset variables as errors, fail a pipeline if any part fails.
- Line 7, `log=$(cd "$(dirname "${1:?usage: install_check.sh LOG_FILE}")" && pwd)/$(basename "$1")`: build the **absolute** path of the log file given as the first argument. `$1` is the first argument; `${1:?message}` stops the script with the message if `$1` is missing. `dirname` gives the folder part of the path; `cd` into it and `pwd` prints where we are (an absolute path), because relative paths would break after the script changes folder later; `basename` gives the file name. The quotes keep names with spaces intact. `&&` runs the next command only if the previous one succeeded.
- Line 8, `root=$(cd "$(dirname "$0")/.." && pwd)`: `$0` is the script's own path; its folder's parent is the repository root.
- Line 9, `work=$(mktemp -d)`: make a new empty temporary directory and keep its name.
- Line 10, `trap 'rm -rf "$work"' EXIT`: when the script ends, however it ends, delete that directory (`rm -rf` removes a folder and everything in it without asking). Single quotes delay the expansion of `$work` until the trap runs.
- Line 12, `cd "$root"`: go to the repository.
- Line 13, `uv build --out-dir "$work/dist" >/dev/null`: build the wheel into the temporary folder. `>/dev/null` throws the normal output away (errors still show on standard error).
- Line 14, `uv venv --quiet "$work/venv"`: create a **new, empty** virtual environment in the temporary folder. It contains no packages from the project's own `.venv`.
- Line 15, `uv pip install --quiet --python "$work/venv/bin/python" "$work"/dist/*.whl`: install only the built wheel into it; `*.whl` is a **glob**, expanded by the shell to the wheel's file name.
- Line 16, `echo "installed into a fresh environment: $(uv pip list ... | tail -n +3 | tr -s ' ' | tr '\n' ';')"`: list what is installed (the wheel alone), `tail -n +3` drops the two header lines, `tr -s ' '` squeezes runs of spaces to one, `tr '\n' ';'` turns newlines into semicolons so it fits on one line. `2>/dev/null` hides uv's messages on standard error.
- Line 18, `cd "$work"`: leave the repository, so Python cannot find the source tree by the current folder.
- Line 19, `env -u PYTHONPATH "$work/venv/bin/logsum" --help | head -1`: run the installed command with the variable `PYTHONPATH` removed (`env -u` unsets it for this one command), print only the first line (`head -1`).
- Line 20: run the installed command on the log. Success means the **packaged wheel** works.

### `scripts/mutation_check.sh`

```bash
#!/usr/bin/env bash
# Copy the project to a scratch folder, change the latency suffix the parser accepts from "ms" to "s",
# and run the unit tests there. They must fail: that proves the parser tests would catch the mistake.
set -euo pipefail

root=$(cd "$(dirname "$0")/.." && pwd)
work=$(mktemp -d)
trap 'rm -rf "$work"' EXIT

cp -R "$root/src" "$root/tests" "$root/docs" "$root/pyproject.toml" "$root/README.md" "$root/LICENSE" "$work/"
sed -i.bak 's/_LATENCY_SUFFIX = "ms"/_LATENCY_SUFFIX = "s"/' "$work/src/logsum/domain/request.py"
rm "$work/src/logsum/domain/request.py.bak"
grep -n '_LATENCY_SUFFIX = ' "$work/src/logsum/domain/request.py"

cd "$work"
if PYTHONPATH="$work/src" "$root/.venv/bin/python" -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -15; then
  :
fi
status=${PIPESTATUS[0]}
if [ "$status" -eq 0 ]; then
  echo "MUTANT SURVIVED: the tests did not notice the change" >&2
  exit 1
fi
echo "mutant killed: the tests failed as they should"
```
(`scripts/mutation_check.sh`, lines 1 to 24)

A **mutation check** deliberately breaks the code ("a mutant") and demands that the tests notice ("kill" it).

- Lines 6 to 8: same setup as before: the repository root, a temporary folder, cleanup on exit.
- Line 10, `cp -R ... "$work/"`: copy the source, tests, docs and metadata files into the scratch folder (`-R` copies folders recursively). The real repository is never changed.
- Line 11, `sed -i.bak 's/_LATENCY_SUFFIX = "ms"/_LATENCY_SUFFIX = "s"/' ...`: `sed` edits text; `s/old/new/` replaces the first match on each line; `-i.bak` edits the file in place and keeps a backup named `.bak` (this spelling works on both macOS and Linux, unlike a bare `-i`). Line 12 deletes the backup.
- Line 13, `grep -n '_LATENCY_SUFFIX = ' ...`: print the changed line with its line number as evidence.
- Line 15, `cd "$work"`.
- Line 16: run the unit tests in the scratch copy, with `PYTHONPATH="$work/src"` (an environment variable set for this one command) so Python imports the broken copy, using the project's own Python (`$root/.venv/bin/python`). `2>&1` sends error output into the same stream as normal output; `| tail -15` keeps the last fifteen lines. The `if ...; then :; fi` wrapper exists so that `set -e` does not stop the script when the tests fail; `:` is a command that does nothing.
- Line 19, `status=${PIPESTATUS[0]}`: `PIPESTATUS` is an array of the exit statuses of the commands in the last pipeline; element 0 is the first command's (the tests'). It is read straight after the `if` block, which holds the status of the pipeline in the `if` condition.
- Lines 20 to 24: `-eq 0` compares numbers. If the tests passed, the mutant **survived**: print a message to standard error (`>&2`) and exit with status 1. Otherwise print that the mutant was killed.

## Try it yourself

```bash
bash -n scripts/install_check.sh && bash -n scripts/mutation_check.sh && echo "syntax ok"
```
Expected: `syntax ok` (`bash -n` reads a script and reports syntax errors without running it).

```bash
make mutation-check 2>&1 | tail -4
```
Expected: the last four lines: two `FAILED tests/unit/...` lines, a summary such as `15 failed, 89 passed in 12.38s`, and `mutant killed: the tests failed as they should`. (Without `| tail -4` the output also starts with the changed line `9:_LATENCY_SUFFIX = "s"`.)

```bash
make install-check 2>&1 | tail -6
```
Expected: the last six lines, which are the end of the summary of the sample log (five path lines and `bad lines: 300`). Without `| tail -6` the output starts with `installed into a fresh environment: logsum 0.1.0;` and the first line of the help.

```bash
bash -c 'set -e; false; echo "not reached"'; echo "exit code $?"
```
Expected: no output from the `echo`, then `exit code 1`: `set -e` stopped at the failing `false`.

## Mistakes people make

- **Leaving variables unquoted** (`rm -rf $work`): a name with a space becomes two words. Quote every expansion.
- **No `set -euo pipefail`:** a failure in the middle is ignored and the script reports success.
- **Cleaning up at the end of the script only.** If it fails earlier, the temporary folder stays. `trap ... EXIT` runs always.
- **Using `sed -i` without a suffix** (works on Linux, fails on macOS). The `-i.bak` form works on both.
- **Parsing `ls` output** or depending on the current folder. These scripts compute absolute paths first.

## Check yourself

**1. What does `set -e` do?**
Stops the script at the first command that exits with a non-zero status.

**2. What is `trap '...' EXIT` for?**
To run a cleanup command when the script ends, whether it succeeded or failed.

**3. What does `$(...)` do?**
Runs the command inside and replaces the whole expression with its output.

**4. Why does `install_check.sh` leave the repository folder before running the installed command?**
So Python cannot find the source tree by the current folder; success then proves the wheel itself works.

**5. In `mutation_check.sh`, what does a passing test run mean?**
The mutant survived: the tests did not notice the deliberate bug, so the script exits 1.

## Further reading

- GNU Bash reference manual: https://www.gnu.org/software/bash/manual/bash.html ("Shell Parameter Expansion" for `${1:?...}`, "The Set Builtin", "Bourne Shell Builtins" for `trap`). macOS ships bash 3.2; the scripts use only features present there.
- `man sed`, `man grep`, `man mktemp`, `man env` on your system.
