"""The lesson's scenario, end to end through the installed commands: 500,000 lines in, a summary out."""

from __future__ import annotations

import gzip
import json
import resource
import shutil
import subprocess
import sys
from pathlib import Path

import pytest

pytestmark = pytest.mark.e2e

BIN = Path(sys.executable).parent
MEMORY_BUDGET_BYTES = 50 * 1024 * 1024
PLANTED_BAD_LINES = 300
LINES = 500_000


def run(*command, **kwargs):
    return subprocess.run(
        [str(part) for part in command], capture_output=True, text=True, check=True, timeout=300, **kwargs
    )


def summary_of(path, *flags):
    return json.loads(run(BIN / "logsum", path, "--json", *flags).stdout)


@pytest.fixture(scope="module")
def sample_log(tmp_path_factory: pytest.TempPathFactory) -> Path:
    path = tmp_path_factory.mktemp("lesson") / "sample.log"
    result = run(BIN / "logsum-make-log", path)
    assert f"wrote {LINES} lines ({PLANTED_BAD_LINES} bad)" in result.stdout
    return path


def test_the_summary_counts_every_line_and_exactly_the_planted_bad_ones(sample_log):
    document = summary_of(sample_log)
    assert document["bad_lines"] == PLANTED_BAD_LINES
    assert document["total_requests"] == LINES - PLANTED_BAD_LINES
    assert sum(document["statuses"].values()) == LINES - PLANTED_BAD_LINES
    assert set(document["statuses"]) == {"200", "404", "500"}
    assert len(document["slowest_paths"]) == 5  # the log has five paths, fewer than the ten asked for


def test_peak_memory_stays_under_fifty_megabytes_and_does_not_grow_with_the_file(sample_log, tmp_path):
    full = summary_of(sample_log, "--stats")["stats"]["peak_memory_bytes"]
    tenth = tmp_path / "tenth.log"
    with sample_log.open(encoding="utf-8") as source, tenth.open("w", encoding="utf-8") as target:
        target.writelines(line for _, line in zip(range(LINES // 10), source, strict=False))
    small = summary_of(tenth, "--stats")["stats"]["peak_memory_bytes"]
    assert full < MEMORY_BUDGET_BYTES
    # exact latencies grow by 8 bytes per request, which is the cost the lesson names; the lines themselves do not
    assert full < small + 8 * LINES + 1_000_000


def test_the_process_resident_memory_is_also_under_fifty_megabytes(sample_log):
    before = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    run(BIN / "logsum", sample_log)
    peak = resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss
    resident = peak if sys.platform == "darwin" else peak * 1024  # bytes on macOS, kilobytes on Linux
    assert peak >= before
    assert resident < MEMORY_BUDGET_BYTES, f"resident {resident / 2**20:.1f} MB"


def test_the_hand_checked_log_prints_exactly_19_95(tmp_path):
    small = tmp_path / "small.log"
    run(BIN / "logsum-make-log", small, "--small")
    assert summary_of(small)["slowest_paths"] == [{"path": "/orders/1234", "p95_ms": 19.95, "requests": 20}]


def test_a_gzip_copy_gives_the_same_summary(sample_log, tmp_path):
    compressed = tmp_path / "sample.log.gz"
    with sample_log.open("rb") as source, gzip.open(compressed, "wb", compresslevel=1) as target:
        shutil.copyfileobj(source, target)
    assert summary_of(compressed) == summary_of(sample_log)


def test_the_histogram_estimator_agrees_with_the_exact_one_within_its_bucket_width(sample_log):
    exact = {entry["path"]: entry["p95_ms"] for entry in summary_of(sample_log)["slowest_paths"]}
    histogram = summary_of(sample_log, "--estimator", "histogram", "--bucket-ms", "5")["slowest_paths"]
    assert len(histogram) == len(exact)
    for entry in histogram:
        assert 0 <= exact[entry["path"]] - entry["p95_ms"] < 5
