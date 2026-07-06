"""
Play by play definitions
"""

from typing import Literal

from pydantic import BaseModel

from .common import Meta


class Action(BaseModel):
    # start from 0, multiple actions could have same action number
    # e.g. block and missed shot are two actions with same action number
    actionNumber: int
    clock: str  # format is like "PT12M00.00S"
    period: int
    teamId: int  # could be 0 for no team belonging
    teamTricode: str  # empty string for no team belonging
    personId: int  # could be 0 for no person belonging
    playerName: str
    playerNameI: str
    xLegacy: int
    yLegacy: int
    shotDistance: int
    shotResult: Literal["Made", "Missed", ""]
    isFieldGoal: int
    scoreHome: str  # "0" when action is not scored
    scoreAway: str  # "0" when action is not scored
    pointsTotal: int  # scoreHome + scoreAway, 0 when action is not scored
    location: Literal["v", "h", " ", ""]
    description: str
    actionType: str
    subType: str
    videoAvailable: int
    # field goal value (no matter made or missed), 0 for non field goal action
    shotValue: int
    actionId: int  # start from 1


class Game(BaseModel):
    gameId: str
    videoAvailable: int
    actions: list[Action]


class PlayByPlayData(BaseModel):
    """
    Content of stats.nba.com/stats/playbyplayv3 response
    """

    meta: Meta
    game: Game
