import { render, screen } from '@testing-library/react';
import { Grid } from '../../src/components/Grid';
import { Grid as GridType } from '../../src/types';

describe('Grid Component', () => {
    const mockGrid: GridType = [
        [2, null, null, null],
        [null, 4, null, null],
        [null, null, 8, null],
        [null, null, null, 16]
    ];

    test('renders 16 background cells', () => {
        render(<Grid grid={null} />);
        const cells = screen.getAllByTestId('grid-cell');
        expect(cells).toHaveLength(16);
    });

    test('renders tiles from grid prop', () => {
        render(<Grid grid={mockGrid} />);

        expect(screen.getByText('2')).toBeInTheDocument();
        expect(screen.getByText('4')).toBeInTheDocument();
        expect(screen.getByText('8')).toBeInTheDocument();
        expect(screen.getByText('16')).toBeInTheDocument();
    });

    test('renders no tiles when grid is null', () => {
        render(<Grid grid={null} />);
        // tile-container should be empty (no Tile components)
        // We can check that no text is rendered or query by tile testid if we knew them
        // But since we didn't mock Tile, it runs full Tile code.
        // Tile produces 'tile-X-Y' testids.
        const tiles = screen.queryAllByTestId(/tile-\d-\d/);
        expect(tiles).toHaveLength(0);
    });
});
