import os

from reco.src.base import Recommender
from reco.src.gemini import GeminiRecommender
from reco.src.ollama import OllamaRecommender
from reco.src.heuristic import HeuristicRecommender


def get_recommender(reco_type: str = "auto") -> Recommender:
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
        return GeminiRecommender(os.getenv("GEMINI_API_KEY"))

    if reco_type == "ollama":
        return OllamaRecommender(host=os.getenv("OLLAMA_HOST"))

    if reco_type == "heuristic":
        return HeuristicRecommender()

    # Auto mode: check environment variables
    if reco_type == "auto":
        try:
            return GeminiRecommender(os.getenv("GEMINI_API_KEY"))
        except Exception as e:
            print(f"Failed to initialize GeminiRecommender: {e}")

        try:
            return OllamaRecommender(host=os.getenv("OLLAMA_HOST"))
        except Exception as e:
            print(f"Failed to initialize OllamaRecommender: {e}")

    # Default to heuristic
    return HeuristicRecommender()
