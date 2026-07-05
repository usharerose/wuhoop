import pytest

from quart import Quart
from quart.typing import TestClientProtocol

from wuhoop.api.app import create_app


@pytest.fixture
def app() -> Quart:
    return create_app()


@pytest.fixture
def client(app: Quart) -> TestClientProtocol:
    return app.test_client()
