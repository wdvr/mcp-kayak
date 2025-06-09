"""CLI entrypoint to run the FastMCP server."""
from .server import server

if __name__ == "__main__":
    server.run()
