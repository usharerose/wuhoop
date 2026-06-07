"""
Database models
"""

import datetime

from sqlalchemy import DateTime, Integer, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """
    Base class for all models
    """

    created_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.UTC),
        comment="Record creation timestamp",
    )
    updated_at: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.datetime.now(datetime.UTC),
        onupdate=lambda: datetime.datetime.now(datetime.UTC),
        comment="Record last update timestamp",
    )


class FactGameEvent(Base):
    __tablename__ = "fact_game_events"
    __table_args__ = {
        "comment": (
            "Fact table for basketball game events. "
            "Stores basic metadata, e.g. team participants, and scoring outcomes."
        ),
    }

    id: Mapped[str] = mapped_column(
        String(30),
        primary_key=True,
        comment="Unique game identifier from source API",
    )
    league_id: Mapped[str] = mapped_column(
        String(2),
        nullable=False,
        comment="League identifier",
    )
    season_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Season identifier, the start year of the season",
    )
    season_stage_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Identifier of the stage during the season for the game",
    )
    round_number: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Round number for elimination tournaments, 0 means no rounds",
    )
    series_index: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Series index within the round, 0-based, resets for each round",
    )
    schedule_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Internal scheduling identifier of the game, not sequential properly",
    )
    game_datetime: Mapped[datetime.datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        comment="Game start time in UTC",
    )
    status_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Game status: 1=not started, 2=in progress, 3=completed",
    )
    period_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Current period number (e.g., 1-4 for regulation, 5+ for overtime)",
    )
    away_team_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Away team unique identifier",
    )
    away_team_tricode: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Away team 3-letter abbreviation code",
    )
    away_team_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Away team full name",
    )
    away_team_city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Away team city name",
    )
    away_team_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="Away team current score",
    )
    home_team_id: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        comment="Home team unique identifier",
    )
    home_team_tricode: Mapped[str] = mapped_column(
        String(10),
        nullable=False,
        comment="Home team 3-letter abbreviation code",
    )
    home_team_name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        comment="Home team full name",
    )
    home_team_city: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="Home team city name",
    )
    home_team_score: Mapped[int] = mapped_column(
        Integer,
        default=0,
        comment="Home team current score",
    )
