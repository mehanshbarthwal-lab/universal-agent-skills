import contextlib
import sys
import os
import ipaddress
import socket
from urllib.parse import urlparse, unquote
from collections.abc import AsyncIterator
from mcp.server.fastmcp import FastMCP
from mcp.types import ToolAnnotations
from starlette.applications import Starlette
from mcp.server.sse import SseServerTransport
from starlette.requests import Request
from starlette.routing import Mount, Route
from starlette.types import Receive, Scope, Send
from mcp.server import Server
from mcp.server.streamable_http_manager import StreamableHTTPSessionManager
from typing import Any
import requests
from markitdown import MarkItDown
import uvicorn

# Initialize FastMCP server for MarkItDown (SSE)
mcp = FastMCP("markitdown")


def _is_private_or_loopback_ip(ip: ipaddress.IPv4Address | ipaddress.IPv6Address) -> bool:
    return (
        ip.is_private
        or ip.is_loopback
        or ip.is_link_local
        or ip.is_multicast
        or ip.is_reserved
        or ip.is_unspecified
    )


def _validate_uri(uri: str) -> None:
    parsed = urlparse(uri)
    scheme = parsed.scheme.lower()
    if not scheme:
        raise ValueError(f"Invalid URI '{uri}': missing scheme. Supported schemes: http, https, file, data.")

    if scheme in ("http", "https"):
        hostname = parsed.hostname
        if not hostname:
            raise ValueError("HTTP/HTTPS URI missing hostname.")

        allow_private = os.getenv("MARKITDOWN_ALLOW_PRIVATE_NETWORKS", "false").strip().lower() in ("true", "1", "yes")
        if not allow_private:
            if hostname.lower() in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
                raise ValueError(f"Access to loopback address '{hostname}' is blocked for security.")
            try:
                addr_info = socket.getaddrinfo(hostname, None)
                for family, _, _, _, sockaddr in addr_info:
                    ip_str = sockaddr[0]
                    ip = ipaddress.ip_address(ip_str)
                    if _is_private_or_loopback_ip(ip):
                        raise ValueError(
                            f"Access to private/local network address '{ip_str}' is blocked for security. "
                            "Set MARKITDOWN_ALLOW_PRIVATE_NETWORKS=true to allow if required."
                        )
            except socket.gaierror as e:
                raise ValueError(f"Could not resolve host '{hostname}': {e}")

    elif scheme == "file":
        raw_path = unquote(parsed.path)
        if sys.platform == "win32" and raw_path.startswith("/") and len(raw_path) > 2 and raw_path[2] == ":":
            raw_path = raw_path[1:]
        path = os.path.realpath(raw_path)

        allow_all = os.getenv("MARKITDOWN_ALLOW_ALL_FILES", "false").strip().lower() in ("true", "1", "yes")
        if not allow_all:
            norm = path.replace("\\", "/").lower()
            norm_raw = os.path.abspath(raw_path).replace("\\", "/").lower()

            base_resolved = os.path.basename(path).lower()
            base_raw = os.path.basename(raw_path).lower()
            is_env_file = any(
                b == ".env" or b.startswith(".env.")
                for b in (base_resolved, base_raw)
            )

            sensitive_markers = [
                "/etc/shadow", "/etc/passwd", "/etc/sudoers",
                "credentials.env", ".aws/credentials", ".ssh/id_rsa",
                ".ssh/id_ed25519", ".ssh/id_ecdsa",
                ".kube/config", ".netrc", ".npmrc",
                ".gnupg", ".docker/config.json",
            ]
            if is_env_file or any(marker in norm or marker in norm_raw for marker in sensitive_markers):
                raise ValueError(f"Access to sensitive file path '{path}' is blocked.")

    elif scheme == "data":
        pass
    else:
        raise ValueError(f"Unsupported URI scheme: '{scheme}'. Supported schemes: http, https, file, data.")


class SSRFProtectedSession(requests.Session):
    """Session that intercepts all outgoing requests and redirects to enforce SSRF validation."""

    def send(self, request: requests.PreparedRequest, **kwargs: Any) -> requests.Response:
        if request.url:
            _validate_uri(request.url)
        return super().send(request, **kwargs)

    def resolve_redirects(
        self,
        resp: requests.Response,
        req: requests.PreparedRequest,
        stream: bool = False,
        timeout: Any = None,
        verify: Any = True,
        cert: Any = None,
        proxies: Any = None,
        yield_requests: bool = False,
        **adapter_kwargs: Any,
    ):
        for redirected_req in super().resolve_redirects(
            resp,
            req,
            stream=stream,
            timeout=timeout,
            verify=verify,
            cert=cert,
            proxies=proxies,
            yield_requests=yield_requests,
            **adapter_kwargs,
        ):
            if redirected_req.url:
                _validate_uri(redirected_req.url)
            yield redirected_req


