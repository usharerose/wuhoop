"""
Unit tests for wuhoop.sources.play_by_play.query_play_by_play.
"""

from wuhoop.sources import query_play_by_play
from wuhoop.sources.base import SourceClient
from wuhoop.sources.schemas import PlayByPlayData


class TestQueryPlayByPlay:

    async def test_returns_play_by_play_data(
        self,
        source_client_transport_factory,
        get_source_data,
    ) -> None:
        transport = source_client_transport_factory(
            playbyplayv3=get_source_data("tests/data/play_by_play.json")
        )
        client = SourceClient(transport=transport)
        data = await query_play_by_play(game_id="0021500874", client=client)

        assert isinstance(data, PlayByPlayData)

        game = data.game
        assert game.gameId == "0021500874"

        action = game.actions[10]
        assert action.clock == "PT10M26.00S"
        assert action.period == 1
        assert action.teamId == 1610612744
        assert action.personId == 101106
        assert action.xLegacy == -9
        assert action.yLegacy == 13
        assert action.shotDistance == 2
        assert action.shotResult == "Made"
        assert action.isFieldGoal == 1
        assert action.scoreHome == "8"
        assert action.scoreAway == "2"
        assert action.pointsTotal == 10
        assert action.location == "v"
        assert action.actionType == "Made Shot"
        assert action.subType == "Alley Oop Layup shot"
        assert action.shotValue == 2
        assert action.actionId == 11

    async def test_returns_play_by_play_data_with_team_action(
        self,
        source_client_transport_factory,
        get_source_data,
    ) -> None:
        """
        For team behavior, the person would be the team
        """
        transport = source_client_transport_factory(
            playbyplayv3=get_source_data("tests/data/play_by_play.json")
        )
        client = SourceClient(transport=transport)
        data = await query_play_by_play(game_id="0021500874", client=client)

        assert isinstance(data, PlayByPlayData)

        game = data.game
        assert game.gameId == "0021500874"

        # team rebound
        action = game.actions[13]
        assert action.teamId == 0
        assert action.personId == 1610612744
        assert action.location == "v"
        assert action.actionType == "Rebound"
        assert action.subType == "Unknown"
        assert action.shotValue == 0

    async def test_request_params_default_period_bounds(
        self,
        source_client_transport_factory,
        get_source_data,
    ) -> None:
        transport = source_client_transport_factory(
            playbyplayv3=get_source_data("tests/data/play_by_play.json")
        )
        client = SourceClient(transport=transport)
        await query_play_by_play(game_id="0021500874", client=client)

        # Note: integer params survive URL encoding as strings — what the
        # real NBA API would see.
        request_info, *_ = transport._requests
        actual_endpoint, actual_params = request_info
        assert actual_endpoint == "playbyplayv3"
        assert actual_params == {"GameID": "0021500874", "StartPeriod": "0", "EndPeriod": "0"}

    async def test_request_params_custom_period_bounds(
        self,
        source_client_transport_factory,
        get_source_data,
    ) -> None:
        transport = source_client_transport_factory(
            playbyplayv3=get_source_data("tests/data/play_by_play.json")
        )
        client = SourceClient(transport=transport)
        _ = await query_play_by_play(
            game_id="0021500874",
            start_period_id=1,
            end_period_id=1,
            client=client,
        )

        request_info, *_ = transport._requests
        _, actual_params = request_info
        assert actual_params == {"GameID": "0021500874", "StartPeriod": "1", "EndPeriod": "1"}
