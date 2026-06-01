"""
Fetch Scoreboard statistics of National Basketball Association
"""

import argparse
import asyncio
import datetime
from urllib.parse import urljoin

import httpx

from constants import BASE_URL, ENDPOINT, HEADERS
from schemas import LeagueId, ScoreboardData, ScoreboardGameBrief


async def query_scoreboard(
    game_date: datetime.date,
    league_id: LeagueId = LeagueId.NBA,
) -> ScoreboardData:
    """
    Query Scoreboard statistics from remote

    :param game_date: The date of the games
    :type game_date: datetime.date
    :param league_id: The identifier of the league
    :type league_id: LeagueId
    :return: A dictionary containing the scoreboard statistics
    :rtype: dict[str, Any]
    """
    params = {
        "GameDate": game_date.strftime("%Y-%m-%d"),
        "LeagueID": league_id,
    }
    async with httpx.AsyncClient(headers=HEADERS) as client:
        response = await client.get(urljoin(BASE_URL, ENDPOINT), params=params)
        return ScoreboardData.model_validate_json(response.content.decode("utf-8"))


async def main(
    game_date: datetime.date,
    league_id: LeagueId = LeagueId.NBA,
) -> dict[str, ScoreboardGameBrief]:
    data: ScoreboardData = await query_scoreboard(
        game_date=game_date,
        league_id=league_id,
    )

    result: dict[str, ScoreboardGameBrief] = {}
    for game in data.scoreboard.games:
        result[game.gameId] = ScoreboardGameBrief(
            away_team_tricode=game.awayTeam.teamTricode,
            away_team_score=game.awayTeam.score,
            home_team_tricode=game.homeTeam.teamTricode,
            home_team_score=game.homeTeam.score,
        )
        print(
            f"  {game.awayTeam.teamTricode} {game.awayTeam.score}  @  "
            f"{game.homeTeam.teamTricode} {game.homeTeam.score}  "
            f"[{game.gameStatusText}]"
        )
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Query NBA scoreboard statistics")
    parser.add_argument(
        "--game-date",
        default=datetime.date.today().strftime("%Y-%m-%d"),
        help="Game date in YYYY-MM-DD format (default: today)",
    )
    parser.add_argument(
        "--league-id",
        default=LeagueId.NBA,
        type=LeagueId,
        choices=list(LeagueId),
        help="League ID (default: NBA)",
    )
    args = parser.parse_args()
    asyncio.run(
        main(
            game_date=datetime.date.fromisoformat(args.game_date),
            league_id=args.league_id,
        )
    )
