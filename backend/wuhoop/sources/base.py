"""
Base classes for external data source clients and endpoints
"""

import json
from abc import ABC, abstractmethod
from collections.abc import Mapping
from typing import Any, ClassVar
from urllib.parse import urljoin

import httpx
from pydantic import BaseModel, ConfigDict

from wuhoop.constants import BASE_URL as SOURCE_BASE_URL
from wuhoop.constants import HEADERS as SOURCE_HEADERS


class EndpointParams(BaseModel):
    """
    Base class for typed endpoint request parameters
    """

    model_config = ConfigDict(
        use_enum_values=True,
        populate_by_name=True,
    )

    def to_params(self) -> dict[str, Any]:
        """
        Return HTTP query parameters using endpoint aliases and JSON-safe values.
        """
        return self.model_dump(mode="json", by_alias=True, exclude_none=True)


class SourceClient:
    """
    Async HTTP client for external data source
    """

    BASE_URL: ClassVar[str] = SOURCE_BASE_URL
    HEADERS: ClassVar[Mapping[str, str]] = SOURCE_HEADERS
    TIMEOUT: ClassVar[float] = 10.0

    def __init__(
        self,
        headers: Mapping[str, str] | None = None,
        timeout: float | None = None,
        *,
        transport: httpx.AsyncBaseTransport | None = None,
    ):
        self._headers = headers if headers is not None else self.HEADERS
        self._timeout = timeout if timeout is not None else self.TIMEOUT
        self._transport = transport

    async def get_dict(
        self,
        endpoint_path: str,
        params: Mapping[str, Any],
    ) -> dict[str, Any]:
        async with httpx.AsyncClient(
            headers=self._headers,
            timeout=self._timeout,
            transport=self._transport,
        ) as client:
            response = await client.get(
                urljoin(self.BASE_URL, endpoint_path),
                params=params,
            )
        data: dict[str, Any] = json.loads(response.content.decode("utf-8"))
        return data


class BaseEndpoint[ParamsT: EndpointParams, ResponseModelT: BaseModel](ABC):
    @property
    @abstractmethod
    def endpoint_path(self) -> str:
        """
        Source endpoint path, e.g. "scoreboardv3".
        """

    @property
    @abstractmethod
    def response_model(self) -> type[ResponseModelT]:
        """
        Pydantic model used to validate the endpoint response.
        """

    async def fetch(self, client: SourceClient, params: ParamsT) -> ResponseModelT:
        """
        Fetch this endpoint with typed parameters and validate the JSON response.

        The params model is serialized using source API aliases before the
        request is sent. The returned JSON object is validated into this
        endpoint's configured Pydantic response model.
        """
        data = await client.get_dict(self.endpoint_path, params.to_params())
        return self.response_model.model_validate(data)
