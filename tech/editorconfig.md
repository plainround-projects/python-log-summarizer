# EditorConfig

<!-- fmt:off -->

## What it is

A small settings file, `.editorconfig`, that tells any text editor (for example VS Code, IntelliJ or Vim) how to treat files in this folder: tabs or spaces, how many, which line ending, whether to trim trailing spaces. The file format is called INI: `[pattern]` headings followed by `key = value` lines.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **terminal** is a window where you type a line of text, press Enter, and the computer runs it. The program that reads your line is the **shell** (here `zsh` or `bash`). Everything typed in a terminal is a **command**: a program's name followed by **arguments**, the words that tell it what to do.
- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- **JSON** is a text format for data: objects `{"name": "x", "count": 3}` (names with values), lists `[1, 2, 3]`, text in double quotes, numbers, `true`, `false` and `null`. Almost every language can read and write it, which makes it the usual way programs exchange data.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- **Continuous integration (CI)** means a server runs the project's checks automatically every time code is pushed, so a broken change is noticed at once.
- **YAML** and **TOML** are text formats for settings files. Both hold named values and nested groups; TOML writes groups as `[headings]`, YAML uses indentation.
- A **linter** reads code without running it and reports likely mistakes and style problems. A **formatter** rewrites the layout of the code into one agreed style.

## Why this repository uses it

Several people and several tools touch the same files. Without one agreed setting, one editor adds tabs, another trims spaces, and the diffs fill with whitespace changes. The Makefile needs real tab characters, the Markdown files need to keep trailing spaces, and YAML needs two-space indentation.

## Where it appears

| File | What it does with it |
| --- | --- |
| `.editorconfig` | the whole file. |

## How it works underneath

The editor looks for `.editorconfig` in the folder of the file being edited and in each folder above it, until a file says `root = true`. For each `[pattern]` that matches the file name, it applies the keys. Later matching sections override earlier ones. Many editors support this natively; some need a plugin.

## Walkthrough of this repository's use

```ini
root = true

[*]
charset = utf-8
end_of_line = lf
insert_final_newline = true
trim_trailing_whitespace = true
indent_style = space
indent_size = 4

[*.{yml,yaml,json,toml}]
indent_size = 2

[Makefile]
indent_style = tab

[*.md]
trim_trailing_whitespace = false
```
(`.editorconfig`, lines 1 to 18)

- `root = true`: stop searching in parent folders.
- `[*]`: the section for every file.
- `charset = utf-8`: save as UTF-8, the encoding the Python source and the Markdown rely on.
- `end_of_line = lf`: lines end with a line feed (`\n`), the Unix and macOS convention; Windows editors would otherwise write `\r\n`.
- `insert_final_newline = true`: every file ends with a newline, which POSIX text tools expect.
- `trim_trailing_whitespace = true`: remove spaces at the ends of lines when saving.
- `indent_style = space`, `indent_size = 4`: indent with four spaces (the Python convention).
- `[*.{yml,yaml,json,toml}]` / `indent_size = 2`: these formats use two spaces.
- `[Makefile]` / `indent_style = tab`: Make requires a tab character before each command line; spaces there are a syntax error ("missing separator").
- `[*.md]` / `trim_trailing_whitespace = false`: in Markdown two trailing spaces mean a line break, so they must not be trimmed.

## Try it yourself

```bash
cat .editorconfig | head -8
```
Expected: the first lines of the file shown above.

```bash
grep -n '^ ' Makefile || echo "no line starts with a space"
```
Expected: either `no line starts with a space`, or a single line: the second line of the long `.PHONY` list, which is a continuation of the line above (a line ending in a backslash goes on in the next line, and its leading spaces are harmless). No *command* line starts with spaces; a command indented with spaces instead of a tab is a Make error.

```bash
grep -c "	" Makefile
```
Expected: a number above zero: the tab characters that begin command lines.

## Mistakes people make

- **Editor without support.** VS Code needs the "EditorConfig for VS Code" extension; without it the file is ignored.
- **Spaces in a Makefile.** The `[Makefile]` section exists to prevent exactly this.
- **Trimming whitespace in Markdown** and losing intended line breaks.
- **Treating it as a formatter.** It sets editor behavior on save; Ruff is what enforces Python layout in CI.

## Check yourself

**1. What does `root = true` do?**
Tells the editor to stop looking for more `.editorconfig` files in parent folders.

**2. Why must Makefiles use tabs?**
Make's syntax requires a tab before each command line; spaces cause `missing separator`.

**3. Why is whitespace trimming off for Markdown?**
Two trailing spaces mean a line break in Markdown.

**4. What line ending does `lf` select?**
A single line-feed character, the Unix and macOS convention.

**5. Does `.editorconfig` check code in CI?**
No. It only guides editors; Ruff checks and formats Python in CI.

## Further reading

- EditorConfig specification and supported properties: https://editorconfig.org/
