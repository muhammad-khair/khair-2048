from __future__ import annotations

import random
from typing import Any, List, Optional

from src.game.constants import GOAL_NUMBER, GRID_LENGTH, START_COUNT, START_NUMBER


type Board = List[List[Optional[int]]]


class GameBoard:
    def __init__(self, board: Board, goal: int, prop_numbers: List[int]):
        if not board or not board[0]:
            raise ValueError("Board is empty")

        self.__board = board
        self.goal = goal
        self.__prop_numbers = prop_numbers
    @staticmethod
    def create_new(
        grid_length: int = GRID_LENGTH,
        goal_number: int = GOAL_NUMBER,
        starting_count: int = START_COUNT,
        starting_number: int = START_NUMBER,
    ) -> GameBoard:
        board: Board = [
            [None for _ in range(grid_length)]
            for _ in range(grid_length)
        ]

        rng = lambda: random.randint(0, grid_length - 1)
        for _ in range(starting_count):
            r, c = rng(), rng()
            while board[r][c] == starting_number:
                r, c = rng(), rng()
            board[r][c] = starting_number

        return GameBoard(
            board=board,
            goal=goal_number,
            prop_numbers=[starting_number, starting_number * 2],
        )


    def move_left(self) -> None:
        pass

    def move_right(self) -> None:
        pass

    def move_up(self) -> None:
        pass

    def move_down(self) -> None:
        pass

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GameBoard):
            return False
        conditions = (
            self.__board == other.__board,
            self.goal == other.goal,
            self.__prop_numbers == other.__prop_numbers,
        )
        return all(conditions)

    def __str__(self) -> str:
        rows = (
            f"[{', '.join(repr(item) for item in row)}]"
            for row in self.__board
        )
        return "[\n  " + ",\n  ".join(rows) + "\n]"
