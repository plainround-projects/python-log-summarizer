import random

import pytest

from logsum.domain.request import parse
from logsum.infrastructure.sample_log import write_sample_log, write_small_log


def test_the_sample_log_has_exactly_the_planted_number_of_bad_lines(tmp_path):
    path = tmp_path / "sample.log"
    write_sample_log(path, lines=2000, bad_lines=30, rng=random.Random(7))
    lines = path.read_text(encoding="utf-8").split("\n")[:-1]
    assert len(lines) == 2000
    assert sum(parse(line) is None for line in lines) == 30
    assert sum(line == "" for line in lines) == 10


def test_the_same_seed_gives_the_same_file_and_another_seed_a_different_one(tmp_path):
    first, second, third = (tmp_path / name for name in ("a.log", "b.log", "c.log"))
    write_sample_log(first, lines=500, bad_lines=5, rng=random.Random(7))
    write_sample_log(second, lines=500, bad_lines=5, rng=random.Random(7))
    write_sample_log(third, lines=500, bad_lines=5, rng=random.Random(8))
    assert first.read_bytes() == second.read_bytes() != third.read_bytes()


def test_a_file_longer_than_one_write_batch_is_complete(tmp_path):
    path = tmp_path / "long.log"
    write_sample_log(path, lines=25_000, bad_lines=0, rng=random.Random(1))
    assert path.read_text(encoding="utf-8").count("\n") == 25_000


@pytest.mark.parametrize(("lines", "bad"), [(10, 11), (10, -1)])
def test_more_bad_lines_than_lines_is_refused(tmp_path, lines, bad):
    with pytest.raises(ValueError, match="bad_lines"):
        write_sample_log(tmp_path / "x.log", lines=lines, bad_lines=bad, rng=random.Random(1))


def test_the_small_log_has_twenty_lines_of_one_to_twenty_milliseconds(tmp_path):
    path = tmp_path / "small.log"
    write_small_log(path)
    requests = [parse(line) for line in path.read_text(encoding="utf-8").splitlines()]
    assert [request.latency_ms for request in requests if request] == list(range(1, 21))
