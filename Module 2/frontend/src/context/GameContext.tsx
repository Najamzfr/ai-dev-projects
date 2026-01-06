import React, { createContext, useContext, useState, ReactNode, useEffect } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { apiClient, ApiError } from '@/lib/api-client';
import type { LeaderboardEntry, GameMode } from '@/types/api';
import { showSuccess, showError } from '@/lib/toast';

// Game mode types (re-export for compatibility)
export type { GameMode };

// Screen types for navigation
export type GameScreen = 'login' | 'menu' | 'game' | 'gameover' | 'leaderboard';

// Re-export LeaderboardEntry for compatibility
export type { LeaderboardEntry };

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
  isLoadingLeaderboard: boolean;
  leaderboardError: Error | null;
  addLeaderboardEntry: (score: number) => Promise<void>;
  isSubmittingScore: boolean;
  submitError: Error | null;
}

const GameContext = createContext<GameContextType | undefined>(undefined);

export function GameProvider({ children }: { children: ReactNode }) {
  const [username, setUsername] = useState('');
  const [currentScreen, setCurrentScreen] = useState<GameScreen>('login');
  const [gameMode, setGameMode] = useState<GameMode>('walls');
  const [currentScore, setCurrentScore] = useState(0);
  const queryClient = useQueryClient();

  // Fetch leaderboard from backend
  const {
    data: leaderboardData,
    isLoading: isLoadingLeaderboard,
    error: leaderboardError,
  } = useQuery({
    queryKey: ['leaderboard', gameMode, 'score', 10, 0],
    queryFn: () => apiClient.getLeaderboard(10, 0, gameMode, 'score'),
    staleTime: 30000, // Cache for 30 seconds
    refetchOnWindowFocus: false,
    retry: 3, // Retry failed requests up to 3 times
    retryDelay: (attemptIndex) => Math.min(1000 * 2 ** attemptIndex, 30000), // Exponential backoff
  });
  
  // Show error toast if leaderboard fetch fails
  useEffect(() => {
    if (leaderboardError) {
      showError('Failed to load leaderboard. Please refresh the page.');
    }
  }, [leaderboardError]);

  // Submit score mutation
  const submitScoreMutation = useMutation({
    mutationFn: async (score: number) => {
      return apiClient.submitScore({
        username,
        score,
        mode: gameMode,
      });
    },
    onSuccess: () => {
      // Invalidate and refetch leaderboard
      queryClient.invalidateQueries({ queryKey: ['leaderboard'] });
      showSuccess('Score submitted successfully!');
    },
    onError: (error: ApiError) => {
      console.error('Failed to submit score:', error);
      const errorMessage = error.message || 'Failed to submit score. Please try again.';
      showError(errorMessage);
    },
  });

  // Add new entry to leaderboard (now calls backend API)
  const addLeaderboardEntry = async (score: number) => {
    if (!username) {
      throw new Error('Username is required');
    }

    try {
      await submitScoreMutation.mutateAsync(score);
    } catch (error) {
      // Error is handled by mutation, but we can re-throw if needed
      throw error;
    }
  };

  // Get leaderboard entries from query data
  const leaderboard = leaderboardData?.data || [];

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
        isLoadingLeaderboard,
        leaderboardError: leaderboardError as Error | null,
        addLeaderboardEntry,
        isSubmittingScore: submitScoreMutation.isPending,
        submitError: submitScoreMutation.error as Error | null,
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