@mcp.tool(
    annotations=ToolAnnotations(
        readOnlyHint=True,
        destructiveHint=False,
        idempotentHint=True,
        openWorldHint=True,
    )
)
async def convert_to_markdown(uri: str) -> str:
    """Convert a resource described by an http:, https:, file: or data: URI to markdown"""
    _validate_uri(uri)
    session = SSRFProtectedSession()
    session.headers.update(
        {"Accept": "text/markdown, text/html;q=0.9, text/plain;q=0.8, */*;q=0.1"}
    )
    return MarkItDown(
        enable_plugins=check_plugins_enabled(),
        requests_session=session,
    ).convert_uri(uri).markdown



def check_plugins_enabled() -> bool:
    return os.getenv("MARKITDOWN_ENABLE_PLUGINS", "false").strip().lower() in (
        "true",
        "1",
        "yes",
    )


def create_starlette_app(mcp_server: Server, *, debug: bool = False) -> Starlette:
    sse = SseServerTransport("/messages/")
    session_manager = StreamableHTTPSessionManager(
        app=mcp_server,
        event_store=None,
        json_response=True,
        stateless=True,
    )

    async def handle_sse(request: Request) -> None:
        async with sse.connect_sse(
            request.scope,
            request.receive,
            request._send,
        ) as (read_stream, write_stream):
            await mcp_server.run(
                read_stream,
                write_stream,
                mcp_server.create_initialization_options(),
            )

    async def handle_streamable_http(
        scope: Scope, receive: Receive, send: Send
    ) -> None:
        await session_manager.handle_request(scope, receive, send)

    @contextlib.asynccontextmanager
    async def lifespan(app: Starlette) -> AsyncIterator[None]:
        """Context manager for session manager."""
        async with session_manager.run():
            print("Application started with StreamableHTTP session manager!")
            try:
                yield
            finally:
                print("Application shutting down...")

    return Starlette(
        debug=debug,
        routes=[
            Route("/sse", endpoint=handle_sse),
            Mount("/mcp", app=handle_streamable_http),
            Mount("/messages/", app=sse.handle_post_message),
        ],
        lifespan=lifespan,
    )


# Main entry point
def main():
    import argparse

    mcp_server = mcp._mcp_server

    parser = argparse.ArgumentParser(description="Run a MarkItDown MCP server")

    parser.add_argument(
        "--http",
        action="store_true",
        help="Run the server with Streamable HTTP and SSE transport rather than STDIO (default: False)",
    )
    parser.add_argument(
        "--sse",
        action="store_true",
        help="(Deprecated) An alias for --http (default: False)",
    )
    parser.add_argument(
        "--host", default=None, help="Host to bind to (default: 127.0.0.1)"
    )
    parser.add_argument(
        "--port", type=int, default=None, help="Port to listen on (default: 3001)"
    )
    args = parser.parse_args()

    use_http = args.http or args.sse

    if not use_http and (args.host or args.port):
        parser.error(
            "Host and port arguments are only valid when using streamable HTTP or SSE transport (see: --http)."
        )
        sys.exit(1)

    if use_http:
        host = args.host if args.host else "127.0.0.1"
        if args.host and args.host not in ("127.0.0.1", "localhost"):
            print(
                "\n"
                "WARNING: The server is being bound to a non-localhost interface "
                f"({host}).\n"
                "This exposes the server to other machines on the network or Internet.\n"
                "The server has NO authentication and runs with your user's privileges.\n"
                "Any process or user that can reach this interface can read files and\n"
                "fetch network resources accessible to this user.\n"
                "Only proceed if you understand the security implications.\n",
                file=sys.stderr,
            )
        starlette_app = create_starlette_app(mcp_server, debug=True)
        uvicorn.run(
            starlette_app,
            host=host,
            port=args.port if args.port else 3001,
        )
    else:
        mcp.run()


if __name__ == "__main__":
    main()
