# pip-audit (vulnerability check)

<!-- fmt:off -->

## What it is

A **vulnerability** here is a security flaw in a published package version, recorded in a public database with an identifier (for example `GHSA-...` or `CVE-...`). **pip-audit** is a program that takes a list of exact package versions and asks a vulnerability database (by default the Python Packaging Advisory Database, through PyPI) whether any of them has a known flaw. Version here: 2.10.1.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A **pipe**, written `|`, sends the standard output of the command on its left into the standard input of the command on its right, for example `sort file | head -3`.
- A **redirection** sends a channel somewhere else. `> file` writes standard output to a file, `2>&1` sends standard error to wherever standard output goes, and `/dev/null` is a special file that throws away whatever is written to it.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- An **environment variable** is a named piece of text that a program inherits from the program that started it, for example `PORT=9000`. Programs read them to find out their settings without a settings file. In a shell, `NAME=value command` sets a variable for that one command.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **lock** lets only one thread at a time run a protected piece of code; the others wait. It is how threads avoid changing the same data at the same moment.
- A **hash** (or **digest**) is a short fixed-size fingerprint computed from data. The same data always gives the same fingerprint, and a tiny change gives a completely different one, so equal fingerprints are used to check that two results are identical.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- **Continuous integration (CI)** means a server runs the project's checks automatically every time code is pushed, so a broken change is noticed at once.
- A **lock file** records the exact version and checksum of every package the project uses, so installing again gives byte-for-byte the same environment.
- A **database** stores data in **tables** of rows and columns. **SQL** is the language for asking it questions (`SELECT`) and changing it (`INSERT`, `UPDATE`). A **transaction** groups changes so that either all of them happen or none does.
- A **cache** is a saved copy of something slow to make, kept so the next request is fast.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- **Serialization** turns an object in memory into bytes or text that can be saved or sent. **Pickle** is Python's format for it; a process pool pickles every argument and result to move them between processes.

## Why this repository uses it

The template's Security rule reads: "dependencies pinned with a lock file and checked by the CI's audit step". `make audit` exports the locked packages and checks every one of them, so a flaw published tomorrow in a package locked today turns the next CI run red.

## Where it appears

| File | What it does with it |
| --- | --- |
| `Makefile` | `audit` exports the lock file, runs pip-audit on it and deletes the export. |
| `.github/workflows/ci.yml` | runs `make audit`. |
| `uv.lock` | the list of exact versions that is checked. |

## How it works underneath

pip-audit does two things. It reads the exact versions to check, from an installed environment or from a requirements file. Then it sends the package names and versions to the database service and prints a table of any matches: package, installed version, vulnerability id, and the version that fixes it. With no matches it prints `No known vulnerabilities found`. It needs the network.

Two options matter here. `--no-deps` says "check only the packages in the file; do not work out their dependencies again" (the file already lists everything, because it came from the lock). `--disable-pip` says "do not use pip to resolve anything"; the combination requires that the file has hashes or exact pins, which an `uv export` file does.

## Walkthrough of this repository's use

```make
audit: ## check the locked dependencies for known vulnerabilities
	$(UV) export --frozen --no-emit-project --format requirements-txt --output-file .audit-requirements.txt
	$(RUN) pip-audit --no-deps --disable-pip -r .audit-requirements.txt
	rm -f .audit-requirements.txt
```
(`Makefile`, lines 49 to 52)

1. `uv export --frozen --no-emit-project --format requirements-txt --output-file .audit-requirements.txt` writes the locked packages (see `uv.md`).
2. `$(RUN) pip-audit --no-deps --disable-pip -r .audit-requirements.txt` runs pip-audit from the project environment. `-r` names the requirements file to read. Exit code 0 means no known flaws; 1 means at least one was found.
3. `rm -f .audit-requirements.txt` removes the file (`-f` makes `rm` quiet if it is missing).

Because the audit runs against the lock, it is the lock that is judged, not whatever is installed on the machine.

During development the output also contained many lines `WARNING:cachecontrol.controller:Cache entry deserialization failed, entry ignored`: pip-audit keeps an HTTP cache, and an old cache entry could not be read by the newer library. They are harmless; the last line decides.

## Try it yourself

```bash
make audit 2>&1 | tail -3
```
Expected (needs the network): a line `No known vulnerabilities found`, then `rm -f .audit-requirements.txt`.

```bash
uv run --frozen pip-audit --version
```
Expected: `pip-audit 2.10.1`.

```bash
ls .audit-requirements.txt
```
Expected: `No such file or directory`: the target cleaned up after itself.

## Mistakes people make

- **Auditing the wrong thing.** Auditing the installed environment can miss what the lock says; auditing the lock export checks what a fresh install will get.
- **Ignoring the exit code.** A pipe such as `pip-audit | tail` hides a failure; the Makefile runs it directly.
- **Running it offline.** The check needs the database service; offline it fails, which CI would also report.
- **Treating "no known vulnerabilities" as "secure".** It means none are published for these versions.
- **Pinning to silence a finding without updating.** The fix is a newer locked version (`uv lock --upgrade-package <name>`).

## Check yourself

**1. What does pip-audit compare?**
Exact package versions (from the exported lock) against a database of published vulnerabilities.

**2. Why does `make audit` export the lock first?**
pip-audit reads a requirements file; the export turns `uv.lock` into one, with the exact versions and hashes.

**3. What do `--no-deps` and `--disable-pip` do?**
`--no-deps` checks only the listed packages without resolving more; `--disable-pip` stops it using pip to resolve.

**4. Why does CI run the audit on every push?**
A new flaw in an already locked package makes the next run fail, so it is noticed.

**5. What would you do if it reports a flaw in a locked package?**
Upgrade that package in the lock (`uv lock --upgrade-package <name>`), run the tests, commit the new lock.

## Further reading

- pip-audit on PyPI and GitHub: https://pypi.org/project/pip-audit/ (version 2.10.1).
- Python Packaging Advisory Database: https://github.com/pypa/advisory-database
