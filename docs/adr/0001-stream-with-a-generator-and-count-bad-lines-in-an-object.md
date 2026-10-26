# 1. Stream with a generator; count bad lines in an object

Status: accepted, 2026-10-26

## Context

The tool must use the same memory for a 5 GB log as for a 5 MB one, and a malformed line (a missing field, `abc` for a latency, an empty line) must never stop the run. The generator that yields parsed requests also has to report how many lines it skipped.

## Decision

`stream_requests` is a generator over any iterable of lines. It yields one `Request` at a time and adds one to a `BadLineCounter` for each line `parse` rejects. The count is in an object the caller passes in, because a generator's `return` value is only visible through `StopIteration.value`, which a `for` loop swallows. The file is opened by an adapter behind the `LineSource` port, as a context manager, so it is closed on every path.

## Alternatives considered

- **Yield a `Request | BadLine` union:** no mutable object, but every consumer must filter and the tally cannot just loop over requests.
- **Return the count through `StopIteration.value`:** correct, but only by driving the generator by hand.
- **`list(open(path))` then loop:** simplest, and exactly the mistake the lesson warns about; memory grows with the file (`make demo-memory`).

## Consequences

- Memory depends on the tally, not the file; measured at 4.0 MB traced (35.9 MB resident, the interpreter included) for 500,000 lines.
- The one mutable object in the design is small and owned by the use case.
- One pass over the file; a second summary needs a second run.
