import { Grid, MoveResponse, RecommendationResponse, ModelsResponse } from '../types';
import { SERVER_HOST } from '../configs/config';

export class ApiError extends Error {
    constructor(
        public status: number,
        message: string
    ) {
        super(message);
        this.name = 'ApiError';
        // Essential for proper prototype chain inheritance in some environments
        Object.setPrototypeOf(this, ApiError.prototype);
    }
}

const handleResponse = async <T>(response: Response): Promise<T> => {
    if (!response.ok) {
        let errorMessage = `Request failed with status ${response.status}`;

        try {
            const errorBody = await response.json();
            // Try different common error fields
            errorMessage = errorBody.error || errorBody.detail || errorBody.message || errorMessage;

            // If it's an object (like {"error": {"message": "..."}}), stringify it or dig deeper
            if (typeof errorMessage === 'object') {
                errorMessage = JSON.stringify(errorMessage);
            }
        } catch (_error) {
            // Failed to parse JSON, stick to status text
        }

        throw new ApiError(response.status, errorMessage);
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

    listModels: async (): Promise<ModelsResponse> => {
        const response = await fetch(`${SERVER_HOST}/api/models`, {
            method: 'GET',
        });
        return handleResponse<ModelsResponse>(response);
    },

    getRecommendation: async (
        grid: Grid,
        provider: string,
        model: string
    ): Promise<RecommendationResponse> => {
        const response = await fetch(`${SERVER_HOST}/api/recommend`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ grid, provider, model }),
        });
        return handleResponse<RecommendationResponse>(response);
    },
};
