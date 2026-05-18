"""
Application-wide constants
"""

BASE_URL: str = "https://stats.nba.com/stats/"
ENDPOINT: str = "scoreboardv3"


HEADERS: dict[str, str] = {
    "host": "stats.nba.com",
    "origin": "https://www.nba.com",
    "referer": "https://www.nba.com/",
    "user-agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 Safari/537.36"
    ),
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-site",
    "x-nba-stats-origin": "stats",
    "x-nba-stats-token": "true",
}
