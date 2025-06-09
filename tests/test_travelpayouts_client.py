import os
import sys
from typing import Any

sys.path.insert(
    0,
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..")),
)  # noqa: E402

import pytest

from mcp_kayak.travelpayouts_client import TravelpayoutsClient


def test_init_requires_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("TRAVELPAYOUTS_APIKEY", raising=False)
    with pytest.raises(ValueError):
        TravelpayoutsClient()


def test_search_flights(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TRAVELPAYOUTS_APIKEY", "dummy")
    calls: list[dict[str, Any]] = []

    def fake_post(url: str, json: dict[str, Any], timeout: int) -> Any:
        calls.append(json)

        class Resp:
            def raise_for_status(self) -> None:
                pass

            def json(self) -> dict[str, Any]:
                return {"flights": []}

        return Resp()

    monkeypatch.setattr("httpx.post", fake_post)
    client = TravelpayoutsClient()
    result = client.search_flights("NYC", "LAX", "2024-01-01")
    assert calls[0]["segments"][0]["origin"] == "NYC"
    assert calls[0]["segments"][1]["origin"] == "LAX"  # return segment
    assert calls[0]["currency"] == "USD"
    assert result == {"flights": []}


def test_search_flights_custom_currency(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TRAVELPAYOUTS_APIKEY", "dummy")
    calls: list[dict[str, Any]] = []

    def fake_post(url: str, json: dict[str, Any], timeout: int) -> Any:
        calls.append(json)

        class Resp:
            def raise_for_status(self) -> None:
                pass

            def json(self) -> dict[str, Any]:
                return {"flights": []}

        return Resp()

    monkeypatch.setattr("httpx.post", fake_post)
    client = TravelpayoutsClient(currency="EUR")
    client.search_flights("NYC", "LAX", "2024-01-01")
    assert all(call["currency"] == "EUR" for call in calls)
