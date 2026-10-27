# JSON and JSON Schema (and the `jsonschema` library)

<!-- fmt:off -->

## What it is

**JSON** is a text format for data: objects `{"key": value}`, lists `[1, 2]`, strings, numbers, `true`, `false`, `null`. Almost every language can read and write it, which makes it the usual way for one program's output to become another's input. A **JSON Schema** is a JSON document that describes what a valid JSON document looks like (which keys, which types, which ranges). The Python library **`jsonschema`** (version 4.26.0) checks a document against a schema and raises an error that says what is wrong.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- An **argument** is a word given to a command. An **option** (also called a **flag**) is an argument that starts with a hyphen, such as `--help` or `-n`, and changes how the command behaves; some take a value (`--output result.txt`).
- A program has three channels: **standard input** (what it reads), **standard output** (what it prints normally) and **standard error** (where it prints problems and progress). They are separate so a pipe or a file can take the output while errors still show on the screen.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- **Latency** is how long one request takes. A **percentile** says what share of requests were at least that fast: **p95** is the time that 95 out of 100 requests beat, so it shows how bad the slow tail is, which an average hides.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.

## Why this repository uses it

The lesson's third stretch goal: "Add a `--json` output and a test that checks it against a schema." Other programs will read `logsum --json`, so its shape is a promise. The schema writes the promise down, and a test keeps the program to it.

## Where it appears

| File | What it does with it |
| --- | --- |
| `docs/summary.schema.json` | the schema of the `--json` output. |
| `src/logsum/interfaces/render.py` | `render_json` builds the document and prints it with `json.dumps`. |
| `tests/conftest.py` | loads the schema as a fixture. |
| `tests/unit/interfaces/test_cli.py` | validates the output with `jsonschema.validate`. |
| `pyproject.toml` | `jsonschema` and `types-jsonschema` in the development group. |

## How it works underneath

JSON is parsed into the language's own types: in Python, objects become dictionaries, lists become lists, `null` becomes `None`. `json.dumps(value, indent=2)` goes the other way and returns text; `indent=2` adds line breaks and two-space indentation. Object keys must be strings, so the status codes (integers) are turned into strings (`"200"`) before dumping.

`jsonschema.validate(instance, schema)` walks the instance and the schema together. Each schema keyword is a rule: `type` (a JSON type), `required` (keys that must be present), `properties` (a schema per key), `additionalProperties: false` (no keys other than the listed ones), `minimum`, `pattern` (a regular expression), `items` (a schema for each list element). The first mismatch raises `ValidationError` naming the path in the document.

## Walkthrough of this repository's use

**Building the document.**

```python
def render_json(report: RunReport, *, show_stats: bool) -> str:
    """The same summary as JSON, described by docs/summary.schema.json."""
    summary = report.summary
    document: dict[str, object] = {
        "total_requests": summary.total_requests,
        "bad_lines": summary.bad_lines,
        "statuses": {str(status): count for status, count in summary.status_counts.items()},
        "slowest_paths": [
            {"path": entry.path, "p95_ms": round(entry.p95_ms, 2), "requests": entry.requests}
            for entry in summary.slowest_paths
        ],
    }
    if show_stats:
        document["stats"] = {
            "elapsed_seconds": round(report.elapsed_seconds, 3),
            "peak_memory_bytes": report.peak_memory_bytes,
        }
    return json.dumps(document, indent=2)
```
(`src/logsum/interfaces/render.py`, lines 26 to 43)

`dict[str, object]` types the dictionary: text keys, values of any kind. `{str(status): count for ...}` is a **dictionary comprehension** that makes the status codes text. `round(entry.p95_ms, 2)` keeps two decimals. `stats` is added only with `--stats`. The function returns text; `main` prints it to standard output.

