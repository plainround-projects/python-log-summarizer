# import-linter (the dependency rule as a test)

<!-- fmt:off -->

## What it is

An **import** is a line such as `from logsum.domain import request` that makes one module use another. **import-linter** reads all the imports in a package, draws the graph of who imports whom, and checks the graph against rules written in a settings file. A broken rule is a failed check with the offending import path printed. It finds imports by reading the source, not by running it; the graph is built by its helper library **grimp**. Versions: import-linter 2.15, grimp 3.18.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **terminal** is a window where you type a line of text, press Enter, and the computer runs it. The program that reads your line is the **shell** (here `zsh` or `bash`). Everything typed in a terminal is a **command**: a program's name followed by **arguments**, the words that tell it what to do.
- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- A **process** is one running program, with its own memory and a number, its **process id** or **PID**. A program can start other processes, its **children**, and wait for them or stop them.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- Work is **CPU-bound** when the processor is the limit (counting, comparing, hashing) and **I/O-bound** when the program mostly waits for **input/output**: the disk, the network or a database.
- A **hash** (or **digest**) is a short fixed-size fingerprint computed from data. The same data always gives the same fingerprint, and a tiny change gives a completely different one, so equal fingerprints are used to check that two results are identical.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- **Continuous integration (CI)** means a server runs the project's checks automatically every time code is pushed, so a broken change is noticed at once.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.
- A **database** stores data in **tables** of rows and columns. **SQL** is the language for asking it questions (`SELECT`) and changing it (`INSERT`, `UPDATE`). A **transaction** groups changes so that either all of them happen or none does.
- A **cache** is a saved copy of something slow to make, kept so the next request is fast.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- A **dataclass** is a class whose fields are listed once with their types; Python then writes the constructor, the printed form and the equality check for you.
- An **enumeration** (`enum`) is a fixed set of named values, such as the report modes, so a typo is an error instead of a silent new value.
- A **linter** reads code without running it and reports likely mistakes and style problems. A **formatter** rewrites the layout of the code into one agreed style.

## Why this repository uses it

The template says the layers are folders, "domain depends on nothing; application depends on domain; infrastructure and interfaces depend on both; nothing depends on interfaces", and that the rule is "enforced by the linter or a test". A rule that lives only in the README erodes the first time someone is in a hurry. Here a violation fails `make lint` and CI.

## Where it appears

| File | What it does with it |
| --- | --- |
| `pyproject.toml` | `[tool.importlinter]` and two `[[tool.importlinter.contracts]]` tables. |
| `Makefile` | `lint` ends with `lint-imports`, the command import-linter installs. |
| `src/*/domain, application, infrastructure, interfaces` | the four layer folders the contracts name. |

## How it works underneath

`lint-imports` first builds an **import graph** of the root package: one node per module, one edge for each import. With `include_external_packages = true` the graph also gets a node for each installed or standard-library package that the code imports (so rules can mention `sqlite3` or `fastapi`).

A **contract** is one rule. Two types are used:

- **layers**: modules are listed from the top layer to the bottom. A higher layer may import a lower one; a lower layer must never import a higher one, directly or through a chain of other modules. The tool searches the graph for any such upward path and prints it.
- **forbidden**: a set of source modules must not import (directly or indirectly) any module in a forbidden set. Indirect imports count, so a domain module cannot reach `sqlite3` by going through a helper.

The command exits 0 when every contract is kept and 1 when any is broken, which is what `make` and CI look at. The first run builds a cache (`.import_linter_cache/`, ignored by git).

## Walkthrough of this repository's use

```toml
[tool.importlinter]
root_package = "logsum"
include_external_packages = true
```
(`pyproject.toml`, lines 74 to 76)

- `root_package = "logsum"`: the package whose imports are analyzed (the folder `src/logsum`).
- `include_external_packages = true`: add the outside packages the code imports to the graph, so a `forbidden` contract can name them.

