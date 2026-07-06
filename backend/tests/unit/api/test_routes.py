"""
Unit tests for API layer

Uses Quart's test client; the service layer is monkeypatched at its import
site inside routes.py so no HTTP / DB / network is touched.
"""

import datetime
from http import HTTPStatus
from unittest.mock import AsyncMock, MagicMock, patch

from wuhoop.services.scoreboard import ScoreboardData

from quart.typing import TestClientProtocol


class TestAPIHealth:

    async def test_returns_ok(self, client: TestClientProtocol) -> None:
        response = await client.get("/health")
        assert response.status_code == HTTPStatus.OK
        content = await response.get_json()
        assert content == {"status": "ok"}


class TestAPIIndex:

    async def test_returns_welcome_message(self, client: TestClientProtocol) -> None:
        response = await client.get("/")
        assert response.status_code == HTTPStatus.OK
        content = await response.get_json()
        assert content == {"message": "Wu Hoop Scoreboard API"}


class TestListScoreboards:

    @patch("wuhoop.api.routes.get_scoreboards")
    async def test_returns_success_response(
        self,
        mock_svc_get_scoreboards: MagicMock,
        client: TestClientProtocol,
    ) -> None:
        mock_svc_get_scoreboards.return_value = [
            ScoreboardData(
                game_id="0042500206",
                game_code="20260515/DETCLE",
                game_status_code=3,
                game_time_utc=datetime.datetime(2026, 5, 15, 23, tzinfo=datetime.UTC),
                period=4,
                away_team_id=1610612766,
                away_team_name="Pistons",
                away_team_city="Detroit",
                away_team_tricode="DET",
                away_team_slug="pistons",
                away_team_score=115,
                home_team_id=1610612739,
                home_team_name="Cavaliers",
                home_team_city="Cleveland",
                home_team_tricode="CLE",
                home_team_slug="cavaliers",
                home_team_score=94,
            ),
            ScoreboardData(
                game_id="0042500236",
                game_code="20260515/SASMIN",
                game_status_code=3,
                game_time_utc=datetime.datetime(2026, 5, 16, 1, 30, tzinfo=datetime.UTC),
                period=4,
                away_team_id=1610612759,
                away_team_name="Spurs",
                away_team_city="San Antonio",
                away_team_tricode="SAS",
                away_team_slug="spurs",
                away_team_score=139,
                home_team_id=1610612750,
                home_team_name="Timberwolves",
                home_team_city="Minnesota",
                home_team_tricode="MIN",
                home_team_slug="timberwolves",
                home_team_score=109,
            ),
        ]
        response = await client.get("/api/v1/scoreboards?date=2026-05-15")
        assert response.status_code == HTTPStatus.OK

        content = await response.get_json()
        assert isinstance(content["data"], list)
        assert len(content["data"]) == 2

        first, *_ = content["data"]
        assert first["game_id"] == "0042500206"
        assert first["home_team_score"] == 94

    @patch(
        "wuhoop.api.routes.get_scoreboards",
        new_callable=AsyncMock
    )
    async def test_called_parameters(
        self,
        mock_svc_get_scoreboards: AsyncMock,
        client: TestClientProtocol,
    ) -> None:
        mock_svc_get_scoreboards.return_value = [
            ScoreboardData(
                game_id="0042500206",
                game_code="20260515/DETCLE",
                game_status_code=3,
                game_time_utc=datetime.datetime(2026, 5, 15, 23, tzinfo=datetime.UTC),
                period=4,
                away_team_id=1610612766,
                away_team_name="Pistons",
                away_team_city="Detroit",
                away_team_tricode="DET",
                away_team_slug="pistons",
                away_team_score=115,
                home_team_id=1610612739,
                home_team_name="Cavaliers",
                home_team_city="Cleveland",
                home_team_tricode="CLE",
                home_team_slug="cavaliers",
                home_team_score=94,
            ),
            ScoreboardData(
                game_id="0042500236",
                game_code="20260515/SASMIN",
                game_status_code=3,
                game_time_utc=datetime.datetime(2026, 5, 16, 1, 30, tzinfo=datetime.UTC),
                period=4,
                away_team_id=1610612759,
                away_team_name="Spurs",
                away_team_city="San Antonio",
                away_team_tricode="SAS",
                away_team_slug="spurs",
                away_team_score=139,
                home_team_id=1610612750,
                home_team_name="Timberwolves",
                home_team_city="Minnesota",
                home_team_tricode="MIN",
                home_team_slug="timberwolves",
                home_team_score=109,
            ),
        ]
        _ = await client.get("/api/v1/scoreboards?date=2026-05-15")
        mock_svc_get_scoreboards.assert_called_once_with(
            game_date=datetime.date(2026, 5, 15)
        )

    @patch(
        "wuhoop.api.routes.get_scoreboards",
        new_callable=AsyncMock
    )
    async def test_fallback_today_game_date(
        self,
        mock_svc_get_scoreboards: AsyncMock,
        client: TestClientProtocol,
    ) -> None:
        mock_svc_get_scoreboards.return_value = []
        response = await client.get("/api/v1/scoreboards")
        assert response.status_code == HTTPStatus.OK

        content = await response.get_json()
        assert isinstance(content["data"], list)
        assert len(content["data"]) == 0

        mock_svc_get_scoreboards.assert_called_once_with(
            game_date=datetime.datetime.now(datetime.UTC).date(),
        )
