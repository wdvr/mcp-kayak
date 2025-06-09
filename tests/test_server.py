"""Tests for the FastMCP server wrapper."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # noqa: E402

from fastapi.testclient import TestClient  # noqa: E402
from mcp_kayak.server import app, server  # noqa: E402


class DummyLoc:
    latitude = 37.5483
    longitude = -121.9886


def test_ping() -> None:
    client = TestClient(app)
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.json() == {"pong": True}


def test_server_has_run() -> None:
    assert hasattr(server, "run")


def test_airports(monkeypatch) -> None:
    client = TestClient(app)

    def fake_geocode(self, location: str):
        return DummyLoc()

    monkeypatch.setattr("mcp_kayak.airport_locator.Nominatim.geocode", fake_geocode)
    monkeypatch.setattr(
        "airportsdata.load",
        lambda kind: {
            "SJC": {"name": "San Jose International", "lat": 37.3626, "lon": -121.929},
            "OAK": {"name": "Oakland International", "lat": 37.7213, "lon": -122.221},
        },
    )
    monkeypatch.setattr("airportsdata.load_iata_macs", lambda: {})

    resp = client.get("/airports", params={"location": "Fremont, CA", "limit": 1})
    assert resp.status_code == 200
    data = resp.json()
    assert data["airports"][0]["code"] == "SJC"


def test_flights(monkeypatch) -> None:
    client = TestClient(app)

    monkeypatch.setenv("TRAVELPAYOUTS_APIKEY", "dummy")

    called: dict[str, dict[str, str]] = {}

    def fake_get(url: str, params: dict[str, str], timeout: int):
        called["params"] = params

        class Resp:
            def raise_for_status(self) -> None:
                pass

            def json(self) -> dict[str, list[object]]:
                return {"flights": []}

        return Resp()

    monkeypatch.setattr("httpx.get", fake_get)

    resp = client.get(
        "/flights",
        params={"origin": "NYC", "destination": "LAX", "date": "2024-01-01"},
    )
    assert resp.status_code == 200
    assert resp.json() == {"flights": []}
    assert called["params"]["currency"] == "USD"


def test_tools_available() -> None:
    tools = [t.name for t in server.list_tools()]
    assert "ping_ping_get" in tools
    assert "airports_airports_get" in tools
    assert "flights_flights_get" in tools
