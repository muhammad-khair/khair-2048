from __future__ import annotations

from enum import Enum

from src.game.board import GameBoard


class Direction(str, Enum):
    """
    Enum representing the four possible move directions in the game.
    Inherits from str to allow direct JSON serialization.
    """
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"

    def apply_to_board(self, board: GameBoard) -> None:
        """
        Apply this direction's move to the given board.
        
        Args:
            board: GameBoard instance to move
        """
        if self == Direction.UP:
            board.move_up()
        elif self == Direction.DOWN:
            board.move_down()
        elif self == Direction.LEFT:
            board.move_left()
        elif self == Direction.RIGHT:
            board.move_right()
