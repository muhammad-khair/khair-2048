import unittest
from unittest.mock import patch, MagicMock

from reco.src.factory import get_recommender
from reco.src.gemini import GeminiRecommender
from reco.src.heuristic import HeuristicRecommender
from reco.src.ollama import OllamaRecommender


class TestRecommenderFactory(unittest.TestCase):
    def test_recommender_factory_heuristic(self):
        """Test factory returns HeuristicRecommender for 'heuristic' type."""
        reco = get_recommender("heuristic")
        self.assertIsInstance(reco, HeuristicRecommender)

    @patch("reco.src.gemini.genai.Client")
    def test_recommender_factory_gemini(self, mock_client_class):
        """Test factory returns GeminiRecommender for 'gemini' type."""
        # Setup mock for model validation
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.name = "gemini-3-pro-high"
        mock_client.models.list.return_value = [mock_model]
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            reco = get_recommender("gemini")
            self.assertIsInstance(reco, GeminiRecommender)

    @patch("reco.src.ollama.ollama.list")
    def test_recommender_factory_ollama(self, mock_list):
        """Test factory returns OllamaRecommender for 'ollama' type."""
        mock_model = MagicMock()
        mock_model.model = "llama3"
        mock_list.return_value = {'models': [mock_model]}
        
        with patch.dict("os.environ", {"OLLAMA_HOST": "http://localhost:11434"}):
            reco = get_recommender("ollama")
            self.assertIsInstance(reco, OllamaRecommender)

    @patch("reco.src.gemini.genai.Client")
    def test_recommender_factory_auto_gemini(self, mock_client_class):
        """Test auto mode returns GeminiRecommender when GEMINI_API_KEY is set."""
        # Setup mock for model validation
        mock_client = MagicMock()
        mock_model = MagicMock()
        mock_model.name = "gemini-3-pro-high"
        mock_client.models.list.return_value = [mock_model]
        mock_client_class.return_value = mock_client

        with patch.dict("os.environ", {"GEMINI_API_KEY": "fake-key"}):
            reco = get_recommender("auto")
            self.assertIsInstance(reco, GeminiRecommender)

    @patch("reco.src.ollama.ollama.list")
    def test_recommender_factory_auto_ollama(self, mock_list):
        """Test auto mode returns OllamaRecommender when OLLAMA_HOST is set."""
        mock_model = MagicMock()
        mock_model.model = "llama3"
        mock_list.return_value = {'models': [mock_model]}
        
        # We need to simulate Gemini init failing so it falls back to Ollama
        # But we can just ensure GEMINI_API_KEY is unset
        with patch.dict("os.environ", {"OLLAMA_HOST": "http://localhost:11434"}, clear=True):
            reco = get_recommender("auto")
            self.assertIsInstance(reco, OllamaRecommender)

    def test_recommender_factory_auto_default(self):
        """Test auto mode returns HeuristicRecommender when no env vars are set."""
        with patch.dict("os.environ", {}, clear=True):
            reco = get_recommender("auto")
            self.assertIsInstance(reco, HeuristicRecommender)

    def test_recommender_factory_invalid_type(self):
        """Test factory returns HeuristicRecommender for invalid type."""
        reco = get_recommender("invalid_type")
        self.assertIsInstance(reco, HeuristicRecommender)

if __name__ == '__main__':
    unittest.main()
