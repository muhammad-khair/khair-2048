import React from 'react';
import { Grid as GridType } from '../types';
import { Tile } from './Tile';

interface GridProps {
    grid: GridType | null;
    id?: string;
    className?: string;
}

export const Grid: React.FC<GridProps> = ({ grid, id = "grid-container", className = "grid-container" }) => {
    return (
        <div id={id} className={className} data-testid="grid-container">
            {[...Array(16)].map((_, i) => (
                <div key={i} className="grid-cell" data-testid="grid-cell" />
            ))}

            <div className="tile-container">
                {grid && grid.map((row, r) =>
                    row.map((val, c) =>
                        val !== null && <Tile key={`${r}-${c}`} value={val} row={r} col={c} />
                    )
                )}
            </div>
        </div>
    );
};
