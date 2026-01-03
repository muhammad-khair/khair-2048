# Game Module

Core logic for the 2048 sliding tile game.

## Overview

This module provides the independent engine for the game, handling the 4x4 grid, tile generation, movement rules, and game state validation (Ongoing, Won, Lost).

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
