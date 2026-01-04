from typing import List

from google import genai

from src.recommendation.prompt.prompt import PromptBasedRecommender


class GeminiRecommenderException(Exception):
    pass


class GeminiRecommender(PromptBasedRecommender):
    """
    AI-powered recommender using Google Gemini API.
    Reuses a single client instance for all models.
    """

    def __init__(self, api_key: str):
        """
        Initialize the Gemini recommender with a reusable client.

        Args:
            api_key: Google Gemini API key.
        """
        if not api_key:
            raise ValueError("Gemini API key must be provided")
        self.__client = genai.Client(api_key=api_key)

    def query_model(self, prompt: str, model: str) -> str:
        """Query the specified model."""
        try:
            response = self.__client.models.generate_content(
                model=model,
                contents=prompt,
            )
        except Exception as e:
            raise GeminiRecommenderException(f"Query error: {e}")

        return response.text.strip()
    
    def list_available_models_from_client(self) -> List[str]:
        """List models using the existing client instance."""
        try:
            return [m.name.removeprefix("models/") for m in self.__client.models.list()]
        except Exception:
            return []

    @staticmethod
    def list_available_models(api_key: str) -> List[str]:
        """List available Gemini models (static method for registry)."""
        if not api_key:
            return []
        try:
            client = genai.Client(api_key=api_key)
            return [m.name.removeprefix("models/") for m in client.models.list()]
        except Exception:
            return []
