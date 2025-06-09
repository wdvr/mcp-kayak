"""FastMCP server definition for kayak."""
from __future__ import annotations

from dotenv import load_dotenv
import asyncio
from fastapi import FastAPI
from fastmcp import FastMCP
from fastmcp.server.openapi import MCPType, RouteMap

from .travelpayouts_client import TravelpayoutsClient

from .airport_locator import airports_for_location_async

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
) -> dict[str, object]:
    """Search for flights using Travelpayouts."""
    client = TravelpayoutsClient()
    return await asyncio.to_thread(
        client.search_flights, origin, destination, date, cabin
    )


# Convert the FastAPI application to a FastMCP server
server: FastMCP = FastMCP.from_fastapi(
    app,
    route_maps=[
        RouteMap(methods=["GET"], pattern=r"/ping", mcp_type=MCPType.TOOL),
        RouteMap(methods=["GET"], pattern=r"/airports", mcp_type=MCPType.TOOL),
        RouteMap(methods=["GET"], pattern=r"/flights", mcp_type=MCPType.TOOL),
    ],
    mcp_names={
        "ping_ping_get": "ping",
        "airports_airports_get": "airports",
        "flights_flights_get": "flights",
    },
)


if __name__ == "__main__":
    # Running as a script will default to the transport specified in env
    server.run()
