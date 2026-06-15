"""
Scoreboard service - business logic for fetching scoreboard data
"""

import datetime

from pydantic import BaseModel

from wuhoop.constants import LeagueId
from wuhoop.sources import query_scoreboard
from wuhoop.sources.schemas import ScoreboardData as QueryScoreboardResult


class ScoreboardData(BaseModel):
    game_id: str
    game_code: str
    game_status_code: int
    game_time_utc: datetime.datetime
    period: int

    away_team_id: int
    away_team_name: str
    away_team_city: str
    away_team_tricode: str
    away_team_slug: str
    away_team_score: int

    home_team_id: int
    home_team_name: str
    home_team_city: str
    home_team_tricode: str
    home_team_slug: str
    home_team_score: int


async def get_scoreboards(
    game_date: datetime.date,
    league_id: LeagueId = LeagueId.NBA,
) -> list[ScoreboardData]:
    scoreboards: list[ScoreboardData] = []
    try:
        data: QueryScoreboardResult = await query_scoreboard(
            game_date=game_date, league_id=league_id
        )
    except Exception:
        return scoreboards

    for game in data.scoreboard.games:
        scoreboards.append(
            ScoreboardData(
                game_id=game.gameId,
                game_code=game.gameCode,
                game_status_code=game.gameStatus,
                game_time_utc=datetime.datetime.strptime(game.gameTimeUTC, "%Y-%m-%dT%H:%M:%SZ"),
                period=game.period,
                away_team_id=game.awayTeam.teamId,
                away_team_name=game.awayTeam.teamName,
                away_team_city=game.awayTeam.teamCity,
                away_team_tricode=game.awayTeam.teamTricode,
                away_team_slug=game.awayTeam.teamSlug,
                away_team_score=game.awayTeam.score,
                home_team_id=game.homeTeam.teamId,
                home_team_name=game.homeTeam.teamName,
                home_team_city=game.homeTeam.teamCity,
                home_team_tricode=game.homeTeam.teamTricode,
                home_team_slug=game.homeTeam.teamSlug,
                home_team_score=game.homeTeam.score,
            )
        )
    return scoreboards
