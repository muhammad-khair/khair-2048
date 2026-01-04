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



class OllamaSettings(BaseModel):
    """
    Configuration for the Ollama model server.

    Attributes:
        host (str): Base URL for the Ollama API. Defaults to "http://localhost:11434".
        model (str): Model identifier to use when calling Ollama. Defaults to "llama3.1".
    """
    host: str = "http://localhost:11434"
    model: str = "llama3.1"


class GeminiSettings(BaseModel):
    """
    Configuration for Google Gemini integration.

    Attributes:
        api_key (str): API key for Gemini. Set as an empty string to disable or when not configured. Defaults to "".
        model (str): Model identifier to use when calling Gemini. Defaults to "gemini-2.5-flash".
    """
    api_key: str = ""
    model: str = "gemini-2.5-flash"


class RecommendationSettings(BaseModel):
    """
    Recommendation system settings, grouping engine-specific configs.

    Attributes:
        mode (str): Selection mode for recommendation provider (e.g. "auto", "ollama", "gemini"). Defaults to "heuristic".
        ollama (OllamaSettings): Ollama sub-configuration.
        gemini (GeminiSettings): Gemini sub-configuration.
    """
    mode: str = "heuristic"
    ollama: OllamaSettings = OllamaSettings()
    gemini: GeminiSettings = GeminiSettings()


class Settings(BaseSettings):
    """
    Top-level application settings loaded from environment or `.env`.

    Attributes:
        app (AppSettings): Application server settings.
        recommendation (RecommendationSettings): Recommendation subsystem settings.

    Notes:
        - Uses `env_nested_delimiter="__"` to support nested env vars like `RECOMMENDATION__OLLAMA__HOST`.
        - Loads variables from `.env` by default and ignores unknown extras.
    """
    app: AppSettings = AppSettings()
    recommendation: RecommendationSettings = RecommendationSettings()

    model_config = SettingsConfigDict(
        env_nested_delimiter="__",
        env_file=".env",
        extra="ignore",
    )


SETTINGS = Settings()
