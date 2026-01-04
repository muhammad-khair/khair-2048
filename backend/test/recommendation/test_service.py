import unittest
from unittest.mock import MagicMock, patch

from src.game.direction import Direction
from src.recommendation.service import RecommendationService


class TestRecommendationService(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [2, 2, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]

    @patch("src.recommendation.service.registry")
    @patch("src.recommendation.service.RecommendationService._simulate_move")
    def test_get_recommendation_success(self, mock_simulate, mock_registry):
        """Test successful recommendation retrieval."""
        # Setup mock recommender
        mock_recommender = MagicMock()
        mock_recommender.suggest_move.return_value = ("left", "Good move")
        mock_registry.get_recommender.return_value = mock_recommender
        
        # Setup mock simulation result
        mock_simulate.return_value = [[4, None, None, None], [None]*4, [None]*4, [None]*4]

        response = RecommendationService.get_recommendation(
            grid=self.grid,
            provider="test_provider",
            model="test_model"
        )

        self.assertEqual(response.suggested_move, "left")
        self.assertEqual(response.rationale, "Good move")
        self.assertEqual(response.predicted_grid[0][0], 4)
        
        mock_registry.get_recommender.assert_called_with("test_provider", "test_model")
        mock_recommender.suggest_move.assert_called_with(self.grid, "test_model")

    @patch("src.recommendation.service.registry")
    @patch("src.recommendation.service.SimpleHeuristicRecommender")
    def test_get_recommendation_fallback(self, mock_heuristic_class, mock_registry):
        """Test fallback to heuristic when primary recommender fails."""
        # Setup primary failure
        mock_registry.get_recommender.side_effect = Exception("API Error")
        
        # Setup heuristic fallback
        mock_heuristic = MagicMock()
        mock_heuristic.suggest_move.return_value = ("up", "Fallback rationale")
        mock_heuristic_class.return_value = mock_heuristic

        response = RecommendationService.get_recommendation(
            grid=self.grid,
            provider="gemini",
            model="pro"
        )

        self.assertEqual(response.suggested_move, "up")
        self.assertIn("Fallback to Heuristic", response.rationale)
        self.assertIn("API Error", response.rationale)

    def test_simulate_move(self):
        """Test internal move simulation logic."""
        # Setup a board where 'left' causes a merge
        grid = [
            [2, 2, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        
        # 2, 2 becomes 4, None
        predicted = RecommendationService._simulate_move(grid, Direction.LEFT)
        self.assertEqual(predicted[0][0], 4)
        self.assertIsNone(predicted[0][1])
        
        # Ensure original grid is untouched (though simulated logic uses deepcopy internally, 
        # we pass a list of list here so we check the result)


if __name__ == '__main__':
    unittest.main()
