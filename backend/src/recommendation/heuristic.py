from copy import deepcopy
from typing import Tuple

from src.game.board import GameBoard
from src.game.constants import GOAL_NUMBER
from src.recommendation.base import Recommender, Board


class HeuristicRecommender(Recommender):
    """
    A heuristic-based recommender for 2048.
    """

    def suggest_move(self, grid: Board) -> Tuple[str, str]:
        directions = ['left', 'right', 'up', 'down']
        best_move = 'left'
        best_score = -1
        
        for d in directions:
            game = GameBoard(board=grid, goal=GOAL_NUMBER, prop_numbers=[])
            sim = deepcopy(game)
            
            try:
                if d == 'left': sim.move_left()
                elif d == 'right': sim.move_right()
                elif d == 'up': sim.move_up()
                elif d == 'down': sim.move_down()
            except:
                continue

            # If move didn't change the board, ignore it
            if sim.get_board() == grid:
                continue
            
            score = self.__calculate_score(sim)
            if score > best_score:
                best_score = score
                best_move = d
        
        rationale = f"Moving {best_move} is the best tactical choice right now to maximize empty spaces and tile organization."
        if best_score == -1:
            return "left", "No moves seem to change the board state."
            
        return best_move, rationale

    def __calculate_score(self, game: GameBoard) -> float:
        grid = game.get_board()
        empty_count = sum(row.count(None) for row in grid)
        
        # Heuristic: Favor empty spaces and high values in corners
        score = empty_count * 10
        
        max_val = game.largest_number()
        # check if max_val is in a corner (bottom-right: index 3,3)
        if grid[3][3] == max_val:
            score += 50
            
        return score
