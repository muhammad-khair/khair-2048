from typing import Dict, List, Tuple

from src.config.settings import SETTINGS
from src.recommendation.base import BaseRecommender
from src.recommendation.heuristic.simple import SimpleHeuristicRecommender
from src.recommendation.prompt.gemini import GeminiRecommender
from src.recommendation.prompt.ollama import OllamaRecommender


class ModelInfo:
    """Information about a single model."""
    def __init__(self, provider: str, model: str, display_name: str):
        self.provider = provider
        self.model = model
        self.display_name = display_name


class ModelRegistry:
    """
    Singleton registry that discovers and caches available recommendation models.
    Stores one recommender instance per provider to enable client reuse.
    """
    _instance = None
    _initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    def __init__(self):
        if not ModelRegistry._initialized:
            self._models: Dict[Tuple[str, str], str] = {}
            self._providers: Dict[str, BaseRecommender] = {}
            self._discover_models()
            ModelRegistry._initialized = True
    
    def _discover_models(self) -> None:
        """Discover all available models and cache their provider instances."""
        self._register_heuristic()
        self._register_provider('gemini', GeminiRecommender, 
                               SETTINGS.recommendation.gemini.api_key,
                               SETTINGS.recommendation.gemini.allowed_models)
        self._register_provider('ollama', OllamaRecommender,
                               SETTINGS.recommendation.ollama.host,
                               SETTINGS.recommendation.ollama.allowed_models)
    
    def _register_heuristic(self) -> None:
        """Register heuristic recommender."""
        self._providers['heuristic'] = SimpleHeuristicRecommender()
        self._models[('heuristic', 'simple')] = 'heuristic'
    
    def _register_provider(self, name: str, recommender_class, config_value: str, allowed_models: List[str]) -> None:
        """
        Generic provider registration.
        
        Args:
            name: Provider name ('gemini' or 'ollama')
            recommender_class: Recommender class to instantiate
            config_value: API key or host URL
            allowed_models: List of allowed model names
        """
        # Skip if no config or no allowed models
        if not config_value or not allowed_models:
            return
        
        # Get available models
        available = recommender_class.list_available_models(config_value)
        if not available:
            return
        
        # Filter by allowlist
        models_to_register = [m for m in available if m in allowed_models]
        if not models_to_register:
            return
        
        # Create provider instance
        if name == 'gemini':
            self._providers[name] = recommender_class(api_key=config_value)
        else:  # ollama
            self._providers[name] = recommender_class(host=config_value)
        
        # Register models
        for model in models_to_register:
            self._models[(name, model)] = name
    
    def get_recommender(self, provider: str, model: str) -> BaseRecommender:
        """Get the recommender instance for the specified provider."""
        if (provider, model) not in self._models:
            raise ValueError(f"Model {provider}/{model} not available")
        return self._providers[provider]
    
    def list_models(self) -> List[ModelInfo]:
        """List all available models."""
        return [
            ModelInfo(
                provider=provider,
                model=model,
                display_name=f"{provider.title()} - {model}" if provider != 'heuristic' 
                            else f"Heuristic - {model.title()}"
            )
            for provider, model in self._models.keys()
        ]


registry = ModelRegistry()
