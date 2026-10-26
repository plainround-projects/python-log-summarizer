import pytest

from logsum.domain.errors import InvalidSettingError
from logsum.infrastructure.settings import Settings


def test_no_environment_gives_the_defaults():
    assert Settings.from_environ({}) == Settings(
        log_level="WARNING", top=10, estimator="exact", bucket_ms=5, max_latency_ms=10_000
    )


def test_every_variable_is_read():
    settings = Settings.from_environ(
        {
            "LOGSUM_LOG_LEVEL": "debug",
            "LOGSUM_TOP": "3",
            "LOGSUM_ESTIMATOR": "histogram",
            "LOGSUM_BUCKET_MS": "2",
            "LOGSUM_MAX_LATENCY_MS": "500",
        }
    )
    assert (settings.log_level, settings.top, settings.estimator, settings.bucket_ms, settings.max_latency_ms) == (
        "debug",
        3,
        "histogram",
        2,
        500,
    )


def test_an_empty_variable_means_the_default():
    assert Settings.from_environ({"LOGSUM_TOP": "", "LOGSUM_ESTIMATOR": ""}) == Settings()


@pytest.mark.parametrize(
    "environ",
    [
        {"LOGSUM_TOP": "many"},
        {"LOGSUM_TOP": "0"},
        {"LOGSUM_ESTIMATOR": "median"},
        {"LOGSUM_LOG_LEVEL": "LOUD"},
        {"LOGSUM_BUCKET_MS": "0"},
        {"LOGSUM_BUCKET_MS": "50", "LOGSUM_MAX_LATENCY_MS": "10"},
    ],
)
def test_a_value_the_program_cannot_use_is_rejected_by_name(environ):
    with pytest.raises(InvalidSettingError):
        Settings.from_environ(environ)
