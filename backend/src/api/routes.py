from fastapi import APIRouter, HTTPException, Request

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


from src.config.limiter import limiter

router = APIRouter()


@router.post("/new", response_model=Board)
@limiter.limit(SETTINGS.rate_limit.new_game)
async def new_game(request: Request):
    """
    Initialize a new game and return the starting grid.
    """
    game = GameBoard.create_new()
    return game.get_board()


@router.get("/models", response_model=ModelsResponse)
@limiter.limit(SETTINGS.rate_limit.models)
async def list_models(request: Request):
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
@limiter.limit(SETTINGS.rate_limit.move)
async def move(request: Request, move_request: MoveRequest):
    """
    Process a move based on the provided grid and direction.
    
    This endpoint is stateless. It reconstructs the game state from the 
    provided grid, performs the move, and returns the result.
    """
    # Reconstruct game state from the client-provided grid
    game = GameBoard(
        board=move_request.grid,
        goal=SETTINGS.game.goal_number,
        prop_numbers=[SETTINGS.game.start_number, SETTINGS.game.start_number * 2],
        turns=move_request.turns
    )
    
    try:
        direction = Direction(move_request.direction.lower())
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
@limiter.limit(SETTINGS.rate_limit.recommend)
async def recommend(request: Request, rec_request: RecommendationRequest):
    """
    Get a move recommendation using the specified model.
    """
    result = RecommendationService.get_recommendation(
        grid=rec_request.grid,
        provider=rec_request.provider,
        model=rec_request.model
    )
    
    return RecommendationResponse(
        suggested_move=result.suggested_move,
        rationale=result.rationale,
        predicted_grid=result.predicted_grid
    )
