# mypy (the static type checker)

<!-- fmt:off -->

## What it is

A **type hint** is a note in the code that says what kind of value a variable, a parameter or a return value holds: `def parse(line: str) -> Request | None`. Python itself ignores hints when it runs. **mypy** is a separate program that reads the code and the hints, without running anything, and reports places where the code contradicts them (passing a number where text is expected, using a value that may be `None`, calling a function that does not exist). This is called *static* checking, because it happens before the program runs. Version here: 2.4.0.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **terminal** is a window where you type a line of text, press Enter, and the computer runs it. The program that reads your line is the **shell** (here `zsh` or `bash`). Everything typed in a terminal is a **command**: a program's name followed by **arguments**, the words that tell it what to do.
- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- **JSON** is a text format for data: objects `{"name": "x", "count": 3}` (names with values), lists `[1, 2, 3]`, text in double quotes, numbers, `true`, `false` and `null`. Almost every language can read and write it, which makes it the usual way programs exchange data.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- The **interpreter** is the program that reads Python source files and carries them out. `python` starts it. **CPython** is the standard one, written in C.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **decorator** is a line starting with `@` above a function or class. It passes the function to another function that wraps or registers it, for example `@pytest.fixture` or `@dataclass`.
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **fake** (or **mock**, or **stub**) is a simple stand-in for a real part of the system, such as a clock that only moves when the test says so, used so a test is fast and gives the same result every time.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- **Continuous integration (CI)** means a server runs the project's checks automatically every time code is pushed, so a broken change is noticed at once.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.
- A **cache** is a saved copy of something slow to make, kept so the next request is fast.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.
- A **protocol** is a description of the methods an object must have, without saying which class it is. In this repository's architecture a **port** is such a description of what the inner layers need, and an **adapter** is a class in the outer layer that does the real work behind it.

## Why this repository uses it

The template asks for "typed code" checked in CI, and the lesson's step 2 asks for strict mode to pass. Types document each function's contract and catch a class of mistakes (such as forgetting that `parse` can return `None`) that tests only find if someone writes the right test.

## Where it appears

| File | What it does with it |
| --- | --- |
| `pyproject.toml` | `[tool.mypy]` and its `[[tool.mypy.overrides]]` for the tests. |
| `Makefile` | `lint` runs `mypy` with no arguments, so it checks `files`. |
| `src/` | every function is fully annotated; strict mode requires it. |
| `tests/` | type-checked too, with the annotation requirement relaxed for test functions. |

## How it works underneath

mypy builds a model of every module: the classes, the functions with their parameter and return types, and the types of variables. It then walks each function body and, for each expression, works out the type and checks it against what is expected. When a function returns `Request | None`, mypy *narrows* the type after a check: after `if request is None: return`, it knows `request` is a `Request`. Code that skips the check and uses `request.status` is an error.

Libraries ship type information in two ways: inline hints (and a `py.typed` marker file) or separate "stub" packages (here `types-jsonschema` where used). A library with neither is treated as untyped.

mypy keeps a cache folder (`.mypy_cache/`, ignored by git) so the second run only rechecks changed files. It exits with 0 when it finds nothing and 1 otherwise.

## Walkthrough of this repository's use

```toml
[tool.mypy]
python_version = "3.12"
strict = true
files = ["src", "tests", "scripts/compare_memory.py"]

# Test functions are named for the behavior they check; annotating every one adds noise, not safety.
```
(`pyproject.toml`, lines 46 to 51)

- `python_version = "3.12"`: the Python version to assume when checking (it decides which built-in types and syntax exist).
- `strict = True`: turns on a bundle of the strictest checks at once (see below).
- `files = ["src", "tests", "scripts/compare_memory.py"]`: what to check when `mypy` is run with no arguments.

**What `strict = true` switches on.** `strict` is one switch that turns on thirteen separate checks. `mypy --help` of the pinned version 2.4.0 lists them as: `--disallow-any-generics`, `--disallow-subclassing-any`, `--disallow-untyped-calls`, `--disallow-untyped-defs`, `--disallow-incomplete-defs`, `--check-untyped-defs`, `--disallow-untyped-decorators`, `--warn-redundant-casts`, `--warn-unused-ignores`, `--warn-return-any`, `--no-implicit-reexport`, `--strict-equality` and `--extra-checks`. In a settings file the same names are written with underscores. Each one, in plain words:

