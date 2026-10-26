# 2. Four layers with ports and adapters, enforced by import-linter

Status: accepted, 2026-10-26

## Context

The program is small, but its parts change for different reasons: the line format (domain), how a run is orchestrated and timed (application), which file formats and memory meter are used (infrastructure), the flags and output (interfaces). The template asks for the dependency rule to be visible in the tree and enforced.

## Decision

Folders `domain`, `application`, `infrastructure`, `interfaces` under `src/logsum/`. The application layer declares the ports it needs (`LineSource`, `Clock`, `MemoryMeter`) and infrastructure implements them. `interfaces` wires adapters into the use case. An import-linter `layers` contract enforces the direction; a `forbidden` contract keeps `gzip`, `argparse`, `tracemalloc`, `pathlib`, `os` and `sys` out of `domain` and `application`. Time and memory measurement are injected, so the use case is tested with a stepping clock and a fixed meter.

## Alternatives considered

- **One module `logsum.py`:** what the lesson's first step creates; it cannot show which code is allowed to do I/O.
- **Only a layers convention in the README:** drifts without a check.

## Consequences

- The domain and application layers are tested with no files, at 100% coverage.
- Real-file behavior (gzip, truncation, undecodable bytes, a closed pipe) is tested once, in the adapter.
- More files than a script needs; the cost is deliberate and small.
