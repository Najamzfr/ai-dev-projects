import React from 'react';
import { useGame } from '@/context/GameContext';
import { Button } from '@/components/ui/button';

export function GameOverScreen() {
  const { 
    currentScore, 
    gameMode, 
    setCurrentScreen,
    isSubmittingScore,
    submitError,
  } = useGame();

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      {/* Game Over Text */}
      <div className="mb-8 text-center">
        <h1 className="text-destructive font-pixel text-2xl md:text-4xl mb-4 animate-pulse">
          GAME OVER
        </h1>
        <div className="w-24 h-1 bg-destructive mx-auto" 
             style={{ boxShadow: '0 0 15px hsl(var(--destructive))' }} />
      </div>

      {/* Score Card */}
      <div className="bg-card border-2 border-primary neon-box rounded-lg p-8 mb-8 text-center">
        <p className="text-muted-foreground font-game text-sm mb-2">YOUR SCORE</p>
        <p className="text-primary neon-text font-pixel text-4xl md:text-6xl mb-4">
          {currentScore}
        </p>
        <p className="text-secondary neon-text-secondary font-game text-xs">
          Mode: {gameMode === 'walls' ? 'WALLS' : 'WALLS-THROUGH'}
        </p>
      </div>

      {/* Score Submission Status */}
      {isSubmittingScore && (
        <p className="text-muted-foreground font-game text-xs mb-8 animate-pulse">
          Submitting score...
        </p>
      )}
      
      {!isSubmittingScore && !submitError && (
        <p className="text-muted-foreground font-game text-xs mb-8 animate-float">
          ✓ Score added to leaderboard
        </p>
      )}
      
      {submitError && (
        <div className="mb-8 text-center">
          <p className="text-destructive font-game text-xs mb-2">
            Failed to submit score
          </p>
          <p className="text-muted-foreground font-game text-xs">
            {submitError.message || 'Please try again later'}
          </p>
        </div>
      )}

      {/* Action Buttons */}
      <div className="flex flex-col gap-4 w-full max-w-xs">
        <Button
          onClick={() => setCurrentScreen('game')}
          className="bg-primary text-primary-foreground hover:bg-primary/80 
                     font-pixel text-xs py-6 transition-all duration-300
                     hover:shadow-[0_0_20px_hsl(var(--primary))]"
        >
          PLAY AGAIN
        </Button>
        
        <Button
          onClick={() => setCurrentScreen('leaderboard')}
          variant="outline"
          className="border-secondary text-secondary hover:bg-secondary/10 
                     font-pixel text-xs py-6 transition-all duration-300
                     hover:shadow-[0_0_15px_hsl(var(--secondary))]"
        >
          LEADERBOARD
        </Button>
        
        <Button
          onClick={() => setCurrentScreen('menu')}
          variant="ghost"
          className="text-muted-foreground hover:text-primary font-game text-xs"
        >
          Main Menu
        </Button>
      </div>
    </div>
  );
}
