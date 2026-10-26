import runpy

import pytest


def test_python_dash_m_logsum_runs_the_command(data_dir, monkeypatch, capsys):
    monkeypatch.setattr("sys.argv", ["logsum", str(data_dir / "small.log")])
    with pytest.raises(SystemExit) as stop:
        runpy.run_module("logsum", run_name="__main__")
    assert stop.value.code == 0
    assert "19.95" in capsys.readouterr().out
