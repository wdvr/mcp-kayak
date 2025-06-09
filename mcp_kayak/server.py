"""FastMCP server definition for kayak."""
from __future__ import annotations

import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastmcp import FastMCP

# Load environment variables from .env if present
load_dotenv()

app = FastAPI(title="mcp-kayak")


@app.get("/ping")
async def ping() -> dict[str, bool]:
    """Health check endpoint."""
    return {"pong": True}


# Convert the FastAPI application to a FastMCP server
server: FastMCP = FastMCP.from_fastapi(app)


if __name__ == "__main__":
    # Running as a script will default to the transport specified in env
    server.run()
