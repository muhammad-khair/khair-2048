import React from 'react';

export const GameExplanation: React.FC = () => {
    return (
        <p className="game-explanation">
            <strong className="important">How to play:</strong> Use your <strong>arrow keys</strong> or { }
            <strong>buttons</strong> to move the tiles. When two tiles with the same number touch, they <strong>merge into one!</strong>
        </p>
    );
};
