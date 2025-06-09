from __future__ import annotations

import json
from importlib import resources
from functools import lru_cache


@lru_cache(maxsize=None)
def _load_airlines() -> dict[str, str]:
    data_path = resources.files("mcp_kayak.data").joinpath("airlines.json")
    with resources.as_file(data_path) as path:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)


def get_airline_name(code: str) -> str | None:
    """Return the airline name for a two-letter IATA code."""
    code = code.upper()
    return _load_airlines().get(code)


def format_duration(minutes: int) -> str:
    """Return a human-friendly duration string for minutes."""
    hours, mins = divmod(minutes, 60)
    parts: list[str] = []
    if hours:
        parts.append(f"{hours}h")
    if mins or not parts:
        parts.append(f"{mins}m")
    return "".join(parts)
