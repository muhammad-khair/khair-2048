import unittest
from unittest.mock import MagicMock, patch

from reco.src.gemini import GeminiRecommender


class TestGeminiRecommender(unittest.TestCase):
    def setUp(self):
        self.grid = [
            [2, 2, None, None],
            [None, None, None, None],
            [None, None, None, None],
            [None, None, None, None]
        ]

    @patch("reco.src.gemini.genai.Client")
    def test_gemini_recommender_initialization(self, mock_client_class):
        """Test that GeminiRecommender initializes with API key."""
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.name = "gemini-3-pro-high"
        mock_client.models.list.return_value = [mock_model]
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            recommender = GeminiRecommender("fake-key")
            self.assertIsNotNone(recommender.client)
            mock_client_class.assert_called_once_with(api_key="fake-key")

    @patch("reco.src.gemini.genai.Client")
    def test_gemini_recommender_invalid_model(self, mock_client_class):
        """Test initialization raises error for invalid model."""
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.name = "gemini-3-pro-high"
        mock_client.models.list.return_value = [mock_model]
        mock_client_class.return_value = mock_client

        with self.assertRaises(ValueError):
             GeminiRecommender(api_key="fake-key", model_name="invalid-model")

    def test_gemini_recommender_no_api_key(self):
        """Test that GeminiRecommender raises error without API key."""
        with patch.dict("os.environ", {}, clear=True):
            # Passing None explicitly to trigger the ValueError check inside __init__
            # If we don't pass anything, it raises TypeError which is also valid but different.
            with self.assertRaises(ValueError):
                GeminiRecommender(api_key=None)

    @patch("reco.src.gemini.genai.Client")
    def test_gemini_recommender_suggest_move(self, mock_client_class):
        """Test successful move suggestion from Gemini API."""
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.name = "gemini-3-pro-high"
        mock_client.models.list.return_value = [mock_model]
        
        mock_response = MagicMock()
        mock_response.text = '{"move": "left", "rationale": "Merging tiles on the left is optimal."}'
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            recommender = GeminiRecommender("fake-key")
            move, rationale = recommender.suggest_move(self.grid)

            self.assertEqual(move, "left")
            self.assertEqual(rationale, "Merging tiles on the left is optimal.")

    @patch("reco.src.gemini.genai.Client")
    def test_gemini_recommender_with_markdown(self, mock_client_class):
        """Test parsing response with markdown code blocks."""
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.name = "gemini-3-pro-high"
        mock_client.models.list.return_value = [mock_model]
        
        mock_response = MagicMock()
        mock_response.text = '```json\n{"move": "right", "rationale": "Best move."}\n```'
        mock_client.models.generate_content.return_value = mock_response
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            recommender = GeminiRecommender("fake-key")
            move, rationale = recommender.suggest_move(self.grid)

            self.assertEqual(move, "right")
            self.assertEqual(rationale, "Best move.")

    @patch("reco.src.gemini.genai.Client")
    def test_gemini_recommender_fallback_on_error(self, mock_client_class):
        """Test fallback behavior when API call fails."""
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.name = "gemini-3-pro-high"
        mock_client.models.list.return_value = [mock_model]
        
        mock_client.models.generate_content.side_effect = Exception("API Error")
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            recommender = GeminiRecommender("fake-key")
            move, rationale = recommender.suggest_move(self.grid)

            self.assertEqual(move, "up")
            self.assertIn("AI suggests moving up", rationale)

if __name__ == '__main__':
    unittest.main()
