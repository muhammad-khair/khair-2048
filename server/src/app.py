import os

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from game.src.board import GameBoard, Board
from game.src.constants import GOAL_NUMBER, START_NUMBER

app = FastAPI(title="2048 Game API")

# Setup static file serving for the React frontend
current_dir = os.path.dirname(os.path.abspath(__file__))
# Path to the React build directory (now in root ./web/dist)
static_dir = os.path.abspath(os.path.join(current_dir, "../../web/dist"))

# Mount assets directory (Vite puts them there)
assets_dir = os.path.join(static_dir, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


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


@app.post("/new", response_model=Board)
async def new_game():
    """
    Initialize a new game and return the starting grid.
    """
    game = GameBoard.create_new()
    return game.get_board()


@app.post("/move", response_model=MoveResponse)
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


@app.get("/")
async def read_index():
    """
    Serve the main index.html file for the game frontend.
    """
    return FileResponse(os.path.join(static_dir, "index.html"))
