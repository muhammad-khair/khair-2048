from abc import ABC, abstractmethod
from typing import List, Optional, Tuple

Board = List[List[Optional[int]]]

class Recommender(ABC):
    """
    Abstract base class for a 2048 move recommender.
    """

    @abstractmethod
    def suggest_move(self, grid: Board) -> Tuple[str, str]:
        """
        Suggest the next best move and provide a rationale.

        Args:
            grid: A 4x4 2D list representing the current game board.

        Returns:
            A tuple of (suggested_move, rationale), where suggested_move is 
            one of ('up', 'down', 'left', 'right').
        """
        pass
