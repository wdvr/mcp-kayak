from __future__ import annotations

import asyncio
from typing import Any

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import airportsdata


def airports_for_location(location: str, limit: int = 5) -> list[dict[str, Any]]:
    """Return nearest airports for a location."""
    geo = Nominatim(user_agent="mcp-kayak")
    loc = geo.geocode(location)
    if loc is None:
        raise ValueError("Location not found")
    lat = loc.latitude
    lon = loc.longitude

    airports = airportsdata.load("IATA")
    results: list[dict[str, Any]] = []
    for code, data in airports.items():
        if not data.get("lat") or not data.get("lon"):
            continue
        dist = geodesic((lat, lon), (data["lat"], data["lon"]))
        results.append({"code": code, "name": data["name"], "distance_km": dist.km})
    results.sort(key=lambda r: r["distance_km"])
    return results[:limit]


async def airports_for_location_async(location: str, limit: int = 5) -> list[dict[str, Any]]:
    """Async wrapper for :func:`airports_for_location`."""
    return await asyncio.to_thread(airports_for_location, location, limit)
