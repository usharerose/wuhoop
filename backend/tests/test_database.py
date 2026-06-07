"""
Tests for database connection and models
"""

import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from wuhoop.db import FactGameEvent, async_session


class TestDatabaseConnection:
    async def test_database_connection(self) -> None:
        """
        Test that database connection works
        """
        async with async_session() as session:
            assert isinstance(session, AsyncSession)


class TestFactGameEventModel:
    async def test_fact_game_event_model_creation(self) -> None:
        """
        Test FactGameEvent model creation and field types
        """
        game = FactGameEvent(
            id="0042500161",
            league_id="00",
            season_id=2025,
            season_stage_id=4,
            round_number=1,
            series_index=6,
            schedule_id=1,
            game_datetime=datetime.datetime(2026, 4, 18, 19, 30, tzinfo=datetime.UTC),
            status_id=3,
            period_count=4,
            away_team_id=1610612750,
            away_team_tricode="MIN",
            away_team_name="Timberwolves",
            away_team_city="Minnesota",
            away_team_score=105,
            home_team_id=1610612743,
            home_team_tricode="DEN",
            home_team_name="Nuggets",
            home_team_city="Denver",
            home_team_score=116,
        )

        assert game.id == "0042500161"
        assert game.away_team_tricode == "MIN"
        assert game.home_team_tricode == "DEN"
        assert game.away_team_score == 105
        assert game.home_team_score == 116
        assert game.status_id == 3
