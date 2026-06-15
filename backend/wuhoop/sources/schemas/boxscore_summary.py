"""
Boxscore summary definitions
"""

from typing import Literal

from pydantic import BaseModel, field_validator

from .common import Meta


class Arena(BaseModel):
    arenaId: int
    arenaName: str
    arenaCity: str
    arenaState: str
    arenaCountry: str
    arenaTimezone: str  # e.g. Eastern
    arenaStreetAddress: str
    arenaPostalCode: str


class Official(BaseModel):
    personId: int
    name: str
    nameI: str
    firstName: str
    familyName: str
    jerseyNum: str
    assignment: str  # always empty string

    @field_validator("jerseyNum", mode="before")
    @classmethod
    def strip_jersey_number(cls, value: str) -> str:
        """
        '15  ' -> '15'
        """
        return value.strip()


class Broadcaster(BaseModel):
    broadcasterId: int
    broadcastDisplay: str
    broadcasterDisplay: str
    broadcasterVideoLink: str
    broadcasterDescription: str
    broadcasterTeamId: int  # TODO: figure out the business meaning, could be -1
    regionId: int


class Broadcasters(BaseModel):
    internationalBroadcasters: list[Broadcaster]
    internationalRadioBroadcasters: list[Broadcaster]
    internationalOttBroadcasters: list[Broadcaster]
    nationalBroadcasters: list[Broadcaster]
    nationalRadioBroadcasters: list[Broadcaster]
    nationalOttBroadcasters: list[Broadcaster]
    homeTvBroadcasters: list[Broadcaster]
    homeRadioBroadcasters: list[Broadcaster]
    homeOttBroadcasters: list[Broadcaster]
    awayTvBroadcasters: list[Broadcaster]
    awayRadioBroadcasters: list[Broadcaster]
    awayOttBroadcasters: list[Broadcaster]


class TeamStatistics(BaseModel):
    dummyKey: Literal["dummyValue"]


class Period(BaseModel):
    period: int
    periodType: Literal["REGULAR", "OVERTIME"]
    score: int


class Player(BaseModel):
    personId: int
    name: str
    nameI: str
    firstName: str
    familyName: str
    jerseyNum: str


class InActivePlayer(BaseModel):
    personId: int
    firstName: str
    familyName: str
    jerseyNum: str

    @field_validator("jerseyNum", mode="before")
    @classmethod
    def strip_jersey_number(cls, value: str) -> str:
        """
        ' 7' -> '7'
        """
        return value.strip()


class Team(BaseModel):
    teamId: int
    teamName: str
    teamCity: str
    teamTricode: str
    teamSlug: str
    teamWins: int
    teamLosses: int
    score: int
    inBonus: str
    timeoutsRemaining: int
    seed: int
    statistics: TeamStatistics
    periods: list[Period]
    players: list[Player]
    inactives: list[InActivePlayer]


class TeamAbstractStats(BaseModel):
    teamId: int
    teamCity: str
    teamName: str
    teamTricode: str
    teamSlug: str
    score: int
    wins: int
    losses: int


class Meeting(BaseModel):
    recencyOrder: int
    gameId: str
    gameTimeUTC: str  # format: YY-mm-ddTHH:MM:SSZ
    gameEt: str  # format: YY-mm-ddTHH:MM:SSZ
    gameStatus: int
    gameStatusText: str
    gameClock: str  # e.g. "PT00M00.00S"
    broadcasterVideoLink: str
    awayTeam: TeamAbstractStats
    homeTeam: TeamAbstractStats


class LastFiveMeetings(BaseModel):
    """
    Last five game meetings result for the same matchup teams
    """

    meetings: list[Meeting]


class TeamPreGameChartStatistics(BaseModel):
    """
    average statistics per game
    """

    points: float
    reboundsTotal: float
    assists: float
    steals: float
    blocks: float
    turnovers: float
    fieldGoalsPercentage: float
    threePointersPercentage: float
    freeThrowsPercentage: float
    pointsInThePaint: float
    pointsSecondChance: float
    pointsFastBreak: float
    playerPtsLeaderFirstName: str
    playerPtsLeaderFamilyName: str
    playerPtsLeaderId: int
    playerPtsLeaderPts: float
    playerRebLeaderFirstName: str
    playerRebLeaderFamilyName: str
    playerRebLeaderId: int
    playerRebLeaderReb: float
    playerAstLeaderFirstName: str
    playerAstLeaderFamilyName: str
    playerAstLeaderId: int
    playerAstLeaderAst: float
    playerBlkLeaderFirstName: str
    playerBlkLeaderFamilyName: str
    playerBlkLeaderId: int
    playerBlkLeaderBlk: float


