from typing import List, Optional


type Board = List[List[Optional[int]]]


class GameBoard:
    def __init__(self, board: Board, goal: int, prop_numbers: List[int]):
        if not board or not board[0]:
            raise ValueError("Board is empty")

        self.__board = board
        self.goal = goal
        self.__prop_numbers = prop_numbers

    def move_left(self) -> None:
        pass

    def move_right(self) -> None:
        pass

    def move_up(self) -> None:
        pass

    def move_down(self) -> None:
        pass

    def __str__(self) -> str:
        rows = (
            f"[{', '.join(repr(item) for item in row)}]"
            for row in self.__board
        )
        return "[\n  " + ",\n  ".join(rows) + "\n]"
