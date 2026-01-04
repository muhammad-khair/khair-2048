import React, { useCallback, useEffect, useState } from 'react';
import './index.css';

import { Grid as GridType, Status, ModelInfo } from './types';
import { RecommendationResponse } from './types';
import { Header } from './components/Header';
import { GameOverlay } from './components/GameOverlay';
import { Grid } from './components/Grid';
import { Controls } from './components/Controls';
import { Recommendation } from './components/Recommendation';
import { ModelSelector } from './components/ModelSelector';
import { ErrorMessage } from './components/ErrorMessage';
import { GameExplanation } from './components/GameExplanation';
import { ServerTransport, ApiError } from './services/transport';

const App: React.FC = () => {
  const [grid, setGrid] = useState<GridType | null>(null);
  const [currentBest, setCurrentBest] = useState<number>(0);
  const [sessionBest, setSessionBest] = useState<number>(0);
  const [turns, setTurns] = useState<number>(0);
  const [status, setStatus] = useState<Status>('ONGOING');
  const [isGameOver, setIsGameOver] = useState<boolean>(false);
  const [recommendation, setRecommendation] = useState<RecommendationResponse | null>(null);
  const [recoLoading, setRecoLoading] = useState<boolean>(false);
  const [availableModels, setAvailableModels] = useState<ModelInfo[]>([]);
  const [selectedProvider, setSelectedProvider] = useState<string>('heuristic');
  const [selectedModel, setSelectedModel] = useState<string>('simple');
  const [errorInfo, setErrorInfo] = useState<{ message: string } | null>(null);

  const handleApiError = useCallback((err: any) => {
    console.error('API Error:', err);
    let message = 'An unexpected error occurred';

    if (err instanceof ApiError || err.name === 'ApiError') {
      message = err.message;
    } else if (err instanceof Error) {
      message = err.message;
    }

    setErrorInfo({ message });
  }, []);

  const startNewGame = useCallback(async () => {
    try {
      const data = await ServerTransport.startNewGame();
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
      handleApiError(err);
    }
  }, [handleApiError]);

  const move = useCallback(async (direction: string) => {
    if (!grid || isGameOver) return;

    try {
      const data = await ServerTransport.move(grid, direction, turns);

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
      handleApiError(err);
    }
  }, [grid, isGameOver, turns, handleApiError]);

  useEffect(() => {
    startNewGame();
    setRecommendation(null);
  }, [startNewGame]);

  const handleRecommend = async () => {
    if (!grid || isGameOver || recoLoading) return;
    setRecoLoading(true);
    try {
      const data = await ServerTransport.getRecommendation(grid, selectedProvider, selectedModel);
      setRecommendation(data);
    } catch (err) {
      handleApiError(err);
    } finally {
      setRecoLoading(false);
    }
  };

  // Fetch available models on mount
  useEffect(() => {
    const fetchModels = async () => {
      try {
        const data = await ServerTransport.listModels();
        setAvailableModels(data.models);
        // Set default model if available
        if (data.models.length > 0) {
          setSelectedProvider(data.models[0].provider);
          setSelectedModel(data.models[0].model);
        }
      } catch (err) {
        console.error('Failed to fetch models', err);
        // Fallback to heuristic
      }
    };
    fetchModels();
  }, []);

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

  useEffect(() => {
    let touchStartX = 0;
    let touchStartY = 0;

    const handleTouchStart = (e: TouchEvent) => {
      touchStartX = e.touches[0].clientX;
      touchStartY = e.touches[0].clientY;
    };

    const handleTouchEnd = (e: TouchEvent) => {
      if (isGameOver) return;
      const touchEndX = e.changedTouches[0].clientX;
      const touchEndY = e.changedTouches[0].clientY;

      const diffX = touchEndX - touchStartX;
      const diffY = touchEndY - touchStartY;

      if (Math.abs(diffX) > Math.abs(diffY)) {
        if (diffX > 30) move('right');
        else if (diffX < -30) move('left');
      } else {
        if (diffY > 30) move('down');
        else if (diffY < -30) move('up');
      }
    };

    window.addEventListener('touchstart', handleTouchStart, { passive: true });
    window.addEventListener('touchend', handleTouchEnd, { passive: true });
    return () => {
      window.removeEventListener('touchstart', handleTouchStart);
      window.removeEventListener('touchend', handleTouchEnd);
    };
  }, [move, isGameOver]);

  return (
    <div className="container">
      <Header
        currentBest={currentBest}
        sessionBest={sessionBest}
        onNewGame={startNewGame}
      />

      {errorInfo && (
        <ErrorMessage
          message={errorInfo.message}
          onDismiss={() => setErrorInfo(null)}
        />
      )}

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

      <ModelSelector
        models={availableModels}
        selectedProvider={selectedProvider}
        selectedModel={selectedModel}
        onChange={(provider, model) => {
          setSelectedProvider(provider);
          setSelectedModel(model);
        }}
        disabled={isGameOver || recoLoading}
      />

      {recommendation && (
        <Recommendation recommendation={recommendation} />
      )}



      <GameExplanation />
    </div>
  );
};

export default App;
