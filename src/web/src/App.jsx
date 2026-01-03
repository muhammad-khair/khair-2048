import { useState, useEffect, useCallback } from 'react';

const Tile = ({ value, row, col }) => {
  return (
    <div className={`tile tile-${value} tile-position-${row + 1}-${col + 1}`}>
      {value}
    </div>
  );
};

const App = () => {
  const [grid, setGrid] = useState(null);
  const [currentBest, setCurrentBest] = useState(0);
  const [sessionBest, setSessionBest] = useState(0);
  const [status, setStatus] = useState('ONGOING');
  const [isGameOver, setIsGameOver] = useState(false);

  const startNewGame = useCallback(async () => {
    try {
      const resp = await fetch('/new', { method: 'POST' });
      const data = await resp.json();
      setGrid(data);
      setCurrentBest(0);
      setStatus('ONGOING');
      setIsGameOver(false);
    } catch (err) {
      console.error('Failed to start new game', err);
    }
  }, []);

  const move = useCallback(async (direction) => {
    if (!grid || isGameOver) return;

    try {
      const resp = await fetch('/move', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ grid, direction })
      });

      if (!resp.ok) return;

      const data = await resp.json();

      // Only update if grid changed
      if (JSON.stringify(grid) !== JSON.stringify(data.grid)) {
        setGrid(data.grid);
        setCurrentBest(data.largest_number);
        if (data.largest_number > sessionBest) {
          setSessionBest(data.largest_number);
        }
        setStatus(data.status);
        if (data.status === 'WIN' || data.status === 'LOSE') {
          setIsGameOver(true);
        }
      }
    } catch (err) {
      console.error('Move failed', err);
    }
  }, [grid, isGameOver, sessionBest]);

  useEffect(() => {
    startNewGame();
  }, [startNewGame]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if (isGameOver) return;
      let dir = null;
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

  // Swipe logic
  useEffect(() => {
    let startX = 0;
    let startY = 0;

    const handleTouchStart = (e) => {
      startX = e.touches[0].clientX;
      startY = e.touches[0].clientY;
    };

    const handleTouchEnd = (e) => {
      if (isGameOver) return;
      const endX = e.changedTouches[0].clientX;
      const endY = e.changedTouches[0].clientY;
      const dx = endX - startX;
      const dy = endY - startY;

      if (Math.max(Math.abs(dx), Math.abs(dy)) > 30) {
        let dir = null;
        if (Math.abs(dx) > Math.abs(dy)) {
          dir = dx > 0 ? 'right' : 'left';
        } else {
          dir = dy > 0 ? 'down' : 'up';
        }
        if (dir) move(dir);
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
      <header>
        <div className="header-top">
          <h1 className="logo">2048</h1>
        </div>
        <div className="header-bottom">
          <div className="scores-container">
            <div className="score-container session-best">
              <div className="score-label">SESSION BEST</div>
              <div className="score-value">{sessionBest}</div>
            </div>
            <div className="score-container">
              <div className="score-label">CURRENT BEST</div>
              <div className="score-value">{currentBest}</div>
            </div>
          </div>
          <button className="restart-button" onClick={startNewGame}>New Game</button>
        </div>
        <div className="above-game">
          <p className="game-intro">Join the numbers and get to the <strong>2048 tile!</strong></p>
        </div>
      </header>

      <div className="game-container">
        {isGameOver && (
          <div className={`game-message ${status === 'WIN' ? 'game-won' : 'game-over'}`} style={{ display: 'flex' }}>
            <p>{status === 'WIN' ? 'You win!' : 'Game over!'}</p>
            <div className="lower">
              <a className="retry-button" onClick={startNewGame}>New Game</a>
            </div>
          </div>
        )}

        <div id="grid-container" className="grid-container">
          {[...Array(16)].map((_, i) => (
            <div key={i} className="grid-cell" />
          ))}

          <div className="tile-container">
            {grid && grid.map((row, r) =>
              row.map((val, c) =>
                val !== null && <Tile key={`${r}-${c}`} value={val} row={r} col={c} />
              )
            )}
          </div>
        </div>
      </div>

      <div className="controls">
        <button className="control-btn" onClick={() => move('up')}>↑</button>
        <div className="middle-controls">
          <button className="control-btn" onClick={() => move('left')}>←</button>
          <button className="control-btn" onClick={() => move('down')}>↓</button>
          <button className="control-btn" onClick={() => move('right')}>→</button>
        </div>
      </div>

      <p className="game-explanation">
        <strong className="important">How to play:</strong> Use your <strong>arrow keys</strong> or
        <strong>buttons</strong> to move the tiles. When two tiles with the same number touch, they <strong>merge into one!</strong>
      </p>
    </div>
  );
};

export default App;
