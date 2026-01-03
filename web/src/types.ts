export type Grid = (number | null)[][];
export type Status = 'ONGOING' | 'WIN' | 'LOSE';

export interface MoveResponse {
    grid: Grid;
    status: Status;
    largest_number: number;
    turns: number;
}

export interface RecommendationResponse {
    suggested_move: string;
    rationale: string;
    predicted_grid: Grid;
}
