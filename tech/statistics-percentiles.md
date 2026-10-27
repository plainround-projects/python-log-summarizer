# Percentiles and `statistics.quantiles`

<!-- fmt:off -->

## What it is

A **percentile** answers: "what value is bigger than this share of the numbers?" The 95th percentile (p95) of response times is the time that 95 percent of requests were faster than; the slowest 5 percent were slower. Averages hide slow requests; p95 shows them. Python's `statistics.quantiles(data, n=100)` returns the 99 cut points that divide sorted data into 100 equal groups; the 95th percentile is the cut point at index 94.

### Everyday words used on this page

These are defined here once so nothing below is assumed.

- A **file path** names a file by the folders leading to it, separated by `/`, such as `src/logsum/cli.py`. A **folder** (also called a **directory**) holds files and other folders. A path that starts with `/` is **absolute** (from the top of the disk); any other path is **relative** to the **current directory**, the folder the shell is working in.
- **HTTP** is the way programs ask for things over a network. A **request** has a method (`GET` reads, `POST` creates), a path (`/items/1`) and sometimes a body. The **response** has a **status code** (200 means success, 404 not found, 422 the request was understood but its data was wrong, 503 service unavailable) and usually a body.
- A **library** is code written by someone else that your program uses. A **package** is a library prepared for installation, with a name and a **version** such as `0.162.0`. A **dependency** is a package your project needs; **pinning** means fixing the exact version so every machine gets the same code.
- A **module** is one Python file; a **package** in the Python sense is a folder of modules with an `__init__.py` file. `import x` or `from x import y` makes the names defined in module `x` available.
- A **function** is a named block of code you can run with `name(arguments)` and that may give back a value with `return`. A **class** is a blueprint for objects that bundle data (**fields**) with functions (**methods**); calling the class makes an **object**, one instance of it.
- A **type hint** is a note in the code, such as `count: int` or `-> str`, that says what kind of value a name holds or a function returns. Python ignores it when running; tools like `mypy` read it to find mistakes without running the program. The forms used in this repository: `list[int]` (a list of whole numbers), `dict[str, int]` (a dictionary from text to whole numbers), `tuple[int, str]` (exactly two items, of those types), `tuple[str, ...]` (any number of text items), `X | None` (either an `X` or nothing), `Callable[[int], str]` (a function that takes a whole number and returns text), `type[X]` (the class `X` itself, not an object made from it).
- An **exception** (also called an **error**) is an object that stops the normal flow when something goes wrong. `raise` creates one; `try: ... except SomeError: ...` catches it and carries on.
- A **test** is a small program that runs part of your code and checks the result with `assert`, which fails if its condition is false. A failing test points at a change that broke something.
- **Latency** is how long one request takes. A **percentile** says what share of requests were at least that fast: **p95** is the time that 95 out of 100 requests beat, so it shows how bad the slow tail is, which an average hides.
- A **repository** is a project folder whose history is tracked by **git**. A **commit** is one saved snapshot with a message; a **branch** is a named line of commits.
- An **immutable** object cannot be changed after it is made. Code that holds one can be sure nobody changes it behind its back.

## Why this repository uses it

The lesson ranks paths by their p95 latency and requires that the 20-line log (latencies 1 to 20 ms) give exactly 19.95, "computed independently" by `statistics.quantiles`.

## Where it appears

| File | What it does with it |
| --- | --- |
| `src/logsum/domain/percentile.py` | `p95` and `p95_from_ranks`. |
| `src/logsum/domain/distribution.py` | `ExactLatencies` keeps every latency; `HistogramLatencies` counts them in fixed buckets. |
| `tests/unit/domain/test_percentile.py` | the hand-checked value 19.95 and a check that the two functions agree for sample sizes 1 to 1000. |

## How it works underneath

