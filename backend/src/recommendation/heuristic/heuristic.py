from abc import ABC, abstractmethod
from copy import deepcopy
from typing import Tuple, Callable, List

from src.config.settings import SETTINGS
from src.game.board import GameBoard, Board
from src.recommendation.base import BaseRecommender


class HeuristicRecommender(BaseRecommender, ABC):
    """
    Abstract base class for heuristic-based recommenders.
    All heuristic recommenders should extend this class.
    """

    def suggest_move(self, grid: Board, model: str) -> Tuple[str, str]:
        movement_set: List[Tuple[str, Callable[[GameBoard], None]]] = [
            ('left', lambda b: b.move_left()),
            ('right', lambda b: b.move_right()),
            ('up', lambda b: b.move_up()),
            ('down', lambda b: b.move_down()),
        ]
        best_move = 'left'
        best_score = -1

        for move, execute_move in movement_set:
            game = GameBoard(board=grid, goal=SETTINGS.game.goal_number, prop_numbers=[])
            simulation = deepcopy(game)
            execute_move(simulation)

            # If move didn't change the board, ignore it
            if simulation.get_board() == grid:
                continue

            score = self.calculate_score(game, simulation)
            if score > best_score:
                best_score = score
                best_move = move

        if best_score == -1:
            return "left", "No moves seem to change the board state."

        rationale = self.template_rationale(best_move)
        return best_move, rationale

    @abstractmethod
    def calculate_score(self, previous: GameBoard, game: GameBoard) -> int:
        pass

    @abstractmethod
    def template_rationale(self, best_move: str) -> str:
        pass
