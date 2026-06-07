"""
Application Middleware
"""

import uuid

from quart import Quart, g, request


async def add_request_id() -> None:
    req_headers = request.headers
    g.request_id = req_headers.get("Wh-Request-Id") or uuid.uuid4().hex


def install(app: Quart) -> None:
    app.before_request(add_request_id)
