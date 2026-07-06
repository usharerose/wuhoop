"""
boxscoresummaryv3 endpoint
"""

from pydantic import Field

from .base import BaseEndpoint, EndpointParams, SourceClient
from .schemas import BoxScoreSummaryData


class BoxscoreSummaryParams(EndpointParams):
    game_id: str = Field(alias="GameID")


class BoxscoreSummaryEndpoint(BaseEndpoint[BoxscoreSummaryParams, BoxScoreSummaryData]):
    @property
    def endpoint_path(self) -> str:
        return "boxscoresummaryv3"

    @property
    def response_model(self) -> type[BoxScoreSummaryData]:
        return BoxScoreSummaryData


async def query_boxscore_summary(
    game_id: str,
    *,
    client: SourceClient | None = None,
) -> BoxScoreSummaryData:
    return await BoxscoreSummaryEndpoint().fetch(
        client or SourceClient(),
        BoxscoreSummaryParams.model_validate({"game_id": game_id}),
    )
