"""FastMCP server definition for kayak."""
from __future__ import annotations

from dotenv import load_dotenv
import asyncio
from fastapi import FastAPI
from fastmcp import FastMCP
from fastmcp.server.openapi import MCPType, RouteMap

from .travelpayouts_client import TravelpayoutsClient

from .airport_locator import airports_for_location_async
from .airline_utils import format_duration, get_airline_name

# Load environment variables from .env if present
load_dotenv()

app = FastAPI(title="mcp-kayak")


@app.get("/ping")
async def ping() -> dict[str, bool]:
    """Health check endpoint."""
    return {"pong": True}


@app.get("/airports")
async def airports(location: str, limit: int = 5) -> dict[str, list[dict[str, float | str]]]:
    """Return closest airports for a location."""
    results = await airports_for_location_async(location, limit)
    return {"airports": results}


@app.get("/flights")
async def flights(
    origin: str,
    destination: str,
    date: str,
    cabin: str = "economy",
    currency: str | None = None,
) -> dict[str, object]:
    """Search for flights using Travelpayouts."""
    client = TravelpayoutsClient()
    return await asyncio.to_thread(
        client.search_flights,
        origin,
        destination,
        date,
        cabin,
        currency,
    )


@app.get("/decode")
async def decode(
    airline_code: str,
    duration: int,
    layovers: int | None = None,
) -> dict[str, object]:
    """Decode coded flight data into human readable form."""
    result = {
        "airline": get_airline_name(airline_code) or airline_code,
        "duration": format_duration(duration),
    }
    if layovers is not None:
        result["layovers"] = layovers
    return result


# Convert the FastAPI application to a FastMCP server
server: FastMCP = FastMCP.from_fastapi(
    app,
    route_maps=[
        RouteMap(methods=["GET"], pattern=r"/ping", mcp_type=MCPType.TOOL),
        RouteMap(methods=["GET"], pattern=r"/airports", mcp_type=MCPType.TOOL),
        RouteMap(methods=["GET"], pattern=r"/flights", mcp_type=MCPType.TOOL),
        RouteMap(methods=["GET"], pattern=r"/decode", mcp_type=MCPType.TOOL),
    ],
    mcp_names={
        "ping_ping_get": "ping",
        "airports_airports_get": "airports",
        "flights_flights_get": "flights",
        "decode_decode_get": "decode",
    },
)


if __name__ == "__main__":
    # Running as a script will default to the transport specified in env
    server.run()
