"""
Tests for app functions
"""
import datetime
from contextlib import contextmanager
from typing import Iterator
from unittest.mock import AsyncMock, Mock, patch

import pytest

from src.app import main, query_scoreboard
from src.schemas import ScoreboardData


@contextmanager
def patch_httpx_client(
    http_method: str,
    status_code: int,
    response_content: bytes
) -> Iterator[AsyncMock]:
    mock_response = Mock(
        content=response_content,
        status_code=status_code,
    )
    mock_client = AsyncMock()
    mock_client.__aenter__.return_value = mock_client
    setattr(mock_client, http_method.lower(), AsyncMock(return_value=mock_response))
    with patch("httpx.AsyncClient", return_value=mock_client):
        yield mock_client


class TestQueryScoreboard:
    async def test_returns_scoreboard_data(
        self,
        game_date: datetime.date,
        nba_league_id: str,
        nba_scoreboard_response_content: bytes,
    ) -> None:
        with patch_httpx_client("get", 200, nba_scoreboard_response_content):
            data = await query_scoreboard(
                game_date=game_date,
                league_id=nba_league_id,
            )
        assert data.scoreboard.gameDate == "2026-05-15"
        assert len(data.scoreboard.games) == 2

    async def test_request_params(
        self,
        game_date: datetime.date,
        nba_league_id: str,
        nba_scoreboard_response_content: bytes,
    ) -> None:
        with patch_httpx_client("get", 200, nba_scoreboard_response_content) as mock_client:
            await query_scoreboard(
                game_date=game_date,
                league_id=nba_league_id,
            )
            mock_client.get.assert_called_once()
            call_kwargs = mock_client.get.call_args.kwargs
            assert call_kwargs["params"]["LeagueID"] == "00"
            assert call_kwargs["params"]["GameDate"] == "2026-05-15"

    async def test_non_200_response_causes_validation_error(
        self,
        game_date: datetime.date,
        nba_league_id: str,
    ) -> None:
        with patch_httpx_client("get", 500, b""):
            with pytest.raises(ValueError):
                await query_scoreboard(
                    game_date=game_date,
                    league_id=nba_league_id,
                )


class TestMain:
    async def test_returns_dict_keyed_by_game_id(
        self,
        monkeypatch,
        game_date: datetime.date,
        nba_scoreboard_response_content: bytes,
    ) -> None:
        data = ScoreboardData.model_validate_json(nba_scoreboard_response_content)

        async def mock_query(*args, **kwargs):
            return data

        monkeypatch.setattr("src.app.query_scoreboard", mock_query)
        result = await main(game_date=game_date)
        assert isinstance(result, dict)
        assert "0042500206" in result

    async def test_game_brief_values(
        self,
        monkeypatch,
        game_date: datetime.date,
        nba_scoreboard_response_content: bytes,
    ) -> None:
        data = ScoreboardData.model_validate_json(nba_scoreboard_response_content)

        async def mock_query(*args, **kwargs):
            return data

        monkeypatch.setattr("src.app.query_scoreboard", mock_query)
        result = await main(game_date=game_date)
        brief = result["0042500206"]
        assert brief.away_team_tricode == "DET"
        assert brief.away_team_score == 115
        assert brief.home_team_tricode == "CLE"
        assert brief.home_team_score == 94
