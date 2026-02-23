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

    test('renders difficulty selector with default value', () => {
        render(<Header currentBest={0} sessionBest={0} onNewGame={onNewGameMock} />);

        const select = screen.getByDisplayValue('Easy');
        expect(select).toBeInTheDocument();
    });

    test('renders all difficulty options', () => {
        render(<Header currentBest={0} sessionBest={0} onNewGame={onNewGameMock} />);

        expect(screen.getByText('Easy')).toBeInTheDocument();
        expect(screen.getByText('Medium')).toBeInTheDocument();
        expect(screen.getByText('Hard')).toBeInTheDocument();
    });

    test('calls onDifficultyChange when difficulty is changed', () => {
        const onDifficultyChangeMock = vi.fn();
        render(
            <Header 
                currentBest={0} 
                sessionBest={0} 
                onNewGame={onNewGameMock} 
                onDifficultyChange={onDifficultyChangeMock}
            />
        );

        const select = screen.getByDisplayValue('Easy');
        fireEvent.change(select, { target: { value: 'HARD' } });
        
        expect(onDifficultyChangeMock).toHaveBeenCalledWith('HARD');
    });

    test('displays passed difficulty value', () => {
        render(
            <Header 
                currentBest={0} 
                sessionBest={0} 
                onNewGame={onNewGameMock} 
                difficulty="MEDIUM"
            />
        );

        expect(screen.getByDisplayValue('Medium')).toBeInTheDocument();
    });
});
