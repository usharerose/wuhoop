"""
scoreboardv3 endpoint
"""

import datetime

from pydantic import Field

from wuhoop.constants import LeagueId

from .base import BaseEndpoint, EndpointParams, SourceClient
from .schemas import ScoreboardData


class ScoreboardParams(EndpointParams):
    game_date: datetime.date = Field(alias="GameDate")
    league_id: LeagueId = Field(default=LeagueId.NBA, alias="LeagueID")


class ScoreboardEndpoint(BaseEndpoint[ScoreboardParams, ScoreboardData]):
    @property
    def endpoint_path(self) -> str:
        return "scoreboardv3"

    @property
    def response_model(self) -> type[ScoreboardData]:
        return ScoreboardData


async def query_scoreboard(
    game_date: datetime.date,
    league_id: LeagueId = LeagueId.NBA,
    *,
    client: SourceClient | None = None,
) -> ScoreboardData:
    return await ScoreboardEndpoint().fetch(
        client or SourceClient(),
        ScoreboardParams.model_validate({"game_date": game_date, "league_id": league_id}),
    )
