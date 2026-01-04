import json
from abc import ABC, abstractmethod
from typing import Dict, List, Tuple

from src.recommendation.base import Board, BaseRecommender


class PromptBasedRecommender(BaseRecommender, ABC):
    """
    Prompt based recommender abstract class.
    """

    def suggest_move(self, grid: Board, model: str) -> Tuple[str, str]:
        """
        Suggest the best move using its implementation's model.

        Args:
            grid: Current game board state.
            model: Model name to use for this recommendation.

        Returns:
            Tuple of (move, rationale) where move is one of: up, down, left, right
        """
        try:
            prompt = f"""
            Analyze this 2048 grid: {grid}
            Suggest the best next move (up, down, left, right).
            Provide a one-sentence rationale for the move.
            Output ONLY a JSON object with keys "move" and "rationale".
            Example: {{"move": "left", "rationale": "Consolidates tiles on the left edge."}}
            """

            response = self.query_model(prompt, model)
            data = self._parse_response_text(response)

            move = data.get("move", "up").lower()
            rationale = data.get("rationale", "")
            if move not in ["up", "down", "left", "right"]:
                move = "up"
            return move, rationale

        except Exception as e:
            print(f"Model API recommendation failed: {e}")
            return "up", "AI suggests moving up to maintain board balance."

    @abstractmethod
    def query_model(self, prompt: str, model: str) -> str:
        """
        Query implementation model for response.

        Args:
            prompt: Prompt to query.
            model: Model name to use.

        Returns:
            Stringed response.
        """
        pass

    def _parse_response_text(self, text: str) -> Dict[str, str]:
        """
        Parse response text into dictionary context. Can be overriden in implementing class.

        Args:
            text: Text to parse for response content.

        Returns:
            Dictionary holding response content.
        """
        try:
            # Parse response, handling potential markdown code blocks
            text = text.strip()
            if text.startswith("```json"):
                text = text[7:-3].strip()
            elif text.startswith("```"):
                text = text[3:-3].strip()
            return json.loads(text)

        except (json.JSONDecodeError, KeyError, AttributeError):
            return {}

    @staticmethod
    @abstractmethod
    def list_available_models(host: str) -> List[str]:
        """List available models for prompting."""
        pass
