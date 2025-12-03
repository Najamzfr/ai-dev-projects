import { GameProvider, useGame } from '@/context/GameContext';
import { LoginScreen } from '@/components/LoginScreen';
import { MainMenu } from '@/components/MainMenu';
import { GameBoard } from '@/components/GameBoard';
import { GameOverScreen } from '@/components/GameOverScreen';
import { Leaderboard } from '@/components/Leaderboard';

// Main game router component
function GameRouter() {
  const { currentScreen } = useGame();

  switch (currentScreen) {
    case 'login':
      return <LoginScreen />;
    case 'menu':
      return <MainMenu />;
    case 'game':
      return <GameBoard />;
    case 'gameover':
      return <GameOverScreen />;
    case 'leaderboard':
      return <Leaderboard />;
    default:
      return <LoginScreen />;
  }
}

// Main index page with provider
const Index = () => {
  return (
    <GameProvider>
      <main className="min-h-screen bg-background">
        <GameRouter />
      </main>
    </GameProvider>
  );
};

export default Index;