- `disallow_any_generics`: a *generic* type must say what it holds. `list` alone is an error; `list[int]` is right. (`Any`, in a type hint, is the type that switches checking off for a value.)
- `disallow_subclassing_any`: a class may not inherit from something whose type is `Any`, for example a class imported from a library that has no type information.
- `disallow_untyped_calls`: a function that has type hints may not call a function that has none, because the answer would be `Any`.
- `disallow_untyped_defs`: every `def` must have type hints on all its parameters and on its return value.
- `disallow_incomplete_defs`: a `def` with hints on only some of its parameters is an error.
- `check_untyped_defs`: look inside functions that have no hints too (mypy skips their bodies by default).
- `disallow_untyped_decorators`: a function that has hints may not be wrapped by a decorator that has none, because the wrapped function would lose its types.
- `warn_redundant_casts`: a `cast(...)` that changes nothing is an error.
- `warn_unused_ignores`: a `# type: ignore` comment that hides no error is an error, so old exceptions do not pile up.
- `warn_return_any`: a function declared to return a specific type may not return a value whose type is `Any`.
- `no_implicit_reexport`: a name that a module only imported is not part of that module's public names unless it is re-exported on purpose (`from x import y as y`, or listed in `__all__`); importing it from there is an error.
- `strict_equality`: comparing values of types that can never be equal (`1 == "1"`, or `x in some_list_of_strings` for an `int`) is an error.
- `extra_checks`: further checks that are correct but strict: for example, partial overlap in `TypedDict` updates is refused, and arguments added with `Concatenate` become positional-only.

Implicit `Optional` (a parameter written `x: int = None`) is an error in every mypy version since 0.990, with or without strict; it is not part of the bundle.

```toml
[[tool.mypy.overrides]]
module = ["tests.*"]
disallow_untyped_defs = false
disallow_incomplete_defs = false
disallow_untyped_calls = false
```
(`pyproject.toml`, lines 52 to 56)

The override applies only to modules matching `tests.*`. It turns three strict checks back off for test code: `disallow_untyped_defs`, `disallow_incomplete_defs` and `disallow_untyped_calls`. The comment above it in the file gives the reason: test functions are named for the behavior they check, and annotating every one adds noise, not safety. The tests are still type-checked: a call with the wrong argument type is still an error.



**The call.** In the Makefile's `lint` target the line is simply:

```make
	$(RUN) mypy
```
(`Makefile`, line 42)

with no file arguments, so mypy uses `files` from the settings above.

## Try it yourself

```bash
uv run --frozen mypy --version
```
Expected: `mypy 2.4.0 (compiled: yes)`.

```bash
uv run --frozen mypy
```
Expected: `Success: no issues found in NN source files`.

```bash
printf 'def double(x: int) -> int:\n    return x * 2\n\ndouble("a")\n' > /tmp/demo_types.py && uv run --frozen mypy --strict /tmp/demo_types.py; rm /tmp/demo_types.py
```
Expected: `error: Argument 1 to "double" has incompatible type "str"; expected "int"  [arg-type]` and `Found 1 error in 1 file`.

```bash
printf 'def first(items):\n    return items[0]\n' > /tmp/demo_untyped.py && uv run --frozen mypy --strict /tmp/demo_untyped.py; rm /tmp/demo_untyped.py
```
Expected: `error: Function is missing a type annotation  [no-untyped-def]`: strict mode refuses unannotated functions.

## Mistakes people make

- **Adding `# type: ignore` to silence an error.** Strict mode reports an ignore that suppresses nothing, but a needed ignore hides a real problem. This repository's source has almost none, each with a reason.
- **Using `Any` to make errors go away.** `Any` switches checking off for that value. Prefer a precise type or a `Protocol`.
- **Believing types are checked at run time.** They are not; mypy runs before the program. Boundaries that get data from outside (files, HTTP) validate it separately.
- **Annotating with `list` instead of `list[int]`.** Strict mode rejects bare generics.
- **Forgetting to check for `None`.** The checker will not let you.

## Check yourself

**1. Does Python check type hints when the program runs?**
No. The interpreter ignores them. mypy is a separate program that checks them before the program runs.

**2. What does `strict = true` require of every function?**
Annotations on all parameters and the return value, among other checks.

**3. What does narrowing mean?**
After a check such as `if x is None: return`, mypy knows `x` has the non-`None` type for the rest of the function.

**4. Why does the test override relax three checks?**
Test functions are named for the behavior they check and annotating each adds noise, not safety; the rest of strict mode still applies to tests.

**5. What does the command `mypy` with no arguments check?**
The paths listed in `files` in `[tool.mypy]`.

## Further reading

- mypy documentation: https://mypy.readthedocs.io/en/stable/ (version 2.4.0 here): "Command line", "The mypy configuration file", "Type narrowing".
- Python typing documentation: https://docs.python.org/3.14/library/typing.html and the typing specification at https://typing.python.org/.
