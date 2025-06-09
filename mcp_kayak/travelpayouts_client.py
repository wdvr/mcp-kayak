"""Client for querying the Travelpayouts flight search API."""
from __future__ import annotations

import os
from typing import Any

import httpx


class TravelpayoutsClient:
    """Simple client for Travelpayouts flight search."""

    BASE_URL = "https://api.travelpayouts.com/aviasales/v3"

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        currency: str | None = None,
    ) -> None:
        self.api_key = api_key or os.getenv("TRAVELPAYOUTS_APIKEY")
        if not self.api_key:
            raise ValueError("TRAVELPAYOUTS_APIKEY missing")
        self.base_url = base_url or self.BASE_URL
        self.currency = currency or os.getenv("TRAVELPAYOUTS_CURRENCY", "USD")

    def search_flights(
        self,
        origin: str,
        destination: str,
        date: str,
        cabin: str = "economy",
        currency: str | None = None,
    ) -> dict[str, Any]:
        """Query flights from the Travelpayouts API."""
        params = {
            "origin": origin,
            "destination": destination,
            "depart_date": date,
            "trip_class": cabin,
            "token": self.api_key,
            "currency": currency or self.currency,
        }
        resp = httpx.get(
            f"{self.base_url}/prices_for_dates",
            params=params,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
