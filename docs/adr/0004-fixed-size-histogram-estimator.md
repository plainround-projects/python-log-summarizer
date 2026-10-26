# 4. A fixed-size histogram as the alternative latency store

Status: accepted, 2026-10-26

## Context

`ExactLatencies` keeps one integer per request per path, so a path with tens of millions of requests holds tens of millions of integers. The lesson's stretch goal replaces it with a fixed-size histogram and asks to state the accuracy given up.

## Decision

`HistogramLatencies(bucket_ms, max_latency_ms)` keeps an array of counts, one per bucket of `bucket_ms` (default 5 ms, up to 10,000 ms, so 2,001 counters of 8 bytes, about 16 KB per path). A latency is remembered as the lower edge of its bucket; one at or over the cap counts as the cap. The percentile uses the same rank arithmetic as the exact one, over bucket counts. Selected with `--estimator histogram`.

## Accuracy given up

For whole-millisecond latencies below the cap: the p95 is never above the exact one and at most `bucket_ms - 1` below it. With `bucket_ms=1` it is identical to the exact value. Above the cap the answer is wrong only if more than 5 percent of a path's requests exceed it. Memory per path is fixed; the number of paths is not (see the limits in ARCHITECTURE.md).

## Alternatives considered

- **Logarithmic buckets (HDR histogram, t-digest):** constant relative error across magnitudes; more code, and a dependency or a lot of arithmetic. The path to take for a service with latencies from microseconds to minutes.
- **Reservoir sampling:** bounded memory but a random error instead of a bounded one.

## Consequences

- Unit tests check both claims (never above, less than one bucket below) over several widths and that memory does not change with the number of requests.
- The e2e test runs both estimators on 500,000 lines and compares them within the bucket width.
