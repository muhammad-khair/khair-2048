import unittest
from unittest.mock import patch, MagicMock

from src.recommendation.factory import get_recommender
from src.recommendation.gemini import GeminiRecommender
from src.recommendation.heuristic import HeuristicRecommender
from src.recommendation.ollama import OllamaRecommender


class TestRecommenderFactory(unittest.TestCase):
    def test_recommender_factory_heuristic(self):
        """Test factory returns HeuristicRecommender for 'heuristic' type."""
        reco = get_recommender("heuristic")
        self.assertIsInstance(reco, HeuristicRecommender)

    @patch("src.recommendation.factory.SETTINGS")
    @patch("src.recommendation.gemini.genai.Client")
    def test_recommender_factory_gemini(self, mock_client_class, mock_settings):
        """Test factory returns GeminiRecommender for 'gemini' type."""
        mock_settings.recommendation.gemini.api_key = "fake-key"
        mock_settings.recommendation.gemini.model = "gemini-2.5-flash"

        # Setup mock for model validation
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.name = "gemini-2.5-flash"
        mock_client.models.list.return_value = [mock_model]
        mock_client_class.return_value = mock_client

        reco = get_recommender("gemini")
        self.assertIsInstance(reco, GeminiRecommender)

    @patch("src.recommendation.factory.SETTINGS")
    @patch("src.recommendation.ollama.ollama.list")
    def test_recommender_factory_ollama(self, mock_list, mock_settings):
        """Test factory returns OllamaRecommender for 'ollama' type."""
        mock_settings.recommendation.ollama.host = "http://localhost:11434"
        mock_settings.recommendation.ollama.model = "llama3.1:8b"

        # Setup mock for model validation
        mock_model = MagicMock()
        mock_model.model = "llama3.1:8b"
        mock_list.return_value = {'models': [mock_model]}

        reco = get_recommender("ollama")
        self.assertIsInstance(reco, OllamaRecommender)

    @patch("src.recommendation.factory.SETTINGS")
    @patch("src.recommendation.gemini.genai.Client")
    def test_recommender_factory_auto_gemini(self, mock_client_class, mock_settings):
        """Test auto mode returns GeminiRecommender when GEMINI_API_KEY is set."""
        mock_settings.recommendation.gemini.api_key = "fake-key"
        mock_settings.recommendation.gemini.model = "gemini-2.5-flash"

        # Setup mock for model validation
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.name = "gemini-2.5-flash"
        mock_client.models.list.return_value = [mock_model]
        mock_client_class.return_value = mock_client

        reco = get_recommender("auto")
        self.assertIsInstance(reco, GeminiRecommender)

    @patch("src.recommendation.factory.SETTINGS")
    @patch("src.recommendation.ollama.ollama.list")
    def test_recommender_factory_auto_ollama(self, mock_list, mock_settings):
        """Test auto mode returns OllamaRecommender when OLLAMA_HOST is set."""
        mock_settings.recommendation.gemini.api_key = ""  # unset RECOMMENDATION_GEMINI_API_KEY
        mock_settings.recommendation.gemini.model = "gemini-2.5-flash"
        mock_settings.recommendation.ollama.host = "http://localhost:11434"
        mock_settings.recommendation.ollama.model = "llama3.1:8b"

        # Setup mock for model validation
        mock_model = MagicMock()
        mock_model.model = "llama3.1:8b"
        mock_list.return_value = {'models': [mock_model]}
        
        # We need to simulate Gemini init failing so it falls back to Ollama
        reco = get_recommender("auto")
        self.assertIsInstance(reco, OllamaRecommender)

    @patch("src.recommendation.factory.SETTINGS")
    @patch("src.recommendation.ollama.ollama.list")
    def test_recommender_factory_auto_default(self, mock_ollama_list, mock_settings):
        """Test auto mode returns HeuristicRecommender when no env vars are set."""
        mock_settings.recommendation.gemini.api_key = ""  # unset RECOMMENDATION_GEMINI_API_KEY
        mock_ollama_list.return_value = {'models': []}

        reco = get_recommender("auto")
        self.assertIsInstance(reco, HeuristicRecommender)

    def test_recommender_factory_invalid_type(self):
        """Test factory returns HeuristicRecommender for invalid type."""
        reco = get_recommender("invalid_type")
        self.assertIsInstance(reco, HeuristicRecommender)

if __name__ == '__main__':
    unittest.main()
