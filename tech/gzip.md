# gzip (compressed logs)

<!-- fmt:off -->

## What it is

**gzip** is a way to compress a file: the same information in fewer bytes. A file whose name ends in `.gz` is in this format. Python's standard `gzip` module opens such a file and, if you ask for text mode, gives you decompressed lines as you read them.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- Every program, when it ends, hands back a whole number called its **exit code**. `0` means success; any other number means a failure. The shell shows the last one in `$?`, and tools such as `make` and CI stop when a command returns a non-zero code.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **generator** is a function that uses `yield` to hand out values one at a time and pause in between, so a huge sequence never has to exist in memory all at once.
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- A **fake** (or **mock**, or **stub**) is a simple stand-in for a real part of the system, such as a clock that only moves when the test says so, used so a test is fast and gives the same result every time.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.

## Why this repository uses it

The lesson's first stretch goal: read gzip-compressed logs "transparently with `gzip.open` when the file ends in `.gz`". Real logs are rotated and compressed; the tool must read them without unpacking them first (which would need disk space for the whole file and defeat the streaming).

## Where it appears

| File | What it does with it |
| --- | --- |
| `src/logsum/infrastructure/log_files.py` | `_open_text` picks `gzip.open` for `.gz` names. |
| `tests/integration/test_real_files.py` | real gzip files: a good one, a truncated one, and a text file that is wrongly named `.gz`. |
| `tests/e2e/test_lesson_scenario.py` | the 500,000-line log compressed, summarized, and compared with the plain summary. |

## How it works underneath

Compression finds repeated patterns and writes them in a shorter form. The gzip format stores the compressed bytes in blocks with a header and a checksum at the end. Reading is **streaming**: the decompressor takes a few kilobytes of compressed data, produces some text, and continues, so memory stays small even for a very large file. Because the checksum is at the end, a file that was cut short is only found out when the reader reaches the missing part, as an `EOFError`; a file that is not gzip at all fails at the first read with `BadGzipFile` (a kind of `OSError`).

## Walkthrough of this repository's use

```python
    def _open_text(path: Path) -> TextIO:
        if path.suffix == ".gz":
            return gzip.open(path, "rt", encoding=_ENCODING, errors="replace")
        return path.open(encoding=_ENCODING, errors="replace")
```
(`src/logsum/infrastructure/log_files.py`, lines 35 to 38)

- `path.suffix == ".gz"`: the file name's last extension.
- `gzip.open(path, "rt", encoding=..., errors="replace")`: open for reading (`r`) in **text** mode (`t`), so lines arrive as text and not as bytes. `errors="replace"` swaps bytes that are not valid UTF-8 for the replacement character (a diamond with a question mark) instead of raising, so one bad byte sequence becomes one more bad line.
- `path.open(encoding=..., errors="replace")` is the same for a plain file.

```python
    def _lines(handle: TextIO, location: str) -> Iterator[str]:
        try:
            yield from handle
        except (OSError, EOFError) as error:
            raise UnreadableLogFileError(location, str(error)) from error
```
(`src/logsum/infrastructure/log_files.py`, lines 41 to 45)

`yield from handle` hands out the lines one by one. Errors that can only appear **while reading** (a truncated or corrupted gzip file raises `EOFError` or `OSError`) are caught here and re-raised as the named `UnreadableLogFileError`, because opening a gzip file succeeds even when its end is missing. The user gets `logsum: cannot read ...`, exit code 1, and no traceback.

## Try it yourself

```bash
gzip -k -c data/small.log > /tmp/small.log.gz && uv run --frozen logsum /tmp/small.log.gz | head -3
```
Expected (after `make up`): the same summary as for `data/small.log` (`statuses: {200: 20}` and the 19.95 line).

```bash
head -c 50 /tmp/small.log.gz > /tmp/cut.log.gz; uv run --frozen logsum /tmp/cut.log.gz; echo "exit code $?"
```
Expected: one logfmt line with `level=ERROR ... msg="cannot read the log"`, then `logsum: cannot read /tmp/cut.log.gz: Compressed file ended before the end-of-stream marker was reached`, and `exit code 1`.

```bash
echo "not gzip" > /tmp/fake.log.gz; uv run --frozen logsum /tmp/fake.log.gz; echo "exit code $?"; rm /tmp/small.log.gz /tmp/cut.log.gz /tmp/fake.log.gz
```
Expected: the same two lines with the reason `Not a gzipped file (b'no')`, and `exit code 1`.

## Mistakes people make

- **Unpacking before reading.** It costs disk space and time; stream instead.
- **Opening in binary mode and forgetting to decode.** `"rt"` gives text.
- **Assuming an open succeeds means the file is intact.** Errors surface during reading.
- **Trusting the extension.** A file called `.gz` may not be gzip; the error path above handles it.

## Check yourself

**1. What does mode `"rt"` mean?**
Read (`r`), as text (`t`): you get decoded lines, not bytes.

**2. Why can a truncated gzip file be opened successfully?**
The header is at the start and is intact; the damage is found only when the reader reaches the missing end.

**3. What does `errors="replace"` do?**
Replaces undecodable bytes with a replacement character instead of raising an error.

**4. Why not decompress the file to disk first?**
It needs disk space for the whole file and breaks the lesson's memory goal; streaming reads a little at a time.

**5. Which named error does the user see for a damaged file?**
`UnreadableLogFileError`, printed as `logsum: cannot read ...` with exit code 1.

## Further reading

- `gzip` module: https://docs.python.org/3.14/library/gzip.html ; the gzip file format (RFC 1952): https://www.rfc-editor.org/rfc/rfc1952
