"""End-to-end integration test — proves the application actually works.

Starts the real FastAPI server, sends real API requests, and verifies
the full autopilot cycle completes. This is not a unit test of individual
components — it is a proof that the assembled application is functional.

Every assertion is backed by a real HTTP response, not a mock.
"""

from __future__ import annotations

import json
import time
import threading
from urllib.request import urlopen, Request
from urllib.error import URLError

import pytest

fastapi = pytest.importorskip("fastapi")
uvicorn = pytest.importorskip("uvicorn")


@pytest.fixture(scope="module")
def server_url(tmp_path_factory):
    """Start the real server on a random port, yield the base URL."""
    import socket
    from netops_autopilot.web.server import create_app

    # Find a free port.
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind(("127.0.0.1", 0))
    port = sock.getsockname()[1]
    sock.close()

    app = create_app()
    ready = threading.Event()

    def _serve():
        import uvicorn as _uv
        config = _uv.Config(app, host="127.0.0.1", port=port,
                            log_level="error", access_log=False)
        server = _uv.Server(config)
        ready.set()
        server.run()

    thread = threading.Thread(target=_serve, daemon=True)
    thread.start()
    ready.wait(timeout=10)

    # Wait for the server to be responsive.
    url = f"http://127.0.0.1:{port}"
    deadline = time.monotonic() + 15
    while time.monotonic() < deadline:
        try:
            resp = urlopen(Request(f"{url}/healthz", method="GET"), timeout=2)
            if resp.status == 200:
                break
        except Exception:
            time.sleep(0.3)
    else:
        pytest.fail("server did not start in time")

    yield url


def _api(url: str, method: str, path: str, data: dict = None) -> dict:
    """Make a real HTTP request to the server."""
    body = json.dumps(data).encode("utf-8") if data else None
    req = Request(
        f"{url}{path}",
        data=body,
        method=method,
        headers={"Content-Type": "application/json"} if body else {},
    )
    resp = urlopen(req, timeout=30)
    return json.loads(resp.read())


def test_healthz_returns_ok(server_url):
    """The server is alive and reports its version."""
    data = _api(server_url, "GET", "/healthz")
    assert data["status"] == "ok"
    assert data["service"] == "netops-autopilot"
    assert "version" in data


def test_demo_run_completes_successfully(server_url):
    """The full autopilot cycle runs to completion on the simulated fabric.

    This is the core proof: the application can discover, design, render,
    and stage a network configuration without any hardware.
    """
    # Start a demo run.
    result = _api(server_url, "POST", "/runs", {
        "port": "SIM0",
        "sim": True,
        "execute": False,
        "intent": "2",
    })
    run_id = result["run_id"]
    assert result["status"] in ("PENDING", "RUNNING")

    # Poll until complete.
    deadline = time.monotonic() + 120
    final_data = None
    while time.monotonic() < deadline:
        data = _api(server_url, "GET", f"/runs/{run_id}")
        if data["status"] in ("COMPLETE", "BLOCKED", "ERROR"):
            final_data = data
            break
        time.sleep(1)

    assert final_data is not None, "run did not finish in 120 seconds"
    assert final_data["status"] == "COMPLETE"
    assert final_data["final"] == "COMPLETE-STAGED"
    assert final_data["error"] is None
    assert len(final_data["phases"]) > 0


def test_topology_is_available_after_run(server_url):
    """After a run completes, the topology endpoint returns real data."""
    # Start and wait for a demo run.
    result = _api(server_url, "POST", "/runs", {
        "port": "SIM0", "sim": True, "execute": False, "intent": "2",
    })
    run_id = result["run_id"]

    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        data = _api(server_url, "GET", f"/runs/{run_id}")
        if data["status"] in ("COMPLETE", "BLOCKED", "ERROR"):
            break
        time.sleep(1)

    topo = _api(server_url, "GET", f"/runs/{run_id}/topology")
    assert "nodes" in topo
    assert len(topo["nodes"]) >= 2, "should discover at least 2 devices"
    assert "edges" in topo
    assert len(topo["edges"]) >= 1, "should find at least 1 link"


def test_html_report_is_rendered(server_url):
    """After a run, the HTML report endpoint returns a real HTML document."""
    result = _api(server_url, "POST", "/runs", {
        "port": "SIM0", "sim": True, "execute": False, "intent": "2",
    })
    run_id = result["run_id"]

    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        data = _api(server_url, "GET", f"/runs/{run_id}")
        if data["status"] in ("COMPLETE", "BLOCKED", "ERROR"):
            break
        time.sleep(1)

    req = Request(f"{server_url}/runs/{run_id}/report", method="GET")
    resp = urlopen(req, timeout=30)
    html = resp.read().decode("utf-8")
    assert "<html" in html.lower()
    assert "netops" in html.lower()
    assert len(html) > 1000


def test_json_report_is_rendered(server_url):
    """After a run, the JSON report endpoint returns structured data."""
    result = _api(server_url, "POST", "/runs", {
        "port": "SIM0", "sim": True, "execute": False, "intent": "2",
    })
    run_id = result["run_id"]

    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        data = _api(server_url, "GET", f"/runs/{run_id}")
        if data["status"] in ("COMPLETE", "BLOCKED", "ERROR"):
            break
        time.sleep(1)

    report = _api(server_url, "GET", f"/runs/{run_id}/report.json")
    assert "run_id" in report or "final" in report


def test_multiple_runs_can_execute_concurrently(server_url):
    """Two demo runs can run at the same time without interfering."""
    r1 = _api(server_url, "POST", "/runs", {
        "port": "SIM0", "sim": True, "execute": False, "intent": "2",
    })
    r2 = _api(server_url, "POST", "/runs", {
        "port": "SIM0", "sim": True, "execute": False, "intent": "2",
    })
    assert r1["run_id"] != r2["run_id"]

    deadline = time.monotonic() + 120
    while time.monotonic() < deadline:
        d1 = _api(server_url, "GET", f"/runs/{r1['run_id']}")
        d2 = _api(server_url, "GET", f"/runs/{r2['run_id']}")
        if d1["status"] in ("COMPLETE", "BLOCKED", "ERROR") and \
           d2["status"] in ("COMPLETE", "BLOCKED", "ERROR"):
            break
        time.sleep(1)

    assert d1["status"] == "COMPLETE"
    assert d2["status"] == "COMPLETE"
