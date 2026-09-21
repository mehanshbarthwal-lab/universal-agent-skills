"""Tests for the Streamable HTTP transport on the MCP server (issue #1143).

These exercise the ASGI wiring in-process (no uvicorn, no real socket) via
Starlette's TestClient, so they stay fast and offline. The stdio path is
unchanged and covered elsewhere.
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

pytest.importorskip("mcp")
pytest.importorskip("starlette")

from starlette.testclient import TestClient  # noqa: E402

from graphify import serve as serve_mod  # noqa: E402

SAMPLE_GRAPH = {
    "directed": True,
    "nodes": [
        {"id": "a", "label": "Alpha", "community": 0},
        {"id": "b", "label": "Beta", "community": 0},
    ],
    "edges": [
        {"source": "a", "target": "b", "relation": "calls", "confidence": "EXTRACTED"},
    ],
}

_INIT_BODY = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-03-26",
        "capabilities": {},
        "clientInfo": {"name": "test", "version": "0"},
    },
}

_MCP_HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
}


def _graph_file(tmp_path: Path) -> str:
    p = tmp_path / "graph.json"
    p.write_text(json.dumps(SAMPLE_GRAPH), encoding="utf-8")
    return str(p)


def _client(app) -> TestClient:
    # Default host is 127.0.0.1, so the DNS-rebinding guard only accepts that
    # Host header (TestClient otherwise sends the disallowed "testserver").
    return TestClient(app, base_url="http://127.0.0.1")


def test_app_builds_and_initialize_succeeds(tmp_path):
    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        resp = client.post("/mcp", headers=_MCP_HEADERS, json=_INIT_BODY)
        assert resp.status_code == 200
        # json_response=True returns a single JSON-RPC envelope.
        payload = resp.json()
        assert payload["jsonrpc"] == "2.0"
        assert payload["result"]["serverInfo"]["name"] == "graphify"


def test_unknown_path_is_404(tmp_path):
    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        resp = client.post("/nope", headers=_MCP_HEADERS, json=_INIT_BODY)
        assert resp.status_code == 404


def test_api_key_missing_is_401(tmp_path):
    app = serve_mod._build_http_app(_graph_file(tmp_path), api_key="s3cret", json_response=True)
    with _client(app) as client:
        resp = client.post("/mcp", headers=_MCP_HEADERS, json=_INIT_BODY)
        assert resp.status_code == 401
        assert resp.json()["error"] == "unauthorized"


def test_api_key_wrong_is_401(tmp_path):
    app = serve_mod._build_http_app(_graph_file(tmp_path), api_key="s3cret", json_response=True)
    with _client(app) as client:
        resp = client.post(
            "/mcp",
            headers={**_MCP_HEADERS, "Authorization": "Bearer nope"},
            json=_INIT_BODY,
        )
        assert resp.status_code == 401


def test_api_key_bearer_ok(tmp_path):
    app = serve_mod._build_http_app(_graph_file(tmp_path), api_key="s3cret", json_response=True)
    with _client(app) as client:
        resp = client.post(
            "/mcp",
            headers={**_MCP_HEADERS, "Authorization": "Bearer s3cret"},
            json=_INIT_BODY,
        )
        assert resp.status_code == 200
        assert resp.json()["result"]["serverInfo"]["name"] == "graphify"


def test_api_key_x_api_key_header_ok(tmp_path):
    app = serve_mod._build_http_app(_graph_file(tmp_path), api_key="s3cret", json_response=True)
    with _client(app) as client:
        resp = client.post(
            "/mcp",
            headers={**_MCP_HEADERS, "X-API-Key": "s3cret"},
            json=_INIT_BODY,
        )
        assert resp.status_code == 200


def test_blank_api_key_means_no_auth(tmp_path):
    # An empty/whitespace key must normalize to "no auth", not a key of "".
    app = serve_mod._build_http_app(_graph_file(tmp_path), api_key="   ", json_response=True)
    with _client(app) as client:
        resp = client.post("/mcp", headers=_MCP_HEADERS, json=_INIT_BODY)
        assert resp.status_code == 200


def test_api_key_bearer_scheme_case_insensitive(tmp_path):
    app = serve_mod._build_http_app(_graph_file(tmp_path), api_key="s3cret", json_response=True)
    with _client(app) as client:
        resp = client.post(
            "/mcp",
            headers={**_MCP_HEADERS, "Authorization": "bearer s3cret"},
            json=_INIT_BODY,
        )
        assert resp.status_code == 200


def test_custom_mount_path(tmp_path):
    app = serve_mod._build_http_app(_graph_file(tmp_path), path="/graph", json_response=True)
    with _client(app) as client:
        ok = client.post("/graph", headers=_MCP_HEADERS, json=_INIT_BODY)
        assert ok.status_code == 200
        missing = client.post("/mcp", headers=_MCP_HEADERS, json=_INIT_BODY)
        assert missing.status_code == 404


def test_tools_list_over_http(tmp_path):
    """A full initialize -> tools/list round trip works over the HTTP transport."""
    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        init = client.post("/mcp", headers=_MCP_HEADERS, json=_INIT_BODY)
        assert init.status_code == 200
        session_id = init.headers.get("mcp-session-id")
        assert session_id, "stateful transport should return a session id"
        notify_headers = {**_MCP_HEADERS, "mcp-session-id": session_id}
        client.post(
            "/mcp",
            headers=notify_headers,
            json={"jsonrpc": "2.0", "method": "notifications/initialized"},
        )
        resp = client.post(
            "/mcp",
            headers=notify_headers,
            json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        )
        assert resp.status_code == 200
        names = {t["name"] for t in resp.json()["result"]["tools"]}
        assert {"query_graph", "get_node", "graph_stats"} <= names


def _project_with_graph(tmp_path, node_count: int, name: str = "proj") -> str:
    """Create ``<proj>/graphify-out/graph.json`` and return the project dir."""
    proj = tmp_path / name
    (proj / "graphify-out").mkdir(parents=True)
    graph = {
        "directed": True,
        "nodes": [{"id": f"n{i}", "label": f"N{i}", "community": 0} for i in range(node_count)],
        "edges": [],
    }
    (proj / "graphify-out" / "graph.json").write_text(json.dumps(graph), encoding="utf-8")
    return str(proj)


def _init_session(client) -> dict:
    init = client.post("/mcp", headers=_MCP_HEADERS, json=_INIT_BODY)
    assert init.status_code == 200
    headers = {**_MCP_HEADERS, "mcp-session-id": init.headers.get("mcp-session-id")}
    client.post("/mcp", headers=headers, json={"jsonrpc": "2.0", "method": "notifications/initialized"})
    return headers


def _call_tool(client, headers, name, arguments, rid) -> str:
    resp = client.post("/mcp", headers=headers, json={
        "jsonrpc": "2.0", "id": rid, "method": "tools/call",
        "params": {"name": name, "arguments": arguments},
    })
    assert resp.status_code == 200
    return resp.json()["result"]["content"][0]["text"]


def test_project_path_is_optional_on_every_tool(tmp_path):
    """Multi-project support is additive: every tool gains an optional
    project_path, and none of them makes it required."""
    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        headers = _init_session(client)
        resp = client.post("/mcp", headers=headers,
                            json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
        for tool in resp.json()["result"]["tools"]:
            props = tool["inputSchema"].get("properties", {})
            assert "project_path" in props, f"{tool['name']} missing project_path"
            assert "project_path" not in tool["inputSchema"].get("required", [])


def test_project_path_routes_to_that_projects_graph(tmp_path):
    """One running server answers against the default graph when project_path is
    omitted, and against a project's own graph when it is supplied."""
    proj = _project_with_graph(tmp_path, node_count=3)  # default graph has 2 nodes
    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        headers = _init_session(client)
        assert "Nodes: 2" in _call_tool(client, headers, "graph_stats", {}, rid=2)
        assert "Nodes: 3" in _call_tool(client, headers, "graph_stats", {"project_path": proj}, rid=3)
        # Falling back to the default afterwards still works (no state leak).
        assert "Nodes: 2" in _call_tool(client, headers, "graph_stats", {}, rid=4)


