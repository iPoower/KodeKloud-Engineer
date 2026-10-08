"""Small stdlib-only HTTP service for a local Docker hardening lab.

Not intended for internet-facing production use.
"""
from __future__ import annotations

import json
import os
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit


class Handler(BaseHTTPRequestHandler):
    server_version = "LocalLab"
    sys_version = ""

    def do_GET(self) -> None:
        path = urlsplit(self.path).path
        if path == "/health":
            self.reply(200, {"status": "ok"})
        elif path == "/":
            self.reply(200, {"service": "hardened-http-lab", "status": "running"})
        else:
            self.reply(404, {"error": "not_found"})

    def reply(self, status: int, payload: dict[str, str]) -> None:
        data = json.dumps(payload, separators=(",", ":")).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        # This lab avoids writing request paths to container logs.
        return


def create_server(host: str = "127.0.0.1", port: int = 0) -> ThreadingHTTPServer:
    return ThreadingHTTPServer((host, port), Handler)


if __name__ == "__main__":
    host = os.environ.get("LAB_BIND_HOST", "0.0.0.0")  # inside container only
    port = int(os.environ.get("LAB_PORT", "8080"))
    server = create_server(host, port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
