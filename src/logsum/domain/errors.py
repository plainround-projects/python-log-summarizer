"""Named errors, so callers handle a failure by what it means and not by message text."""


class LogsumError(Exception):
    """Base class of every error this program raises on purpose."""


class UnreadableLogFileError(LogsumError):
    """The log file does not exist, is a directory, or cannot be opened or decompressed."""

    def __init__(self, location: str, reason: str) -> None:
        super().__init__(f"cannot read {location}: {reason}")
        self.location = location
        self.reason = reason


class EmptyDistributionError(LogsumError):
    """A percentile was asked of a distribution that holds no latencies."""


class InvalidSettingError(LogsumError):
    """A setting (environment variable or flag) has a value the program cannot use."""
