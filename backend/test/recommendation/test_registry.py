import unittest
from unittest.mock import patch

from src.recommendation.registry import ModelRegistry


class TestModelRegistry(unittest.TestCase):
    def setUp(self):
        # Reset singleton instance before each test
        ModelRegistry._instance = None
        ModelRegistry._initialized = False

    @patch("src.recommendation.registry.SETTINGS")
    @patch("src.recommendation.registry.GeminiRecommender")
    @patch("src.recommendation.registry.OllamaRecommender")
    def test_registry_discovery(self, mock_ollama, mock_gemini, mock_settings):
        """Test that models are discovered and registered correctly."""
        # Setup mocks
        mock_settings.recommendation.gemini.api_key = "fake-key"
        mock_settings.recommendation.gemini.allowed_models = ["gemini-pro"]
        mock_settings.recommendation.ollama.host = "http://localhost:11434"
        mock_settings.recommendation.ollama.allowed_models = ["llama2"]

        mock_gemini.list_available_models.return_value = ["gemini-pro", "gemini-ultra"]
        mock_ollama.list_available_models.return_value = ["llama2", "mistral"]

        # Initialize registry
        registry = ModelRegistry()

        # Check heuristic registration
        heuristic = registry.get_recommender("heuristic", "simple")
        self.assertIsNotNone(heuristic)

        # Check Gemini registration
        gemini = registry.get_recommender("gemini", "gemini-pro")
        self.assertIsNotNone(gemini)
        # Should not register excluded models
        with self.assertRaises(ValueError):
            registry.get_recommender("gemini", "gemini-ultra")

        # Check Ollama registration
        ollama = registry.get_recommender("ollama", "llama2")
        self.assertIsNotNone(ollama)
        # Should not register excluded models
        with self.assertRaises(ValueError):
            registry.get_recommender("ollama", "mistral")

    @patch("src.recommendation.registry.SETTINGS")
    @patch("src.recommendation.registry.GeminiRecommender")
    def test_registry_empty_allowlist_gemini(self, mock_gemini, mock_settings):
        """Test that empty allowlist prevents registration."""
        mock_settings.recommendation.gemini.api_key = "fake-key"
        mock_settings.recommendation.gemini.allowed_models = []  # Empty allowlist

        mock_gemini.list_available_models.return_value = ["gemini-pro"]

        registry = ModelRegistry()

        # Should prompt Gemini registration to be skipped
        with self.assertRaises(ValueError):
            registry.get_recommender("gemini", "gemini-pro")

    def test_list_models_format(self):
        """Test that list_models returns correctly formatted info."""
        # Mock dependencies manually for this test to control internal state
        registry = ModelRegistry()
        # Manually inject a mock model
        registry._models[('test_provider', 'test_model')] = 'test_provider'
        
        models = registry.list_models()
        model_info = next(m for m in models if m.provider == 'test_provider')
        
        self.assertEqual(model_info.model, 'test_model')
        self.assertEqual(model_info.display_name, 'Test_Provider - test_model')


if __name__ == '__main__':
    unittest.main()
