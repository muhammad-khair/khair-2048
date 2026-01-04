from typing import List

from pydantic import BaseModel
from pydantic_settings import BaseSettings, SettingsConfigDict


class AppSettings(BaseModel):
    """
    Application server settings.

    Attributes:
        host (str): Host address to bind the server to. Defaults to "127.0.0.1".
        port (int): Port number the server listens on. Defaults to 8000.
        hot_reload (bool): Enable auto-reload for development. Defaults to True.
        cors_allow_origins (List[str]): Hostnames to allow CORS middleware. Defaults to ["*"].
    """
    host: str = "127.0.0.1"
    port: int = 8000
    hot_reload: bool = True
    cors_allow_origins: List[str] = ["*"]


class GameSettings(BaseModel):
    """
    Game configuration settings.

    Attributes:
        grid_length (int): Size of the game grid (NxN). Defaults to 4.
        min_start_count (int): Minimum number of tiles to start with. Defaults to 2.
        max_start_count (int): Maximum number of tiles to start with. Defaults to 4.
        start_number (int): Starting tile value. Defaults to 2.
        goal_number (int): Target number to win the game. Defaults to 2048.
    """
    grid_length: int = 4
    min_start_count: int = 2
    max_start_count: int = 4
    start_number: int = 2
    goal_number: int = 2048


class OllamaSettings(BaseModel):
    """
    Configuration for the Ollama model server.

    Attributes:
        host (str): Base URL for the Ollama API. Defaults to "http://localhost:11434".
        allowed_models (List[str]): List of allowed model names. Empty list means no models allowed.
    """
    host: str = "http://localhost:11434"
    allowed_models: List[str] = [
        "deepseek-r1:1.5b",
        "llama3.2:latest",
    ]


class GeminiSettings(BaseModel):
    """
    Configuration for Google Gemini integration.

    Attributes:
        api_key (str): API key for Gemini. Set as an empty string to disable or when not configured. Defaults to "".
        allowed_models (List[str]): List of allowed model names. Defaults to stable versions only.
    """
    api_key: str = ""
    allowed_models: List[str] = [
        "gemini-2.0-flash",
        "gemini-1.5-flash",
        "gemini-1.5-pro",
    ]


class RecommendationSettings(BaseModel):
    """
    Recommendation system settings, grouping engine-specific configs.

    Attributes:
        ollama (OllamaSettings): Ollama sub-configuration.
        gemini (GeminiSettings): Gemini sub-configuration.
    """
    ollama: OllamaSettings = OllamaSettings()
    gemini: GeminiSettings = GeminiSettings()


class RateLimitSettings(BaseModel):
    """
    API rate limiting configuration.
    Values should be in the format "limit/period" (e.g., "60/minute").
    """
    move: str = "60/minute"
    new_game: str = "10/minute"
    recommend: str = "20/minute"
    models: str = "10/minute"


class Settings(BaseSettings):
    """
    Top-level application settings loaded from environment or `.env`.

    Attributes:
        app (AppSettings): Application server settings.
        game (GameSettings): Game configuration settings.
        recommendation (RecommendationSettings): Recommendation subsystem settings.
        rate_limit (RateLimitSettings): API rate limiting settings.

    Notes:
        - Uses `env_nested_delimiter="__"` to support nested env vars like `RECOMMENDATION__OLLAMA__HOST`.
        - Loads variables from `.env` by default and ignores unknown extras.
    """
    app: AppSettings = AppSettings()
    game: GameSettings = GameSettings()
    recommendation: RecommendationSettings = RecommendationSettings()
    rate_limit: RateLimitSettings = RateLimitSettings()

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )


SETTINGS = Settings()
