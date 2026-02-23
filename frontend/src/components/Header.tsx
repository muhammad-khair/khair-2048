import React from 'react';

export type Difficulty = 'EASY' | 'MEDIUM' | 'HARD';

interface HeaderProps {
    currentBest: number;
    sessionBest: number;
    onNewGame: () => void;
    difficulty?: Difficulty;
    onDifficultyChange?: (difficulty: Difficulty) => void;
}

export const Header: React.FC<HeaderProps> = ({
    currentBest,
    sessionBest,
    onNewGame,
    difficulty = 'EASY',
    onDifficultyChange
}) => {
    return (
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
                <div className="new-game-controls">
                    <button className="restart-button" onClick={onNewGame}>New Game</button>
                    <select
                        className="difficulty-select"
                        value={difficulty}
                        onChange={(e) => onDifficultyChange?.(e.target.value as Difficulty)}
                    >
                        <option value="EASY">Easy</option>
                        <option value="MEDIUM">Medium</option>
                        <option value="HARD">Hard</option>
                    </select>
                </div>
            </div>
            <div className="above-game">
                <p className="game-intro">Join the numbers and get to the <strong>2048 tile!</strong></p>
            </div>
        </header>
    );
};
