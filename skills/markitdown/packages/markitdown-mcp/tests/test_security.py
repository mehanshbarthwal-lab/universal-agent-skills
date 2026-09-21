import os
import pytest
import requests
from requests.adapters import HTTPAdapter
from markitdown_mcp.__main__ import mcp, _validate_uri, SSRFProtectedSession


def test_convert_to_markdown_annotations():
    """Verify convert_to_markdown annotations match requirements."""
    tools = mcp._tool_manager.list_tools()
    tool = next((t for t in tools if t.name == "convert_to_markdown"), None)
    assert tool is not None
    assert tool.annotations.readOnlyHint is True
    assert tool.annotations.destructiveHint is False
    assert tool.annotations.idempotentHint is True
    assert tool.annotations.openWorldHint is True


@pytest.mark.parametrize(
    "marker",
    [
        ".env",
        ".kube/config",
        ".netrc",
        ".npmrc",
        ".gnupg",
        ".ssh/id_ecdsa",
        ".docker/config.json",
        "/etc/shadow",
        "/etc/passwd",
        "/etc/sudoers",
        "credentials.env",
        ".aws/credentials",
        ".ssh/id_rsa",
        ".ssh/id_ed25519",
    ],
)
def test_sensitive_markers_blocked(marker):
    """Verify every sensitive marker is blocked by _validate_uri."""
    uri = f"file:///home/user/{marker}"
    with pytest.raises(ValueError, match="Access to sensitive file path"):
        _validate_uri(uri)


def test_env_filename_matching():
    """Verify harmless files like my.envelope.txt are allowed while .env.production is blocked."""
    # my.envelope.txt is NOT blocked
    _validate_uri("file:///home/user/docs/my.envelope.txt")

    # .env.production IS blocked
    with pytest.raises(ValueError, match="Access to sensitive file path"):
        _validate_uri("file:///home/user/app/.env.production")


def test_symlink_to_blocked_file_rejected(tmp_path):
    """Verify symlinks pointing to sensitive files are resolved and blocked."""
    secret_file = tmp_path / ".env"
    secret_file.write_text("API_SECRET=super_secret_value")

    link_file = tmp_path / "innocent_document.txt"
    try:
        os.symlink(str(secret_file), str(link_file))
    except (OSError, NotImplementedError) as exc:
        pytest.skip(f"Symlinks not supported on this platform/privilege level: {exc}")

    link_uri = f"file:///{str(link_file).replace(os.sep, '/')}"
    with pytest.raises(ValueError, match="Access to sensitive file path"):
        _validate_uri(link_uri)


def test_redirect_to_loopback_blocked():
    """Verify SSRFProtectedSession blocks redirects targeting loopback or private ranges."""
    session = SSRFProtectedSession()

    class RedirectAdapter(HTTPAdapter):
        def send(self, request, **kwargs):
            resp = requests.Response()
            resp.request = request
            if request.url == "http://example.com/initial":
                resp.status_code = 302
                resp.headers["location"] = "http://127.0.0.1:8080/admin"
                resp.url = request.url
            else:
                resp.status_code = 200
                resp.url = request.url
            return resp

    session.mount("http://", RedirectAdapter())

    with pytest.raises(ValueError, match="Access to loopback address"):
        session.get("http://example.com/initial")


def test_redirect_to_private_ip_blocked():
    """Verify SSRFProtectedSession blocks redirects targeting private RFC1918 IPs."""
    session = SSRFProtectedSession()

    class PrivateRedirectAdapter(HTTPAdapter):
        def send(self, request, **kwargs):
            resp = requests.Response()
            resp.request = request
            if request.url == "http://example.com/start":
                resp.status_code = 302
                resp.headers["location"] = "http://192.168.1.1/router"
                resp.url = request.url
            else:
                resp.status_code = 200
                resp.url = request.url
            return resp

    session.mount("http://", PrivateRedirectAdapter())

    with pytest.raises(ValueError, match="Access to private/local network address"):
        session.get("http://example.com/start")
