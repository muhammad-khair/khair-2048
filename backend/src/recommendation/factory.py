from src.config.settings import SETTINGS
from src.recommendation.base import Recommender
from src.recommendation.gemini import GeminiRecommender
from src.recommendation.ollama import OllamaRecommender
from src.recommendation.heuristic import HeuristicRecommender


def get_recommender(reco_type: str = SETTINGS.recommendation.mode) -> Recommender:
    """
    Factory method to get the requested recommender.

    Args:
        reco_type: Type of recommender to create. Options:
            - "auto": Automatically select based on environment variables
            - "heuristic": Use heuristic-based recommender
            - "gemini": Use Google Gemini API recommender
            - "ollama": Use Ollama recommender

    Returns:
        Recommender instance
    """
    if reco_type == "gemini":
        return GeminiRecommender(
            api_key=SETTINGS.recommendation.gemini.api_key,
            model_name=SETTINGS.recommendation.gemini.model,
        )

    if reco_type == "ollama":
        return OllamaRecommender(
            host=SETTINGS.recommendation.ollama.host,
            model_name=SETTINGS.recommendation.ollama.model,
        )

    if reco_type == "heuristic":
        return HeuristicRecommender()

    # Auto mode: check environment variables
    if reco_type == "auto":
        try:
            return GeminiRecommender(
                api_key=SETTINGS.recommendation.gemini.api_key,
                model_name=SETTINGS.recommendation.gemini.model,
            )
        except Exception as e:
            print(f"Failed to initialize GeminiRecommender: {e}")

        try:
            return OllamaRecommender(
                host=SETTINGS.recommendation.ollama.host,
                model_name=SETTINGS.recommendation.ollama.model,
            )
        except Exception as e:
            print(f"Failed to initialize OllamaRecommender: {e}")

    # Default to heuristic
    return HeuristicRecommender()
