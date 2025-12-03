import React from 'react';
import { useGame, GameMode } from '@/context/GameContext';
import { Button } from '@/components/ui/button';

export function MainMenu() {
  const { username, gameMode, setGameMode, setCurrentScreen } = useGame();

  const handleStartGame = () => {
    setCurrentScreen('game');
  };

  const handleViewLeaderboard = () => {
    setCurrentScreen('leaderboard');
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      {/* Welcome Message */}
      <div className="mb-8 text-center">
        <p className="text-muted-foreground font-game text-sm mb-2">WELCOME</p>
        <h2 className="text-primary neon-text font-pixel text-lg md:text-xl">
          {username}
        </h2>
      </div>

      {/* Title */}
      <h1 className="game-title text-2xl md:text-4xl mb-12 text-primary animate-pulse-glow">
        MAIN MENU
      </h1>

      {/* Mode Selection */}
      <div className="w-full max-w-md mb-8">
        <p className="text-secondary neon-text-secondary text-center font-pixel text-xs mb-4">
          SELECT MODE
        </p>
        
        <div className="grid grid-cols-2 gap-4">
          <ModeButton
            mode="walls"
            currentMode={gameMode}
            onClick={() => setGameMode('walls')}
            label="WALLS"
            description="Die on impact"
          />
          <ModeButton
            mode="walls-through"
            currentMode={gameMode}
            onClick={() => setGameMode('walls-through')}
            label="THROUGH"
            description="Pass through"
          />
        </div>
      </div>

      {/* Action Buttons */}
      <div className="flex flex-col gap-4 w-full max-w-xs">
        <Button
          onClick={handleStartGame}
          className="bg-primary text-primary-foreground hover:bg-primary/80 
                     font-pixel text-xs py-6 transition-all duration-300
                     hover:shadow-[0_0_20px_hsl(var(--primary))]"
        >
          PLAY GAME
        </Button>
        
        <Button
          onClick={handleViewLeaderboard}
          variant="outline"
          className="border-secondary text-secondary hover:bg-secondary/10 
                     font-pixel text-xs py-6 transition-all duration-300
                     hover:shadow-[0_0_15px_hsl(var(--secondary))]"
        >
          LEADERBOARD
        </Button>
      </div>

      {/* Mode Info */}
      <div className="mt-12 text-center">
        <p className="text-muted-foreground font-game text-xs">
          Current Mode: <span className="text-primary">{gameMode === 'walls' ? 'WALLS' : 'WALLS-THROUGH'}</span>
        </p>
      </div>
    </div>
  );
}

interface ModeButtonProps {
  mode: GameMode;
  currentMode: GameMode;
  onClick: () => void;
  label: string;
  description: string;
}

function ModeButton({ mode, currentMode, onClick, label, description }: ModeButtonProps) {
  const isSelected = mode === currentMode;
  
  return (
    <button
      onClick={onClick}
      className={`p-4 border-2 rounded-lg transition-all duration-300 ${
        isSelected
          ? 'border-primary bg-primary/10 neon-box'
          : 'border-muted hover:border-primary/50'
      }`}
    >
      <p className={`font-pixel text-xs mb-1 ${isSelected ? 'text-primary' : 'text-muted-foreground'}`}>
        {label}
      </p>
      <p className="text-muted-foreground font-game text-xs">
        {description}
      </p>
    </button>
  );
}
