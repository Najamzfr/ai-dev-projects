import { useState, useEffect, useCallback, useRef } from 'react';
import { GameMode } from '@/context/GameContext';

// Game constants
const GRID_SIZE = 20;
const INITIAL_SPEED = 150;
const SPEED_INCREMENT = 5;
const MIN_SPEED = 50;

// Direction vectors
type Direction = 'UP' | 'DOWN' | 'LEFT' | 'RIGHT';
const DIRECTIONS: Record<Direction, { x: number; y: number }> = {
  UP: { x: 0, y: -1 },
  DOWN: { x: 0, y: 1 },
  LEFT: { x: -1, y: 0 },
  RIGHT: { x: 1, y: 0 },
};

// Position type
interface Position {
  x: number;
  y: number;
}

export function useSnakeGame(mode: GameMode, onGameOver: (score: number) => void) {
  // Snake state - starts in the middle
  const [snake, setSnake] = useState<Position[]>([
    { x: 10, y: 10 },
    { x: 9, y: 10 },
    { x: 8, y: 10 },
  ]);
  
  // Food position
  const [food, setFood] = useState<Position>({ x: 15, y: 10 });
  
  // Current direction
  const [direction, setDirection] = useState<Direction>('RIGHT');
  
  // Game state
  const [isPlaying, setIsPlaying] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [score, setScore] = useState(0);
  const [speed, setSpeed] = useState(INITIAL_SPEED);
  
  // Use refs to access current state in intervals
  const directionRef = useRef(direction);
  const snakeRef = useRef(snake);
  const foodRef = useRef(food);
  
  // Update refs when state changes
  useEffect(() => {
    directionRef.current = direction;
  }, [direction]);
  
  useEffect(() => {
    snakeRef.current = snake;
  }, [snake]);
  
  useEffect(() => {
    foodRef.current = food;
  }, [food]);

  // Generate random food position
  const generateFood = useCallback((currentSnake: Position[]): Position => {
    let newFood: Position;
    do {
      newFood = {
        x: Math.floor(Math.random() * GRID_SIZE),
        y: Math.floor(Math.random() * GRID_SIZE),
      };
    } while (currentSnake.some(segment => segment.x === newFood.x && segment.y === newFood.y));
    return newFood;
  }, []);

  // Check collision with self
  const checkSelfCollision = useCallback((head: Position, body: Position[]): boolean => {
    return body.some(segment => segment.x === head.x && segment.y === head.y);
  }, []);

  // Check wall collision (only in walls mode)
  const checkWallCollision = useCallback((head: Position): boolean => {
    return head.x < 0 || head.x >= GRID_SIZE || head.y < 0 || head.y >= GRID_SIZE;
  }, []);

  // Wrap position for walls-through mode
  const wrapPosition = useCallback((pos: Position): Position => {
    return {
      x: (pos.x + GRID_SIZE) % GRID_SIZE,
      y: (pos.y + GRID_SIZE) % GRID_SIZE,
    };
  }, []);

  // Move snake
  const moveSnake = useCallback(() => {
    const currentSnake = snakeRef.current;
    const currentDirection = directionRef.current;
    const currentFood = foodRef.current;
    
    const head = currentSnake[0];
    const delta = DIRECTIONS[currentDirection];
    
    let newHead: Position = {
      x: head.x + delta.x,
      y: head.y + delta.y,
    };

    // Handle wall collision based on mode
    if (mode === 'walls') {
      if (checkWallCollision(newHead)) {
        setIsPlaying(false);
        onGameOver(score);
        return;
      }
    } else {
      // Walls-through mode: wrap around
      newHead = wrapPosition(newHead);
    }

    // Check self collision
    if (checkSelfCollision(newHead, currentSnake.slice(0, -1))) {
      setIsPlaying(false);
      onGameOver(score);
      return;
    }

    // Create new snake
    const newSnake = [newHead, ...currentSnake];

    // Check if food eaten
    if (newHead.x === currentFood.x && newHead.y === currentFood.y) {
      // Keep the tail (snake grows)
      setSnake(newSnake);
      setFood(generateFood(newSnake));
      setScore(prev => prev + 10);
      // Increase speed
      setSpeed(prev => Math.max(MIN_SPEED, prev - SPEED_INCREMENT));
    } else {
      // Remove tail
      newSnake.pop();
      setSnake(newSnake);
    }
  }, [mode, score, onGameOver, checkWallCollision, checkSelfCollision, wrapPosition, generateFood]);

  // Game loop
  useEffect(() => {
    if (!isPlaying || isPaused) return;

    const gameLoop = setInterval(moveSnake, speed);
    return () => clearInterval(gameLoop);
  }, [isPlaying, isPaused, speed, moveSnake]);

  // Keyboard controls
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (!isPlaying) return;

      // Prevent default for arrow keys
      if (['ArrowUp', 'ArrowDown', 'ArrowLeft', 'ArrowRight', ' '].includes(e.key)) {
        e.preventDefault();
      }

      // Pause with space
      if (e.key === ' ') {
        setIsPaused(prev => !prev);
        return;
      }

      const currentDir = directionRef.current;
      
      switch (e.key) {
        case 'ArrowUp':
        case 'w':
        case 'W':
          if (currentDir !== 'DOWN') setDirection('UP');
          break;
        case 'ArrowDown':
        case 's':
        case 'S':
          if (currentDir !== 'UP') setDirection('DOWN');
          break;
        case 'ArrowLeft':
        case 'a':
        case 'A':
          if (currentDir !== 'RIGHT') setDirection('LEFT');
          break;
        case 'ArrowRight':
        case 'd':
        case 'D':
          if (currentDir !== 'LEFT') setDirection('RIGHT');
          break;
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isPlaying]);

  // Start game
  const startGame = useCallback(() => {
    setSnake([
      { x: 10, y: 10 },
      { x: 9, y: 10 },
      { x: 8, y: 10 },
    ]);
    setFood({ x: 15, y: 10 });
    setDirection('RIGHT');
    setScore(0);
    setSpeed(INITIAL_SPEED);
    setIsPlaying(true);
    setIsPaused(false);
  }, []);

  // Toggle pause
  const togglePause = useCallback(() => {
    setIsPaused(prev => !prev);
  }, []);

  return {
    snake,
    food,
    score,
    isPlaying,
    isPaused,
    gridSize: GRID_SIZE,
    startGame,
    togglePause,
  };
}
