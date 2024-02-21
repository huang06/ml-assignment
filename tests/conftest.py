from __future__ import annotations

from pathlib import Path

import pytest

here = Path(__file__).resolve().parent


@pytest.fixture(autouse=True)
def mock_env(monkeypatch):
    monkeypatch.setenv(
        "LLM_DIR",
        str(here / "../artifacts/models--facebook--m2m100_418M/snapshots/62d980b8566a7c30e96918baf450d6a7218aadec"),
    )
