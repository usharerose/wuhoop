"""
playbyplayv3 endpoint
"""

from pydantic import Field

from .base import BaseEndpoint, EndpointParams, SourceClient
from .schemas import PlayByPlayData


class PlayByPlayParams(EndpointParams):
    game_id: str = Field(alias="GameID")
    start_period_id: int = Field(default=0, alias="StartPeriod")
    end_period_id: int = Field(default=0, alias="EndPeriod")


class PlayByPlayEndpoint(BaseEndpoint[PlayByPlayParams, PlayByPlayData]):
    @property
    def endpoint_path(self) -> str:
        return "playbyplayv3"

    @property
    def response_model(self) -> type[PlayByPlayData]:
        return PlayByPlayData


async def query_play_by_play(
    game_id: str,
    start_period_id: int = 0,
    end_period_id: int = 0,
    *,
    client: SourceClient | None = None,
) -> PlayByPlayData:
    return await PlayByPlayEndpoint().fetch(
        client or SourceClient(),
        PlayByPlayParams.model_validate(
            {
                "game_id": game_id,
                "start_period_id": start_period_id,
                "end_period_id": end_period_id,
            }
        ),
    )
