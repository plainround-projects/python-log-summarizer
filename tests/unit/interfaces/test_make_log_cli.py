from logsum.domain.request import parse
from logsum.interfaces.make_log_cli import entrypoint, main


def test_it_writes_the_requested_log_and_says_so(tmp_path, capsys):
    path = tmp_path / "sample.log"
    assert main([str(path), "--lines", "300", "--bad", "6", "--seed", "1"]) == 0
    assert "wrote 300 lines (6 bad)" in capsys.readouterr().out
    assert sum(parse(line) is None for line in path.read_text(encoding="utf-8").splitlines()) == 6


def test_small_writes_the_twenty_line_log(tmp_path, capsys):
    path = tmp_path / "small.log"
    assert main([str(path), "--small"]) == 0
    assert len(path.read_text(encoding="utf-8").splitlines()) == 20
    assert "wrote 20 lines" in capsys.readouterr().out


def test_more_bad_lines_than_lines_exits_two(tmp_path, capsys):
    assert main([str(tmp_path / "x.log"), "--lines", "5", "--bad", "9"]) == 2
    assert "bad_lines" in capsys.readouterr().err


def test_entrypoint_reads_the_process_arguments(tmp_path, monkeypatch):
    monkeypatch.setattr("sys.argv", ["logsum-make-log", str(tmp_path / "x.log"), "--small"])
    assert entrypoint() == 0
