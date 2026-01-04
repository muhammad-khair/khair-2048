import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.config.settings import SETTINGS
from src.api.routes import router

app = FastAPI(title="2048 Game API")

# Add CORS allow origins middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=SETTINGS.app.cors_allow_origins,
    allow_credentials=True,
    allow_methods=["*"], # allow methods
    allow_headers=["*"], # allow headers
)

# Include the API router with the prefix
app.include_router(router, prefix="/api")

# Setup static file serving for the React frontend
current_dir = os.path.dirname(os.path.abspath(__file__))
static_dir = os.path.abspath(os.path.join(current_dir, "../../frontend/dist"))
assets_dir = os.path.join(static_dir, "assets")
if os.path.exists(assets_dir):
    app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")


@app.get("/")
async def read_index():
    """
    Serve the main index.html file for the game frontend.
    """
    return FileResponse(os.path.join(static_dir, "index.html"))


def main() -> None:
    """Driver logic to launch the FastAPI server."""
    app_settings = SETTINGS.app

    print(f"Starting 2048 game server at http://{app_settings.host}:{app_settings.port}")
    print("Press Ctrl+C to stop the server.")

    uvicorn.run(
        "src.main:app",
        host=app_settings.host,
        port=app_settings.port,
        reload=app_settings.hot_reload
    )


if __name__ == "__main__":
    main()
