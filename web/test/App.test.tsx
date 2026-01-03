import {fireEvent, render, screen, waitFor} from '@testing-library/react';
import {beforeEach, describe, expect, it, vi} from 'vitest';
import App from '../src/App';
import React from 'react';

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

        // Check for mocked tiles
        await waitFor(() => {
            const tiles = screen.getAllByText('2');
            expect(tiles.length).toBeGreaterThan(0);
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
                largest_number: 2
            })
        });

        fireEvent.keyDown(window, { key: 'ArrowRight', code: 'ArrowRight' });

        await waitFor(() => {
            expect(globalThis.fetch).toHaveBeenCalledWith('/move', expect.any(Object));
        });
    });
});
