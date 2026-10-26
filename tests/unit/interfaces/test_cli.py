import io
import json

import pytest
from jsonschema import validate

from logsum.infrastructure.settings import Settings
from logsum.interfaces.cli import distribution_factory, entrypoint, main


def run(*argv, environ=None):
    out, err = io.StringIO(), io.StringIO()
    code = main(list(argv), environ=environ or {}, stdout=out, stderr=err)
    return code, out.getvalue(), err.getvalue()


def test_help_prints_usage_and_exits_zero(capsys):
    with pytest.raises(SystemExit) as stop:
        main(["--help"], environ={})
    assert stop.value.code == 0
    assert "usage: logsum" in capsys.readouterr().out


def test_the_small_log_prints_the_hand_checked_percentile(data_dir):
    code, out, _ = run(str(data_dir / "small.log"))
    assert code == 0
    assert "statuses: {200: 20}" in out
    assert "19.95  /orders/1234  (20 requests)" in out
    assert "bad lines: 0" in out


def test_the_two_path_fixture_counts_statuses_bad_lines_and_orders_paths(data_dir):
    code, out, _ = run(str(data_dir / "two_paths.log"))
    assert code == 0
    assert "statuses: {200: 4, 404: 1, 500: 1}" in out
    assert "bad lines: 3" in out
    assert out.index("/b") < out.index("/a")  # /b is slower


def test_json_output_follows_the_published_schema(data_dir, summary_schema):
    code, out, _ = run(str(data_dir / "two_paths.log"), "--json", "--stats")
    assert code == 0
    document = json.loads(out)
    validate(document, summary_schema)
    assert document["bad_lines"] == 3
    assert document["stats"]["peak_memory_bytes"] > 0


def test_json_output_without_stats_has_no_stats_key_and_still_validates(data_dir, summary_schema):
    _, out, _ = run(str(data_dir / "small.log"), "--json")
    validate(json.loads(out), summary_schema)
    assert "stats" not in json.loads(out)


def test_stats_adds_elapsed_time_and_peak_memory_to_the_text(data_dir):
    _, out, _ = run(str(data_dir / "small.log"), "--stats")
    assert "elapsed: " in out
    assert "peak memory: " in out


def test_top_limits_the_paths_listed(data_dir):
    _, out, _ = run(str(data_dir / "two_paths.log"), "--top", "1")
    assert "(top 1)" in out
    assert "/a" not in out.split("bad lines")[0].split("(top 1):")[1]


def test_the_histogram_estimator_is_selectable_and_close_to_exact(data_dir):
    _, exact, _ = run(str(data_dir / "small.log"), "--json")
    _, histogram, _ = run(str(data_dir / "small.log"), "--json", "--estimator", "histogram", "--bucket-ms", "1")
    assert json.loads(histogram)["slowest_paths"] == json.loads(exact)["slowest_paths"]


def test_the_environment_supplies_defaults_and_flags_override_them(data_dir):
    _, out, _ = run(str(data_dir / "two_paths.log"), environ={"LOGSUM_TOP": "1"})
    assert "(top 1)" in out
    _, out, _ = run(str(data_dir / "two_paths.log"), "--top", "2", environ={"LOGSUM_TOP": "1"})
    assert "(top 2)" in out


def test_a_missing_file_exits_one_with_a_message_and_a_structured_log_line(tmp_path):
    code, out, err = run(str(tmp_path / "missing.log"), "--log-level", "ERROR")
    assert code == 1
    assert out == ""
    assert "logsum: cannot read" in err
    assert "level=ERROR" in err


def test_a_bad_setting_in_the_environment_exits_two():
    code, _, err = run("x.log", environ={"LOGSUM_TOP": "lots"})
    assert code == 2
    assert "LOGSUM_TOP" in err


def test_a_bad_flag_value_exits_two():
    code, _, err = run("x.log", "--top", "0")
    assert code == 2
    assert "top must be at least 1" in err


def test_the_distribution_factory_follows_the_estimator_setting():
    assert type(distribution_factory(Settings())()).__name__ == "ExactLatencies"
    assert type(distribution_factory(Settings(estimator="histogram"))()).__name__ == "HistogramLatencies"


def test_entrypoint_returns_the_exit_code_of_main(data_dir, monkeypatch):
    monkeypatch.setattr("sys.argv", ["logsum", str(data_dir / "small.log")])
    assert entrypoint() == 0


def test_ctrl_c_exits_with_130_and_a_one_line_message(monkeypatch, capsys):
    def interrupted(*_args, **_kwargs):
        raise KeyboardInterrupt

    monkeypatch.setattr("logsum.interfaces.cli.main", interrupted)
    assert entrypoint() == 130
    assert capsys.readouterr().err.strip() == "logsum: interrupted"


def test_a_closed_pipe_exits_zero_and_points_stdout_at_devnull(monkeypatch, tmp_path):
    redirected = []

    def pipe_closed(*_args, **_kwargs):
        raise BrokenPipeError

    stand_in = (tmp_path / "stdout").open("w", encoding="utf-8")
    monkeypatch.setattr("logsum.interfaces.cli.main", pipe_closed)
    monkeypatch.setattr("os.dup2", lambda source, target: redirected.append(target))
    monkeypatch.setattr("sys.stdout", stand_in)
    assert entrypoint() == 0
    assert redirected == [stand_in.fileno()]
    stand_in.close()
