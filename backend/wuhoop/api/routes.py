"""
API routes
"""

import datetime
import json
from http import HTTPStatus

from quart import Blueprint, Response, request

from wuhoop.services.scoreboard import get_scoreboards

from .schemas import HealthResponse, ScoreboardData, ScoreboardsResponse

bp = Blueprint("api_v1", __name__, url_prefix="/api/v1")
root_bp = Blueprint("root", __name__)


@root_bp.get("/health")
async def health() -> Response:
    return Response(
        json.dumps(HealthResponse(status="ok").model_dump()),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@root_bp.get("/")
async def index() -> Response:
    return Response(
        json.dumps({"message": "Wu Hoop Scoreboard API"}),
        status=HTTPStatus.OK,
        content_type="application/json",
    )


@bp.get("/scoreboards")
async def list_scoreboards() -> Response:
    a_date = datetime.datetime.strptime(
        request.args.get(
            "date",
            datetime.datetime.now(datetime.UTC).strftime("%Y-%m-%d"),
        ),
        "%Y-%m-%d",
    ).date()
    result = await get_scoreboards(game_date=a_date)
    data: list[ScoreboardData] = []
    for scoreboard in result:
        data.append(
            ScoreboardData(
                game_id=scoreboard.game_id,
                game_code=scoreboard.game_code,
                game_status_code=scoreboard.game_status_code,
                game_time_utc=scoreboard.game_time_utc,
                period=scoreboard.period,
                away_team_id=scoreboard.away_team_id,
                away_team_name=scoreboard.away_team_name,
                away_team_city=scoreboard.away_team_city,
                away_team_tricode=scoreboard.away_team_tricode,
                away_team_slug=scoreboard.away_team_slug,
                away_team_score=scoreboard.away_team_score,
                home_team_id=scoreboard.home_team_id,
                home_team_name=scoreboard.home_team_name,
                home_team_city=scoreboard.home_team_city,
                home_team_tricode=scoreboard.home_team_tricode,
                home_team_slug=scoreboard.home_team_slug,
                home_team_score=scoreboard.home_team_score,
            )
        )
    response = ScoreboardsResponse(data=data)
    return Response(
        json.dumps(response.model_dump(mode="json")),
        status=HTTPStatus.OK.value,
        content_type="application/json",
    )
