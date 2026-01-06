/** TypeScript types for API responses */

export type GameMode = 'walls' | 'walls-through';

export interface LeaderboardEntry {
  id?: number;
  username: string;
  score: number;
  mode: GameMode;
  date: string;
}

export interface ScoreSubmission {
  username: string;
  score: number;
  mode: GameMode;
}

export interface PaginationMeta {
  total: number;
  limit: number;
  offset: number;
  has_more: boolean;
}

export interface PaginatedResponse<T> {
  data: T[];
  meta: PaginationMeta;
}

export interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: Record<string, any>;
  };
}

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
}

export interface StatsResponse {
  total_players: number;
  total_scores: number;
  average_score: number;
  top_score: number;
}

