import { render, screen } from '@testing-library/react';
import { Tile } from '../../src/components/Tile';
import '@testing-library/jest-dom';

describe('Tile Component', () => {
    test('renders with correct value and classes', () => {
        render(<Tile value={2} row={0} col={0} />);

        const tileElement = screen.getByTestId('tile-0-0');
        expect(tileElement).toHaveTextContent('2');
        expect(tileElement).toHaveClass('tile');
        expect(tileElement).toHaveClass('tile-2');
        expect(tileElement).toHaveClass('tile-position-1-1');
    });

    test('renders large values correctly', () => {
        render(<Tile value={2048} row={3} col={3} />);

        const tileElement = screen.getByTestId('tile-3-3');
        expect(tileElement).toHaveTextContent('2048');
        expect(tileElement).toHaveClass('tile-2048');
        expect(tileElement).toHaveClass('tile-position-4-4');
    });
});
