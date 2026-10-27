# Hatchling (the build backend)

<!-- fmt:off -->

## What it is

A **build backend** is the program that turns a project's source into a package that can be installed. Hatchling is a build backend from the Hatch project. Its output is a **wheel** (a `.whl` file, which is a zip archive with a standard layout and name) and a **source distribution** (a `.tar.gz` of the source). Hatchling is not a command you type: tools such as `uv build` or `pip` call it.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- An **environment variable** is a named piece of text that a program inherits from the program that started it, for example `PORT=9000`. Programs read them to find out their settings without a settings file. In a shell, `NAME=value command` sets a variable for that one command.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **lock** lets only one thread at a time run a protected piece of code; the others wait. It is how threads avoid changing the same data at the same moment.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- A **lock file** records the exact version and checksum of every package the project uses, so installing again gives byte-for-byte the same environment.
- An **entry point** (or **console script**) is a command, such as `logsum`, that the installer creates and that starts a named Python function.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.

## Why this repository uses it

The lesson ends by installing the project "like a user would" from a built wheel. Something has to build that wheel. Hatchling needs very little configuration for a `src/` layout and has no setup script to maintain.

## Where it appears

| File | What it does with it |
| --- | --- |
| `pyproject.toml` | `[build-system]` names Hatchling; `[tool.hatch.build.targets.wheel]` says which folder to package. |
| `Makefile` | `build` runs `uv build`; the install check builds a wheel too. |
| `scripts/` | any script that installs from `dist/` relies on the wheel Hatchling built. |

## How it works underneath

When you run `uv build`, uv does this:

1. reads `[build-system] requires` and installs those packages (Hatchling, here) into a throwaway environment;
2. imports the module named in `build-backend` (`hatchling.build`) and calls its standard functions `build_sdist` and `build_wheel` (the interface defined by PEP 517);
3. Hatchling reads the rest of `pyproject.toml`, collects the files named by the wheel table, writes the `METADATA` file (name, version, description, dependencies), writes entry points for `[project.scripts]`, zips everything, and returns the wheel's name;
4. uv puts the results in `dist/`.

A wheel installs by unpacking: its `site-packages` part is copied into the environment and the launcher files are written. An **editable install** (what `uv sync` does for the project itself) instead writes a small `.pth` file that points at `src/`, so edits to the source take effect without rebuilding.

The `requires = ["hatchling>=1.25"]` rule is a lower bound and is **not locked** by `uv.lock`: the build environment is temporary. The build on the development machine used Hatchling 1.32.4.

## Walkthrough of this repository's use

```toml
[build-system]
requires = ["hatchling>=1.25"]
build-backend = "hatchling.build"
```
(`pyproject.toml`, lines 1 to 3)

- `requires = ["hatchling>=1.25"]`: install Hatchling 1.25 or newer before building.
- `build-backend = "hatchling.build"`: the Python module that exposes the PEP 517 functions.

```toml
[tool.hatch.build.targets.wheel]
packages = ["src/logsum"]
```
(`pyproject.toml`, lines 32 to 33)

`[tool.hatch.build.targets.wheel]` configures the *wheel* target (Hatchling has others, such as `sdist`). `packages = ["src/logsum"]` lists the folders to include, with the part before the last slash removed inside the wheel: the folder `src/<package>` is installed as the top-level package `<package>`. Without this line Hatchling looks for a folder named after the project and finds none.

The rest of `[project]` (name, version, readme, license, scripts) is read by Hatchling too; the `readme` file must exist or the build stops, which is why a first `uv add` before the README existed failed during this project's creation.

## Try it yourself

```bash
uv build --out-dir /tmp/wheel-demo
```
Expected: `Building source distribution...`, `Building wheel from source distribution...`, then two `Successfully built ...` lines.

```bash
ls /tmp/wheel-demo
```
Expected: one `.tar.gz` and one `.whl` file, named with the project name and version.

```bash
python3 -m zipfile -l /tmp/wheel-demo/*.whl | grep -E "dist-info|__init__"
```
Expected: the package's `__init__.py` files and the `*.dist-info/` files `METADATA`, `WHEEL`, `RECORD` and `entry_points.txt` (the launchers).

```bash
rm -r /tmp/wheel-demo
```

## Mistakes people make

- **Wrong `packages` path.** If it names a folder that does not exist, the wheel is empty and the command fails with `ModuleNotFoundError` after installation.
- **Missing README or license file** that `pyproject.toml` names: the build stops.
- **Thinking the build backend is locked.** It is resolved fresh for each build; pin it (`hatchling==1.32.4`) if exact reproducibility of the wheel matters.
- **Testing only the editable install.** An editable install can work when the wheel is broken (for example when a data file is not packaged); that is why the repository builds and installs the wheel in a clean environment.

## Check yourself

**1. What is a wheel?**
A zip archive, with the extension `.whl`, in a standard layout, containing the package's files and metadata; installing it is unpacking it.

**2. What does `build-backend = "hatchling.build"` tell a tool?**
Which Python module to import and call (`build_wheel`, `build_sdist`) to build the project.

**3. Why is the `packages` line needed here?**
The source is under `src/`, and the folder name does not match what Hatchling would look for by default.

**4. How is an editable install different from installing a wheel?**
An editable install points the environment at the source folder through a `.pth` file, so edits apply at once; a wheel install copies the files.

**5. Is the version of Hatchling used for a build recorded in `uv.lock`?**
No. It is installed in a temporary build environment from the rule `hatchling>=1.25`, so it can differ between builds.

## Further reading

- Hatch / Hatchling documentation: https://hatch.pypa.io/latest/ (build backend, "Build configuration"; version 1.32.4 was used here).
- PEP 517, build system interface: https://peps.python.org/pep-0517/
- Python Packaging User Guide, "Packaging Python projects": https://packaging.python.org/en/latest/tutorials/packaging-projects/
