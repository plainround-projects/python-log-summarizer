"""Reading a log from disk, plain or gzip-compressed, one line at a time."""

from __future__ import annotations

import gzip
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path
from typing import TextIO

from logsum.domain.errors import UnreadableLogFileError

_ENCODING = "utf-8"


class FileLineSource:
    """Opens files by path. A name ending in `.gz` is decompressed on the fly, still a line at a time."""

    @contextmanager
    def open(self, location: str) -> Iterator[Iterator[str]]:
        """Yield the lines of the file at `location`; always close it.

        Bytes that are not valid UTF-8 are replaced and not raised: a line with them is then one more bad
        line, and one bad line never stops the run.
        """
        path = Path(location)
        try:
            handle = self._open_text(path)
        except OSError as error:
            raise UnreadableLogFileError(location, error.strerror or str(error)) from error
        with handle:
            yield self._lines(handle, location)

    @staticmethod
    def _open_text(path: Path) -> TextIO:
        if path.suffix == ".gz":
            return gzip.open(path, "rt", encoding=_ENCODING, errors="replace")
        return path.open(encoding=_ENCODING, errors="replace")

    @staticmethod
    def _lines(handle: TextIO, location: str) -> Iterator[str]:
        try:
            yield from handle
        except (OSError, EOFError) as error:
            raise UnreadableLogFileError(location, str(error)) from error
