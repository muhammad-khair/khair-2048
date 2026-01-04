from fastapi import APIRouter, HTTPException

from src.game.board import GameBoard
from src.config.settings import SETTINGS
from src.game.direction import Direction
from src.recommendation.registry import registry
from src.recommendation.service import RecommendationService
from src.api.models import (
    MoveRequest,
    MoveResponse,
    RecommendationRequest,
    RecommendationResponse,
    ModelsResponse,
    ModelInfo,
    Board
)

router = APIRouter()


@router.post("/new", response_model=Board)
async def new_game():
    """
    Initialize a new game and return the starting grid.
    """
    game = GameBoard.create_new()
    return game.get_board()


@router.get("/models", response_model=ModelsResponse)
async def list_models():
    """
    List all available recommendation models from the registry.
    """
    models = registry.list_models()
    # Convert registry ModelInfo to API ModelInfo
    api_models = [
        ModelInfo(
            provider=m.provider,
            model=m.model,
            display_name=m.display_name
        )
        for m in models
    ]
    return ModelsResponse(models=api_models)


@router.post("/move", response_model=MoveResponse)
async def move(request: MoveRequest):
    """
    Process a move based on the provided grid and direction.
    
    This endpoint is stateless. It reconstructs the game state from the 
    provided grid, performs the move, and returns the result.
    """
    # Reconstruct game state from the client-provided grid
    game = GameBoard(
        board=request.grid,
        goal=SETTINGS.game.goal_number,
        prop_numbers=[SETTINGS.game.start_number, SETTINGS.game.start_number * 2],
        turns=request.turns
    )
    
    try:
        direction = Direction(request.direction.lower())
        direction.apply_to_board(game)
    except ValueError:
        raise HTTPException(
            status_code=400, 
            detail="Invalid direction. Use up, down, left, or right."
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return MoveResponse(
        grid=game.get_board(),
        status=game.status().name,
        largest_number=game.largest_number(),
        turns=game.turns
    )


@router.post("/recommend", response_model=RecommendationResponse)
async def recommend(request: RecommendationRequest):
    """
    Get a move recommendation using the specified model.
    """
    result = RecommendationService.get_recommendation(
        grid=request.grid,
        provider=request.provider,
        model=request.model
    )
    
    return RecommendationResponse(
        suggested_move=result.suggested_move,
        rationale=result.rationale,
        predicted_grid=result.predicted_grid
    )
