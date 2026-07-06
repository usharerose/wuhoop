"""
Shared fixtures for tests
"""

import datetime
import json
from collections.abc import Callable
from http import HTTPStatus
from typing import Any

import httpx
import pytest


@pytest.fixture
def game_date() -> datetime.date:
    return datetime.date(2026, 5, 15)


@pytest.fixture
def nba_league_id() -> str:
    return "00"


@pytest.fixture
def get_source_data() -> Callable[[str], dict[str, Any]]:
    """
    get mock data of stat.nba.com response
    """
    def _get_source_data(file_path: str) -> dict[str, Any]:
        with open(file_path, "r", encoding="utf-8-sig") as f:
            data = json.load(f)
            assert isinstance(data, dict)
            return data
    return _get_source_data


class _SourceClientTransport(httpx.MockTransport):
    def __init__(self, response_mapping: dict[str, dict[str, Any]]) -> None:
        self._response_mapping = response_mapping
        self._requests: list[tuple[str, dict[str, Any]]] = []  # endpoint -> params
        super().__init__(self._handler)

    def _handler(self, request: httpx.Request) -> httpx.Response:
        *_, endpoint_name = request.url.path.rstrip("/").rsplit("/")
        self._requests.append((endpoint_name, dict(request.url.params)))
        if endpoint_name not in self._response_mapping:
            return httpx.Response(
                HTTPStatus.NOT_FOUND.value,
                content=f"No mock response registered for {endpoint_name}".encode("utf-8"),
            )
        return httpx.Response(HTTPStatus.OK.value, json=self._response_mapping[endpoint_name])


@pytest.fixture
def source_client_transport_factory() -> Callable[..., _SourceClientTransport]:

    def _make(**response_mapping: dict[str, Any]) -> _SourceClientTransport:
        return _SourceClientTransport(response_mapping)

    return _make
