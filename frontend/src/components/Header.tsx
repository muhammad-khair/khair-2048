import React from 'react';

interface HeaderProps {
    currentBest: number;
    sessionBest: number;
    onNewGame: () => void;
}

export const Header: React.FC<HeaderProps> = ({ currentBest, sessionBest, onNewGame }) => {
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
                <button className="restart-button" onClick={onNewGame}>New Game</button>
            </div>
            <div className="above-game">
                <p className="game-intro">Join the numbers and get to the <strong>2048 tile!</strong></p>
            </div>
        </header>
    );
};
