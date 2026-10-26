# 3. The 95th percentile: `statistics.quantiles` (exclusive), capped at the maximum

Status: accepted, 2026-10-26

## Context

The lesson defines p95 as `statistics.quantiles(values, n=100)[94]`, and its hand check is 19.95 for the integers 1 to 20. That method (exclusive, the library default) interpolates in the rank space `0.95 * (n + 1)`, which falls past the largest value when `n` is below 19: four latencies of 10, 20, 30 and 40 ms give 47.5 ms. A tool that reports a latency no request had misleads. `statistics.quantiles` also raises for a single data point on Python 3.12.

## Decision

`p95` returns one value for a single request, and otherwise `min(statistics.quantiles(values, n=100)[94], max(values))`. For 20 or more points the cap never applies, so the lesson's 19.95 is exact. `p95_from_ranks` computes the same value from a count and a rank lookup (the arithmetic of `statistics.quantiles`), which lets a histogram answer without expanding itself.

## Alternatives considered

- **`method="inclusive"`:** never exceeds the maximum, but gives 19.05 for 1 to 20, not the lesson's hand-checked 19.95.
- **Skip paths with fewer than two requests** (the lesson's step 4 solution): hides rare paths.
- **Nearest rank:** simple, but a step function; two close samples can give very different answers.

## Consequences

- The result agrees with the library for every sample of 20 or more and is never above the slowest request.
- A property test compares the rank-based version with the library for sample sizes from 1 to 1000.
