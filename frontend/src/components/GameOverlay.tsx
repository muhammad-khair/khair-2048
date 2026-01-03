import React from 'react';
import { Status } from '../types';

interface GameOverlayProps {
    status: Status;
    turns: number;
    onRestart: () => void;
}

export const GameOverlay: React.FC<GameOverlayProps> = ({ status, turns, onRestart }) => {
    return (
        <div className={`game-message ${status === 'WIN' ? 'game-won' : 'game-over'}`} style={{ display: 'flex' }} data-testid="game-overlay">
            <p>{status === 'WIN' ? 'You win!' : 'Game over!'}</p>
            <p className="total-turns">Total turns: {turns}</p>
            <div className="lower">
                <a className="retry-button" onClick={onRestart}>New Game</a>
            </div>
        </div>
    );
};
