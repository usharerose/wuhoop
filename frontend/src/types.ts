export interface Team {
  team_id: number;
  team_name: string;
  team_city: string;
  team_tricode: string;
  team_slug: string;
  score: number;
}

export interface ScoreboardData {
  game_id: string;
  game_code: string;
  game_status_code: number;
  game_time_utc: string;
  period: number;
  away_team_id: number;
  away_team_name: string;
  away_team_city: string;
  away_team_tricode: string;
  away_team_slug: string;
  away_team_score: number;
  home_team_id: number;
  home_team_name: string;
  home_team_city: string;
  home_team_tricode: string;
  home_team_slug: string;
  home_team_score: number;
}

export interface ScoreboardsResponse {
  data: ScoreboardData[];
}
