import type { ScoreboardData } from '../types';

interface ScoreboardTableProps {
  games: ScoreboardData[];
  loading?: boolean;
}

export function ScoreboardTable({ games, loading = false }: ScoreboardTableProps) {
  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  if (games.length === 0) {
    return <div className="empty">No games scheduled for this date. Try selecting a different date.</div>;
  }

  return (
    <table className="scoreboard-table">
      <thead>
        <tr>
          <th>Time</th>
          <th>Away</th>
          <th>Score</th>
          <th>Home</th>
          <th>Score</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        {games.map((game) => (
          <tr key={game.game_id}>
            <td>{formatTime(game.game_time_utc)}</td>
            <td className="team-name">
              {game.away_team_city} {game.away_team_name}
            </td>
            <td className="score">{game.away_team_score}</td>
            <td className="team-name">
              {game.home_team_city} {game.home_team_name}
            </td>
            <td className="score">{game.home_team_score}</td>
            <td className="status">{formatStatus(game.game_status_code)}</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

function formatTime(utcTime: string): string {
  const date = new Date(utcTime);
  return date.toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit',
    hour12: true,
  });
}

function formatStatus(statusCode: number): string {
  switch (statusCode) {
    case 1:
      return 'Scheduled';
    case 2:
      return 'In Progress';
    case 3:
      return 'Final';
    default:
      return 'Unknown';
  }
}
