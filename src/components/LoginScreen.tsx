import React, { useState } from 'react';
import { useGame } from '@/context/GameContext';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';

export function LoginScreen() {
  const { setUsername, setCurrentScreen } = useGame();
  const [inputValue, setInputValue] = useState('');
  const [error, setError] = useState('');

  const handleLogin = () => {
    const trimmed = inputValue.trim().toUpperCase();
    if (trimmed.length < 2) {
      setError('Username must be at least 2 characters');
      return;
    }
    if (trimmed.length > 12) {
      setError('Username must be 12 characters or less');
      return;
    }
    setUsername(trimmed);
    setCurrentScreen('menu');
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter') {
      handleLogin();
    }
  };

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      {/* Animated Snake Logo */}
      <div className="mb-8 animate-float">
        <div className="flex gap-1">
          {[...Array(5)].map((_, i) => (
            <div
              key={i}
              className="w-6 h-6 bg-primary rounded-sm"
              style={{
                opacity: 1 - i * 0.15,
                boxShadow: '0 0 10px hsl(var(--primary))',
              }}
            />
          ))}
        </div>
      </div>

      {/* Title */}
      <h1 className="game-title text-3xl md:text-5xl mb-2 text-primary animate-pulse-glow">
        SNAKE
      </h1>
      <p className="text-secondary neon-text-secondary text-sm mb-12 font-pixel">
        ARCADE
      </p>

      {/* Login Card */}
      <div className="w-full max-w-sm p-6 bg-card border-2 border-primary neon-box rounded-lg">
        <h2 className="text-primary neon-text text-center mb-6 font-pixel text-xs">
          ENTER YOUR NAME
        </h2>
        
        <Input
          type="text"
          value={inputValue}
          onChange={(e) => {
            setInputValue(e.target.value);
            setError('');
          }}
          onKeyDown={handleKeyDown}
          placeholder="PLAYER NAME"
          maxLength={12}
          className="bg-input border-primary/50 text-primary placeholder:text-primary/30 
                     text-center font-game uppercase tracking-wider mb-4
                     focus:border-primary focus:ring-primary"
        />
        
        {error && (
          <p className="text-destructive text-xs text-center mb-4 font-game">
            {error}
          </p>
        )}

        <Button
          onClick={handleLogin}
          className="w-full bg-primary text-primary-foreground hover:bg-primary/80 
                     font-pixel text-xs py-6 transition-all duration-300
                     hover:shadow-[0_0_20px_hsl(var(--primary))]"
        >
          START
        </Button>
      </div>

      {/* Instructions */}
      <p className="text-muted-foreground text-xs mt-8 text-center font-game">
        Use Arrow Keys or WASD to move
      </p>
    </div>
  );
}
