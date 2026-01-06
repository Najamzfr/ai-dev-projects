import React, { useEffect } from 'react';
import { useGame } from '@/context/GameContext';
import { useSnakeGame } from '@/hooks/useSnakeGame';
import { Button } from '@/components/ui/button';
import { Pause, Play, ArrowUp, ArrowDown, ArrowLeft, ArrowRight } from 'lucide-react';

export function GameBoard() {
  const { gameMode, setCurrentScreen, setCurrentScore, addLeaderboardEntry } = useGame();

  const handleGameOver = async (finalScore: number) => {
    setCurrentScore(finalScore);
    // Submit score to backend (non-blocking)
    addLeaderboardEntry(finalScore).catch((error) => {
      console.error('Failed to submit score:', error);
      // Score will still be shown, but submission failed
    });
    setTimeout(() => {
      setCurrentScreen('gameover');
    }, 500);
  };

  const {
    snake,
    food,
    score,
    isPlaying,
    isPaused,
    isWrapping,
    gridSize,
    startGame,
    togglePause,
  } = useSnakeGame(gameMode, handleGameOver);

  // Auto-start game when component mounts
  useEffect(() => {
    startGame();
  }, [startGame]);

  const cellSize = Math.min(
    (window.innerWidth - 48) / gridSize,
    (window.innerHeight - 200) / gridSize,
    20
  );

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      {/* Header */}
      <div className="flex items-center justify-between w-full max-w-md mb-4">
        <div>
          <p className="text-muted-foreground font-game text-xs">MODE</p>
          <p className="text-secondary neon-text-secondary font-pixel text-xs">
            {gameMode === 'walls' ? 'WALLS' : 'THROUGH'}
          </p>
        </div>
        
        <div className="text-center">
          <p className="text-muted-foreground font-game text-xs">SCORE</p>
          <p className="text-primary neon-text font-pixel text-lg">{score}</p>
        </div>
        
        <Button
          onClick={togglePause}
          variant="ghost"
          size="icon"
          className="text-primary hover:bg-primary/10"
        >
          {isPaused ? <Play className="w-5 h-5" /> : <Pause className="w-5 h-5" />}
        </Button>
      </div>

      {/* Game Board */}
      <div
        className="relative border-2 border-primary neon-box bg-card"
        style={{
          width: gridSize * cellSize,
          height: gridSize * cellSize,
        }}
      >
        {/* Grid Background */}
        <div
          className="absolute inset-0"
          style={{
            backgroundImage: `
              linear-gradient(to right, hsl(var(--grid)) 1px, transparent 1px),
              linear-gradient(to bottom, hsl(var(--grid)) 1px, transparent 1px)
            `,
            backgroundSize: `${cellSize}px ${cellSize}px`,
          }}
        />

        {/* Snake */}
        {snake.map((segment, index) => (
          <div
            key={index}
            className="absolute rounded-sm"
            style={{
              left: segment.x * cellSize,
              top: segment.y * cellSize,
              width: cellSize - 2,
              height: cellSize - 2,
              margin: 1,
              backgroundColor: `hsl(150, 100%, ${50 - index * 2}%)`,
              boxShadow: index === 0 
                ? '0 0 10px hsl(var(--snake)), 0 0 20px hsl(var(--snake))'
                : '0 0 5px hsl(var(--snake))',
            }}
          >
            {/* Snake eyes on head */}
            {index === 0 && (
              <>
                <div
                  className="absolute w-1 h-1 bg-background rounded-full"
                  style={{ top: '20%', left: '25%' }}
                />
                <div
                  className="absolute w-1 h-1 bg-background rounded-full"
                  style={{ top: '20%', right: '25%' }}
                />
              </>
            )}
          </div>
        ))}

        {/* Food */}
        <div
          className="absolute rounded-full animate-pulse"
          style={{
            left: food.x * cellSize,
            top: food.y * cellSize,
            width: cellSize - 2,
            height: cellSize - 2,
            margin: 1,
            backgroundColor: 'hsl(var(--food))',
            boxShadow: '0 0 10px hsl(var(--food)), 0 0 20px hsl(var(--food))',
          }}
        />

        {/* Pause Overlay */}
        {isPaused && (
          <div className="absolute inset-0 bg-background/80 flex items-center justify-center">
            <div className="text-center">
              <p className="text-primary font-pixel text-lg animate-blink">PAUSED</p>
              <p className="text-muted-foreground font-game text-xs mt-2">
                Press SPACE to continue
              </p>
            </div>
          </div>
        )}
      </div>

      {/* Mobile Controls */}
      <div className="mt-6 md:hidden">
        <div className="flex flex-col items-center gap-2">
          <MobileButton direction="UP" />
          <div className="flex gap-2">
            <MobileButton direction="LEFT" />
            <MobileButton direction="DOWN" />
            <MobileButton direction="RIGHT" />
          </div>
        </div>
      </div>

      {/* Instructions */}
      <div className="mt-6 text-center">
        <p className="text-muted-foreground font-game text-xs hidden md:block">
          Arrow Keys / WASD to move • SPACE to pause
        </p>
        <Button
          onClick={() => setCurrentScreen('menu')}
          variant="ghost"
          className="text-muted-foreground hover:text-primary font-game text-xs mt-4"
        >
          ← Back to Menu
        </Button>
      </div>
    </div>
  );
}

function MobileButton({ direction }: { direction: 'UP' | 'DOWN' | 'LEFT' | 'RIGHT' }) {
  const icons = {
    UP: ArrowUp,
    DOWN: ArrowDown,
    LEFT: ArrowLeft,
    RIGHT: ArrowRight,
  };
  const Icon = icons[direction];
  
  const handlePress = () => {
    const keyMap = {
      UP: 'ArrowUp',
      DOWN: 'ArrowDown',
      LEFT: 'ArrowLeft',
      RIGHT: 'ArrowRight',
    };
    window.dispatchEvent(new KeyboardEvent('keydown', { key: keyMap[direction] }));
  };

  return (
    <button
      onTouchStart={handlePress}
      onClick={handlePress}
      className="w-12 h-12 bg-muted/50 border border-primary/50 rounded-lg 
                 flex items-center justify-center text-primary active:bg-primary/20"
    >
      <Icon className="w-6 h-6" />
    </button>
  );
}
