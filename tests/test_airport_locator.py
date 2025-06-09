import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))  # noqa: E402

from mcp_kayak import airport_locator


class DummyLoc:
    latitude = 37.5483
    longitude = -121.9886


def test_airports_for_location(monkeypatch):
    def fake_geocode(self, location: str):
        return DummyLoc()

    monkeypatch.setattr(airport_locator.Nominatim, "geocode", fake_geocode)
    monkeypatch.setattr(
        "airportsdata.load",
        lambda kind: {
            "SJC": {"name": "San Jose International", "lat": 37.3626, "lon": -121.929},
            "OAK": {"name": "Oakland International", "lat": 37.7213, "lon": -122.221},
        },
    )

    results = airport_locator.airports_for_location("Fremont, CA", limit=1)
    assert results[0]["code"] == "SJC"
