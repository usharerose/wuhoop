"""
Tests for schema validation
"""
import pytest
from pydantic import ValidationError

from src.schemas import (
    LeagueId,
    Meta,
    Period,
    ScoreboardData,
)


class TestLeagueId:

    def test_nba_value(self) -> None:
        assert LeagueId.NBA == "00"
        assert str(LeagueId.NBA) == "00"


class TestScoreboardData:
    @pytest.fixture(scope="class")
    def data(self, nba_scoreboard_response_content: bytes) -> ScoreboardData:
        return ScoreboardData.model_validate_json(nba_scoreboard_response_content)

    def test_meta(self, data: ScoreboardData) -> None:
        assert isinstance(data.meta, Meta)
        assert data.meta.version == 1

    def test_scoreboard(self, data: ScoreboardData) -> None:
        scoreboard = data.scoreboard
        assert scoreboard.gameDate == "2026-05-15"
        assert scoreboard.leagueId == "00"
        assert scoreboard.leagueName == "National Basketball Association"
        assert len(scoreboard.games) == 2

    def test_game_basic_fields(self, data: ScoreboardData) -> None:
        game, *_ = data.scoreboard.games
        assert game.gameId == "0042500206"
        assert game.gameCode == "20260515/DETCLE"
        assert game.gameStatus == 3
        assert game.gameStatusText == "Final"
        assert game.period == 4
        assert game.gameClock == ""
        assert game.regulationPeriods == 4
        assert game.ifNecessary is False
        assert game.isNeutral is False

    def test_game_playoff_fields(self, data: ScoreboardData) -> None:
        game, *_ = data.scoreboard.games
        assert game.seriesGameNumber == "Game 6"
        assert game.gameLabel == "East Conf. Semifinals"
        assert game.seriesText == "Series tied 3-3"
        assert game.seriesConference == "East"
        assert game.poRoundDesc == "Conf. Semifinals"

    def test_game_leaders(self, data: ScoreboardData) -> None:
        game, *_ = data.scoreboard.games
        leaders = game.gameLeaders
        assert leaders.homeLeaders.name == "James Harden"
        assert leaders.homeLeaders.points == 23
        assert leaders.homeLeaders.teamTricode == "CLE"
        assert leaders.awayLeaders.name == "Cade Cunningham"
        assert leaders.awayLeaders.points == 21
        assert leaders.awayLeaders.teamTricode == "DET"

    def test_team_leaders(self, data: ScoreboardData) -> None:
        game, *_ = data.scoreboard.games
        leaders = game.teamLeaders
        assert leaders.homeLeaders.name == "Donovan Mitchell"
        assert leaders.homeLeaders.points == 25.6
        assert leaders.awayLeaders.name == "Cade Cunningham"
        assert leaders.awayLeaders.points == 29.3

    def test_broadcasters(self, data: ScoreboardData) -> None:
        game, *_ = data.scoreboard.games
        broadcasters = game.broadcasters
        assert len(broadcasters.nationalBroadcasters) == 1

        broadcaster, *_ = broadcasters.nationalBroadcasters
        assert broadcaster.broadcastDisplay == "Amazon"

    def test_team(self, data: ScoreboardData) -> None:
        game, *_ = data.scoreboard.games
        home = game.homeTeam
        assert home.teamId == 1610612739
        assert home.teamName == "Cavaliers"
        assert home.teamCity == "Cleveland"
        assert home.teamTricode == "CLE"
        assert home.teamSlug == "cavaliers"
        assert home.wins == 3
        assert home.losses == 3
        assert home.score == 94
        assert home.seed == 4
        assert home.inBonus is None
        assert home.timeoutsRemaining == 0
        assert len(home.periods) == 4

    def test_period(self, data: ScoreboardData) -> None:
        game, *_ = data.scoreboard.games
        periods = game.homeTeam.periods
        first_period, *_ = periods
        assert first_period.period == 1
        assert first_period.periodType == "REGULAR"
        assert first_period.score == 25
        assert all(isinstance(p, Period) for p in periods)

    def test_validation_error_on_empty_json(self) -> None:
        with pytest.raises(ValidationError):
            ScoreboardData.model_validate_json("{}")
