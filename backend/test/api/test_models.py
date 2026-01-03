from src.game.board import GameBoard
from src.api.models import MoveRequest, MoveResponse, RecommendationRequest, RecommendationResponse


def test_move_request_model():
    """Test MoveRequest model creation."""
    board = GameBoard.create_new().get_board()
    request = MoveRequest(grid=board, direction="up", turns=0)
    assert request.grid == board
    assert request.direction == "up"
    assert request.turns == 0

def test_move_response_model():
    """Test MoveResponse model creation."""
    board = GameBoard.create_new().get_board()
    response = MoveResponse(grid=board, status="ONGOING", largest_number=2, turns=1)
    assert response.grid == board
    assert response.status == "ONGOING"
    assert response.largest_number == 2
    assert response.turns == 1

def test_recommendation_request_model():
    """Test RecommendationRequest model creation."""
    board = GameBoard.create_new().get_board()
    request = RecommendationRequest(grid=board)
    assert request.grid == board

def test_recommendation_response_model():
    """Test RecommendationResponse model creation."""
    board = GameBoard.create_new().get_board()
    response = RecommendationResponse(suggested_move="left", rationale="Test", predicted_grid=board)
    assert response.suggested_move == "left"
    assert response.rationale == "Test"
    assert response.predicted_grid == board
