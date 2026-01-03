import unittest
from unittest.mock import MagicMock, patch

import ollama
from reco.src.ollama import OllamaRecommender


class TestOllamaRecommender(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [2, 2, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]
        self.test_host = "http://localhost:11434"

    @patch("reco.src.ollama.ollama.list")
    def test_ollama_recommender_initialization(self, mock_list):
        """Test that OllamaRecommender initializes with host and model."""
        mock_model = MagicMock()
        mock_model.model = "llama2"
        mock_list.return_value = {'models': [mock_model]}
        
        recommender = OllamaRecommender(host=self.test_host, model_name="llama2")
        self.assertEqual(recommender.host, self.test_host)
        self.assertEqual(recommender.model, "llama2")
        self.assertIsInstance(recommender.client, ollama.Client)

    @patch("reco.src.ollama.ollama.list")
    def test_ollama_recommender_invalid_model(self, mock_list):
        """Test initialization raises error for invalid model."""
        mock_model = MagicMock()
        mock_model.model = "llama3.1:8b"
        mock_list.return_value = {'models': [mock_model]}
        
        with self.assertRaises(ValueError):
            OllamaRecommender(model_name="invalid-model")

    @patch("reco.src.ollama.ollama.Client")
    @patch("reco.src.ollama.ollama.list")
    def test_ollama_recommender_suggest_move(self, mock_list, mock_client_class):
        """Test successful move suggestion from Ollama."""
        mock_model = MagicMock()
        mock_model.model = "llama3.1:8b"
        mock_list.return_value = {'models': [mock_model]}
        
        mock_client = MagicMock()
        mock_response = {
            'message': {
                'content': '{"move": "right", "rationale": "Consolidates tiles to the right."}'
            }
        }
        mock_client.chat.return_value = mock_response
        mock_client_class.return_value = mock_client

        recommender = OllamaRecommender(host=self.test_host)
        move, rationale = recommender.suggest_move(self.grid)

        self.assertEqual(move, "right")
        self.assertEqual(rationale, "Consolidates tiles to the right.")

    @patch("reco.src.ollama.ollama.Client")
    @patch("reco.src.ollama.ollama.list")
    def test_ollama_recommender_with_markdown(self, mock_list, mock_client_class):
        """Test parsing response with markdown code blocks."""
        mock_model = MagicMock()
        mock_model.model = "llama3.1:8b"
        mock_list.return_value = {'models': [mock_model]}

        mock_client = MagicMock()
        mock_response = {
            'message': {
                'content': '```json\n{"move": "left", "rationale": "Best strategy."}\n```'
            }
        }
        mock_client.chat.return_value = mock_response
        mock_client_class.return_value = mock_client

        recommender = OllamaRecommender()
        move, rationale = recommender.suggest_move(self.grid)

        self.assertEqual(move, "left")
        self.assertEqual(rationale, "Best strategy.")

    @patch("reco.src.ollama.ollama.Client")
    @patch("reco.src.ollama.ollama.list")
    def test_ollama_recommender_connection_error(self, mock_list, mock_client_class):
        """Test fallback behavior on connection error."""
        mock_model = MagicMock()
        mock_model.model = "llama3.1:8b"
        mock_list.return_value = {'models': [mock_model]}

        mock_client = MagicMock()
        mock_client.chat.side_effect = ollama.ResponseError("Connection failed")
        mock_client_class.return_value = mock_client

        recommender = OllamaRecommender()
        move, rationale = recommender.suggest_move(self.grid)

        self.assertEqual(move, "down")
        self.assertIn("AI suggests moving down", rationale)


if __name__ == '__main__':
    unittest.main()
