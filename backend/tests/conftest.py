"""
Shared fixtures for tests
"""

import datetime
import os

import pytest

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")


@pytest.fixture
def game_date() -> datetime.date:
    return datetime.date(2026, 5, 15)


@pytest.fixture
def nba_league_id() -> str:
    return "00"


@pytest.fixture(scope="class")
def nba_scoreboard_response_content() -> bytes:
    with open(os.path.join(DATA_DIR, "scoreboard.json"), "rb") as f:
        return f.read()