@pytest.mark.parametrize(
    ("value", "expected"),
    [(None, 8), ("", 8), ("bad", 8), ("0", 1), ("-4", 1), ("3", 3)],
)
def test_max_server_contexts_parsing(monkeypatch, value, expected):
    if value is None:
        monkeypatch.delenv("GRAPHIFY_MAX_CONTEXTS", raising=False)
    else:
        monkeypatch.setenv("GRAPHIFY_MAX_CONTEXTS", value)
    assert serve_mod._max_server_contexts() == expected


def test_project_context_cache_is_lru_and_pins_default_graph(tmp_path, monkeypatch):
    """Project contexts hit, promote, and evict without evicting the default."""
    monkeypatch.setenv("GRAPHIFY_MAX_CONTEXTS", "2")
    original_load = serve_mod._load_graph
    loads: dict[str, int] = {}

    def counting_load(path: str):
        resolved = str(Path(path).resolve())
        loads[resolved] = loads.get(resolved, 0) + 1
        return original_load(path)

    monkeypatch.setattr(serve_mod, "_load_graph", counting_load)
    projects = [
        _project_with_graph(tmp_path, node_count=i + 3, name=f"project-{i}")
        for i in range(3)
    ]
    default_graph = _graph_file(tmp_path)
    app = serve_mod._build_http_app(default_graph, json_response=True)
    with _client(app) as client:
        headers = _init_session(client)
        assert "Nodes: 3" in _call_tool(client, headers, "graph_stats", {"project_path": projects[0]}, rid=2)
        assert "Nodes: 4" in _call_tool(client, headers, "graph_stats", {"project_path": projects[1]}, rid=3)
        # A cache hit promotes project-0 above project-1 in LRU recency.
        assert "Nodes: 3" in _call_tool(client, headers, "graph_stats", {"project_path": projects[0]}, rid=4)
        assert "Nodes: 5" in _call_tool(client, headers, "graph_stats", {"project_path": projects[2]}, rid=5)
        # project-1, not the re-touched project-0, was evicted.
        assert "Nodes: 4" in _call_tool(client, headers, "graph_stats", {"project_path": projects[1]}, rid=6)
        # The configured default graph stays warm even when project capacity is full.
        assert "Nodes: 2" in _call_tool(client, headers, "graph_stats", {}, rid=7)

    first_graph = str((Path(projects[0]) / "graphify-out" / "graph.json").resolve())
    second_graph = str((Path(projects[1]) / "graphify-out" / "graph.json").resolve())
    default_graph = str(Path(default_graph).resolve())
    assert loads[first_graph] == 1
    assert loads[second_graph] == 2
    assert loads[default_graph] == 1


