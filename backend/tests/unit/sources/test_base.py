"""
Unit tests for wuhoop.sources.base: EndpointParams and BaseEndpoint.
"""

from enum import StrEnum

import pytest
from pydantic import Field, ValidationError

from wuhoop.sources.base import BaseEndpoint, EndpointParams


class _OptionalParams(EndpointParams):
    """
    Local subclass with a nullable field, used to verify exclude_none behavior.
    """

    foo: str | None = Field(default=None, alias="Foo")
    bar: str = Field(alias="Bar")


class TestEndpointParamsToParams:
    """
    Test cases for EndpointParams
    """

    def test_uses_field_aliases(self) -> None:
        """
        Key of serialized data should be alias
        """
        params = _OptionalParams.model_validate(
            {"foo": "foo value", "bar": "bar value"}
        )
        actual = params.to_params()
        assert actual == {"Foo": "foo value", "Bar": "bar value"}

    def test_serializes_enum_to_value(self) -> None:
        """
        value should be the value of enum instead of Enum object
        """

        class _EnumObject(StrEnum):
            foo = "Foo"
            bar = "Bar"

        class _EnumParams(EndpointParams):
            value: _EnumObject = Field(alias="Value")

        params = _EnumParams.model_validate({"value": _EnumObject.bar})
        actual = params.to_params()
        assert actual == {"Value": "Bar"}

    def test_excludes_none_values(self) -> None:
        params = _OptionalParams.model_validate({"foo": None, "bar": "baz"})
        actual = params.to_params()
        assert actual == {"Bar": "baz"}

    def test_keeps_explicit_none_when_field_required(self) -> None:
        # Bar is required; passing None to it should raise, not produce None.
        with pytest.raises(ValidationError):
            _OptionalParams.model_validate({"foo": "x", "bar": None})


def test_base_endpoint_is_abstract() -> None:
    # BaseEndpoint declares abstract properties; direct instantiation
    # should be rejected by ABCMeta.
    with pytest.raises(TypeError):
        BaseEndpoint()  # type: ignore[abstract]
