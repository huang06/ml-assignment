from __future__ import annotations

from pathlib import Path

import pytest

here = Path(__file__).resolve().parent


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv(
        "LLM_DIR",
        str(here / "../artifacts/m2m100_418M"),
    )