def test_bad_project_path_errors_without_killing_server(tmp_path):
    """A missing project graph is a tool error, not a process exit — the server
    keeps serving the default graph."""
    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        headers = _init_session(client)
        bad = _call_tool(client, headers, "graph_stats",
                         {"project_path": str(tmp_path / "does-not-exist")}, rid=2)
        assert "not found" in bad.lower()
        assert "Nodes: 2" in _call_tool(client, headers, "graph_stats", {}, rid=3)


def test_corrupt_project_graph_is_a_tool_error_without_killing_server(tmp_path):
    """A CLI-style SystemExit from a client graph cannot stop the MCP server."""
    project = Path(_project_with_graph(tmp_path, node_count=3))
    (project / "graphify-out" / "graph.json").write_text("{not json", encoding="utf-8")
    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        headers = _init_session(client)
        bad = _call_tool(client, headers, "graph_stats", {"project_path": str(project)}, rid=2)
        assert "could not load graph.json" in bad
        assert "Nodes: 2" in _call_tool(client, headers, "graph_stats", {}, rid=3)


def test_stateless_mode_initialize(tmp_path):
    app = serve_mod._build_http_app(_graph_file(tmp_path), stateless=True, json_response=True)
    with _client(app) as client:
        resp = client.post("/mcp", headers=_MCP_HEADERS, json=_INIT_BODY)
        assert resp.status_code == 200


def test_stateless_with_timeout_does_not_raise(tmp_path):
    # session_timeout must be forced to None in stateless mode (the SDK raises
    # RuntimeError otherwise). Building + a request should just work.
    app = serve_mod._build_http_app(
        _graph_file(tmp_path), stateless=True, session_timeout=3600, json_response=True
    )
    with _client(app) as client:
        assert client.post("/mcp", headers=_MCP_HEADERS, json=_INIT_BODY).status_code == 200