```toml
[[tool.importlinter.contracts]]
name = "Domain and application do no I/O and know nothing of the command line"
type = "forbidden"
source_modules = ["logsum.domain", "logsum.application"]
forbidden_modules = ["gzip", "argparse", "tracemalloc", "pathlib", "os", "sys"]
```
(`pyproject.toml`, lines 88 to 92)

The first contract. `name` is the text printed in the report. `type = "layers"` is the contract type. `layers` lists the four layer packages from the top (`interfaces`) to the bottom (`domain`): the command-line and web edge may use everything below it; infrastructure (databases, files, processes) may use the application and domain; the application may use only the domain; the domain uses nothing of this project. The reverse direction is the violation.

The second contract:

```toml
name = "Domain and application do no I/O and know nothing of the command line"
type = "forbidden"
source_modules = ["logsum.domain", "logsum.application"]
forbidden_modules = ["gzip", "argparse", "tracemalloc", "pathlib", "os", "sys"]
```
(`pyproject.toml`, lines 89 to 92)

The second contract is of type `forbidden`: the `source_modules` (domain and application) must not import any of the `forbidden_modules` (`gzip`, `argparse`, `tracemalloc`, `pathlib`, `os`, `sys`), even indirectly. Domain and application do no input or output and know nothing of the command line; those jobs belong to the infrastructure and interfaces layers.

**What a failure looks like.** If someone adds `import gzip` to a domain file, `lint-imports` prints both contracts as `BROKEN`, and names the import chain, for example `logsum.domain.tally -> gzip (l.70)`. (This was tried during development, then undone.)

## Try it yourself

```bash
uv run --frozen lint-imports
```
Expected: a banner, `Analyzed NN files, NNN dependencies.`, then two lines ending in `KEPT` and `Contracts: 2 kept, 0 broken.`

```bash
grep -rn "^import\|^from" src/logsum/domain | grep -v "from __future__\|from logsum.domain\|from dataclasses\|from collections\|from typing" | head
```
Expected: only standard-library imports that the contract allows (for example `datetime`, `statistics`, `array`, `enum`, `bisect`, `hashlib`, `random`), never an import of a higher layer.

To watch a rule break, add a forbidden import to a domain file, run the tool, and undo it:

```bash
cp src/logsum/domain/errors.py /tmp/errors.bak && printf '\nfrom logsum.infrastructure import clock\n' >> src/logsum/domain/errors.py; uv run --frozen lint-imports | grep -E "BROKEN|KEPT"; cp /tmp/errors.bak src/logsum/domain/errors.py
```
Expected: the layers contract shows `BROKEN`. Check `git status` shows no change afterwards.

## Mistakes people make

- **Importing "just one helper" from a higher layer.** The rule exists because this is the shortcut that always looks harmless.
- **Believing only direct imports count.** `forbidden` and `layers` follow chains.
- **Forgetting `include_external_packages`** when a rule names a library: without it the library is not in the graph and the contract is silently empty.
- **Putting the layer rule in the README only.** A rule with no check is a wish.
- **Using a `TYPE_CHECKING` import to dodge the rule.** import-linter counts those imports too, unless configured otherwise.

## Check yourself

**1. What does a `layers` contract allow and forbid?**
A higher layer may import a lower one; a lower layer must not import a higher one, directly or through other modules.

**2. Which layer may import nothing from this project?**
The domain, at the bottom.

**3. What does `include_external_packages = true` add?**
Nodes for imported outside packages, so a rule can forbid, for example, `sqlite3` or `fastapi`.

**4. What is the exit code when a contract is broken?**
1, so `make lint` and CI fail.

**5. How does import-linter find the imports?**
It reads the source code (with grimp), without running it.

## Further reading

- import-linter documentation: https://import-linter.readthedocs.io/en/v2.15/ ("Contract types": layers and forbidden; "Usage").
- grimp, the import graph library: https://grimp.readthedocs.io/
