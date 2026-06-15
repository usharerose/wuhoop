"""
External data sources
"""

from .boxscore_summary import query_boxscore_summary
from .play_by_play import query_play_by_play
from .scoreboard import query_scoreboard

__all__ = ["query_boxscore_summary", "query_play_by_play", "query_scoreboard"]
