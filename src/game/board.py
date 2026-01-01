from __future__ import annotations

import random
from typing import Any, List, Optional, Tuple

from src.game.constants import GOAL_NUMBER, GRID_LENGTH, START_COUNT, START_NUMBER


type Board = List[List[Optional[int]]]
type Coord = Tuple[int, int]


class GameBoard:
    def __init__(
        self,
        board: Board,
        goal: int,
        prop_numbers: List[int],
        turns: int = 0,
    ):
        if not board or not board[0]:
            raise ValueError("Board is empty")

        self.__board = board
        self.goal = goal
        self.__prop_numbers = prop_numbers
        self.turns = turns

        self.__rows = len(board)
        self.__cols = len(board[0])

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

    def __get_next_populated_coord(self, coords: List[Coord]) -> Optional[Coord]:
        for coord in coords:
            idx_row, idx_col = coord
            if self.__board[idx_row][idx_col]:
                return coord
        return None

    def __migrate_numbers_inwards(self, coords: List[Coord]) -> None:
        reference_index = 0
        while reference_index < len(coords):
            row, col = coords[reference_index]
            if self.__board[row][col] is None:
                cursor = self.__get_next_populated_coord(coords[reference_index:])
                if cursor is None:
                    break
                cursor_row, cursor_col = cursor
                self.__board[row][col] = self.__board[cursor_row][cursor_col]
                self.__board[cursor_row][cursor_col] = None

            cursor = self.__get_next_populated_coord(coords[reference_index + 1:])
            if cursor is None:
                break
            cursor_row, cursor_col = cursor
            if self.__board[row][col] == self.__board[cursor_row][cursor_col]:
                self.__board[row][col] += self.__board[cursor_row][cursor_col]
                self.__board[cursor_row][cursor_col] = None
            reference_index += 1

    def move_left(self) -> None:
        pass
        for r in range(self.__rows):
            coords = [(r, c) for c in range(self.__cols)]
            self.__migrate_numbers_inwards(coords)

        self.turns += 1

    def move_right(self) -> None:
        pass
        for r in range(self.__rows):
            coords = [(r, c) for c in reversed(range(self.__cols))]
            self.__migrate_numbers_inwards(coords)

        self.turns += 1

    def move_up(self) -> None:
        pass
        for c in range(self.__cols):
            coords = [(r, c) for r in range(self.__rows)]
            self.__migrate_numbers_inwards(coords)

        self.turns += 1

    def move_down(self) -> None:
        pass
        for c in range(self.__cols):
            coords = [(r, c) for r in reversed(range(self.__rows))]
            self.__migrate_numbers_inwards(coords)

        self.turns += 1

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, GameBoard):
            return False
        conditions = (
            self.__board == other.__board,
            self.goal == other.goal,
            self.__prop_numbers == other.__prop_numbers,
            self.turns == other.turns,
        )
        return all(conditions)

    def __str__(self) -> str:
        rows = (
            f"[{', '.join(repr(item) for item in row)}]"
            for row in self.__board
        )
        return "[\n  " + ",\n  ".join(rows) + "\n]"
