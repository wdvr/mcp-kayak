"""FastMCP server definition for kayak."""
from __future__ import annotations

from dotenv import load_dotenv
from fastapi import FastAPI
from fastmcp import FastMCP

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


# Convert the FastAPI application to a FastMCP server
server: FastMCP = FastMCP.from_fastapi(app)


if __name__ == "__main__":
    # Running as a script will default to the transport specified in env
    server.run()
