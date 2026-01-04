from typing import List

import ollama

from src.recommendation.prompt.prompt import PromptBasedRecommender


class OllamaRecommenderException(Exception):
    pass


class OllamaRecommender(PromptBasedRecommender):
    """
    AI-powered recommender using Ollama.
    Reuses a single client instance for all models.
    """

    def __init__(self, host: str):
        """
        Initialize the Ollama recommender with a reusable client.

        Args:
            host: Ollama host URL (e.g., http://localhost:11434).
        """
        self.__client = ollama.Client(host=host)

    def query_model(self, prompt: str, model: str) -> str:
        """Query the specified model."""
        try:
            response = self.__client.chat(
                model=model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
                format='json',
            )
        except (ollama.ResponseError, ollama.RequestError) as e:
            raise OllamaRecommenderException(f"Query error: {e}")

        try:
            return response['message']['content'].strip()
        except KeyError as e:
            raise OllamaRecommenderException(f"Response error: {e}")

    @staticmethod
    def list_available_models(host: str) -> List[str]:
        """List available Ollama models."""
        try:
            client = ollama.Client(host=host)
            return [model.model for model in client.list().get('models', [])]
        except Exception:
            return []