**The schema.**

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.invalid/logsum/summary.schema.json",
  "title": "logsum summary",
  "description": "The document `logsum --json` prints.",
  "type": "object",
  "additionalProperties": false,
  "required": ["total_requests", "bad_lines", "statuses", "slowest_paths"],
  "properties": {
    "total_requests": { "type": "integer", "minimum": 0, "description": "Lines that parsed as requests." },
    "bad_lines": { "type": "integer", "minimum": 0, "description": "Lines that could not be parsed: counted, never fatal." },
    "statuses": {
      "type": "object",
      "description": "Requests per HTTP status code; the keys are the codes as strings.",
      "propertyNames": { "pattern": "^[1-5][0-9]{2}$" },
      "additionalProperties": { "type": "integer", "minimum": 1 }
    },
    "slowest_paths": {
      "type": "array",
      "description": "Paths by 95th-percentile latency, slowest first.",
      "items": {
        "type": "object",
        "additionalProperties": false,
        "required": ["path", "p95_ms", "requests"],
        "properties": {
          "path": { "type": "string", "pattern": "^/" },
          "p95_ms": { "type": "number", "minimum": 0 },
          "requests": { "type": "integer", "minimum": 1 }
        }
      }
    },
    "stats": {
      "type": "object",
      "description": "Present with --stats.",
      "additionalProperties": false,
      "required": ["elapsed_seconds", "peak_memory_bytes"],
      "properties": {
        "elapsed_seconds": { "type": "number", "minimum": 0 },
        "peak_memory_bytes": { "type": ["integer", "null"], "minimum": 0 }
      }
    }
  }
}
```
(`docs/summary.schema.json`, lines 1 to 43)

- `"$schema"` and `"$id"`: which version of the JSON Schema language this is (2020-12), and a name for this schema (the address is a placeholder; nothing is fetched from it).
- `"type": "object"`, `"additionalProperties": false`: the document is an object with no unlisted keys. A typo such as `bad_line` in the program would fail the test.
- `"required"`: the four keys that must be present; `stats` is optional.
- `"statuses"`: an object whose keys must match `^[1-5][0-9]{2}$` (three digits starting 1 to 5, a regular expression) and whose values are integers of at least 1.
- `"slowest_paths"`: a list; each item is an object with `path` (text starting with `/`), `p95_ms` (a number, 0 or more) and `requests` (an integer, 1 or more), and nothing else.
- `"stats"`: `elapsed_seconds` and `peak_memory_bytes`, which may be `null` (`"type": ["integer", "null"]`) when memory was not measured.

**The test.**

```python
def test_json_output_follows_the_published_schema(data_dir, summary_schema):
    code, out, _ = run(str(data_dir / "two_paths.log"), "--json", "--stats")
    assert code == 0
    document = json.loads(out)
    validate(document, summary_schema)
    assert document["bad_lines"] == 3
```
(`tests/unit/interfaces/test_cli.py`, lines 40 to 45)

`validate(document, summary_schema)` raises `ValidationError` if the output breaks the schema. `summary_schema` is a fixture that loads the file (see `tests/conftest.py`). Types for the library come from `types-jsonschema` so mypy can check the calls.

## Try it yourself

```bash
uv run --frozen logsum data/small.log --json
```
Expected: a JSON document with `total_requests`, `bad_lines`, `statuses` and `slowest_paths` (`"p95_ms": 19.95`).

```bash
uv run --frozen logsum data/small.log --json | python3 -c "import json,sys; d=json.load(sys.stdin); print(sorted(d))"
```
Expected: `['bad_lines', 'slowest_paths', 'statuses', 'total_requests']`.

```bash
uv run --frozen python - <<'EOF'
import json
from jsonschema import validate, ValidationError
schema = json.load(open("docs/summary.schema.json"))
try:
    validate({"total_requests": 1, "bad_lines": 0, "statuses": {}, "slowest_paths": [], "extra": 1}, schema)
except ValidationError as error:
    print(error.message)
EOF
```
Expected: ``Additional properties are not allowed ('extra' was unexpected)``.

## Mistakes people make

- **Integer keys in JSON.** JSON object keys are always text; Python's `json.dumps` silently converts integer keys, which can surprise a reader.
- **A schema nobody tests.** An unused schema drifts; this one is validated in a test.
- **Forgetting `additionalProperties: false`.** Without it extra keys pass.
- **Treating `NaN` as JSON.** It is not valid JSON, even though Python can print it.

## Check yourself

**1. What are the six JSON value kinds?**
Object, list (array), string, number, true/false (boolean) and null.

**2. What does `additionalProperties: false` do?**
Rejects any key the schema does not list.

**3. Why are status codes turned into strings before dumping?**
JSON object keys must be text.

**4. What does `jsonschema.validate` do when the document is wrong?**
Raises `ValidationError` with a message and the path to the offending part.

**5. Why is `peak_memory_bytes` allowed to be `null`?**
It is `None` when `--stats` was not given, so memory was not measured.

## Further reading

- JSON: https://www.json.org/ and RFC 8259 https://www.rfc-editor.org/rfc/rfc8259 ; `json` module: https://docs.python.org/3.14/library/json.html
- JSON Schema 2020-12: https://json-schema.org/draft/2020-12 ; `jsonschema` 4.26.0: https://python-jsonschema.readthedocs.io/en/v4.26.0/
