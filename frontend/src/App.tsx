import { useEffect, useState } from 'react';
import { ScoreboardTable } from './components/ScoreboardTable';
import type { ScoreboardData } from './types';
import './App.css';

function App() {
  const [games, setGames] = useState<ScoreboardData[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedDate, setSelectedDate] = useState(
    new Date().toISOString().split('T')[0]
  );

  const fetchScoreboard = async () => {
    try {
      setLoading(true);
      setError(null);
      const response = await fetch(
        `/api/v1/scoreboards?date=${selectedDate}`
      );
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setGames(data.data || []);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error');
    } finally {
      setLoading(false);
    }
  };

  // 只在初始加载时请求一次
  useEffect(() => {
    fetchScoreboard();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return (
    <div className="app">
      <header className="header">
        <h1>NBA Scoreboard</h1>
        <div className="date-selector">
          <label htmlFor="date-picker">Date:</label>
          <input
            id="date-picker"
            type="date"
            value={selectedDate}
            onChange={(e) => setSelectedDate(e.target.value)}
            className="date-picker"
          />
          <button onClick={fetchScoreboard} className="search-button">
            Search
          </button>
        </div>
      </header>

      {error && <div className="error">Error: {error}</div>}

      <ScoreboardTable games={games} loading={loading} />
    </div>
  );
}

export default App;
