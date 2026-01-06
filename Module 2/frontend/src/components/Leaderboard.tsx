import React from 'react';
import { useGame } from '@/context/GameContext';
import { Button } from '@/components/ui/button';
import { Trophy, Medal, Award } from 'lucide-react';

export function Leaderboard() {
  const { 
    leaderboard, 
    username, 
    setCurrentScreen,
    isLoadingLeaderboard,
    leaderboardError,
  } = useGame();

  const getRankIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <Trophy className="w-5 h-5 text-yellow-400" style={{ filter: 'drop-shadow(0 0 5px gold)' }} />;
      case 2:
        return <Medal className="w-5 h-5 text-gray-300" style={{ filter: 'drop-shadow(0 0 5px silver)' }} />;
      case 3:
        return <Award className="w-5 h-5 text-amber-600" style={{ filter: 'drop-shadow(0 0 5px #cd7f32)' }} />;
      default:
        return <span className="text-muted-foreground font-game text-sm w-5 text-center">{rank}</span>;
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      {/* Title */}
      <h1 className="game-title text-2xl md:text-4xl mb-2 text-primary animate-pulse-glow">
        LEADERBOARD
      </h1>
      <p className="text-secondary neon-text-secondary text-xs mb-8 font-pixel">
        TOP 10 PLAYERS
      </p>

      {/* Leaderboard Table */}
      <div className="w-full max-w-md bg-card border-2 border-primary neon-box rounded-lg overflow-hidden">
        {/* Header */}
        <div className="grid grid-cols-[40px_1fr_80px_80px] gap-2 p-3 bg-primary/10 border-b border-primary/30">
          <p className="text-primary font-pixel text-xs">#</p>
          <p className="text-primary font-pixel text-xs">PLAYER</p>
          <p className="text-primary font-pixel text-xs text-center">SCORE</p>
          <p className="text-primary font-pixel text-xs text-center">MODE</p>
        </div>

        {/* Entries */}
        <div className="max-h-[400px] overflow-y-auto">
          {isLoadingLeaderboard && (
            <div className="p-8 text-center">
              <p className="text-muted-foreground font-game text-sm animate-pulse">
                Loading leaderboard...
              </p>
            </div>
          )}
          
          {leaderboardError && (
            <div className="p-8 text-center">
              <p className="text-destructive font-game text-sm">
                Failed to load leaderboard. Please try again.
              </p>
            </div>
          )}
          
          {!isLoadingLeaderboard && !leaderboardError && leaderboard.map((entry, index) => {
            const isCurrentUser = entry.username === username;
            const rank = index + 1;
            
            return (
              <div
                key={entry.id || `${entry.username}-${entry.score}-${index}`}
                className={`grid grid-cols-[40px_1fr_80px_80px] gap-2 p-3 items-center
                           border-b border-muted/30 transition-colors
                           ${isCurrentUser ? 'bg-primary/5' : 'hover:bg-muted/20'}`}
              >
                <div className="flex items-center justify-center">
                  {getRankIcon(rank)}
                </div>
                
                <p className={`font-game text-sm truncate ${
                  isCurrentUser ? 'text-primary neon-text' : 'text-foreground'
                }`}>
                  {entry.username}
                  {isCurrentUser && <span className="text-xs ml-1">(YOU)</span>}
                </p>
                
                <p className={`font-pixel text-sm text-center ${
                  rank === 1 ? 'text-yellow-400' : 
                  rank === 2 ? 'text-gray-300' : 
                  rank === 3 ? 'text-amber-600' : 'text-muted-foreground'
                }`}>
                  {entry.score}
                </p>
                
                <p className="text-secondary font-game text-xs text-center">
                  {entry.mode === 'walls' ? 'WALLS' : 'THRU'}
                </p>
              </div>
            );
          })}
        </div>

        {/* Empty State */}
        {!isLoadingLeaderboard && !leaderboardError && leaderboard.length === 0 && (
          <div className="p-8 text-center">
            <p className="text-muted-foreground font-game text-sm">
              No scores yet. Be the first!
            </p>
          </div>
        )}
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col gap-4 w-full max-w-xs mt-8">
        <Button
          onClick={() => setCurrentScreen('game')}
          className="bg-primary text-primary-foreground hover:bg-primary/80 
                     font-pixel text-xs py-6 transition-all duration-300
                     hover:shadow-[0_0_20px_hsl(var(--primary))]"
        >
          PLAY GAME
        </Button>
        
        <Button
          onClick={() => setCurrentScreen('menu')}
          variant="ghost"
          className="text-muted-foreground hover:text-primary font-game text-xs"
        >
          ← Back to Menu
        </Button>
      </div>
    </div>
  );
}
