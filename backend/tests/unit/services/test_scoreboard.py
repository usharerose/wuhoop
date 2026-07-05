"""
Unit tests for wuhoop.services.scoreboard.get_scoreboards.

The service wraps query_scoreboard and reshapes the source schema into the
internal ScoreboardData DTO. The source client is mocked using a custom
transport so no HTTP or DB is touched.
"""

import datetime
from typing import Any, Callable

import httpx

from tests.unit.conftest import _SourceClientTransport
from wuhoop.services.scoreboard import get_scoreboards
from wuhoop.sources.base import SourceClient


class TestGetScoreboards:

    async def test_get_scoreboards(
        self,
        game_date: datetime.date,
        source_client_transport_factory: Callable[..., _SourceClientTransport],
        get_source_data: Callable[..., dict[str, Any]],
    ) -> None:
        transport = source_client_transport_factory(
            scoreboardv3=get_source_data("tests/data/scoreboard.json"),
        )
        client = SourceClient(transport=transport)

        result = await get_scoreboards(game_date=game_date, client=client)

        scoreboard, *_ = result
        assert scoreboard.game_id == "0042500206"
        assert scoreboard.game_code == "20260515/DETCLE"
        assert scoreboard.game_status_code == 3
        assert scoreboard.period == 4
        assert scoreboard.away_team_tricode == "DET"
        assert scoreboard.away_team_score == 115
        assert scoreboard.home_team_tricode == "CLE"
        assert scoreboard.home_team_score == 94

    async def test_returns_empty_list_when_source_raises(
        self,
        game_date: datetime.date,
    ) -> None:

        def _error_handler(request: httpx.Request) -> httpx.Response:
            raise httpx.HTTPStatusError(
                "Server error",
                request=request,
                response=httpx.Response(500, request=request),
            )

        client = SourceClient(transport=httpx.MockTransport(_error_handler))
        result = await get_scoreboards(game_date=game_date, client=client)

        assert result == []
