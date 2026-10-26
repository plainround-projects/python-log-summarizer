from datetime import UTC, datetime

import pytest

from logsum.domain.request import Request, parse

GOOD = "2026-03-14T09:26:53Z GET /orders/1234 200 87ms"


def test_a_good_line_becomes_a_request():
    assert parse(GOOD) == Request(datetime(2026, 3, 14, 9, 26, 53, tzinfo=UTC), "GET", "/orders/1234", 200, 87)


def test_an_empty_line_is_not_a_request():
    assert parse("") is None


@pytest.mark.parametrize(
    ("line", "why"),
    [
        ("2026-03-14T09:26:53Z GET /orders/1234 200", "a field is missing"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 87ms extra", "an extra field"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 abcms", "the latency is not a number"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 87", "the latency has no ms suffix"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 87s", "the unit is seconds"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 -5ms", "the latency is negative"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 1_0ms", "the latency uses a digit separator"),
        ("2026-03-14T09:26:53Z GET /orders/1234 200 8.5ms", "the latency is not whole milliseconds"),
        ("2026-03-14T09:26:53Z GET /orders/1234 20x 87ms", "the status is not a number"),
        ("2026-03-14T09:26:53Z GET /orders/1234 99 87ms", "the status is below 100"),
        ("2026-03-14T09:26:53Z GET /orders/1234 600 87ms", "the status is above 599"),
        ("yesterday GET /orders/1234 200 87ms", "the timestamp is not a timestamp"),
        ("2026-03-14T09:26:53 GET /orders/1234 200 87ms", "the timestamp has no time zone"),
        ("2026-03-14T09:26:53Z get /orders/1234 200 87ms", "the method is lowercase"),
        ("2026-03-14T09:26:53Z GET orders/1234 200 87ms", "the path does not start with a slash"),
        ("2026-03-14T09:26:53Z GET /orders/1234 ٢٠٠ 87ms", "the status uses non-ASCII digits"),
    ],
)
def test_a_line_not_in_the_format_is_not_a_request(line, why):
    assert parse(line) is None, why


def test_a_line_with_extra_whitespace_between_fields_still_parses():
    assert parse("  2026-03-14T09:26:53Z   GET  /cart\t404  5ms ") is not None


def test_a_request_cannot_be_changed_after_it_is_made():
    request = parse(GOOD)
    assert request is not None
    with pytest.raises(AttributeError):
        request.status = 500  # type: ignore[misc]
