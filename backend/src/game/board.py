from __future__ import annotations

import random
from copy import deepcopy
from typing import Any, List, Optional, Tuple

from src.config.settings import SETTINGS
from src.game.status import GameStatus

Board = List[List[Optional[int]]]
Coord = Tuple[int, int]


class GameBoardException(Exception):
    """Raised when an invalid operation is performed on the game board."""

    pass


class GameBoard:
    """
    Represents the state and behaviour of a grid-based number-merging game.

    The board maintains the current grid, game goal, possible numbers that
    may be spawned, and the number of turns taken.
    """

    def __init__(
        self,
        board: Board,
        goal: int,
        prop_numbers: List[int],
        turns: int = 0,
    ):
        """
        Create a game board with an existing grid state.

        Args:
            board: A 2D grid representing the board. Each cell contains either
                an integer value or ``None`` if empty.
            goal: The target number required to win the game.
            prop_numbers: Possible numbers that may be spawned after a move.
            turns: Number of turns already taken.

        Raises:
            ValueError: If the provided board is empty or malformed.
        """
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
        grid_length: int = SETTINGS.game.grid_length,
        goal_number: int = SETTINGS.game.goal_number,
        min_starting_count: int = SETTINGS.game.min_start_count,
        max_starting_count: int = SETTINGS.game.max_start_count,
        starting_number: int = SETTINGS.game.start_number,
    ) -> GameBoard:
        """
        Create a new game board with a fresh grid and randomly placed
        starting numbers.

        Args:
            grid_length: Width and height of the square grid.
            goal_number: Target number required to win the game.
            max_starting_count: Maximum number of starting tiles to place.
            min_starting_count: Minimum number of starting tiles to place.
            starting_number: Value of each starting tile.

        Returns:
            GameBoard: A newly initialised game board.
        """
        board: Board = [
            [None for _ in range(grid_length)]
            for _ in range(grid_length)
        ]

        starting_count = random.randint(min_starting_count, max_starting_count)
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

    def get_board(self) -> Board:
        """
        Return a deep copy of the current board state.

        Returns:
            Board: A copy of the internal grid.
        """
        return deepcopy(self.__board)

    def status(self) -> GameStatus:
        """
        Compute the current game status.

        Returns:
            GameStatus:
                - WIN if the goal number has been reached,
                - ONGOING if further moves are possible,
                - LOSE otherwise.
        """
        if self.largest_number() == self.goal:
            return GameStatus.WIN
        if self.__is_still_able_to_move():
            return GameStatus.ONGOING
        return GameStatus.LOSE

    def largest_number(self) -> int:
        """
        Get the largest number currently on the board.

        Returns:
            int: The maximum tile value.
        """
        max_row_scores = [
            max(cell if cell else 0 for cell in row) for row in self.__board
        ]
        return max(max_row_scores)

    def move_left(self) -> None:
        """Move all tiles left according to game rules."""
        coord_groups_to_move = [
            [(r, c) for c in range(self.__cols)]
            for r in range(self.__rows)
        ]
        self.__move(coord_groups_to_move)

    def move_right(self) -> None:
        """Move all tiles right according to game rules."""
        coord_groups_to_move = [
            [(r, c) for c in reversed(range(self.__cols))]
            for r in range(self.__rows)
        ]
        self.__move(coord_groups_to_move)

    def move_up(self) -> None:
        """Move all tiles upward according to game rules."""
        coord_groups_to_move = [
            [(r, c) for r in range(self.__rows)]
            for c in range(self.__cols)
        ]
        self.__move(coord_groups_to_move)

    def move_down(self) -> None:
        """Move all tiles downward according to game rules."""
        coord_groups_to_move = [
            [(r, c) for r in reversed(range(self.__rows))]
            for c in range(self.__cols)
        ]
        self.__move(coord_groups_to_move)

    def __move(self, coord_groups: List[List[Coord]]) -> None:
        """
        Execute a move across multiple coordinate groups.

        Each group represents a row or column to be migrated in order.
        After a successful move, the turn counter is incremented and a
        new number is inserted. If a move does not result in any changes,
        the move is aborted.

        Args:
            coord_groups: Groups of ordered coordinates defining the move.

        Raises:
            GameBoardException: If the game is already in a terminal state.
        """
        if self.status().is_terminal:
            raise GameBoardException(f"Unable to move, status is {self.status()}")

        backup_board = self.get_board()
        for coords in coord_groups:
            self.__migrate_numbers_inwards(coords)

        if backup_board == self.get_board():
            return

        self.turns += 1
        self.__insert_number_into_random_space()

    def __migrate_numbers_inwards(self, coords: List[Coord]) -> None:
        """
        Shift and merge numbers along a single ordered line of coordinates.

        Numbers are moved towards the start of the coordinate list, merging
        adjacent equal values once per move according to game rules.
        """
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

    def __is_still_able_to_move(self) -> bool:
        if not self.__is_full():
            return True

        for r, row in enumerate(self.__board):
            for c in range(len(row)):
                cell_value = self.__board[r][c]
                neighbours = self.__get_neighbouring_coords((r, c))
                neighbour_values = [
                    self.__board[neighbour_r][neighbour_c]
                    for (neighbour_r, neighbour_c) in neighbours
                ]
                if neighbour_values.count(cell_value) > 0:
                    return True
        return False

    def __get_empty_coords(self) -> List[Coord]:
        free_coords: List[Coord] = []
        for r, row in enumerate(self.__board):
            for c in range(len(row)):
                if not self.__board[r][c]:
                    free_coords.append((r, c))
        return free_coords

    def __is_full(self) -> bool:
        return not self.__get_empty_coords()

    def __get_neighbouring_coords(self, coord: Coord) -> List[Coord]:
        r, c = coord
        directions = [
            (1, 0),
            (-1 , 0),
            (0, 1),
            (0, -1)
        ]
        neighbour_coords: List[Coord] = []
        for dr, dc in directions:
            next_r = r + dr
            next_c = c + dc
            if 0 <= next_r < self.__rows and 0 <= next_c < self.__cols:
                neighbour_coords.append((next_r, next_c))
        return neighbour_coords

    def __get_next_populated_coord(self, coords: List[Coord]) -> Optional[Coord]:
        for coord in coords:
            idx_row, idx_col = coord
            if self.__board[idx_row][idx_col]:
                return coord
        return None

    def __insert_number_into_random_space(self) -> None:
        free_slots = self.__get_empty_coords()
        if not free_slots or not self.__prop_numbers:
            return
        next_number = random.choice(self.__prop_numbers)
        r, c = random.choice(free_slots)
        self.__board[r][c] = next_number

    def __copy__(self) -> GameBoard:
        return GameBoard(
            board=deepcopy(self.__board),
            goal=self.goal,
            prop_numbers=deepcopy(self.__prop_numbers),
            turns=self.turns,
        )

    def __deepcopy__(self, memo: Any)-> GameBoard:
        return self.__copy__()

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
            "[" + ", ".join(str(item) for item in row) + "]"
            for row in self.__board
        )
        return "[\n  " + ",\n  ".join(rows) + "\n]"

    def __repr__(self) -> str:
        states = (
            f"status = {self.status()}",
            f"largest_number = {self.largest_number()}",
            f"turns = {self.turns}",
        )
        title = "GameBoard[" + ", ".join(states) + "]"
        return f"{title}\n{self}"
