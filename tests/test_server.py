import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from mcp_kayak.server import app, server
from fastapi.testclient import TestClient


def test_ping() -> None:
    client = TestClient(app)
    resp = client.get("/ping")
    assert resp.status_code == 200
    assert resp.json() == {"pong": True}


def test_server_has_run() -> None:
    assert hasattr(server, "run")
