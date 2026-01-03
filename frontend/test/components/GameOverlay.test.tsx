import { fireEvent, render, screen } from '@testing-library/react';
import { GameOverlay } from '../../src/components/GameOverlay';
import { vi } from 'vitest';

describe('GameOverlay Component', () => {
    const onRestartMock = vi.fn();

    test('renders Win state correctly', () => {
        render(<GameOverlay status="WIN" turns={42} onRestart={onRestartMock} />);

        expect(screen.getByText('You win!')).toBeInTheDocument();
        expect(screen.getByText('Total turns: 42')).toBeInTheDocument();
        expect(screen.getByTestId('game-overlay')).toHaveClass('game-won');
    });

    test('renders Lose state correctly', () => {
        render(<GameOverlay status="LOSE" turns={100} onRestart={onRestartMock} />);

        expect(screen.getByText('Game over!')).toBeInTheDocument();
        expect(screen.getByText('Total turns: 100')).toBeInTheDocument();
        expect(screen.getByTestId('game-overlay')).toHaveClass('game-over');
    });

    test('calls onRestart when button clicked', () => {
        render(<GameOverlay status="LOSE" turns={10} onRestart={onRestartMock} />);

        const button = screen.getByText('New Game');
        fireEvent.click(button);
        expect(onRestartMock).toHaveBeenCalledTimes(1);
    });
});
