import { Grid, MoveResponse, RecommendationResponse } from '../types';
import { SERVER_HOST } from '../configs/config';

const handleResponse = async <T>(response: Response): Promise<T> => {
    if (!response.ok) {
        throw new Error(`Request failed with status ${response.status}`);
    }
    return response.json();
};

export const ServerTransport = {
    startNewGame: async (): Promise<Grid> => {
        const response = await fetch(`${SERVER_HOST}/api/new`, {
            method: 'POST',
        });
        return handleResponse<Grid>(response);
    },

    move: async (grid: Grid, direction: string, turns: number): Promise<MoveResponse> => {
        const response = await fetch(`${SERVER_HOST}/api/move`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ grid, direction, turns }),
        });
        return handleResponse<MoveResponse>(response);
    },

    getRecommendation: async (grid: Grid): Promise<RecommendationResponse> => {
        const response = await fetch(`${SERVER_HOST}/api/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ grid }),
        });
        return handleResponse<RecommendationResponse>(response);
    },
};
