import { fireEvent, render, screen } from '@testing-library/react';
import { Header } from '../../src/components/Header';
import { vi } from 'vitest';

describe('Header Component', () => {
    const onNewGameMock = vi.fn();

    test('renders scores correctly', () => {
        render(<Header currentBest={100} sessionBest={500} onNewGame={onNewGameMock} />);

        expect(screen.getByText('SESSION BEST')).toBeInTheDocument();
        expect(screen.getByText('500')).toBeInTheDocument();
        expect(screen.getByText('CURRENT BEST')).toBeInTheDocument();
        expect(screen.getByText('100')).toBeInTheDocument();
    });

    test('calls onNewGame when button clicked', () => {
        render(<Header currentBest={0} sessionBest={0} onNewGame={onNewGameMock} />);

        const button = screen.getByText('New Game');
        fireEvent.click(button);
        expect(onNewGameMock).toHaveBeenCalledTimes(1);
    });
});
