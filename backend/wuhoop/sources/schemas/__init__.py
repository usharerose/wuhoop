"""
External data source response schema
"""

from .boxscore_summary import BoxScoreSummaryData
from .play_by_play import PlayByPlayData
from .scoreboard import ScoreboardData

__all__ = ["BoxScoreSummaryData", "PlayByPlayData", "ScoreboardData"]