class TeamPostGameChartStatistics(BaseModel):
    """
    statistics of current game
    """

    points: int
    reboundsTotal: int
    assists: int
    steals: int
    blocks: int
    turnovers: int
    fieldGoalsPercentage: float
    threePointersPercentage: float
    freeThrowsPercentage: float
    pointsInThePaint: int
    pointsSecondChance: int
    pointsFastBreak: int
    biggestLead: int
    leadChanges: int
    timesTied: int
    biggestScoringRun: int
    turnoversTeam: int
    turnoversTotal: int
    reboundsTeam: int
    pointsFromTurnovers: int
    benchPoints: int
    playerPtsLeaderFirstName: str
    playerPtsLeaderFamilyName: str
    playerPtsLeaderId: int
    playerPtsLeaderPts: int
    playerRebLeaderFirstName: str
    playerRebLeaderFamilyName: str
    playerRebLeaderId: int
    playerRebLeaderReb: int
    playerAstLeaderFirstName: str
    playerAstLeaderFamilyName: str
    playerAstLeaderId: int
    playerAstLeaderAst: int
    playerBlkLeaderFirstName: str
    playerBlkLeaderFamilyName: str
    playerBlkLeaderId: int
    playerBlkLeaderBlk: int

    @field_validator(
        "points",
        "reboundsTotal",
        "assists",
        "steals",
        "blocks",
        "turnovers",
        "pointsInThePaint",
        "pointsSecondChance",
        "pointsFastBreak",
        "biggestLead",
        "leadChanges",
        "timesTied",
        "biggestScoringRun",
        "turnoversTeam",
        "turnoversTotal",
        "reboundsTeam",
        "pointsFromTurnovers",
        "benchPoints",
        "playerPtsLeaderPts",
        "playerRebLeaderReb",
        "playerAstLeaderAst",
        "playerBlkLeaderBlk",
        mode="before",
    )
    @classmethod
    def float_to_integer(cls, value: float) -> int:
        """
        the raw data type of the fields is float,
        even though is integer from business view
        so that need to convert them, avoiding misunderstanding
        """
        return int(value)


class TeamPreGameChart(BaseModel):
    teamId: int
    teamCity: str
    teamName: str
    teamTricode: str
    statistics: TeamPreGameChartStatistics


class TeamPostGameChart(BaseModel):
    teamId: int
    teamCity: str
    teamName: str
    teamTricode: str
    statistics: TeamPostGameChartStatistics


class PreGameCharts(BaseModel):
    homeTeam: TeamPreGameChart
    awayTeam: TeamPreGameChart


class PostGameCharts(BaseModel):
    homeTeam: TeamPostGameChart
    awayTeam: TeamPostGameChart


class BoxScoreSummary(BaseModel):
    gameId: str
    gameCode: str  # concat by game date and teams code, e.g. 20260515/DETCLE
    gameStatus: int
    gameStatusText: str
    period: int
    gameClock: str
    gameTimeUTC: str
    gameEt: str
    awayTeamId: int
    homeTeamId: int
    duration: str  # HH:MM, e.g. 2:31 means 2 hours and 31 minutes
    attendance: int  # count of attendance
    sellout: int
    seriesGameNumber: str  # Label of series game number, e.g. Game 6. Empty string for regular game
    gameLabel: str  # e.g. East Conf. Semifinals. Empty string for regular game
    gameSubLabel: str
    seriesText: str  # series status short info, e.g. Series tied 3-3
    ifNecessary: bool
    isNeutral: bool
    arena: Arena
    officials: list[Official]
    broadcasters: Broadcasters
    homeTeam: Team
    awayTeam: Team
    lastFiveMeetings: LastFiveMeetings
    pregameCharts: PreGameCharts
    postgameCharts: PostGameCharts
    videoAvailableFlag: int
    ptAvailable: int
    ptXYZAvailable: int
    whStatus: int
    hustleStatus: int
    historicalStatus: int
    gameSubtype: str  # "in-season-knockout" for NBA cup


class BoxScoreSummaryData(BaseModel):
    """
    Content of stats.nba.com/stats/boxscoresummaryv3 response
    """

    meta: Meta
    boxScoreSummary: BoxScoreSummary