def test_session_timeout_zero_disables(tmp_path):
    # 0 / non-positive must disable reaping without tripping the SDK's validation.
    app = serve_mod._build_http_app(_graph_file(tmp_path), session_timeout=0, json_response=True)
    with _client(app) as client:
        assert client.post("/mcp", headers=_MCP_HEADERS, json=_INIT_BODY).status_code == 200


# --- CLI argument parsing -------------------------------------------------

def test_cli_defaults_to_stdio(monkeypatch):
    calls = {}
    monkeypatch.setattr(serve_mod, "serve", lambda gp: calls.setdefault("stdio", gp))
    monkeypatch.setattr(
        serve_mod, "serve_http", lambda *a, **k: calls.setdefault("http", (a, k))
    )
    serve_mod._main(["graphify-out/graph.json"])
    assert calls.get("stdio") == "graphify-out/graph.json"
    assert "http" not in calls


def test_cli_http_passes_flags(monkeypatch):
    captured = {}
    monkeypatch.setattr(serve_mod, "serve", lambda gp: captured.setdefault("stdio", gp))
    monkeypatch.setattr(
        serve_mod, "serve_http", lambda gp, **k: captured.update(gp=gp, **k)
    )
    serve_mod._main([
        "g.json", "--transport", "http", "--host", "0.0.0.0",
        "--port", "9000", "--api-key", "k", "--stateless",
    ])
    assert captured["gp"] == "g.json"
    assert captured["host"] == "0.0.0.0"
    assert captured["port"] == 9000
    assert captured["api_key"] == "k"
    assert captured["stateless"] is True


def test_cli_api_key_from_env(monkeypatch):
    captured = {}
    monkeypatch.setenv("GRAPHIFY_API_KEY", "from-env")
    monkeypatch.setattr(serve_mod, "serve_http", lambda gp, **k: captured.update(**k))
    serve_mod._main(["g.json", "--transport", "http"])
    assert captured["api_key"] == "from-env"


