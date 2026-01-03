import json
from typing import Optional, Tuple

import ollama

from reco.src.base import Board, Recommender


class OllamaRecommender(Recommender):
    """
    AI-powered recommender using Ollama via the official python library.
    """

    def __init__(self, host: Optional[str] = None, model_name: str = "llama3"):
        """
        Initialize the Ollama recommender. Raises an error if the model is not found.

        Args:
            host: Ollama host URL (e.g., http://localhost:11434).
                  If None, uses the library default (localhost).
            model_name: Model name to use (default: llama3).
        """
        self.host = host
        self.client = ollama.Client(host=host)

        available_models = [model.model for model in ollama.list().get('models', [])]
        if model_name not in available_models:
            raise ValueError(f"Model {model_name} not found. Available models: {available_models}")
        self.model = model_name

    def suggest_move(self, grid: Board) -> Tuple[str, str]:
        """
        Suggest the best move using Ollama.

        Args:
            grid: Current game board state.

        Returns:
            Tuple of (move, rationale) where move is one of: up, down, left, right
        """
        try:
            return self._query_ollama(grid)
        except Exception as e:
            print(f"Ollama recommendation failed: {e}")
            return "down", "AI suggests moving down to compress tiles."

    def _query_ollama(self, grid: Board) -> Tuple[str, str]:
        """Query Ollama for a move recommendation."""
        prompt = f"""
        Analyze this 2048 grid: {grid}
        Suggest the best next move (up, down, left, right).
        Provide a one-sentence rationale for the move.
        Output ONLY a JSON object with keys "move" and "rationale".
        Example: {{"move": "left", "rationale": "Consolidates tiles on the left edge."}}
        """

        try:
            response = self.client.chat(
                model=self.model,
                messages=[
                    {
                        'role': 'user',
                        'content': prompt,
                    },
                ],
                format='json',  # Force JSON mode if supported by model
            )

            content = response['message']['content'].strip()

            # Handle potential markdown code blocks even with format='json'
            if content.startswith("```json"):
                content = content[7:-3].strip()
            elif content.startswith("```"):
                content = content[3:-3].strip()

            result = json.loads(content)
            move = result.get("move", "down").lower()
            rationale = result.get("rationale", "")

            # Validate move
            if move not in ["up", "down", "left", "right"]:
                move = "down"

            return move, rationale

        except (json.JSONDecodeError, KeyError, ollama.ResponseError, ollama.RequestError) as e:
            print(f"Ollama query error: {e}")
            raise e
