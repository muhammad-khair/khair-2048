import unittest
from unittest.mock import MagicMock, patch

from src.recommendation.prompt.ollama import OllamaRecommender


class TestOllamaRecommender(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [2, 2, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        self.test_model = "deepseek-r1:1.5b"

    @patch("src.recommendation.prompt.ollama.ollama")
    def test_ollama_recommender_initialization(self, mock_ollama):
        """Test that OllamaRecommender initializes with host only."""
        mock_client = MagicMock()
        mock_ollama.Client.return_value = mock_client

        recommender = OllamaRecommender("http://localhost:11434")
        self.assertIsNotNone(recommender)
        mock_ollama.Client.assert_called_once_with(host="http://localhost:11434")

    @patch("src.recommendation.prompt.ollama.ollama")
    def test_ollama_recommender_suggest_move(self, mock_ollama):
        """Test successful move suggestion from Ollama API."""
        mock_client = MagicMock()
        
        mock_response = {
            'message': {
                'content': '{"move": "left", "rationale": "Merging tiles on the left is optimal."}'
            }
        }
        mock_client.chat.return_value = mock_response
        mock_ollama.Client.return_value = mock_client

        recommender = OllamaRecommender("http://localhost:11434")
        move, rationale = recommender.suggest_move(self.grid, self.test_model)

        self.assertEqual(move, "left")
        self.assertEqual(rationale, "Merging tiles on the left is optimal.")

    @patch("src.recommendation.prompt.ollama.ollama")
    def test_ollama_recommender_with_markdown(self, mock_ollama):
        """Test parsing response with markdown code blocks."""
        mock_client = MagicMock()
        
        mock_response = {
            'message': {
                'content': '```json\n{"move": "right", "rationale": "Best move."}\n```'
            }
        }
        mock_client.chat.return_value = mock_response
        mock_ollama.Client.return_value = mock_client

        recommender = OllamaRecommender("http://localhost:11434")
        move, rationale = recommender.suggest_move(self.grid, self.test_model)

        self.assertEqual(move, "right")
        self.assertEqual(rationale, "Best move.")

    @patch("src.recommendation.prompt.ollama.ollama")
    def test_ollama_recommender_connection_error(self, mock_ollama):
        """Test fallback behavior when connection fails."""
        # Setup valid exception classes for the mock
        class MockResponseError(Exception): pass
        class MockRequestError(Exception): pass
        mock_ollama.ResponseError = MockResponseError
        mock_ollama.RequestError = MockRequestError
        
        mock_client = MagicMock()
        mock_client.chat.side_effect = MockResponseError("Connection Error")
        mock_ollama.Client.return_value = mock_client

        recommender = OllamaRecommender("http://localhost:11434")
        with self.assertRaises(Exception):
            recommender.suggest_move(self.grid, self.test_model)

if __name__ == '__main__':
    unittest.main()
