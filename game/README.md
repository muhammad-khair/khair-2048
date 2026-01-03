# Game Module

Core logic for the 2048 sliding tile game.

## Overview

This module provides the independent engine for the game, handling the 4x4 grid, tile generation, movement rules, and game state validation (Ongoing, Won, Lost).

## Movement Logic

This engine follows the standard 2048 convention: **A move is only valid if it results in a change to the board.**
- If a move (Up, Down, Left, or Right) does not shift any tiles or trigger any merges, the turn counter is not incremented.
- No new random tile is spawned for an invalid (invariant) move.

## Testing

Run unit tests for the game engine:

```bash
# From project root
python -m pytest game/test/
```

## Internal Structure

- `src/board.py`: Contains the `GameBoard` class which is the primary interface.
- `src/status.py`: Defines the `GameStatus` enum.
- `src/constants.py`: Global game settings (Goal number, start numbers, etc.).
