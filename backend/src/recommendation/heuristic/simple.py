from src.game.board import GameBoard
from src.recommendation.heuristic.heuristic import HeuristicRecommender


class SimpleHeuristicRecommender(HeuristicRecommender):
    """
    Simple heuristic-based recommender (current implementation).
    Provider: heuristic
    Model: simple

    A heuristic-based recommender for 2048 that focuses on empty spaces and if largest values are fed to corners.
    """

    def template_rationale(self, best_move: str) -> str:
        return f"Moving {best_move} is the best tactical choice right now to maximize empty spaces and tile organization."

    def calculate_score(self, previous: GameBoard, game: GameBoard) -> int:
        grid = game.get_board()

        # Heuristic: Favor empty spaces and high values in corners
        empty_count = sum(row.count(None) for row in grid)
        score = empty_count * 10

        # Heuristic: Favor if max_val is in any corner
        max_val = game.largest_number()
        corners = [
            (0, 0),
            (0, -1),
            (-1, 0),
            (-1, -1),
        ]
        for r, c in corners:
            if grid[r][c] == max_val:
                score += 50
                break

        return score
