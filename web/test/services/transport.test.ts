import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { ServerTransport } from '../../src/services/transport';
import { Grid } from '../../src/types';

vi.mock('../../src/configs/config', () => ({
    SERVER_HOST: ''
}));

describe('Transport Service', () => {
    // Mock fetch globally
    const fetchMock = vi.fn();
    globalThis.fetch = fetchMock;

    const mockGrid: Grid = [
        [2, null, null, null],
        [null, null, null, null],
        [null, null, null, null],
        [null, null, null, null]
    ];

    beforeEach(() => {
        fetchMock.mockClear();
    });

    afterEach(() => {
        vi.restoreAllMocks();
    });

    describe('startNewGame', () => {
        it('should call /new and return a grid on success', async () => {
            fetchMock.mockResolvedValue({
                ok: true,
                json: async () => mockGrid,
            });

            const result = await ServerTransport.startNewGame();

            expect(fetchMock).toHaveBeenCalledWith('/api/new', { method: 'POST' });
            expect(result).toEqual(mockGrid);
        });

        it('should throw an error when response is not ok', async () => {
            fetchMock.mockResolvedValue({
                ok: false,
                status: 500,
            });

            await expect(ServerTransport.startNewGame()).rejects.toThrow('Request failed with status 500');
        });
    });

    describe('move', () => {
        const mockMoveResponse = {
            grid: mockGrid,
            status: 'ONGOING',
            largest_number: 2,
            turns: 1
        };

        it('should call /move with correct body and return response', async () => {
            fetchMock.mockResolvedValue({
                ok: true,
                json: async () => mockMoveResponse,
            });

            const result = await ServerTransport.move(mockGrid, 'left', 0);

            expect(fetchMock).toHaveBeenCalledWith('/api/move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ grid: mockGrid, direction: 'left', turns: 0 }),
            });
            expect(result).toEqual(mockMoveResponse);
        });
    });

    describe('getRecommendation', () => {
        const mockRecoResponse = {
            suggested_move: 'left',
            rationale: 'Test rationale',
            predicted_grid: mockGrid
        };

        it('should call /recommend with correct body and return response', async () => {
            fetchMock.mockResolvedValue({
                ok: true,
                json: async () => mockRecoResponse,
            });

            const result = await ServerTransport.getRecommendation(mockGrid);

            expect(fetchMock).toHaveBeenCalledWith('/api/recommend', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ grid: mockGrid }),
            });
            expect(result).toEqual(mockRecoResponse);
        });
    });
});
