import io
import logging

from logsum.infrastructure.logging import LogfmtFormatter, configure_logging


def record(message="hello", **fields):
    made = logging.LogRecord("logsum.test", logging.INFO, __file__, 1, message, None, None)
    made.fields = fields
    return made


def test_a_record_becomes_one_logfmt_line_with_its_fields():
    line = LogfmtFormatter().format(record("summarized log", location="a b.log", requests=5))
    assert line.startswith("ts=")
    assert 'level=INFO logger=logsum.test msg="summarized log" location="a b.log" requests=5' in line
    assert "\n" not in line


def test_an_exception_is_kept_on_the_same_line():
    try:
        raise ValueError("boom")
    except ValueError:
        import sys

        made = logging.LogRecord("x", logging.ERROR, __file__, 1, "failed", None, sys.exc_info())
    line = LogfmtFormatter().format(made)
    assert "exc=" in line
    assert "\n" not in line.replace("\\n", "")


def test_configure_logging_replaces_handlers_and_sets_the_level():
    stream = io.StringIO()
    configure_logging("INFO", stream)
    configure_logging("INFO", stream)
    logging.getLogger("logsum.test").info("one", extra={"fields": {"n": 1}})
    assert stream.getvalue().count("msg=one") == 1
    assert len(logging.getLogger().handlers) == 1
