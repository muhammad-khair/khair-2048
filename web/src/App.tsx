import React, { useCallback, useEffect, useState } from 'react';
import './index.css';

import { Grid as GridType, MoveResponse, RecommendationResponse, Status } from './types';
import { Header } from './components/Header';
import { GameOverlay } from './components/GameOverlay';
import { Grid } from './components/Grid';
import { Controls } from './components/Controls';
import { Recommendation } from './components/Recommendation';
import { GameExplanation } from './components/GameExplanation';

const App: React.FC = () => {
  const [grid, setGrid] = useState<GridType | null>(null);
  const [currentBest, setCurrentBest] = useState<number>(0);
  const [sessionBest, setSessionBest] = useState<number>(0);
  const [turns, setTurns] = useState<number>(0);
  const [status, setStatus] = useState<Status>('ONGOING');
  const [isGameOver, setIsGameOver] = useState<boolean>(false);
  const [recommendation, setRecommendation] = useState<RecommendationResponse | null>(null);
  const [recoLoading, setRecoLoading] = useState<boolean>(false);

  const startNewGame = useCallback(async () => {
    try {
      const resp = await fetch('/new', { method: 'POST' });
      const data: GridType = await resp.json();
      setGrid(data);

      // Find the largest number in the new grid
      let maxVal = 0;
      data.forEach(row => {
        row.forEach(val => {
          if (val !== null && val > maxVal) maxVal = val;
        });
      });

      setCurrentBest(maxVal);
      setSessionBest(prev => Math.max(prev, maxVal));
      setTurns(0);

      setStatus('ONGOING');
      setIsGameOver(false);
      setRecommendation(null);
    } catch (err) {
      console.error('Failed to start new game', err);
    }
  }, []);

  const move = useCallback(async (direction: string) => {
    if (!grid || isGameOver) return;

    try {
      const resp = await fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grid, direction, turns })
      });

      if (!resp.ok) return;

      const data: MoveResponse = await resp.json();

      // Only update if grid changed
      if (JSON.stringify(grid) !== JSON.stringify(data.grid)) {
        setGrid(data.grid);
        setCurrentBest(data.largest_number);
        setSessionBest(prev => Math.max(prev, data.largest_number));
        setTurns(data.turns);
        setStatus(data.status);
        if (data.status === 'WIN' || data.status === 'LOSE') {
          setIsGameOver(true);
        }
        setRecommendation(null);
      }
    } catch (err) {
      console.error('Move failed', err);
    }
  }, [grid, isGameOver, turns]);

  useEffect(() => {
    startNewGame();
    setRecommendation(null);
  }, [startNewGame]);

  const handleRecommend = async () => {
    if (!grid || isGameOver || recoLoading) return;
    setRecoLoading(true);
    try {
      const resp = await fetch('/recommend', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grid })
      });
      if (resp.ok) {
        const data: RecommendationResponse = await resp.json();
        setRecommendation(data);
      }
    } catch (err) {
      console.error('Recommendation failed', err);
    } finally {
      setRecoLoading(false);
    }
  };

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (isGameOver) return;
      let dir: string | null = null;
      if (e.key === 'ArrowUp' || e.key === 'w') dir = 'up';
      else if (e.key === 'ArrowDown' || e.key === 's') dir = 'down';
      else if (e.key === 'ArrowLeft' || e.key === 'a') dir = 'left';
      else if (e.key === 'ArrowRight' || e.key === 'd') dir = 'right';

      if (dir) {
        e.preventDefault();
        move(dir);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [move, isGameOver]);

  return (
    <div className="container">
      <Header
        currentBest={currentBest}
        sessionBest={sessionBest}
        onNewGame={startNewGame}
      />

      <div className="game-container">
        {isGameOver && (
          <GameOverlay
            status={status}
            turns={turns}
            onRestart={startNewGame}
          />
        )}

        <Grid grid={grid} />
      </div>

      <Controls
        onMove={move}
        onRecommend={handleRecommend}
        isRecommendLoading={recoLoading}
        disabled={isGameOver}
      />

      {recommendation && (
        <Recommendation recommendation={recommendation} />
      )}

      <GameExplanation />
    </div>
  );
};

export default App;