To get a percentile from `n` sorted values, a rule decides where "95 percent of the way" falls. The **exclusive** method (Python's default) puts the position at `p * (n + 1)`, so for the integers 1 to 20 and p = 0.95 the position is `0.95 * 21 = 19.95`: that is between the 19th value (19) and the 20th (20), 95 percent of the way, so 19 + 0.95 * (20 - 19) = **19.95**. The **inclusive** method uses `p * (n - 1) + 1` and would give 19.05. The exclusive method can land beyond the largest value for very small samples (four values give a position of 4.75, past the 4th), which is why this code caps the answer at the largest value seen.

## Walkthrough of this repository's use

```python
"""The 95th percentile, defined once so every distribution agrees on it."""

from __future__ import annotations

from collections.abc import Callable, Sequence
from statistics import quantiles

from logsum.domain.errors import EmptyDistributionError

_CUTS = 100
_PERCENT = 95
_P95_INDEX = _PERCENT - 1  # quantiles(..., n=100) returns 99 cut points; the 95th is at index 94


def p95(latencies: Sequence[int]) -> float:
    """The 95th percentile by the exclusive method (the `statistics.quantiles` default).

    A single latency is its own percentile. For the integers 1 to 20 the answer is 19.95. The exclusive method
    extrapolates past the largest value when there are few data points (four latencies give 47.5 for a maximum of
    40), so the answer is capped at the largest latency: no request was slower than that.
    """
    if not latencies:
        raise EmptyDistributionError("no latencies to take a percentile of")
    if len(latencies) == 1:
        return float(latencies[0])
    return min(quantiles(latencies, n=_CUTS)[_P95_INDEX], float(max(latencies)))


def p95_from_ranks(count: int, kth_smallest: Callable[[int], int]) -> float:
    """The same value as `p95`, computed from `count` and a lookup of the k-th smallest latency (0-based).

    This lets a histogram answer without expanding itself into a sorted list. The arithmetic is the one in
    `statistics.quantiles`: scale the cut point to the rank space, clamp it, interpolate between neighbors.
    """
    if count == 0:
        raise EmptyDistributionError("no latencies to take a percentile of")
    if count == 1:
        return float(kth_smallest(0))
    spacing = count + 1
    rank = min(max(_PERCENT * spacing // _CUTS, 1), count - 1)
    delta = _PERCENT * spacing - rank * _CUTS
    interpolated = (kth_smallest(rank - 1) * (_CUTS - delta) + kth_smallest(rank) * delta) / _CUTS
    return min(interpolated, float(kth_smallest(count - 1)))
```
(`src/logsum/domain/percentile.py`, lines 1 to 43)

- `_CUTS = 100`, `_PERCENT = 95`, `_P95_INDEX = _PERCENT - 1`: `quantiles(..., n=100)` returns 99 numbers (the 1st to the 99th percentile), so the 95th is at index 94.
- `p95(latencies)`: no values is an error (`EmptyDistributionError`); one value is its own percentile (`statistics.quantiles` needs at least two on Python 3.12); otherwise `quantiles(latencies, n=100)[94]`, capped with `min(..., float(max(latencies)))`.
- `p95_from_ranks(count, kth_smallest)`: the same arithmetic as the library, written for data that is not a list but a histogram: `spacing = count + 1` is the `n + 1`; `rank = _PERCENT * spacing // _CUTS` is the whole-number part of the position (`//` is integer division), clamped between 1 and `count - 1` as the library does; `delta` is the remainder in hundredths; the result mixes the two neighboring values `kth_smallest(rank - 1)` and `kth_smallest(rank)` in the proportion `delta : 100 - delta`. `kth_smallest` is a function the caller supplies (a histogram counts through its buckets to find it).

A fixed-size histogram stores only how many latencies fell in each bucket of `bucket_ms` milliseconds, so memory does not grow with the number of requests; the price is that a latency is remembered as the lower edge of its bucket (see ADR 4 in `docs/adr`).

## Try it yourself

```bash
uv run --frozen python -c "
from statistics import quantiles
print(quantiles(range(1, 21), n=100)[94])
print(quantiles(range(1, 21), n=100, method='inclusive')[94])
"
```
Expected: `19.95` and `19.05`.

```bash
uv run --frozen python -c "
from statistics import quantiles
print(quantiles([10, 20, 30, 40], n=100)[94])
from logsum.domain.percentile import p95
print(p95([10, 20, 30, 40]))
"
```
Expected: `47.5` (past the largest value) and `40.0` (capped).

```bash
uv run --frozen logsum data/small.log
```
Expected: `19.95  /orders/1234  (20 requests)`.

## Mistakes people make

- **Using the mean.** A few very slow requests barely move it.
- **Taking a percentile over all paths mixed together** when the question is which path is slow.
- **Mixing methods** between two tools (exclusive against inclusive) and wondering why numbers differ by a small amount.
- **Trusting p95 of three samples.** Small samples give unstable percentiles.

## Check yourself

**1. What does a p95 of 238 ms mean?**
95 percent of requests took less than 238 ms; 5 percent took longer.

**2. Why is the answer for 1 to 20 exactly 19.95 under the exclusive method?**
The position is 0.95 x 21 = 19.95, 95 percent of the way from the 19th value (19) to the 20th (20).

**3. Why is the result capped at the largest value?**
For tiny samples the exclusive method can give a number larger than any observed value, which no request ever had.

**4. Why does `p95_from_ranks` exist?**
To compute the same percentile from bucket counts without expanding them into a sorted list.

**5. Why is a percentile kept per path?**
The question is which paths are slow compared with each other; one number for all requests would hide that.

## Further reading

- `statistics.quantiles`: https://docs.python.org/3.14/library/statistics.html#statistics.quantiles (the `method` parameter explains exclusive and inclusive).
- Hyndman and Fan, "Sample quantiles in statistical packages" (1996) describes the nine common definitions.
