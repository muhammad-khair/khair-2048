from copy import deepcopy

from fastapi import APIRouter, HTTPException

from src.game.board import GameBoard
from src.game.constants import GOAL_NUMBER, START_NUMBER
from src.recommendation.factory import get_recommender
from src.api.models import MoveRequest, MoveResponse, RecommendationRequest, RecommendationResponse, Board

router = APIRouter()
recommender = get_recommender()

@router.post("/new", response_model=Board)
async def new_game():
    """
    Initialize a new game and return the starting grid.
    """
    game = GameBoard.create_new()
    return game.get_board()


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
        goal=GOAL_NUMBER,
        prop_numbers=[START_NUMBER, START_NUMBER * 2],
        turns=request.turns
    )
    
    direction = request.direction.lower()
    
    try:
        if direction == "up":
            game.move_up()
        elif direction == "down":
            game.move_down()
        elif direction == "left":
            game.move_left()
        elif direction == "right":
            game.move_right()
        else:
            raise HTTPException(
                status_code=400, 
                detail="Invalid direction. Use up, down, left, or right."
            )
    except Exception as e:
        # Handle cases like terminal game states where moves are invalid
        raise HTTPException(status_code=400, detail=str(e))

    return MoveResponse(
        grid=game.get_board(),
        status=game.status().name,
        largest_number=game.largest_number(),
        turns=game.turns
    )


@router.post("/recommend", response_model=RecommendationResponse)
async def recommend(request: RecommendationRequest):
    """
    Get a move recommendation and rationale based on the current board state.
    """
    suggested_move, rationale = recommender.suggest_move(request.grid)
    
    # Simulate the suggested move to show predicted result
    game = GameBoard(
        board=request.grid,
        goal=GOAL_NUMBER,
        prop_numbers=[],
    )
    sim_board = deepcopy(game)
    
    try:
        if suggested_move == "up":
            sim_board.move_up()
        elif suggested_move == "down":
            sim_board.move_down()
        elif suggested_move == "left":
            sim_board.move_left()
        elif suggested_move == "right":
            sim_board.move_right()
    except:
        pass # Invariant moves are fine for simulation
        
    return RecommendationResponse(
        suggested_move=suggested_move,
        rationale=rationale,
        predicted_grid=sim_board.get_board()
    )
