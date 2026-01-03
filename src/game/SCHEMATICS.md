# Game Logic Schematic

This module handles the core game mechanics of the grid game.

## Core Components
- **`GameBoard`**: Main class in `src/game/board.py`. Responsible for:
    - Initializing an empty or existing grid.
    - Implementing the 2048 movement rules (migrate inward, merge matching tiles).
    - Spawning new tiles in random empty slots.
    - Determining game status (Win/Lose/Ongoing).
- **`GameStatus`**: Enum in `src/game/status.py` defining the win/loss/ongoing states.
- **`Constants`**: Global settings in `src/game/constants.py` (e.g., `GRID_LENGTH`, `GOAL_NUMBER`).

## Logic Rules
1. **Movement**: All tiles shift toward the specified direction.
2. **Merging**: Two tiles of the same value merge into one (doubling the value) if they collide during movement. Merging only happens once per tile per move.
3. **Spawning**: After a successful move (one that changed the board state), a new tile (usually 2 or 4) appears in a random empty cell.
4. **Termination**: 
    - **Win**: A tile reaches the `GOAL_NUMBER`.
    - **Lose**: The grid is full and no more merges are possible.
