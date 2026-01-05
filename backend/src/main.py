import uvicorn
from src.config.settings import SETTINGS

def main() -> None:
    """Driver logic to launch the FastAPI server."""
    app_settings = SETTINGS.app

    print(f"Starting 2048 game server at http://{app_settings.host}:{app_settings.port}")
    print("Press Ctrl+C to stop the server.")

    uvicorn.run(
        "src.app.app:app",
        host=app_settings.host,
        port=app_settings.port,
        reload=app_settings.hot_reload
    )


if __name__ == "__main__":
    main()
