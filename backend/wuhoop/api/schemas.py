"""
API response schemas with camelCase naming for Azure Guidelines compliance
"""

import datetime

from pydantic import BaseModel


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


class ScoreboardsResponse(BaseModel):
    data: list[ScoreboardData]


class HealthResponse(BaseModel):
    status: str
