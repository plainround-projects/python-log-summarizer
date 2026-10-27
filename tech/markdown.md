# Markdown

<!-- fmt:off -->

## What it is

**Markdown** is a way of writing formatted text in a plain text file. You mark structure with a few ordinary characters: a line starting with `#` is a heading, a line starting with `-` is a bullet, text between backticks is code. A program called a **renderer** (GitHub, your editor's preview, or the `markdown` library) turns the marks into headings, lists and tables on screen. Because the file itself is plain text, you can read it unrendered, write it in any editor, and store it in git, which shows exactly which words changed.

A file written in Markdown has the ending `.md`. There is no single official Markdown: the common core is described by the **CommonMark** specification, and GitHub adds a few extras (tables, task lists, automatic links) called **GitHub Flavored Markdown**. This repository uses only the common core and tables.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- **JSON** is a text format for data: objects `{"name": "x", "count": 3}` (names with values), lists `[1, 2, 3]`, text in double quotes, numbers, `true`, `false` and `null`. Almost every language can read and write it, which makes it the usual way programs exchange data.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **generator** is a function that uses `yield` to hand out values one at a time and pause in between, so a huge sequence never has to exist in memory all at once.
- Work is **CPU-bound** when the processor is the limit (counting, comparing, hashing) and **I/O-bound** when the program mostly waits for **input/output**: the disk, the network or a database.
- **Latency** is how long one request takes. A **percentile** says what share of requests were at least that fast: **p95** is the time that 95 out of 100 requests beat, so it shows how bad the slow tail is, which an average hides.
- A **hash** (or **digest**) is a short fixed-size fingerprint computed from data. The same data always gives the same fingerprint, and a tiny change gives a completely different one, so equal fingerprints are used to check that two results are identical.
- A **regular expression** is a compact pattern for matching text, for example `^[a-z-]+:` means 'starts with lowercase letters and hyphens, then a colon'.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- A **linter** reads code without running it and reports likely mistakes and style problems. A **formatter** rewrites the layout of the code into one agreed style.

## Why this repository uses it

The project template asks every repository for a README (what it is and how to run it), an architecture document, a changelog and decision records, all kept next to the code and changed in the same commits as the code. Markdown is the format that every code host shows nicely and that needs no tools to write. Writing the documents as text files means a reviewer sees a documentation change in the same diff as the code change.

These `tech/` notes are Markdown too.

## Where it appears

| File | What it does with it |
| --- | --- |
| `ARCHITECTURE.md` | the components, the data flow, the decisions, what production would add. |
| `CHANGELOG.md` | what changed in each released version. |
| `README.md` | what the project is, how to run it, the measured results. |
| `docs/adr/0001-stream-with-a-generator-and-count-bad-lines-in-an-object.md` | a decision record (ADR): one decision, its context and its consequences. |
| `docs/adr/0002-ports-and-adapters-with-four-layers.md` | a decision record (ADR): one decision, its context and its consequences. |
| `docs/adr/0003-percentile-definition.md` | a decision record (ADR): one decision, its context and its consequences. |
| `docs/adr/0004-fixed-size-histogram-estimator.md` | a decision record (ADR): one decision, its context and its consequences. |
| `tech/*.md` | these notes. |
| `.editorconfig` | the `[*.md]` section keeps trailing spaces, which Markdown uses for line breaks. |

## How it works underneath

A renderer reads the file line by line and decides what each block is.

- **Blocks** are separated by blank lines. A *paragraph* is consecutive text lines. A line starting with one to six `#` characters and a space is a *heading* of that level (`#` is the title, `##` a section, `###` a subsection). A line starting with `- ` (or `1. `) begins a *list item*; an indented line continues it. A fence of three backticks (```` ``` ````) starts and ends a *code block*; the text after the opening fence (`bash`, `python`) names the language so colors can be applied; nothing inside is interpreted.
- **Inline marks** work inside a block: `**bold**`, `*italic*`, `` `code` `` and `[text](address)` for a link. A link address without `http` is *relative*: it points to another file in the repository.
- **Tables** (a GitHub extension) are lines that start and end with `|`. The second line, such as `| --- | --- |`, is the *delimiter row*; it separates the header from the body, and colons in it (`:---:`) set alignment. A literal `|` inside a cell must be written `\|`.
- **Hard line breaks.** A single line break inside a paragraph is ignored by the renderer; two spaces at the end of a line, or a backslash, force a break. This is why `.editorconfig` must not trim trailing spaces in `.md` files.
- **HTML comments** such as `<!-- fmt:off -->` are invisible in the rendered page; some tools read them as instructions (ruff's formatter does, see `ruff.md`).

Because the format is so simple, tools can also read it: a script can list the headings of a document with one `grep`, as the commands below do.

## Walkthrough of this repository's use

**The architecture document.** Its first lines and its first table:

```text
    # Architecture: logsum, a streaming log summarizer

    `logsum` reads an access log one line at a time and keeps only a running tally, so its memory depends on the number of distinct paths and on the latency store it uses, not on the size of the file. This document names the components, shows the data flow, records the decisions and says what a production tool would add.

    ## Components and what each owns
```
(`ARCHITECTURE.md`, lines 1 to 5; shown indented by four spaces so that its headings are not read as headings of this note)

- Line 1 starts with one `#`: the document's title.
- Line 3 is a paragraph: a line of ordinary text between blank lines. Inside it, text in backticks (for example the program's name) is shown in a code font.
- Line 5 starts with `##`: a section heading.

```text
    | Lesson's component | Code | Layer | Owns |
    | --- | --- | --- | --- |
    | Access log (store) | `FileLineSource` in `infrastructure/log_files.py` | infrastructure | opening the file (plain or `.gz`), decoding it, closing it, turning I/O failures into `UnreadableLogFileError` |
```
(`ARCHITECTURE.md`, lines 9 to 11; shown indented by four spaces so that its headings are not read as headings of this note)

- The first line is the table's header row: each `|` separates a column.
- The second line is the delimiter row of `---` cells; without it no table is drawn.
- The third line is the first body row. Code names in backticks stay readable inside cells.

**The changelog.**

```text
    # Changelog

    All notable changes to this project are recorded here. The format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/) and the project uses [Semantic Versioning](https://semver.org/).

    ## [0.1.0] - 2026-10-26

    ### Added

    - `logsum`, a command-line tool that streams an access log and prints requests per status, the ten slowest paths by 95th-percentile latency and the number of unparseable lines; `--json`, `--top`, `--stats` (elapsed time and peak memory), `--estimator exact|histogram`.
```
(`CHANGELOG.md`, lines 1 to 9; shown indented by four spaces so that its headings are not read as headings of this note)

- The first heading is the title; the paragraph says which two conventions the file follows. `[Keep a Changelog](https://...)` is a link: the words in square brackets are shown, the address in parentheses is where it goes.
- `## [0.1.0] - date` is one released version; `### Added` is a subsection for the kind of change (the convention also has `Changed`, `Deprecated`, `Removed`, `Fixed` and `Security`). The bullets below describe the changes for a person who uses the tool, not for the person who wrote it.
- *Semantic Versioning* numbers a version `major.minor.patch`: a change that breaks users raises the major number, a new feature the minor, a bug fix the patch.

**A decision record.** One file in `docs/adr/` per decision. The name starts with a number so the order is visible. This is the top of `docs/adr/0003-percentile-definition.md`:

```text
    # 3. The 95th percentile: `statistics.quantiles` (exclusive), capped at the maximum

    Status: accepted, 2026-10-26

    ## Context

    The lesson defines p95 as `statistics.quantiles(values, n=100)[94]`, and its hand check is 19.95 for the integers 1 to 20. That method (exclusive, the library default) interpolates in the rank space `0.95 * (n + 1)`, which falls past the largest value when `n` is below 19: four latencies of 10, 20, 30 and 40 ms give 47.5 ms. A tool that reports a latency no request had misleads. `statistics.quantiles` also raises for a single data point on Python 3.12.

    ## Decision
```
(`docs/adr/0003-percentile-definition.md`, lines 1 to 9; shown indented by four spaces so that its headings are not read as headings of this note)

- `# 3. ...` is the title with the record's number.
- `Status: accepted, date` is a plain paragraph line; a decision can later become *superseded* by a newer one, and the record stays.
- The `##` headings are the same in every record: **Context** (the situation and the forces), **Decision** (what was chosen), and in these records **Alternatives considered** and **Consequences**. ADR stands for *architecture decision record*: a short note kept so that nobody has to guess later why the code is the way it is.



**What each Markdown file of this repository is made of**, counted by reading the files (a heading is a line that starts with one to six `#` and a space; a table is counted by its delimiter row; a code block by its pair of fences):

| File | Lines | Headings | Tables | Code blocks | Links |
| --- | --- | --- | --- | --- | --- |
| `ARCHITECTURE.md` | 88 | 9 | 3 | 1 | 2 |
| `CHANGELOG.md` | 14 | 3 | 0 | 0 | 2 |
| `README.md` | 119 | 9 | 5 | 3 | 7 |
| `docs/adr/0001-stream-with-a-generator-and-count-bad-lines-in-an-object.md` | 23 | 5 | 0 | 0 | 0 |
| `docs/adr/0002-ports-and-adapters-with-four-layers.md` | 22 | 5 | 0 | 0 | 0 |
| `docs/adr/0003-percentile-definition.md` | 22 | 5 | 0 | 0 | 0 |
| `docs/adr/0004-fixed-size-histogram-estimator.md` | 25 | 6 | 0 | 0 | 0 |

## Try it yourself

```bash
grep -n '^## ' ARCHITECTURE.md
```
Expected: one line per section of the architecture document, each starting with its line number, the first being `## Components and what each owns`. This is a tool reading the structure of a Markdown file with one pattern: `^## ` means 'at the start of a line, two hash signs and a space'.

```bash
ls docs/adr
```
Expected: the decision records, one file per decision, named with a number, such as `0001-...md`.

```bash
grep -c '^| ' README.md
```
Expected: a number: the lines of the README that belong to tables.

```bash
head -9 CHANGELOG.md
```
Expected: the title, the sentence naming Keep a Changelog and Semantic Versioning, and the heading of the first release.

## Mistakes people make

- **Forgetting the blank line before a list or a table.** Many renderers then treat it as part of the paragraph above.
- **Forgetting the delimiter row of a table.** Without `| --- |` no table appears; the lines show as text.
- **A `|` inside a table cell.** It ends the cell. Write `\|` (as in `a \| b`).
- **Indenting a code block with spaces by accident.** Four leading spaces also make a code block in Markdown; use fences.
- **Trailing spaces trimmed by an editor.** They are a line break in Markdown; that is why the editor settings leave them alone in `.md` files.
- **Absolute links to a local path.** Use relative links (`docs/adr/0001-...md`) so they work on every machine and on the code host.
- **Documentation that is not updated with the code.** The reason for keeping the documents in the repository is that a change to the code and its explanation travel in one commit.

## Check yourself

**1. What does a line that starts with `## ` mean?**
A section heading, one level below the title (`# `).

**2. What turns a few lines starting with `|` into a table?**
The second line, the delimiter row (`| --- | --- |`).

**3. Why does the repository keep its documentation as `.md` files next to the code?**
They are plain text, readable without tools, shown nicely by code hosts, and changed in the same commit and diff as the code they describe.

**4. What is an ADR for?**
It records one decision with its context, the alternatives and the consequences, so later readers know why the code is the way it is.

**5. Why does `.editorconfig` keep trailing spaces in Markdown files?**
Two trailing spaces force a line break in Markdown; trimming them would change the rendered text.

## Further reading

- CommonMark specification: https://spec.commonmark.org/0.31.2/
- GitHub Flavored Markdown specification (tables): https://github.github.com/gfm/
- Keep a Changelog 1.1.0: https://keepachangelog.com/en/1.1.0/
- Semantic Versioning 2.0.0: https://semver.org/spec/v2.0.0.html
- Architecture decision records (Michael Nygard, 2011): https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions
