"""Client for querying the Google Flights Search API via RapidAPI."""
from __future__ import annotations

import os
from typing import Any

import httpx


class GoogleFlightsClient:
    """Simple client for Google Flights Search."""

    BASE_URL = "https://google-flights13.p.rapidapi.com"

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("GOOGLE_FLIGHTS_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_FLIGHTS_API_KEY missing")
        self.base_url = base_url or self.BASE_URL

    def search_flights(
        self, origin: str, destination: str, date: str, cabin: str = "economy"
    ) -> dict[str, Any]:
        """Query flights from the Google Flights Search API."""
        params = {
            "origin": origin,
            "destination": destination,
            "date": date,
            "cabin": cabin,
        }
        headers = {
            "X-RapidAPI-Key": self.api_key,
        }
        resp = httpx.get(
            f"{self.base_url}/flights",
            params=params,
            headers=headers,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
