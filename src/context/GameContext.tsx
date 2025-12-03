import React, { createContext, useContext, useState, ReactNode } from 'react';

// Game mode types
export type GameMode = 'walls' | 'walls-through';

// Screen types for navigation
export type GameScreen = 'login' | 'menu' | 'game' | 'gameover' | 'leaderboard';

// Leaderboard entry type
export interface LeaderboardEntry {
  username: string;
  score: number;
  mode: GameMode;
  date: string;
}

// Initial mock leaderboard data
const INITIAL_LEADERBOARD: LeaderboardEntry[] = [
  { username: 'PLAYER1', score: 250, mode: 'walls', date: '2024-01-15' },
  { username: 'GAMER42', score: 180, mode: 'walls-through', date: '2024-01-14' },
  { username: 'SNAKEMASTER', score: 150, mode: 'walls', date: '2024-01-13' },
  { username: 'RETRO_FAN', score: 120, mode: 'walls-through', date: '2024-01-12' },
  { username: 'ARCADE_PRO', score: 100, mode: 'walls', date: '2024-01-11' },
];

interface GameContextType {
  username: string;
  setUsername: (name: string) => void;
  currentScreen: GameScreen;
  setCurrentScreen: (screen: GameScreen) => void;
  gameMode: GameMode;
  setGameMode: (mode: GameMode) => void;
  currentScore: number;
  setCurrentScore: (score: number) => void;
  leaderboard: LeaderboardEntry[];
  addLeaderboardEntry: (score: number) => void;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

export function GameProvider({ children }: { children: ReactNode }) {
  const [username, setUsername] = useState('');
  const [currentScreen, setCurrentScreen] = useState<GameScreen>('login');
  const [gameMode, setGameMode] = useState<GameMode>('walls');
  const [currentScore, setCurrentScore] = useState(0);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>(INITIAL_LEADERBOARD);

  // Add new entry to leaderboard and sort by score
  const addLeaderboardEntry = (score: number) => {
    const newEntry: LeaderboardEntry = {
      username,
      score,
      mode: gameMode,
      date: new Date().toISOString().split('T')[0],
    };
    
    setLeaderboard(prev => 
      [...prev, newEntry].sort((a, b) => b.score - a.score).slice(0, 10)
    );
  };

  return (
    <GameContext.Provider
      value={{
        username,
        setUsername,
        currentScreen,
        setCurrentScreen,
        gameMode,
        setGameMode,
        currentScore,
        setCurrentScore,
        leaderboard,
        addLeaderboardEntry,
      }}
    >
      {children}
    </GameContext.Provider>
  );
}

export function useGame() {
  const context = useContext(GameContext);
  if (!context) {
    throw new Error('useGame must be used within a GameProvider');
  }
  return context;
}
