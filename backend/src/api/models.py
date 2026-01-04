from typing import List
from pydantic import BaseModel

from src.game.board import Board


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
    provider: str  # e.g., "ollama", "gemini", "heuristic"
    model: str  # e.g., "deepseek", "gemini-2.5-flash", "simple"


class RecommendationResponse(BaseModel):
    """Schema for a recommendation response."""
    suggested_move: str
    rationale: str
    predicted_grid: Board


class ModelInfo(BaseModel):
    """Information about a single model."""
    provider: str  # e.g., "ollama", "gemini", "heuristic"
    model: str  # e.g., "deepseek", "gemini-2.5-flash", "simple"
    display_name: str  # e.g., "Ollama - DeepSeek", "Gemini 2.5 Flash"


class ModelsResponse(BaseModel):
    """Schema for listing available models."""
    models: List[ModelInfo]