def test_pr_tools_annotations_and_descriptions(tmp_path):
    """The three PR tools have explicit boolean annotations and descriptions."""
    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        headers = _init_session(client)
        resp = client.post(
            "/mcp",
            headers=headers,
            json={"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}},
        )
        assert resp.status_code == 200
        tools = {t["name"]: t for t in resp.json()["result"]["tools"]}

        for name in ("list_prs", "get_pr_impact", "triage_prs"):
            assert name in tools, f"tool {name} missing from tools/list"
            tool = tools[name]
            assert tool["description"], f"{name} description must not be empty"
            ann = tool.get("annotations")
            assert ann is not None, f"{name} must have annotations"
            assert ann.get("readOnlyHint") is True
            assert ann.get("destructiveHint") is False
            assert ann.get("idempotentHint") is True
            assert ann.get("openWorldHint") is True


def test_tool_list_prs_execution(tmp_path, monkeypatch):
    """list_prs validates input and formats PR output correctly."""
    from datetime import datetime, timezone
    from graphify.prs import PRInfo
    import graphify.prs as prs_mod

    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        headers = _init_session(client)

        # 1. Invalid repo format rejected
        err = _call_tool(client, headers, "list_prs", {"repo": "invalid..repo;rm"}, rid=10)
        assert "Error: Invalid repository format" in err

        # 2. Invalid base branch format rejected
        err_base = _call_tool(client, headers, "list_prs", {"base": "-bad-flag"}, rid=11)
        assert "Error: Invalid base branch format" in err_base

        # 3. Successful fetch with mock PRs
        mock_pr = PRInfo(
            number=42,
            title="Feature workflow enhancement",
            branch="feat/workflow",
            base_branch="main",
            author="alice",
            is_draft=False,
            review_decision="APPROVED",
            ci_status="SUCCESS",
            updated_at=datetime.now(timezone.utc),
            expected_base="main",
        )
        monkeypatch.setattr(prs_mod, "fetch_prs", lambda repo=None, base="main": [mock_pr])
        monkeypatch.setattr(prs_mod, "fetch_worktrees", lambda: {})

        res = _call_tool(client, headers, "list_prs", {"repo": "owner/repo", "base": "main"}, rid=12)
        assert "#42" in res
        assert "Feature workflow enhancement" in res
        assert "alice" in res

        # 4. Successful fetch when no base is passed (falls back to _detect_default_branch)
        detected_base = []
        monkeypatch.setattr(
            prs_mod,
            "_detect_default_branch",
            lambda repo=None: detected_base.append(repo) or "main",
        )
        res_no_base = _call_tool(client, headers, "list_prs", {"repo": "owner/repo"}, rid=13)
        assert "#42" in res_no_base
        assert detected_base == ["owner/repo"]



def test_tool_get_pr_impact_execution(tmp_path, monkeypatch):
    """get_pr_impact validates inputs and computes impact metrics."""
    import graphify.prs as prs_mod

    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        headers = _init_session(client)

        # 1. Negative or zero pr_number rejected
        err_num = _call_tool(client, headers, "get_pr_impact", {"pr_number": 0}, rid=20)
        assert "Error: pr_number must be a positive integer." in err_num

        # 2. Invalid repo format rejected
        err_repo = _call_tool(client, headers, "get_pr_impact", {"pr_number": 1, "repo": "bad repo"}, rid=21)
        assert "Error: Invalid repository format" in err_repo

        # 3. Not found / unauthenticated
        monkeypatch.setattr(prs_mod, "_gh", lambda *args: None)
        not_found = _call_tool(client, headers, "get_pr_impact", {"pr_number": 999}, rid=22)
        assert "PR #999 not found or gh not authenticated." in not_found

        # 4. Successful impact calculation
        mock_view = {
            "title": "Update core module",
            "headRefName": "feat/core",
            "baseRefName": "main",
            "author": {"login": "bob"},
            "isDraft": False,
            "reviewDecision": "APPROVED",
            "statusCheckRollup": [],
            "updatedAt": "2026-03-01T00:00:00Z",
        }
        monkeypatch.setattr(prs_mod, "_gh", lambda *args: mock_view)
        monkeypatch.setattr(prs_mod, "fetch_pr_files", lambda number, repo=None: ["a.py", "b.py"])

        res = _call_tool(client, headers, "get_pr_impact", {"pr_number": 10}, rid=23)
        assert "PR #10: Update core module" in res
        assert "Graph impact:" in res
        assert "Files changed (2):" in res


def test_tool_triage_prs_execution(tmp_path, monkeypatch):
    """triage_prs validates inputs and ranks actionable PRs."""
    from datetime import datetime, timezone
    from graphify.prs import PRInfo
    import graphify.prs as prs_mod

    app = serve_mod._build_http_app(_graph_file(tmp_path), json_response=True)
    with _client(app) as client:
        headers = _init_session(client)

        # 1. Invalid repo format rejected
        err = _call_tool(client, headers, "triage_prs", {"repo": "evil/repo;id"}, rid=30)
        assert "Error: Invalid repository format" in err

        # 2. No actionable PRs
        monkeypatch.setattr(prs_mod, "fetch_prs", lambda repo=None, base="main": [])
        monkeypatch.setattr(prs_mod, "fetch_worktrees", lambda: {})
        empty = _call_tool(client, headers, "triage_prs", {"base": "main"}, rid=31)
        assert "No actionable PRs targeting main." in empty

        # 3. Actionable PRs ranked
        actionable_pr = PRInfo(
            number=77,
            title="Refactor query router",
            branch="refactor/router",
            base_branch="main",
            author="carol",
            is_draft=False,
            review_decision="APPROVED",
            ci_status="SUCCESS",
            updated_at=datetime.now(timezone.utc),
            expected_base="main",
        )
        monkeypatch.setattr(prs_mod, "fetch_prs", lambda repo=None, base="main": [actionable_pr])
        monkeypatch.setattr(prs_mod, "fetch_pr_files", lambda number, repo=None: ["router.py"])

        res = _call_tool(client, headers, "triage_prs", {"base": "main"}, rid=32)
        assert "Actionable PRs targeting main: 1" in res
        assert "PR #77" in res
        assert "carol" in res

        # 4. Triage when no base is passed (falls back to _detect_default_branch)
        detected_triage_base = []
        monkeypatch.setattr(
            prs_mod,
            "_detect_default_branch",
            lambda repo=None: detected_triage_base.append(repo) or "main",
        )
        res_no_base = _call_tool(client, headers, "triage_prs", {"repo": "owner/repo"}, rid=33)
        assert "Actionable PRs targeting main: 1" in res_no_base
        assert detected_triage_base == ["owner/repo"]


