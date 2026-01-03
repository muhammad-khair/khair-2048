import json
from typing import Tuple

from google import genai

from src.recommendation.base import Board, Recommender


class GeminiRecommender(Recommender):
    """
    AI-powered recommender using Google Gemini API.
    """

    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        """
        Initialize the Gemini recommender.

        Args:
            api_key: Google Gemini API key.
            model_name: Name of the Gemini model to use.
        """
        if not api_key:
            raise ValueError("GEMINI_API_KEY must be provided or set as environment variable")
        self.api_key = api_key
        self.client = genai.Client(api_key=self.api_key)

        # Validate model availability
        available_models = []
        try:
            available_models = [m.name.removeprefix("models/") for m in self.client.models.list()]
        except Exception as e:
            print(f"Warning: Could not list Gemini models: {e}")
        
        # Only validate if we successfully retrieved the list
        if available_models:
            # Allow both short names (gemini-pro) and full names (models/gemini-pro)
            if model_name not in available_models and f"models/{model_name}" not in available_models:
                 raise ValueError(f"Model {model_name} not found. Available models: {available_models}")

        self.model_name = model_name

    def suggest_move(self, grid: Board) -> Tuple[str, str]:
        """
        Suggest the best move using Google Gemini API.

        Args:
            grid: Current game board state.

        Returns:
            Tuple of (move, rationale) where move is one of: up, down, left, right
        """
        try:
            return self._query_gemini(grid)
        except Exception as e:
            print(f"Gemini API recommendation failed: {e}")
            return "up", "AI suggests moving up to maintain board balance."

    def _query_gemini(self, grid: Board) -> Tuple[str, str]:
        """Query the Gemini API for a move recommendation."""
        prompt = f"""
        Analyze this 2048 grid: {grid}
        Suggest the best next move (up, down, left, right).
        Provide a one-sentence rationale for the move.
        Output ONLY a JSON object with keys "move" and "rationale".
        Example: {{"move": "left", "rationale": "Consolidates tiles on the left edge."}}
        """

        response = self.client.models.generate_content(
            model=self.model_name, contents=prompt
        )

        try:
            # Parse response, handling potential markdown code blocks
            text = response.text.strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            elif text.startswith("```"):
                text = text[3:-3].strip()

            data = json.loads(text)
            move = data.get("move", "up").lower()
            rationale = data.get("rationale", "")

            # Validate move
            if move not in ["up", "down", "left", "right"]:
                move = "up"

            return move, rationale
        except (json.JSONDecodeError, KeyError, AttributeError):
            return "up", "AI suggests moving up to maintain board balance."
