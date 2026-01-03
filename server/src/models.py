from pydantic import BaseModel

from game.src.board import Board


class MoveRequest(BaseModel):
    """Schema for a move request containing the current grid and direction."""
    grid: Board
    direction: str
    turns: int


class MoveResponse(BaseModel):
    """Schema for a move response containing the new grid, status, best tile, and turn count."""
    grid: Board
    status: str
    largest_number: int
    turns: int


class RecommendationRequest(BaseModel):
    """Schema for a recommendation request."""
    grid: Board


class RecommendationResponse(BaseModel):
    """Schema for a recommendation response."""
    suggested_move: str
    rationale: str
    predicted_grid: Board
