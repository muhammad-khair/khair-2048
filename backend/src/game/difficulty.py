from __future__ import annotations

from enum import Enum


class Difficulty(str, Enum):
    """
    Enum representing the four possible move directions in the game.
    Inherits from str to allow direct JSON serialization.
    """
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"

    def get_boulder_count(self) -> int:
        if self == Difficulty.EASY:
            return 0
        elif self == Difficulty.MEDIUM:
            return 1
        elif self == Difficulty.HARD:
            return 2
        else:
            raise ValueError("Invalid difficulty")
