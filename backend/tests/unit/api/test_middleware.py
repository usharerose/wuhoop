"""
Unit tests for wuhoop.api.middleware.
"""

import uuid

from quart import g, Quart

from wuhoop.api.middleware import add_request_id


class TestAddRequestId:

    async def test_generates_uuid_when_no_header(self, app: Quart) -> None:
        async with app.test_request_context("/health"):
            await add_request_id()
            request_id = g.get("request_id")
            assert request_id is not None
            assert isinstance(uuid.UUID(request_id), uuid.UUID)

    async def test_with_request_headers(self, app: Quart) -> None:
        custom_request_id = "customrequestid"
        async with app.test_request_context(
            "/health",
            headers={"Wh-Request-Id": custom_request_id},
        ):
            await add_request_id()
            request_id = g.get("request_id")
            assert request_id is not None
            assert request_id == custom_request_id


class TestInstall:

    async def test_middleware_installed(self, app: Quart) -> None:
        assert len(app.before_request_funcs.get(None, [])) == 1

    async def test_request_with_install(self, app: Quart) -> None:
        async with app.test_client() as client:
            response = await client.get("/health")
            assert response.status_code == 200
