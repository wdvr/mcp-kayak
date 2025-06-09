import os
import sys
from typing import Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest

from mcp_kayak.travelpayouts_client import TravelpayoutsClient


def test_init_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TRAVELPAYOUTS_APIKEY", raising=False)
    with pytest.raises(ValueError):
        TravelpayoutsClient()


def test_search_flights(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TRAVELPAYOUTS_APIKEY", "dummy")
    called: dict[str, Any] = {}

    def fake_get(url: str, params: dict[str, Any], timeout: int) -> Any:
        called["url"] = url
        called["params"] = params

        class Resp:
            def raise_for_status(self) -> None:
                pass

            def json(self) -> dict[str, Any]:
                return {"flights": []}

        return Resp()

    monkeypatch.setattr("httpx.get", fake_get)
    client = TravelpayoutsClient()
    result = client.search_flights("NYC", "LAX", "2024-01-01")
    assert called["params"]["origin"] == "NYC"
    assert "token" in called["params"]
    assert result == {"flights": []}
