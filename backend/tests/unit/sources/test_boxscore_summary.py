"""
Unit tests for wuhoop.sources.boxscore_summary.query_boxscore_summary.
"""

from wuhoop.sources import query_boxscore_summary
from wuhoop.sources.base import SourceClient
from wuhoop.sources.schemas import BoxScoreSummaryData


class TestQueryBoxscoreSummary:

    async def test_returns_boxscore_summary_data(
        self,
        source_client_transport_factory,
        get_source_data,
    ) -> None:
        transport = source_client_transport_factory(
            boxscoresummaryv3=get_source_data("tests/data/boxscore_summary.json")
        )
        client = SourceClient(transport=transport)
        data = await query_boxscore_summary(game_id="0042500206", client=client)

        assert isinstance(data, BoxScoreSummaryData)

        boxscore_summary = data.boxScoreSummary
        assert boxscore_summary.gameId == "0042500206"
        assert boxscore_summary.gameStatus == 3
        assert boxscore_summary.period == 4
        assert boxscore_summary.awayTeamId == 1610612765
        assert boxscore_summary.duration == "2:31"
        assert boxscore_summary.attendance == 19432

        arena = boxscore_summary.arena
        assert arena.arenaId == 1000144
        assert arena.arenaName == "Rocket Arena"
        assert arena.arenaCity == "Cleveland"

        official, *_ = boxscore_summary.officials
        assert official.personId == 2534
        assert official.jerseyNum == "15"

    async def test_request_params_use_game_id_alias(
        self,
        source_client_transport_factory,
        get_source_data,
    ) -> None:
        transport = source_client_transport_factory(
            boxscoresummaryv3=get_source_data("tests/data/boxscore_summary.json")
        )
        client = SourceClient(transport=transport)
        await query_boxscore_summary(game_id="0042500206", client=client)

        request_info, *_ = transport._requests
        actual_endpoint, actual_params = request_info
        assert actual_endpoint == "boxscoresummaryv3"
        assert actual_params == {"GameID": "0042500206"}
