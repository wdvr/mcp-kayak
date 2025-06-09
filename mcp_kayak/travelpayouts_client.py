"""Client for querying the Travelpayouts flight search API."""
from __future__ import annotations

import os
from typing import Any

import httpx


class TravelpayoutsClient:
    """Simple client for Travelpayouts flight search."""

    BASE_URL = "https://api.travelpayouts.com"

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
        *,
        include_return: bool = True,
        return_date: str | None = None,
    ) -> dict[str, Any]:
        """Query flights from the Travelpayouts API.

        The request is sent using the ``/v1/flight_search`` endpoint with one or
        two segments depending on ``include_return``. The optional
        ``return_date`` argument controls the date for the return segment and
        defaults to ``date``.
        """
        segments = [
            {"origin": origin, "destination": destination, "date": date}
        ]
        if include_return:
            segments.append(
                {
                    "origin": destination,
                    "destination": origin,
                    "date": return_date or date,
                }
            )
        payload = {
            "signature": self.api_key,
            "trip_class": cabin[0].upper(),
            "currency": currency or self.currency,
            "passengers": {"adults": 1, "children": 0, "infants": 0},
            "segments": segments,
        }
        resp = httpx.post(
            f"{self.base_url}/v1/flight_search",
            json=payload,
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
