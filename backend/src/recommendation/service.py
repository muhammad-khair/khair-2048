from copy import deepcopy

from src.config.settings import SETTINGS
from src.game.board import GameBoard, Board
from src.game.direction import Direction
from src.recommendation.heuristic.simple import SimpleHeuristicRecommender
from src.recommendation.registry import registry


class RecommendationResponse:
    """Response model for recommendations."""
    def __init__(self, suggested_move: str, rationale: str, predicted_grid: Board):
        self.suggested_move = suggested_move
        self.rationale = rationale
        self.predicted_grid = predicted_grid


class RecommendationService:
    """Service layer for handling game recommendations."""
    
    @staticmethod
    def get_recommendation(grid: Board, provider: str, model: str) -> RecommendationResponse:
        """
        Get a move recommendation and simulate the result.
        Falls back to heuristic if the selected model fails.
        """
        try:
            recommender = registry.get_recommender(provider, model)
            direction_str, rationale = recommender.suggest_move(grid, model)
        except Exception as e:
            # Fallback to heuristic
            print(f"Error with {provider}/{model}: {e}. Falling back to heuristic.")
            recommender = SimpleHeuristicRecommender()
            direction_str, rationale = recommender.suggest_move(grid, "simple")
            
            # Prepend error info
            error_msg = str(e)[:100]
            rationale = f"[Fallback to Heuristic - {provider}/{model} failed: {error_msg}] {rationale}"
        
        # Simulate the move
        direction = Direction(direction_str.lower())
        predicted_grid = RecommendationService._simulate_move(grid, direction)
        
        return RecommendationResponse(
            suggested_move=direction.value,
            rationale=rationale,
            predicted_grid=predicted_grid
        )
    
    @staticmethod
    def _simulate_move(grid: Board, direction: Direction) -> Board:
        """Simulate a move without affecting the original grid."""
        game = GameBoard(
            board=grid,
            goal=SETTINGS.game.goal_number,
            prop_numbers=[],  # No random spawns in simulation
        )
        sim_board = deepcopy(game)
        direction.apply_to_board(sim_board)
        return sim_board.get_board()
