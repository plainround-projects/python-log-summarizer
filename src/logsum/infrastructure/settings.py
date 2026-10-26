"""Configuration from the environment (twelve-factor), validated once, with defaults that work."""

from __future__ import annotations

import logging
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Literal, get_args

from logsum.domain.errors import InvalidSettingError

Estimator = Literal["exact", "histogram"]
ESTIMATORS: tuple[str, ...] = get_args(Estimator)


def _integer(environ: Mapping[str, str], name: str, default: int) -> int:
    raw = environ.get(name)
    if raw is None or raw == "":
        return default
    try:
        return int(raw)
    except ValueError:
        raise InvalidSettingError(f"{name} must be a whole number, got {raw!r}") from None


@dataclass(frozen=True, slots=True)
class Settings:
    """Every tunable of the program. Command-line flags override these; these override the defaults."""

    log_level: str = "WARNING"
    top: int = 10
    estimator: Estimator = "exact"
    bucket_ms: int = 5
    max_latency_ms: int = 10_000

    def __post_init__(self) -> None:
        if logging.getLevelName(self.log_level.upper()) == f"Level {self.log_level.upper()}":
            raise InvalidSettingError(
                f"log level must be DEBUG, INFO, WARNING, ERROR or CRITICAL, got {self.log_level!r}"
            )
        if self.top < 1:
            raise InvalidSettingError(f"top must be at least 1, got {self.top}")
        if self.estimator not in ESTIMATORS:
            raise InvalidSettingError(f"estimator must be one of {', '.join(ESTIMATORS)}, got {self.estimator!r}")
        if self.bucket_ms < 1 or self.max_latency_ms < self.bucket_ms:
            raise InvalidSettingError(
                f"need 1 <= bucket_ms <= max_latency_ms, got {self.bucket_ms} and {self.max_latency_ms}"
            )

    @classmethod
    def from_environ(cls, environ: Mapping[str, str]) -> Settings:
        """Read `LOGSUM_LOG_LEVEL`, `LOGSUM_TOP`, `LOGSUM_ESTIMATOR`, `LOGSUM_BUCKET_MS`, `LOGSUM_MAX_LATENCY_MS`."""
        defaults = cls()
        return cls(
            log_level=environ.get("LOGSUM_LOG_LEVEL") or defaults.log_level,
            top=_integer(environ, "LOGSUM_TOP", defaults.top),
            estimator=environ.get("LOGSUM_ESTIMATOR") or defaults.estimator,  # type: ignore[arg-type]
            bucket_ms=_integer(environ, "LOGSUM_BUCKET_MS", defaults.bucket_ms),
            max_latency_ms=_integer(environ, "LOGSUM_MAX_LATENCY_MS", defaults.max_latency_ms),
        )
