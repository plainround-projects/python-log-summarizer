"""The adapters and the installed command against real files, real gzip and a real pipe."""

from __future__ import annotations

import gzip
import json
import subprocess
import sys
from pathlib import Path

import pytest

from logsum.domain.errors import UnreadableLogFileError
from logsum.infrastructure.log_files import FileLineSource

pytestmark = pytest.mark.integration

COMMAND = Path(sys.executable).parent / "logsum"


def read_all(location):
    with FileLineSource().open(str(location)) as lines:
        return list(lines)


def test_a_plain_file_is_read_line_by_line(data_dir):
    assert len(read_all(data_dir / "small.log")) == 20


def test_a_gzip_file_gives_the_same_lines_as_the_plain_file(data_dir, tmp_path):
    compressed = tmp_path / "small.log.gz"
    compressed.write_bytes(gzip.compress((data_dir / "small.log").read_bytes()))
    assert read_all(compressed) == read_all(data_dir / "small.log")


def test_bytes_that_are_not_utf8_become_a_bad_line_and_not_a_crash(tmp_path):
    path = tmp_path / "binary.log"
    path.write_bytes(
        b"2026-03-14T09:26:53Z GET /a 200 5ms\n\xff\xfe\x00 garbage\n2026-03-14T09:26:53Z GET /a 200 6ms\n"
    )
    assert len(read_all(path)) == 3


def test_a_missing_file_and_a_directory_are_unreadable(tmp_path):
    with (
        pytest.raises(UnreadableLogFileError, match=r"missing\.log"),
        FileLineSource().open(str(tmp_path / "missing.log")),
    ):
        pass
    with pytest.raises(UnreadableLogFileError), FileLineSource().open(str(tmp_path)):
        pass


def test_a_truncated_gzip_file_is_reported_as_unreadable_while_reading(data_dir, tmp_path):
    whole = gzip.compress((data_dir / "small.log").read_bytes() * 200)
    path = tmp_path / "cut.log.gz"
    path.write_bytes(whole[: len(whole) // 2])
    with pytest.raises(UnreadableLogFileError), FileLineSource().open(str(path)) as lines:
        list(lines)


def test_a_file_that_is_not_gzip_but_named_gz_is_unreadable(tmp_path):
    path = tmp_path / "fake.log.gz"
    path.write_text("not compressed\n", encoding="utf-8")
    with pytest.raises(UnreadableLogFileError), FileLineSource().open(str(path)) as lines:
        list(lines)


def test_the_file_is_closed_when_the_reader_stops_early(data_dir):
    with FileLineSource().open(str(data_dir / "small.log")) as lines:
        next(lines)
    # a second open of the same file works, and nothing leaks a warning (pytest turns ResourceWarning into -ra output)
    assert len(read_all(data_dir / "small.log")) == 20


def test_the_installed_command_runs_and_prints_help():
    result = subprocess.run([str(COMMAND), "--help"], capture_output=True, text=True, check=False, timeout=30)
    assert result.returncode == 0
    assert "usage: logsum" in result.stdout


def test_the_installed_command_summarizes_a_gzip_log_as_json(data_dir, tmp_path):
    path = tmp_path / "two.log.gz"
    path.write_bytes(gzip.compress((data_dir / "two_paths.log").read_bytes()))
    result = subprocess.run(
        [str(COMMAND), str(path), "--json"], capture_output=True, text=True, check=False, timeout=30
    )
    assert result.returncode == 0
    assert json.loads(result.stdout)["bad_lines"] == 3


def test_a_missing_file_makes_the_command_exit_one_without_a_traceback(tmp_path):
    result = subprocess.run(
        [str(COMMAND), str(tmp_path / "nope.log")], capture_output=True, text=True, check=False, timeout=30
    )
    assert result.returncode == 1
    assert "Traceback" not in result.stderr


def test_a_reader_that_closes_the_pipe_early_does_not_produce_a_traceback(data_dir):
    process = subprocess.Popen(
        [str(COMMAND), str(data_dir / "small.log")], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    assert process.stdout is not None
    process.stdout.close()
    _, stderr = process.communicate(timeout=30)
    assert "Traceback" not in stderr
    assert process.returncode == 0
