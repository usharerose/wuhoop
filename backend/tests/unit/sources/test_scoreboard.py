"""
Unit tests for scoreboard components
"""

import datetime
from typing import Any, Callable

from tests.unit.conftest import _SourceClientTransport
from wuhoop.constants import LeagueId
from wuhoop.sources import query_scoreboard
from wuhoop.sources.base import SourceClient
from wuhoop.sources.schemas import ScoreboardData


class TestQueryScoreboard:

    async def test_returns_scoreboard_data(
        self,
        game_date: datetime.date,
        nba_league_id: str,
        source_client_transport_factory: Callable[..., _SourceClientTransport],
        get_source_data: Callable[..., dict[str, Any]],
    ) -> None:
        transport = source_client_transport_factory(
            scoreboardv3=get_source_data("tests/data/scoreboard.json"),
        )
        client = SourceClient(transport=transport)
        data = await query_scoreboard(
            game_date=game_date, league_id=LeagueId.from_value(nba_league_id), client=client
        )

        assert isinstance(data, ScoreboardData)

        scoreboard = data.scoreboard
        assert scoreboard.gameDate == "2026-05-15"
        assert scoreboard.leagueId == "00"
        assert scoreboard.leagueName == "National Basketball Association"

        game, *_ = scoreboard.games
        assert game.gameId == "0042500206"
        assert game.gameStatus == 3
        assert game.period == 4
        assert game.regulationPeriods == 4

        game_leaders = game.gameLeaders
        game_home_leaders = game_leaders.homeLeaders
        assert game_home_leaders.personId == 201935
        assert game_home_leaders.name == "James Harden"
        assert game_home_leaders.playerSlug == "james-harden"
        assert game_home_leaders.jerseyNum == "1"
        assert game_home_leaders.position == "G"
        assert game_home_leaders.points == 23
        assert game_home_leaders.rebounds == 7
        assert game_home_leaders.assists == 4

        team_leaders = game.teamLeaders
        away_team_leaders = team_leaders.awayLeaders
        assert away_team_leaders.personId == 1630595
        assert away_team_leaders.name == "Cade Cunningham"
        assert away_team_leaders.playerSlug == "cade-cunningham"
        assert away_team_leaders.jerseyNum == "2"
        assert away_team_leaders.position == "G"
        assert away_team_leaders.points == 29.3
        assert away_team_leaders.rebounds == 5.2
        assert away_team_leaders.assists == 7.7

        broadcasters = game.broadcasters
        nationalBroadcaster, *_ = broadcasters.nationalBroadcasters
        assert nationalBroadcaster.broadcasterId == 1000664
        assert nationalBroadcaster.broadcastDisplay == "Amazon"
        assert nationalBroadcaster.broadcasterTeamId == -1
        assert nationalBroadcaster.broadcasterDescription == ""

        home_team = game.homeTeam
        assert home_team.teamId == 1610612739
        assert home_team.wins == 3
        assert home_team.losses == 3
        assert home_team.score == 94
        assert home_team.seed == 4
        assert home_team.timeoutsRemaining == 0

        first_period, *_ = home_team.periods
        assert first_period.period == 1
        assert first_period.periodType == "REGULAR"
        assert first_period.score == 25

    async def test_request_params(
        self,
        game_date: datetime.date,
        nba_league_id: str,
        source_client_transport_factory: Callable[..., _SourceClientTransport],
        get_source_data: Callable[..., dict[str, Any]],
    ) -> None:
        transport = source_client_transport_factory(
            scoreboardv3=get_source_data("tests/data/scoreboard.json"),
        )
        client = SourceClient(transport=transport)
        await query_scoreboard(
            game_date=game_date, league_id=LeagueId.from_value(nba_league_id), client=client
        )

        request_info, *_ = transport._requests
        actual_endpoint, actual_params = request_info
        assert actual_endpoint == "scoreboardv3"
        assert actual_params == {"GameDate": "2026-05-15", "LeagueID": "00"}

    async def test_request_params_with_default_league_id(
        self,
        game_date: datetime.date,
        source_client_transport_factory: Callable[..., _SourceClientTransport],
        get_source_data: Callable[..., dict[str, Any]],
    ) -> None:
        transport = source_client_transport_factory(
            scoreboardv3=get_source_data("tests/data/scoreboard.json"),
        )
        client = SourceClient(transport=transport)
        await query_scoreboard(game_date=game_date, client=client)

        request_info, *_ = transport._requests
        _, actual_params = request_info
        assert actual_params == {"GameDate": "2026-05-15", "LeagueID": "00"}
