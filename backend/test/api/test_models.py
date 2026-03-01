import unittest
from src.game.board import GameBoard
from src.api.models import MoveRequest, MoveResponse, RecommendationRequest, RecommendationResponse


class TestMoveRequestModel(unittest.TestCase):
    """Test MoveRequest model creation."""
    def test_move_request_model(self):
        board = GameBoard.create_new().get_board()
        request = MoveRequest(grid=board, direction="up", turns=0)
        self.assertEqual(request.grid, board)
        self.assertEqual(request.direction, "up")
        self.assertEqual(request.turns, 0)


class TestMoveResponseModel(unittest.TestCase):
    """Test MoveResponse model creation."""
    def test_move_response_model(self):
        board = GameBoard.create_new().get_board()
        response = MoveResponse(grid=board, status="ONGOING", largest_number=2, turns=1)
        self.assertEqual(response.grid, board)
        self.assertEqual(response.status, "ONGOING")
        self.assertEqual(response.largest_number, 2)
        self.assertEqual(response.turns, 1)


class TestRecommendationRequestModel(unittest.TestCase):
    """Test RecommendationRequest model creation."""
    def test_recommendation_request_model(self):
        board = GameBoard.create_new().get_board()
        request = RecommendationRequest(grid=board, provider="heuristic", model="simple")
        self.assertEqual(request.grid, board)
        self.assertEqual(request.provider, "heuristic")
        self.assertEqual(request.model, "simple")


class TestRecommendationResponseModel(unittest.TestCase):
    """Test RecommendationResponse model creation."""
    def test_recommendation_response_model(self):
        board = GameBoard.create_new().get_board()
        response = RecommendationResponse(suggested_move="left", rationale="Test", predicted_grid=board)
        self.assertEqual(response.suggested_move, "left")
        self.assertEqual(response.rationale, "Test")
        self.assertEqual(response.predicted_grid, board)


if __name__ == "__main__":
    unittest.main()
