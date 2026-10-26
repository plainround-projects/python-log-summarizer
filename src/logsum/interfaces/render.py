"""Turns a run report into text or JSON. Output goes to standard output; logs go to standard error."""

from __future__ import annotations

import json

from logsum.application.summarize import RunReport

_BYTES_PER_MEGABYTE = 1024 * 1024


def render_text(report: RunReport, *, top: int, show_stats: bool) -> str:
    """The human-readable summary: statuses, the slowest paths, the bad-line count, and optionally the run's cost."""
    summary = report.summary
    statuses = ", ".join(f"{status}: {count}" for status, count in summary.status_counts.items())
    lines = [f"statuses: {{{statuses}}}", f"slowest paths by p95 latency in ms (top {top}):"]
    lines.extend(
        f"  {entry.p95_ms:>8.2f}  {entry.path}  ({entry.requests} requests)" for entry in summary.slowest_paths
    )
    lines.append(f"bad lines: {summary.bad_lines}")
    if show_stats:
        lines.append(_stats_line(report))
    return "\n".join(lines)


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


def _stats_line(report: RunReport) -> str:
    peak = "n/a" if report.peak_memory_bytes is None else f"{report.peak_memory_bytes / _BYTES_PER_MEGABYTE:.1f} MB"
    return f"elapsed: {report.elapsed_seconds:.2f}s  peak memory: {peak}"
