import React from 'react';

export interface TileProps {
    value: number;
    row: number;
    col: number;
}

export const Tile: React.FC<TileProps> = ({ value, row, col }) => {
    return (
        <div className={`tile tile-${value} tile-position-${row + 1}-${col + 1}`} data-testid={`tile-${row}-${col}`}>
            {value}
        </div>
    );
};
