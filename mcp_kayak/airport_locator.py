from __future__ import annotations

import asyncio
from typing import Any

from geopy.distance import geodesic
from geopy.geocoders import Nominatim
import airportsdata
import ssl
import certifi


def airports_for_location(location: str, limit: int = 5) -> list[dict[str, Any]]:
    """Return nearest airports for a location."""
    ssl_context = ssl.create_default_context(cafile=certifi.where())
    geo = Nominatim(user_agent="mcp-kayak", ssl_context=ssl_context)
    loc = geo.geocode(location)
    if loc is None:
        raise ValueError("Location not found")
    lat = loc.latitude
    lon = loc.longitude

    airports = airportsdata.load("IATA")
    major_codes: set[str] = set()
    for mac in airportsdata.load_iata_macs().values():
        major_codes.update(mac["airports"].keys())

    results: list[dict[str, Any]] = []
    for code, data in airports.items():
        if not data.get("lat") or not data.get("lon"):
            continue

        name_lower = data["name"].lower()
        is_airport = "airport" in name_lower
        small_terms = ["airstrip", "heliport", "seaplane", "glider", "closed"]
        is_small = any(term in name_lower for term in small_terms)
        is_major = (
            "international" in name_lower
            or code in major_codes
            or (is_airport and not is_small)
        )
        if not is_major:
            continue

        dist = geodesic((lat, lon), (data["lat"], data["lon"]))
        results.append({"code": code, "name": data["name"], "distance_km": dist.km})
    results.sort(key=lambda r: r["distance_km"])
    return results[:limit]


async def airports_for_location_async(location: str, limit: int = 5) -> list[dict[str, Any]]:
    """Async wrapper for :func:`airports_for_location`."""
    return await asyncio.to_thread(airports_for_location, location, limit)
