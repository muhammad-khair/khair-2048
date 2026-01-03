import { fireEvent, render, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import App from '../src/App';

describe('2048 React App', () => {
    beforeEach(() => {
        vi.clearAllMocks();

        // Mock successful initialization
        (globalThis.fetch as any) = vi.fn().mockResolvedValue({
            ok: true,
            json: async () => [[2, null, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null]]
        });
    });

    it('renders progress and tiles on initialization', async () => {
        render(<App />);

        // Check for title
        expect(screen.getByText('2048')).toBeInTheDocument();

        // Check for mocked tiles and score
        await waitFor(() => {
            const tiles = screen.getAllByText('2');
            expect(tiles.length).toBeGreaterThan(0);

            // Both Session Best and Current Best should be 2 initially with our mock
            const scores = screen.getAllByText('2', { selector: '.score-value' });
            expect(scores.length).toBe(2);
        });
    });

    it('calls move API when arrow keys are pressed', async () => {
        render(<App />);

        // Wait for initial grid
        await waitFor(() => screen.getAllByText('2'));

        // Mock move response
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                grid: [[null, 2, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null]],
                status: 'ONGOING',
                largest_number: 2,
                turns: 1
            })
        });

        fireEvent.keyDown(window, { key: 'ArrowRight', code: 'ArrowRight' });

        await waitFor(() => {
            expect(globalThis.fetch).toHaveBeenCalledWith('/move', expect.any(Object));
        });
    });

    it('renders the recommend button', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        const recommendButton = screen.getByText('Recommend');
        expect(recommendButton).toBeInTheDocument();
        expect(recommendButton).not.toBeDisabled();
    });

    it('calls recommend API when recommend button is clicked', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // Mock recommend response
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                suggested_move: 'left',
                rationale: 'Moving left consolidates tiles.',
                predicted_grid: [[4, null, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null]]
            })
        });

        const recommendButton = screen.getByText('Recommend');
        fireEvent.click(recommendButton);

        await waitFor(() => {
            expect(globalThis.fetch).toHaveBeenCalledWith('/recommend', expect.objectContaining({
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            }));
        });
    });

    it('displays loading state when recommendation is in progress', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // Mock a delayed response
        (globalThis.fetch as any).mockImplementation(() =>
            new Promise(resolve => setTimeout(() => resolve({
                ok: true,
                json: async () => ({
                    suggested_move: 'left',
                    rationale: 'Moving left consolidates tiles.',
                    predicted_grid: [[4, null, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null]]
                })
            }), 100))
        );

        const recommendButton = screen.getByText('Recommend');
        fireEvent.click(recommendButton);

        // Check for loading state
        await waitFor(() => {
            expect(screen.getByText('...')).toBeInTheDocument();
        });
    });

    it('displays recommendation result with rationale and mini-grid', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // Mock recommend response
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                suggested_move: 'left',
                rationale: 'Moving left consolidates tiles.',
                predicted_grid: [[4, null, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null]]
            })
        });

        const recommendButton = screen.getByText('Recommend');
        fireEvent.click(recommendButton);

        await waitFor(() => {
            expect(screen.getByText('LEFT')).toBeInTheDocument();
            expect(screen.getByText('"Moving left consolidates tiles."')).toBeInTheDocument();
            expect(screen.getByText('Suggested')).toBeInTheDocument();
        });
    });

    it('clears recommendation when a move is made', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // First, get a recommendation
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                suggested_move: 'left',
                rationale: 'Moving left consolidates tiles.',
                predicted_grid: [[4, null, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null]]
            })
        });

        const recommendButton = screen.getByText('Recommend');
        fireEvent.click(recommendButton);

        await waitFor(() => {
            expect(screen.getByText('LEFT')).toBeInTheDocument();
        });

        // Now make a move
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                grid: [[null, 2, null, null], [null, null, null, null], [null, null, null, null], [null, null, null, null]],
                status: 'ONGOING',
                largest_number: 2,
                turns: 1
            })
        });

        fireEvent.keyDown(window, { key: 'ArrowRight', code: 'ArrowRight' });

        await waitFor(() => {
            expect(screen.queryByText('LEFT')).not.toBeInTheDocument();
        });
    });

    it('disables recommend button when game is over', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // Simulate game over
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                grid: [[2, 4, 2, 4], [4, 2, 4, 2], [2, 4, 2, 4], [4, 2, 4, 2]],
                status: 'LOSE',
                largest_number: 4,
                turns: 10
            })
        });

        fireEvent.keyDown(window, { key: 'ArrowRight', code: 'ArrowRight' });

        await waitFor(() => {
            const recommendButton = screen.getByText('Recommend');
            expect(recommendButton).toBeDisabled();
        });
    });

    it('displays win overlay when player reaches 2048', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // Simulate winning move
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                grid: [[2048, 1024, 512, 256], [128, 64, 32, 16], [8, 4, 2, null], [null, null, null, null]],
                status: 'WIN',
                largest_number: 2048,
                turns: 150
            })
        });

        fireEvent.keyDown(window, { key: 'ArrowLeft', code: 'ArrowLeft' });

        await waitFor(() => {
            expect(screen.getByText('You win!')).toBeInTheDocument();
            expect(screen.getByText('Total turns: 150')).toBeInTheDocument();
        });
    });

    it('displays lose overlay when no moves are available', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // Simulate losing move
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                grid: [[2, 4, 8, 16], [32, 64, 128, 256], [512, 1024, 2, 4], [8, 16, 32, 64]],
                status: 'LOSE',
                largest_number: 1024,
                turns: 200
            })
        });

        fireEvent.keyDown(window, { key: 'ArrowUp', code: 'ArrowUp' });

        await waitFor(() => {
            expect(screen.getByText('Game over!')).toBeInTheDocument();
            expect(screen.getByText('Total turns: 200')).toBeInTheDocument();
        });
    });

    it('allows restarting the game from win overlay', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // Simulate winning
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                grid: [[2048, 1024, 512, 256], [128, 64, 32, 16], [8, 4, 2, null], [null, null, null, null]],
                status: 'WIN',
                largest_number: 2048,
                turns: 150
            })
        });

        fireEvent.keyDown(window, { key: 'ArrowLeft', code: 'ArrowLeft' });

        await waitFor(() => {
            expect(screen.getByText('You win!')).toBeInTheDocument();
        });

        // Mock new game response
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => [[2, null, null, null], [null, 2, null, null], [null, null, null, null], [null, null, null, null]]
        });

        // Click "New Game" button in overlay
        const newGameButtons = screen.getAllByText('New Game');
        const overlayButton = newGameButtons.find(btn => btn.className === 'retry-button');
        fireEvent.click(overlayButton!);

        await waitFor(() => {
            expect(screen.queryByText('You win!')).not.toBeInTheDocument();
            expect(globalThis.fetch).toHaveBeenCalledWith('/new', expect.any(Object));
        });
    });

    it('allows restarting the game from lose overlay', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // Simulate losing
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                grid: [[2, 4, 8, 16], [32, 64, 128, 256], [512, 1024, 2, 4], [8, 16, 32, 64]],
                status: 'LOSE',
                largest_number: 1024,
                turns: 200
            })
        });

        fireEvent.keyDown(window, { key: 'ArrowUp', code: 'ArrowUp' });

        await waitFor(() => {
            expect(screen.getByText('Game over!')).toBeInTheDocument();
        });

        // Mock new game response
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => [[2, null, null, null], [null, 2, null, null], [null, null, null, null], [null, null, null, null]]
        });

        // Click "New Game" button in overlay
        const newGameButtons = screen.getAllByText('New Game');
        const overlayButton = newGameButtons.find(btn => btn.className === 'retry-button');
        fireEvent.click(overlayButton!);

        await waitFor(() => {
            expect(screen.queryByText('Game over!')).not.toBeInTheDocument();
            expect(globalThis.fetch).toHaveBeenCalledWith('/new', expect.any(Object));
        });
    });

    it('disables keyboard controls when game is won', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // Simulate winning
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                grid: [[2048, 1024, 512, 256], [128, 64, 32, 16], [8, 4, 2, null], [null, null, null, null]],
                status: 'WIN',
                largest_number: 2048,
                turns: 150
            })
        });

        fireEvent.keyDown(window, { key: 'ArrowLeft', code: 'ArrowLeft' });

        await waitFor(() => {
            expect(screen.getByText('You win!')).toBeInTheDocument();
        });

        // Clear mock calls
        vi.clearAllMocks();

        // Try to make another move
        fireEvent.keyDown(window, { key: 'ArrowRight', code: 'ArrowRight' });

        // Should not call the move API
        await waitFor(() => {
            expect(globalThis.fetch).not.toHaveBeenCalled();
        });
    });

    it('disables keyboard controls when game is lost', async () => {
        render(<App />);

        await waitFor(() => screen.getAllByText('2'));

        // Simulate losing
        (globalThis.fetch as any).mockResolvedValue({
            ok: true,
            json: async () => ({
                grid: [[2, 4, 8, 16], [32, 64, 128, 256], [512, 1024, 2, 4], [8, 16, 32, 64]],
                status: 'LOSE',
                largest_number: 1024,
                turns: 200
            })
        });

        fireEvent.keyDown(window, { key: 'ArrowUp', code: 'ArrowUp' });

        await waitFor(() => {
            expect(screen.getByText('Game over!')).toBeInTheDocument();
        });

        // Clear mock calls
        vi.clearAllMocks();

        // Try to make another move
        fireEvent.keyDown(window, { key: 'ArrowDown', code: 'ArrowDown' });

        // Should not call the move API
        await waitFor(() => {
            expect(globalThis.fetch).not.toHaveBeenCalled();
        });
    });
});
