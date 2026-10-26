"""Shared fixtures."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="session")
def data_dir() -> Path:
    return ROOT / "tests" / "data"


@pytest.fixture(scope="session")
def summary_schema() -> dict[str, Any]:
    schema: dict[str, Any] = json.loads((ROOT / "docs" / "summary.schema.json").read_text(encoding="utf-8"))
    return schema
