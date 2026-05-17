"""
Schema definitions
"""
from enum import StrEnum
from typing import NamedTuple, TypedDict

from pydantic import BaseModel


class Meta(BaseModel):
    version: int
    request: str
    time: str


class GameLeader(BaseModel):
    personId: int
    name: str
    playerSlug: str
    jerseyNum: str
    position: str
    teamTricode: str
    points: float
    rebounds: float
    assists: float


class GameLeaders(BaseModel):
    homeLeaders: GameLeader
    awayLeaders: GameLeader


class TeamLeader(BaseModel):
    personId: int
    name: str
    playerSlug: str
    jerseyNum: str
    position: str
    teamTricode: str
    points: float
    rebounds: float
    assists: float


class TeamLeaders(BaseModel):
    homeLeaders: TeamLeader
    awayLeaders: TeamLeader


class Broadcaster(BaseModel):
    broadcasterId: int
    broadcastDisplay: str
    broadcasterTeamId: int
    broadcasterDescription: str


class Broadcasters(BaseModel):
    nationalBroadcasters: list[Broadcaster]
    nationalRadioBroadcasters: list[Broadcaster]
    nationalOttBroadcasters: list[Broadcaster]
    homeTvBroadcasters: list[Broadcaster]
    homeRadioBroadcasters: list[Broadcaster]
    homeOttBroadcasters: list[Broadcaster]
    awayTvBroadcasters: list[Broadcaster]
    awayRadioBroadcasters: list[Broadcaster]
    awayOttBroadcasters: list[Broadcaster]


class Period(BaseModel):
    period: int
    periodType: str
    score: int


class Team(BaseModel):
    teamId: int
    teamName: str
    teamCity: str
    teamTricode: str
    teamSlug: str
    wins: int
    losses: int
    score: int
    seed: int
    inBonus: bool | None
    timeoutsRemaining: int
    periods: list[Period]


class Game(BaseModel):
    gameId: str
    gameCode: str
    gameStatus: int
    gameStatusText: str
    period: int
    gameClock: str
    gameTimeUTC: str
    gameEt: str
    regulationPeriods: int
    seriesGameNumber: str
    gameLabel: str
    gameSubLabel: str
    seriesText: str
    ifNecessary: bool
    seriesConference: str
    poRoundDesc: str
    gameSubtype: str
    isNeutral: bool
    gameLeaders: GameLeaders
    teamLeaders: TeamLeaders
    broadcasters: Broadcasters
    homeTeam: Team
    awayTeam: Team


class Scoreboard(BaseModel):
    gameDate: str  # YYYY-MM-DD
    leagueId: str  # 00 for NBA
    leagueName: str  # Full name of the league
    games: list[Game]


class ScoreboardData(BaseModel):
    """
    Content of stats.nba.com/stats/scoreboardv3 response
    """
    meta: Meta
    scoreboard: Scoreboard


class LeagueId(StrEnum):
    NBA = "00"


class ScoreboardQueryParams(TypedDict):
    GameDate: str  # YYYY-MM-DD
    LeagueID: LeagueId


class ScoreboardGameBrief(NamedTuple):
    away_team_tricode: str
    away_team_score: int
    home_team_tricode: str
    home_team_score: int
